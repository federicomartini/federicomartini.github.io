---
layout: single
author_profile: true
permalink: /
---

Helping others to understand AI by calmly learning, building, and sharing lessons learned.

### The Silent Commit
The newsletter where I share experiences, lessons learned and other things I find interesting.

<form
  action="https://buttondown.com/api/emails/embed-subscribe/SilentCommit"
  method="post"
  target="popupwindow"
  onsubmit="window.open('https://buttondown.com/SilentCommit', 'popupwindow')"
  class="embeddable-buttondown-form">
  <input type="email" name="email" id="bd-email" />
  
  <input type="submit" value="Subscribe" />
</form>

### What I do

- Develop AI solutions for business processes
- Present and share insights as a company speaker on digital transformation
- Commit to lifelong learning and continuous improvement


### What I did

- Delivered Machine Learning solutions tailored for manufacturing and industrial processes, enhancing automation and decision-making
- Mentored thousands of developers through Udacity courses on AI, ML, Deep Learning, Android, Azure AI, and VR with Unity
- Designed and implemented complete Industrial IoT architectures, from data collection to visualization through web dashboards
- Handled industrial communication protocols such as OPC-UA, CAN, Modbus, Profinet, Ethernet/IP, RS232/485, and more
- Integrated and managed sensors and actuators across various platforms, ensuring seamless hardware–software interaction
- Built autonomous control systems in C and IEC-61131, including a Minesweeper autopilot and crane stability logic on custom hardware with Codesys
- Developed low-level software for toll payment systems in C and C++, focusing on real-time performance and reliability

### Education

- I graduated in Automation & Computer Science Engineering MS from University of Ferrara

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
