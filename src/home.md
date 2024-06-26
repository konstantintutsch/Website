---
layout: default
permalink: /
title: Konstantin Tutsch
description: Welcome to Konstantin Tutsch's website. Discover lots of information about me, contact options, my photography and my personal blog.
---

## {{ title }}

---

### Recent posts

{% set counter = 0 %}
{% for post in collections.post | reverse %}
    {% if counter < site.recent %}
    {% post post %}
    {% set counter = counter + 1 %}
    {% endif %}
{% endfor %}

Blog - {% include "nav-blog.njk" %}

### Contact

Thought of feedback? Got questions? Or just want to chat? Tell me!

#### Email

Email is the preferred way to get in touch with me. <sup>*[plain text encouraged](https://useplaintext.email/)*</sup>

{% include "email.md" %}

PGP - [`0780 DF44 892D 3E38 97A5  ED3B BF74 22C5 AF13 F183`](/pgp)

#### Mastodon (Fediverse)

I'm also on Mastodon. You can follow me there at {% social "fediverse" %}

### Code

For all those interested in programming, you can take a look at my {% social "github", "GitHub profile" %}

---

<p class="info">{% include "copyright.njk" %}</p>
