---
title: "AI Feed"
layout: single
author_profile: true
permalink: /ai-feed/
---

Automatic digest from Hugging Face, arXiv, OpenAI, Anthropic, Google DeepMind, The Batch, independent voices (Simon Willison, Ahead of AI, One Useful Thing, antirez), and new AI tools worth trying (Product Hunt, GitHub). Updated daily, every title links to the original source.

{% assign items = site.data.ai_feed %}
{% if items and items.size > 0 %}

## Reading

{% assign reading_sources = "Hugging Face Blog,Hugging Face Papers,arXiv (cs.AI),arXiv (DeepSeek/Qwen/Kimi/GLM),OpenAI,Anthropic,Google DeepMind,The Batch,Simon Willison,Ahead of AI,One Useful Thing,antirez,Andrej Karpathy" | split: "," %}
{% for source in reading_sources %}
  {% assign group_items = items | where: "source", source %}
  {% if group_items.size > 0 %}
<h3 class="ai-feed-group-title">{{ source }}</h3>
<ul class="ai-feed-list">
{% for item in group_items %}
  <li class="ai-feed-item">
    {% if item.date and item.date != "" %}<span class="ai-feed-date">{{ item.date }}</span>{% endif %}
    <a href="{{ item.link }}" target="_blank" rel="noopener">{{ item.title }}</a>
  </li>
{% endfor %}
</ul>
  {% endif %}
{% endfor %}

## Tools to try

{% assign tool_sources = "Product Hunt,GitHub (trending AI/LLM/Agents)" | split: "," %}
{% for source in tool_sources %}
  {% assign group_items = items | where: "source", source %}
  {% if group_items.size > 0 %}
<h3 class="ai-feed-group-title">{{ source }}</h3>
<ul class="ai-feed-list">
{% for item in group_items %}
  <li class="ai-feed-item">
    {% if item.date and item.date != "" %}<span class="ai-feed-date">{{ item.date }}</span>{% endif %}
    <a href="{{ item.link }}" target="_blank" rel="noopener">{{ item.title }}</a>
  </li>
{% endfor %}
</ul>
  {% endif %}
{% endfor %}

{% else %}
Feed not generated yet: the first update lands at the next scheduled Action run (or trigger it manually from GitHub Actions, workflow "Update AI Feed").
{% endif %}
