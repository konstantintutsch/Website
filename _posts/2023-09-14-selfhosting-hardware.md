---
layout: post
title: "Selfhosting & Hardware"
---

Just a little bit of infomation about the structure of this blog post, I put the selfhosting part first, because the other stuff is just a boring list. But if you want to know first which hardware I use, just scoll down to the [Hardware](#hardware) heading.

## Selfhosting

Selfhosting is great! Not always. I really like selfhosting, but it can be a lot of work and especially time consuming.

I'm selfhosting on a Raspberry Pi, it runs a GoToSocial (Fediverse), Prosody (XMPP) and Radicale (Cal- & CardDAV) server. A 1T Samsung SSD is attached via USB-A 3 to the Raspberry Pi.

Also: GtS and Radicale aren't directly access by any client. A reverse proxy on a VPS is between them.

The reason is pretty simple: the router of my home network is really weird with ports 80 and 443. So the services wouldn't look "normal" as in: they wouldn't be on default http ports.

The VPS also hosts this website *directly*.

## Hardware

I have got 3 main computers in my life. My phone, my laptop and my Raspberry Pi.

My phone is a Fairphone 4.

My laptop is a [TUXEDO Aura 15 Gen2](https://web.archive.org/web/20220315161215/https://www.tuxedocomputers.com/en/Linux-Hardware/Linux-Notebooks/15-16-inch/TUXEDO-Aura-15-Gen2.tuxedo). I configured it with 32 GB memory (2x16, 3200MHz), an AMD Ryzen 7 5700U (8 cores -> 16 threads, 1.8-4.3GHz) and a 1T NVMe PCIe 4.0 SSD (Samsung 980 Pro). I own a powerful desktop too, but it is on top of a shelf because I have stopped using it.

Last is the Raspberry Pi (4B, 8GB memory).

## Software

- My phone runs [CalyxOS](https://web.archive.org/web/20230723163708/https://calyxos.org/).
- My laptop runs [Gentoo Linux](https://web.archive.org/web/20221104101835/https://www.gentoo.org/) with GNOME. 
- My Rasberry Pi runs Debian.
