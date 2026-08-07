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

{% assign reading_sources = "Hugging Face Blog,Hugging Face Papers,arXiv (cs.AI),OpenAI,Anthropic,Google DeepMind,The Batch,Simon Willison,Ahead of AI,One Useful Thing,antirez" | split: "," %}
{% include ai-feed-groups.html items=items sources=reading_sources %}

## Tools to try

{% assign tool_sources = "Product Hunt (AI),GitHub (new LLM projects)" | split: "," %}
{% include ai-feed-groups.html items=items sources=tool_sources %}

{% else %}
Feed not generated yet: the first update lands at the next scheduled Action run (or trigger it manually from GitHub Actions, workflow "Update AI Feed").
{% endif %}
