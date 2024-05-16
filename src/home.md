---
layout: default
permalink: /
title: Konstantin Tutsch
description: Welcome to Konstantin Tutsch's website. Discover lots of information about me, contact options, my photography and my personal blog.
---

## {{ title }}

<p class="info">{% social "github", "GitHub" %}</p>
<p class="info"><a data-umami-event="photography" href="/i">Photography</a></p>
<p class="info">{% social "mail", "Email" %}</p>
<p class="info">{% social "fediverse", "Mastodon" %}</p>

---

{% set counter = 0 %}
{% for post in collections.post | reverse %}
    {% if counter < 10 %}
    {% navPost post %}
    {% set counter = counter + 1 %}
    {% endif %}
{% endfor %}

---

<p class="info">{% include "nav-blog.njk" %}</p>
