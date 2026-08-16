---
layout: default
title: Sangyeon Cho
permalink: /
---
<section class="intro" aria-labelledby="intro-title">
  <div class="shell intro-grid">
    <div>
      <p class="eyebrow">Causality · Uncertainty · Explanation</p>
      <h1 id="intro-title">Sangyeon Cho</h1>
      <p class="intro-copy">
        Incoming Ph.D. student in Data Science at the
        <a href="https://gsds.snu.ac.kr/"><strong>Graduate School of Data Science, Seoul National University</strong></a>,
        starting in September 2026 and advised in the Causality Lab by Professor
        <a href="https://www.sanghacklee.me/"><strong>Sanghack Lee</strong></a>.
        My research focuses on causal inference, uncertainty quantification,
        conformal prediction, and time-series analysis, particularly
        individualized treatment effect estimation and decision-making under
        uncertainty in longitudinal settings.
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
          <dd>Incoming Ph.D. student</dd>
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
        <p class="section-label">Research</p>
        <h2 id="research-title">Areas of work</h2>
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
          <h3>Uncertainty quantification</h3>
          <p>Conformal prediction and transparent uncertainty measures for individualized treatment effects.</p>
        </div>
      </article>
      <article class="topic-card">
        <span class="topic-number">03</span>
        <div>
          <h3>Time-series analysis</h3>
          <p>Longitudinal and time-dependent settings with evolving treatments, outcomes, and confounding factors.</p>
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section-compact" aria-labelledby="work-title">
  <div class="shell">
    <div class="section-header">
      <div>
        <p class="section-label">Current and past</p>
        <h2 id="work-title">Projects</h2>
      </div>
    </div>
    <ol class="record-list" aria-label="Current and past projects">
      <li class="record-row">
        <span class="record-date">2026–Present</span>
        <div class="record-copy">
          <h3>AI Platform for Predicting Drug Efficacy and Side Effects from Integrated Medical and Multi-omics Data</h3>
          <p>Participant · National research project, Ministry of Food and Drug Safety</p>
        </div>
      </li>
      <li class="record-row">
        <span class="record-date">2025–Present</span>
        <div class="record-copy">
          <h3>Advancing Credit Decision Making</h3>
          <p>Working-level lead · Industry–academia collaborative research project, AFINIT</p>
        </div>
      </li>
      <li class="record-row">
        <span class="record-date">2025</span>
        <div class="record-copy">
          <h3>Metabolomic Big Data Analysis</h3>
          <p>Participant · National research project, Ministry of Food and Drug Safety</p>
        </div>
      </li>
    </ol>
  </div>
</section>

<section class="section section-compact" aria-labelledby="news-title">
  <div class="shell">
    <div class="section-header">
      <div>
        <p class="section-label">Updates</p>
        <h2 id="news-title">News</h2>
      </div>
    </div>
    <ol class="record-list" aria-label="News">
      <li class="record-row">
        <time class="record-date" datetime="2025">2025</time>
        <div class="record-copy"><p>Opened this website.</p></div>
      </li>
    </ol>
  </div>
</section>

<section class="section section-compact" aria-labelledby="recent-title">
  <div class="shell">
    <div class="section-header">
      <div>
        <p class="section-label">Writing</p>
        <h2 id="recent-title">Recent writing</h2>
      </div>
      <a class="section-link" href="{{ '/blog/' | relative_url }}">View all posts →</a>
    </div>
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
  </div>
</section>

<section class="section section-compact" aria-labelledby="education-title">
  <div class="shell">
    <div class="section-header">
      <div>
        <p class="section-label">Training</p>
        <h2 id="education-title">Education</h2>
      </div>
    </div>
    <ol class="record-list" aria-label="Education">
      <li class="record-row">
        <span class="record-date">Sep 2026–</span>
        <div class="record-copy">
          <h3>Ph.D. in Data Science</h3>
          <p>Seoul National University · Incoming</p>
        </div>
      </li>
      <li class="record-row">
        <span class="record-date">Aug 2026</span>
        <div class="record-copy">
          <h3>Master of Data Science</h3>
          <p>Seoul National University</p>
        </div>
      </li>
      <li class="record-row">
        <span class="record-date">2024</span>
        <div class="record-copy">
          <h3>B.A. in Economics</h3>
          <p>Seoul National University</p>
        </div>
      </li>
    </ol>
  </div>
</section>
