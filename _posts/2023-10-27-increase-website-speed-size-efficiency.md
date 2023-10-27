---
layout: post
title: Increasing the efficiency of a website
description: How I have and you can improve the speed, transfer size and overall efficiency of a website.
tags: Blog Self-hosting
time: 21:19:00 +0200
---

{% include heading.html level=3 text="Why" %}

The answer is pretty simple: **speed**.

Decreasing your page's size includes writing efficient CSS and HTML and also proving small image files in a fitting format. Additionally, many others including myself have also decided to avoid JavaScript completely. 

There also is [The 512KB Club](https://512kb.club/) by Kev Quirk which is a collection of sites transferring less than 512kb initially.

{% include heading.html level=3 text="Favicon" %}

{% highlight html %}
<!-- Icons -->
<link rel="icon" href="/assets/images/favicon-48.png" type="image/png" sizes="48x48">
<link rel="icon" href="/assets/images/favicon-96.png" type="image/png" sizes="96x96">
<link rel="icon" href="/assets/images/favicon-144.png" type="image/png" sizes="144x144">
<link rel="icon" href="/assets/images/favicon-192.png" type="image/png" sizes="192x192">
<link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml" sizes="any">
<link rel="apple-touch-icon" href="/assets/images/favicon-192.png" type="image/png" sizes="192x192">
{% endhighlight %}

This is my part of the header dedicated to the favicon. As you can see, I provide it in multiples of 48px and as an SVG. This allows the client to decide which scale is needed and then only load that version instead of downloading a large favicon to then only downscale it.

You could also choose WebP instead of PNG to decrease the favicon's size even more, but WebP is not a standard for favicons and could become a compatibility issue for some systems. I do not recommend it.

{% include heading.html level=3 text="CSS" %}

Split your CSS files. For example, I've got a `style.css` applied to all pages, but also a `blog.css` only loaded for blog posts.

I also write CSS with less blank space, but the impact is extremly limited and almost non-existent.

{% include heading.html level=3 text="Images" %}

To decrease your images sizes, just encode it to a WebP. WebP's are extremely small and were optimized especially for the web.

Furthermore, for my icon, I wrote the SVG code directly into the HTML. This removes the communication between client and server for yet another file.

{% highlight html %}
<div id="top">
    <a id="site" href="/">
        <svg id="logo" viewBox="0 0 12.7 12.7">
            <g id="layer1" stroke="#000" stroke-linecap="square">
                <circle id="path788" cx="6.35" cy="6.35" r="5" fill="none"/>
                <path id="path1224" d="m1.6605 6.893 7.6874 3.1458"/>
                <path id="path1226" d="m10.426 8.4694-4.842-6.8633"/>
                <path id="path1240" d="m8.0537 6.223-0.44234 0.66357"/>
                <path id="path1242" d="m3.2493 6.9411 0.96239-0.76841"/>
                <path id="path2192" d="m9.7719 9.6868-7.1723-5.9957"/>
            </g>
        </svg>
        <h1 id="title">{{ site.title }}</h1>
    </a>
</div>
{% endhighlight %}

{% include heading.html level=3 text="Measuring your site" %}

You can use [GTmetrix](https://gtmetrix.com/). It is a great tool to get not only info on your site's performance, but also tips on improving it and a "waterfall" of all files loaded: their size and loading time, combined in a timeline.

Here's a few screenshots on how the home page of this site performend:

{% include image.html file="gtmetrix-2023-10-27.webp" alt="a performance report on this site by gtmetrix. grade a with 99% performance and 100% structure. largest contentfuk paint took 756ms and the site was fully loaded after 1.2s" caption="Overall performance" %}

{% include image.html file="gtmetrix-2023-10-27-waterfall.webp" alt="a diagramm of the loading for this site. 71.4kb uncompressed loaded in 1.3s" caption="The waterfall" %}
