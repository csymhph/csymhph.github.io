---
layout: page
title: Blog
permalink: /blog/
---

Here I keep track of what I study and work on.

<ul class="post-list">
  {% for post in site.posts %}

    <li class="post-item">

      <div class="post-date">
        {{ post.date | date: "%Y-%m-%d" }}
      </div>

      <div class="post-title">
        <a href="{{ post.url | relative_url }}">
          {{ post.title }}
        </a>
      </div>

      {% if post.categories %}
      <div class="post-tags">
        {% for cat in post.categories %}
          <span>#{{ cat }}</span>
        {% endfor %}
      </div>
      {% endif %}

    </li>

  {% endfor %}
</ul>
