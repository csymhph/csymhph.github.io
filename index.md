---
layout: default
title: Sangyeon Cho
permalink: /
---
<section class="intro" aria-labelledby="intro-title">
  <div class="shell intro-grid">
    <div>
      <p class="eyebrow">Causality · Uncertainty · Time</p>
      <h1 id="intro-title">Sangyeon Cho</h1>
      <p class="intro-copy">
        Master's student at the
        <a href="https://gsds.snu.ac.kr/"><strong>Graduate School of Data Science, Seoul National University</strong></a>,
        interested in causal inference, conformal prediction, and time-series
        causal inference.
      </p>
      <div class="actions" aria-label="Primary contact links">
        <a class="button button-primary" href="mailto:{{ site.email }}">Email me ↗</a>
        <a class="button button-secondary" href="https://github.com/{{ site.github_username }}">GitHub ↗</a>
      </div>
    </div>

    <aside class="profile-card" aria-label="Current profile">
      <dl>
        <div class="profile-card-row">
          <dt>Current</dt>
          <dd>Master's student</dd>
        </div>
        <div class="profile-card-row">
          <dt>At</dt>
          <dd>SNU Graduate School of Data Science</dd>
        </div>
        <div class="profile-card-row">
          <dt>Based</dt>
          <dd>Seoul, Republic of Korea</dd>
        </div>
      </dl>
    </aside>
  </div>
</section>

<section class="section" aria-labelledby="research-title">
  <div class="shell">
    <div class="section-header">
      <div>
        <p class="section-label">Focus</p>
        <h2 id="research-title">Research interests</h2>
      </div>
    </div>
    <div class="topic-grid">
      <article class="topic-card">
        <span class="topic-number">01</span>
        <div>
          <h3>Causal inference</h3>
          <p>Reasoning about interventions, counterfactuals, and causal structure.</p>
        </div>
      </article>
      <article class="topic-card">
        <span class="topic-number">02</span>
        <div>
          <h3>Conformal prediction</h3>
          <p>Quantifying predictive uncertainty with transparent guarantees.</p>
        </div>
      </article>
      <article class="topic-card">
        <span class="topic-number">03</span>
        <div>
          <h3>Time-series causality</h3>
          <p>Studying causal questions when relationships evolve over time.</p>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="recent-title">
  <div class="shell">
    <div class="section-header">
      <div>
        <p class="section-label">Continuously updated</p>
        <h2 id="recent-title">Recent writing</h2>
      </div>
      <a class="section-link" href="{{ '/blog/' | relative_url }}">View all posts →</a>
    </div>

    <div class="content-grid">
      {% if site.posts.size > 0 %}
      <ol class="list" aria-label="Recent posts">
        {% for post in site.posts limit: 3 %}
        <li class="post-row">
          <time class="row-date" datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%Y-%m-%d" }}</time>
          <a class="row-title" href="{{ post.url | relative_url }}">{{ post.title | escape }}</a>
          <span class="row-category">{{ post.categories | join: " · " }}</span>
        </li>
        {% endfor %}
      </ol>
      {% else %}
      <p class="quiet-note">Writing will appear here as posts are published.</p>
      {% endif %}

      <aside class="side-card" aria-labelledby="work-title">
        <p class="section-label">Selected work</p>
        <h3 id="work-title">Current and recent projects</h3>
        <ul class="compact-list">
          <li><strong>Advancing Credit Decision Making</strong><span>Afinit · 2026</span></li>
          <li><strong>Metabolomic Big Data Analysis</strong><span>MFDS · 2025</span></li>
        </ul>
      </aside>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="about-title">
  <div class="shell details-grid">
    <div>
      <p class="section-label">Background</p>
      <h2 id="about-title">Across disciplines</h2>
    </div>
    <div class="prose-block">
      <p>
        I work with Professor <a href="https://www.sanghacklee.me/">Sanghack Lee</a>
        in the Causality Lab. Before joining the lab, I majored in Economics at
        Seoul National University.
      </p>
      <p>
        My interests also extend to machine learning, economics, and philosophy.
        I welcome conversations with people from different backgrounds.
      </p>
      <div class="background-panels">
        <section class="background-panel" aria-labelledby="education-title">
          <h3 id="education-title">Education</h3>
          <p>B.A. in Economics, Seoul National University, 2018–2024</p>
        </section>
        <section class="background-panel" aria-labelledby="news-title">
          <h3 id="news-title">News</h3>
          <ul class="news-list">
            <li><time datetime="2025">2025</time><span>Opened this website</span></li>
          </ul>
        </section>
      </div>
      <div class="contact-fact">
        <span>Contact</span>
        <p><a href="mailto:csymhph@snu.ac.kr">csymhph@snu.ac.kr</a> · <a href="mailto:csymhph@gmail.com">csymhph@gmail.com</a></p>
      </div>
    </div>
  </div>
</section>
