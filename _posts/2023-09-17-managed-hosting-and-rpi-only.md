---
title: Hosting improvements
description: My website is hosted via managed hosting now. I also increased my Raspberry Pi's network performance. Both are good, even the first one, trust me.
tags: Blog Self-hosting Opinion
---

{% include heading.html level=3 text="Managed hosting for my website 🛡️" %}

I've decided to stop using a VPS to host this site and instead move it to managed hosting. It's more expensive now, but worth it. This may seem stupid. Why limit yourself with managed hosting? A VPS can do a lot more than just a webserver and even was cheaper in my case.

The answer is pretty simple in the end. A VPS isn't as reliable, less secure and limit by it's performance.

The managed hosting plan I use has DDoS protection (you never know), is **not** limit to requests or bandwith, provides 50G of webspace and 20G of email (which I won't use, *notmuch* is just way to useful).

I also like to accidentally break things which isn't good for a personal website.

A few tiny changes were also made to the code of this website. I implemented the the link preview metadata from [OpenGraph](https://ogp.me).

{% include heading.html level=3 text="The Pi lost it's friend" %}

My Raspberry Pi is now on it's own (and that's good!).

I previously had a VPS to host reverse proxies to my [GoToSocial](https://social.konstantintutsch.de) and Radicale server. I decided to stop using a VPS for that and moved the reverse proxies directly onto the Raspberry Pi. Therefore, both subdomains also point to to Pi instead of the VPS.

If you now post something in the Fediverse and e. g. tag my account, it's a tiny, *unnoticable* amount faster 😁

You may wonder now, he could have done that earlier (you'd be right), but that's just the partial truth. You have to know that my router is very *selfish*.

If I visit e. g. my GtS instance from inside my home network, the router should exchange packets with the Pi just like when doing it from outside the network, but instead the router itself is answering with it's own web interface.

What I did was pretty simple in the end: the Raspberry Pi also hosts Pi-hole, a DNS server to block malicious domains, ads and etc. My devices use it as their DNS server as long as they're in the network.

But I can also configure custom DNS entries in Pi-hole, so I added custom entries for the domains which point to the local addresses of the Raspberry Pi. The DNS data, which points to the public addresses of my router, is ignored while my devices are connected to my local network and they automatically use the local addresses instead.
