---
title: "AI Feed"
layout: single
author_profile: true
permalink: /ai-feed/
---

Automatic digest from Hugging Face, arXiv, OpenAI, Anthropic, Google DeepMind and The Batch. Updated daily, every title links to the original source.

{% assign items = site.data.ai_feed %}
{% if items and items.size > 0 %}
<ul class="ai-feed-list">
{% for item in items %}
  <li class="ai-feed-item">
    <span class="ai-feed-source">{{ item.source }}</span>
    {% if item.date and item.date != "" %}<span class="ai-feed-date">{{ item.date }}</span>{% endif %}
    <a href="{{ item.link }}" target="_blank" rel="noopener">{{ item.title }}</a>
  </li>
{% endfor %}
</ul>
{% else %}
Feed not generated yet: the first update lands at the next scheduled Action run (or trigger it manually from GitHub Actions, workflow "Update AI Feed").
{% endif %}
