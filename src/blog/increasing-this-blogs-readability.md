---
layout: post
title: Increasing this blog's readability
description: I have improved this blog's readability. Here's how.
tags: ["post", "blog"]
date: 2023-11-12T19:21:32+01:00
---

In the last few weeks, I have gradually tried to improve this website's readability and efficiency.

### Domain

The most noticiable revision is probably that I moved this website to a new domain. The site's domain now is `konstantintutsch.com` instead of the old `konstantintutsch.de`.

I mainly changed the domain because `.com` suits this site better. I don't write german content here, so using the german TLD didn't really fit except that I'm from Germany.

### Style

But I did not only chose a different domain, I also changed multiple elements of this site.

#### Header

First, I decided to get rid of the big heading with my name. This change adds a bit more to the website's simplicity.

{% image "website-before-com.webp", "A browser window with this site open. Logo + title “Konstantin Tutsch”, below links to the Blog, Contact and About page.", "Before …" %}
{% image "website-after-com.webp", "A browser window with this site open. Logo + links to the Blog, Contact and About page.", "… and after." %}

Additionally, as you can see on the second image, the title's sizes increased.

#### Code

Furthermore, I decided to change the syle of code. I removed highlighting. This may sound horrible, but I can gurantee you it is not.

For the highlighting to work, a lot of CSS was necessary. All of that is gone now and simplicity has won again!

{% image "code-after-com.webp", "A browser window with a blog post open. Gray code.", "Simple!" %}

### Inner workings

You probably guessed it, things changed. Here's a short list:

- I published the SSG code for this website on [Codeberg](https://codeberg.org/konstantintutsch/Website).
- I added `<lastmod>` to the site's [sitemap](/sitemap.xml).
- I limited the [RSS feed](/feed.xml) to 8 posts.
- I moved the feed from `feed.rss` to `feed.xml`.
