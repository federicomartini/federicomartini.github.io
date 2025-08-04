---
layout: single
author_profile: true
permalink: /
---


Hi, I'm Federico Martini 
I'm a software engineer and AI enthusiast based in Italy 🇮🇹  
I build things that connect machines, data, and people.
I love coding, learning, and trying new things

---

### What I do

- AI & Machine Learning applications for industry
- Industrial IoT, Data Analysis & Web Dashboards
- Company Speaker on Digital Services
- Lifelong Learner
- Runner

---

### What I did

- Toll payments systems in C and CPP
- Minesweeper autopilot system in C and IEC-61131
- Rear-Mounted crane stability system in Codesys on custom control units
- Management of sensors and actuators in every single applications
- Management of the communication using OPC-UA, CAN, Modbus, Profinet, Ethernet/IP, Ethernet, Serial RS232/485, and many other protocols
- Mentor for many courses released by Udacity on AI, Machine Learning, Deep Learning, Android Development, Azure AI tools, VR Development in Unity

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

{% if site.posts.size > 1 %}
  <p><a href="{{ '/posts/' | relative_url }}" class="btn btn--primary">View All Posts</a></p>
{% endif %}
