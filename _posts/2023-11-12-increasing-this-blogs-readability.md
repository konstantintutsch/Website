---
title: Increasing this blog's readability
description: I have improved this blog's readability. Here's how.
tags: Blog
time: 2023-11-12 19:21:32 +0100
---

In the last few weeks, I have gradually tried to improve this website's readability and efficiency.

{% include heading.html level=3 text="Domain" %}

The most noticiable revision is probably that I moved this website to a new domain. The site's domain now is `konstantintutsch.com` instead of the old `konstantintutsch.de`.

I mainly changed the domain because `.com` suits this site better. I don't write german content here, so using the german TLD didn't really fit except that I'm from Germany.

{% include heading.html level=3 text="Style" %}

But I did not only chose a different domain, I also changed multiple elements of this site.

{% include heading.html level=4 text="Header" %}

First, I decided to get rid of the big heading with my name. This change adds a bit more to the website's simplicity.

{% include image.html file="website-before-com.webp" alt="A browser window with this site open. Logo + title “Konstantin Tutsch”, below links to the Blog, Contact and About page." caption="Before …" %}
{% include image.html file="website-after-com.webp" alt="A browser window with this site open. Logo + links to the Blog, Contact and About page." caption="… and after." %}

Additionally, as you can see on the second image, the title's sizes increased.

{% include heading.html level=4 text="Code" %}

Furthermore, I decided to change the syle of code. I removed highlighting. This may sound horrible, but I can gurantee you it is not.

For the highlighting to work, a lot of CSS was necessary. All of that is gone now and simplicity has won again!

{% include image.html file="code-after-com.webp" alt="A browser window with a blog post open. Gray code." caption="Simple!" %}

{% include heading.html level=3 text="Inner workings" %}

You probably guessed it, things changed. Here's a short list:

- I published the SSG code for this website on [Codeberg](https://codeberg.org/konstantintutsch/Website).
- I added `<lastmod>` to the site's [sitemap](/sitemap.xml).
- I limited the [RSS feed](/feed.xml) to 8 posts.
- I moved the feed from `feed.rss` to `feed.xml`.
