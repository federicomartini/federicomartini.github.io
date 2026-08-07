"""Aggrega in _data/ai_feed.yml (letto dalla pagina /ai-feed/) sia articoli/paper da
leggere sia tool AI nuovi da provare (prodotti, librerie, progetti open source).

Fonti con RSS nativo: Hugging Face Blog, arXiv, OpenAI News, Google DeepMind Blog,
Simon Willison, Ahead of AI, One Useful Thing, antirez, Product Hunt (AI).
Fonti senza RSS (scraping mirato sulla pagina di listing): Anthropic News, The Batch.
Hugging Face Papers: API JSON pubblica usata dalla loro stessa pagina /papers.
GitHub: API di ricerca pubblica, repo taggati "llm" creati di recente per stelle.

Ogni fonte è isolata in try/except: se una fonte cambia struttura o è irraggiungibile,
le altre continuano a essere aggiornate normalmente.
"""

import time
from datetime import date, datetime, timedelta

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (compatible; federicomartini-ai-feed/1.0; +https://federicomartini.github.io/)"
MAX_PER_SOURCE = 10
OUTPUT_PATH = "_data/ai_feed.yml"

HEADERS = {"User-Agent": USER_AGENT}
THE_BATCH_DATE_FORMATS = ("%B %d, %Y", "%b %d, %Y")


def _the_batch_article_date(article) -> str:
    """Le card 'in evidenza' mettono la data in un badge (formato abbreviato 'Jul 31, 2026'),
    le card secondarie in un footer (formato esteso 'January 22, 2025'). Si provano entrambe."""
    candidates = []
    footer = article.find("footer")
    if footer:
        span = footer.find("span")
        if span:
            candidates.append(span.get_text(strip=True))
    tag_link = article.find("a", href=lambda h: h and "/the-batch/tag/" in h)
    if tag_link:
        candidates.append(tag_link.get_text(strip=True))

    for text in candidates:
        for fmt in THE_BATCH_DATE_FORMATS:
            try:
                return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
    return ""


def parse_rss(url: str, source: str) -> list[dict]:
    feed = feedparser.parse(url, agent=USER_AGENT)
    items = []
    for entry in feed.entries[:MAX_PER_SOURCE]:
        parsed_date = entry.get("published_parsed") or entry.get("updated_parsed")
        date_str = time.strftime("%Y-%m-%d", parsed_date) if parsed_date else ""
        items.append(
            {
                "source": source,
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", ""),
                "date": date_str,
            }
        )
    return items


def fetch_hf_papers() -> list[dict]:
    r = requests.get("https://huggingface.co/api/daily_papers", headers=HEADERS, timeout=20)
    r.raise_for_status()
    items = []
    for entry in r.json()[:MAX_PER_SOURCE]:
        paper = entry.get("paper", entry)
        paper_id = paper.get("id") or entry.get("id")
        title = (paper.get("title") or entry.get("title") or "").strip()
        if not paper_id or not title:
            continue
        items.append(
            {
                "source": "Hugging Face Papers",
                "title": title,
                "link": f"https://huggingface.co/papers/{paper_id}",
                "date": (entry.get("publishedAt") or "")[:10],
            }
        )
    return items


def fetch_anthropic_news() -> list[dict]:
    r = requests.get("https://www.anthropic.com/news", headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    items = []
    seen_links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not href.startswith("/news/"):
            continue
        title_el = a.find("span", class_=lambda c: c and "title" in c)
        if not title_el:
            continue
        link = "https://www.anthropic.com" + href
        if link in seen_links:
            continue
        seen_links.add(link)

        date_str = ""
        time_el = a.find("time")
        if time_el:
            try:
                date_str = datetime.strptime(time_el.get_text(strip=True), "%b %d, %Y").strftime("%Y-%m-%d")
            except ValueError:
                date_str = ""

        items.append({"source": "Anthropic", "title": title_el.get_text(strip=True), "link": link, "date": date_str})
        if len(items) >= MAX_PER_SOURCE:
            break
    return items


def fetch_the_batch() -> list[dict]:
    r = requests.get("https://www.deeplearning.ai/the-batch", headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    items = []
    seen_links = set()
    # Scoping to <article> cards (not just any link with aria-label) esclude di per se
    # i link di navigazione come la search box ("/the-batch/search"), che non sono card.
    for article in soup.find_all("article"):
        a = article.find("a", attrs={"aria-label": True, "href": True})
        if not a or not a["href"].startswith("/the-batch/"):
            continue
        link = "https://www.deeplearning.ai" + a["href"]
        if link in seen_links:
            continue
        seen_links.add(link)

        date_str = _the_batch_article_date(article)

        items.append({"source": "The Batch", "title": a["aria-label"].strip(), "link": link, "date": date_str})
        if len(items) >= MAX_PER_SOURCE:
            break
    return items


def fetch_product_hunt() -> list[dict]:
    return parse_rss("https://www.producthunt.com/feed?category=artificial-intelligence", "Product Hunt")


GITHUB_TOPICS = ["llm", "ai-agents", "rag"]


def _github_search(query: str, per_page: int) -> list[dict]:
    r = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": query, "sort": "stars", "order": "desc", "per_page": per_page},
        headers={"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT},
        timeout=20,
    )
    r.raise_for_status()
    return r.json().get("items", [])


def fetch_github_new_repos() -> list[dict]:
    """Meta' degli slot da repo appena creati (novita' genuine, con una soglia minima
    di stelle per escludere rumore), meta' da repo con push recente in una fascia di
    stelle che esclude sia il rumore sia i soliti giganti storici (transformers,
    ollama, ecc.), sempre uguali giorno dopo giorno se si ordinasse per stelle assolute
    senza limite superiore: l'obiettivo e' roba di valore che sta avendo un momento
    ora, non la top list eterna ne' tutto cio' che viene caricato a prescindere."""
    since = (date.today() - timedelta(days=14)).isoformat()
    half = MAX_PER_SOURCE // 2

    seen_ids: set[int] = set()
    fresh: list[dict] = []
    active: list[dict] = []
    for topic in GITHUB_TOPICS:
        for repo in _github_search(f"topic:{topic} created:>{since} stars:>20", half):
            if repo["id"] not in seen_ids:
                seen_ids.add(repo["id"])
                fresh.append(repo)
        for repo in _github_search(f"topic:{topic} pushed:>{since} stars:200..50000", half):
            if repo["id"] not in seen_ids:
                seen_ids.add(repo["id"])
                active.append(repo)

    fresh.sort(key=lambda r: r["stargazers_count"], reverse=True)
    active.sort(key=lambda r: r["stargazers_count"], reverse=True)
    selected = fresh[:half] + active[: MAX_PER_SOURCE - half]

    items = []
    for repo in selected:
        description = (repo.get("description") or "").strip()
        title = f"{repo['full_name']} ({repo['stargazers_count']}★)"
        if description:
            title += f" · {description}"
        items.append(
            {
                "source": "GitHub (trending AI/LLM/Agents)",
                "title": title[:180],
                "link": repo["html_url"],
                "date": repo["pushed_at"][:10],
            }
        )
    return items


def fetch_chinese_labs_papers() -> list[dict]:
    """Paper dei team dietro i modelli cinesi piu' rilevanti (DeepSeek, Qwen, Kimi,
    GLM). Cerca per autore, non per parola nel titolo: "DeepSeek-AI", "Qwen Team" e
    "Kimi Team" sono le firme collettive che questi team usano davvero su arXiv,
    zero falsi positivi. GLM non ha una firma fissa (cambia ad ogni versione:
    "GLM-5-Team", "GLM-V Team", ecc.) quindi si combina titolo+autore ("GLM" nel
    titolo E un autore che contiene "Team"): da sola la parola "GLM" nel titolo
    prenderebbe anche paper di statistica (Generalized Linear Model, sigla
    decennale scorrelata) o di "Graph Language Model", niente a che fare con Zhipu."""
    queries = [
        'au:"DeepSeek-AI"',
        'au:"Qwen Team"',
        'au:"Kimi Team"',
        "ti:GLM AND au:Team",
    ]
    seen_ids: set[str] = set()
    papers = []
    for q in queries:
        r = requests.get(
            "https://export.arxiv.org/api/query",
            params={"search_query": q, "max_results": MAX_PER_SOURCE},
            headers={"User-Agent": USER_AGENT},
            timeout=20,
        )
        r.raise_for_status()
        for entry in feedparser.parse(r.text).entries:
            arxiv_id = entry.get("id", "")
            if arxiv_id and arxiv_id not in seen_ids:
                seen_ids.add(arxiv_id)
                papers.append(entry)

    papers.sort(key=lambda e: e.get("published", ""), reverse=True)
    items = []
    for entry in papers[:MAX_PER_SOURCE]:
        parsed_date = entry.get("published_parsed")
        date_str = time.strftime("%Y-%m-%d", parsed_date) if parsed_date else ""
        items.append(
            {
                "source": "arXiv (DeepSeek/Qwen/Kimi/GLM)",
                "title": entry.get("title", "").replace("\n", " ").strip(),
                "link": entry.get("link", ""),
                "date": date_str,
            }
        )
    return items


SOURCES = [
    ("Hugging Face Blog", lambda: parse_rss("https://huggingface.co/blog/feed.xml", "Hugging Face Blog")),
    ("arXiv (cs.AI)", lambda: parse_rss("https://rss.arxiv.org/rss/cs.AI", "arXiv (cs.AI)")),
    ("arXiv (DeepSeek/Qwen/Kimi/GLM)", fetch_chinese_labs_papers),
    ("OpenAI News", lambda: parse_rss("https://openai.com/news/rss.xml", "OpenAI")),
    ("Google DeepMind Blog", lambda: parse_rss("https://deepmind.google/blog/rss.xml", "Google DeepMind")),
    ("Hugging Face Papers", fetch_hf_papers),
    ("Anthropic News", fetch_anthropic_news),
    ("The Batch", fetch_the_batch),
    ("Simon Willison", lambda: parse_rss("https://simonwillison.net/atom/entries/", "Simon Willison")),
    ("Ahead of AI (Sebastian Raschka)", lambda: parse_rss("https://magazine.sebastianraschka.com/feed", "Ahead of AI")),
    ("One Useful Thing (Ethan Mollick)", lambda: parse_rss("https://www.oneusefulthing.org/feed", "One Useful Thing")),
    ("antirez (Salvatore Sanfilippo)", lambda: parse_rss("https://antirez.com/rss", "antirez")),
    ("Andrej Karpathy", lambda: parse_rss("https://karpathy.bearblog.dev/feed/", "Andrej Karpathy")),
    ("Product Hunt (AI)", fetch_product_hunt),
    ("GitHub (trending AI/LLM/Agents)", fetch_github_new_repos),
]


def main() -> None:
    all_items: list[dict] = []
    for label, fetcher in SOURCES:
        try:
            fetched = fetcher()
            print(f"{label}: {len(fetched)} elementi")
            all_items.extend(fetched)
        except Exception as exc:  # una fonte che fallisce non deve bloccare le altre
            print(f"{label}: SALTATA per errore -> {type(exc).__name__}: {exc}")

    all_items.sort(key=lambda x: x.get("date") or "", reverse=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(all_items, f, allow_unicode=True, sort_keys=False)

    print(f"\nTotale: {len(all_items)} elementi scritti in {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
