---
layout: page
title: Blog
permalink: /blog/
kicker: A growing archive
summary: Study notes, project notes, and ideas accumulate here without making the homepage longer every time a post is published.
---
<section class="content-section" aria-labelledby="archive-title">
  <div class="archive-toolbar">
    <div>
      <p class="section-label">Archive</p>
      <h2 id="archive-title">All posts</h2>
    </div>
    <p class="archive-count">{{ site.posts | size }} {% if site.posts.size == 1 %}post{% else %}posts{% endif %}</p>
  </div>

  {% if site.posts.size > 0 %}
  <ol class="list archive-list">
    {% for post in site.posts %}
    <li class="post-row">
      <time class="row-date" datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time>
      <a class="row-title" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
      <span class="row-category">{{ post.categories | join: " · " }}</span>
    </li>
    {% endfor %}
  </ol>
  {% else %}
  <div class="empty-state">
    <h2>No posts yet.</h2>
    <p>Study notes and project notes will appear here when they are published.</p>
  </div>
  {% endif %}
</section>
