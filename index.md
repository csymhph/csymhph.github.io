---
layout: default
title: Sangyeon Cho
permalink: /
---
<section class="intro" id="top" aria-labelledby="intro-title">
  <div class="shell intro-grid">
    <div class="intro-main">
      <h1 id="intro-title">{{ site.title | escape }}</h1>
      <p class="role">
        Causality Lab,
        <a href="https://gsds.snu.ac.kr/">Graduate School of Data Science, Seoul National University</a>,
        with <a href="https://www.sanghacklee.me/">Sanghack Lee</a>.
        Continuing in the lab as a Ph.D. student from September 2026.
      </p>
      <p class="claim">{{ site.claim }}</p>
      <p class="contact">
        <span class="contact-label">Contact</span>
        {{ site.email | escape }}
      </p>
    </div>
    {% if site.portrait and site.portrait != empty %}
    <aside class="intro-aside">
      <img class="portrait" src="{{ site.portrait | relative_url }}" alt="Portrait of {{ site.title | escape }}" width="200" height="200">
      {% if site.cv_url and site.cv_url != empty or site.linkedin_url and site.linkedin_url != empty %}
      <p class="profile-links">
        {% if site.cv_url and site.cv_url != empty %}<a href="{{ site.cv_url | escape }}">CV</a>{% endif %}
        {% if site.cv_url and site.cv_url != empty and site.linkedin_url and site.linkedin_url != empty %}<span class="separator-mark" aria-hidden="true">·</span>{% endif %}
        {% if site.linkedin_url and site.linkedin_url != empty %}<a href="{{ site.linkedin_url | escape }}">LinkedIn</a>{% endif %}
      </p>
      {% endif %}
    </aside>
    {% endif %}
  </div>
</section>

<section class="band" id="research-interests" aria-labelledby="research-interests-title">
  <div class="shell">
    <h2 id="research-interests-title">Research interests</h2>
    <div class="areas">
      {% for area in site.research_interests %}
      <div class="area">
        <h3>{{ area.name }}</h3>
        <p>{{ area.description }}</p>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<section class="band" id="works" aria-labelledby="works-title">
  <div class="shell">
    <h2 id="works-title">Works</h2>
    <p class="section-intro">A short selection of current work, workshop presentations, and my master's thesis.</p>
    <ol class="records" aria-label="Works">
      <li class="record">
        <span class="record-date">In progress</span>
        <div class="record-copy">
          <h3>Conformal Meta-learner for Individual Treatment Effects under Unmeasured Confounding</h3>
          <p>Jaeho Jeong, Sangyeon Cho, and Sanghack Lee†</p>
        </div>
      </li>
      <li class="record">
        <span class="record-date">Under review</span>
        <div class="record-copy">
          <h3>Decomposing Conformal Uncertainty: Calibration- and Instance-Driven Feature Attribution</h3>
          <p>Sangyeon Cho*, Minyoung Cho*, Jungsoo Kim*, and Sanghack Lee†</p>
        </div>
      </li>
      <li class="record">
        <span class="record-date">Under review</span>
        <div class="record-copy">
          <h3>OPERA-S: Deterministic Tail Safety in Ensemble Off-Policy Evaluation</h3>
          <p>Hyunwoo Kim, Gyeongchan Han, Bogeun Kim, Serjin Kim, Sangyeon Cho, Junha Ham, Jaehyeok Shin, and Sanghack Lee†</p>
        </div>
      </li>
      <li class="record">
        <span class="record-date">ICML 2026 (WS)</span>
        <div class="record-copy">
          <h3>A Tale of Two Uncertainties: Global–Local Attribution for Conformal Prediction</h3>
          <p>Sangyeon Cho*, Minyoung Cho*, Jungsoo Kim*, and Sanghack Lee† · 2nd Workshop on Epistemic Intelligence in Machine Learning (EIML), non-archival · Spotlight talk</p>
        </div>
      </li>
      <li class="record">
        <span class="record-date">Aug 2026</span>
        <div class="record-copy">
          <h3>Conformal Prediction for Individual Treatment Effects under Time-Varying Treatment Strategies</h3>
          <p>Sangyeon Cho · Master of Data Science, Seoul National University</p>
        </div>
      </li>
    </ol>
    <p class="note">* Equal contribution. † Corresponding author.</p>
  </div>
</section>

<section class="band" id="research-projects" aria-labelledby="research-projects-title">
  <div class="shell">
    <h2 id="research-projects-title">Research projects</h2>
    <ol class="records" aria-label="Research projects">
      <li class="record">
        <span class="record-date">2026–Present</span>
        <div class="record-copy">
          <h3>AI Platform for Predicting Drug Efficacy and Side Effects from Integrated Medical and Multi-omics Data</h3>
          <p>Ministry of Food and Drug Safety</p>
        </div>
      </li>
      <li class="record">
        <span class="record-date">2025–2026</span>
        <div class="record-copy">
          <h3>Advancing Credit Decision Making</h3>
          <p>Industry–academia collaboration, AFINIT</p>
        </div>
      </li>
      <li class="record">
        <span class="record-date">2025</span>
        <div class="record-copy">
          <h3>Metabolomic Big Data Analysis</h3>
          <p>Ministry of Food and Drug Safety</p>
        </div>
      </li>
    </ol>
  </div>
</section>

<section class="band" id="news" aria-labelledby="news-title">
  <div class="shell">
    <h2 id="news-title">News</h2>
    <ol class="records" aria-label="News">
      <li class="record">
        <time class="record-date" datetime="2026-08">Aug 2026</time>
        <div class="record-copy">
          <h3>I completed my Master of Data Science at SNU!</h3>
          <p>Many thanks to my advisor, Professor Sanghack Lee, and all my collaborators.</p>
        </div>
      </li>
      <li class="record">
        <time class="record-date" datetime="2026-07">Jul 2026</time>
        <div class="record-copy"><h3>Spotlight talk at the EIML workshop, ICML 2026</h3></div>
      </li>
    </ol>
  </div>
</section>

<section class="band" id="education" aria-labelledby="education-title">
  <div class="shell">
    <h2 id="education-title">Education</h2>
    <ol class="records" aria-label="Education">
      <li class="record">
        <span class="record-date">Sep 2026–</span>
        <div class="record-copy"><h3>Ph.D. in Data Science</h3><p>Seoul National University</p></div>
      </li>
      <li class="record">
        <span class="record-date">Aug 2026</span>
        <div class="record-copy"><h3>Master of Data Science</h3><p>Seoul National University</p></div>
      </li>
      <li class="record">
        <span class="record-date">2024</span>
        <div class="record-copy"><h3>B.A. in Economics</h3><p>Seoul National University</p></div>
      </li>
    </ol>
  </div>
</section>

<section class="band" id="hobbies" aria-labelledby="hobbies-title">
  <div class="shell">
    <h2 id="hobbies-title">Hobbies</h2>
    <ul class="interests">
      <li><h3>Calligraphy</h3></li>
      <li><h3>Piano</h3></li>
      <li><h3>Baseball</h3></li>
    </ul>
  </div>
</section>
