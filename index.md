---
layout: single
author_profile: true
permalink: /
---

Helping others by calmly learning AI, building applications and sharing lessons.

---

### What I do

- Develop AI solutions for business processes
- Present and share insights as a company speaker on digital transformation
- Commit to lifelong learning and continuous improvement

---

### What I did

- Designed and deployed Machine Learning solutions for real-world industrial use cases, from vision systems to predictive models
- Developed full Industrial IoT pipelines, integrating data acquisition, processing, and web-based dashboards for factory insights
- Engineered toll payment systems using C and C++, with a focus on embedded performance and reliability
- Created a fully autonomous Minesweeper autopilot in C and IEC-61131 for PLC-based environments
- Developed a stability control system for rear-mounted cranes using Codesys and custom hardware platforms
- Handled low-level sensor and actuator integration across diverse applications, ensuring real-time performance
- Managed industrial communication protocols including OPC-UA, CAN, Modbus, Profinet, Ethernet/IP, RS232/485, and more
- Served as a Mentor and Reviewer for Udacity, supporting thousands of students in AI, ML, Deep Learning, Android, Azure AI, and VR with Unity

---

### Education

- I graduated in Automation & Computer Science Engineering MS from University of Ferrara

---

### Find me

- [GitHub](https://github.com/federicomartini) 
- [Linkedin](https://www.linkedin.com/in/federicomartini/)
- [X](https://x.com/martinife)

---

### Recent Posts
About my learnings, experiences and thoughts

{% for post in site.posts limit:5 %}
  <article class="archive__item" itemscope itemtype="https://schema.org/CreativeWork">
    <h2 class="archive__item-title" itemprop="headline">
      <a href="{{ post.url | relative_url }}" rel="permalink">{{ post.title }}</a>
    </h2>
    {% if post.excerpt %}
      <p class="archive__item-excerpt" itemprop="description">{{ post.excerpt | markdownify | strip_html | truncate: 160 }}</p>
    {% endif %}
  </article>
{% endfor %}

{% if site.posts.size > 5 %}
  <p><a href="{{ '/posts/' | relative_url }}" class="btn btn--primary">View All Posts</a></p>
{% endif %}
