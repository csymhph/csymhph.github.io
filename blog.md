---
layout: page
title: Blog
permalink: /blog/
---

# Blog

Here I keep track of what I study and work on.

<ul>
  {% for post in site.posts %}
    <li>
      <span>{{ post.date | date: "%Y-%m-%d" }}</span>
      &nbsp;—&nbsp;
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
