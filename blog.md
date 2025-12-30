---
layout: page
title: Blog
permalink: /blog/
---
Here I keep track of what I study and work on.

<ul class="post-list">
  {% for post in site.posts %}
    <li class="post-item">
      <span class="post-date">
        {{ post.date | date: "%Y-%m-%d" }}
      </span>
      <a class="post-title" href="{{ post.url | relative_url }}">
        {{ post.title }}
      </a>
      {% if post.categories %}
        <span class="post-tags">
          {% for cat in post.categories %}
            #{{ cat }}{% unless forloop.last %} {% endunless %}
          {% endfor %}
        </span>
      {% endif %}
    </li>
  {% endfor %}
</ul>
