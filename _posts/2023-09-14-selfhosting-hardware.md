---
layout: post
title: "Selfhosting and Hardware"
description: This post is just a boring list of which devices I use, what software runs on them and how exactly I host the services.
---

## Selfhosting

{% include image.html file="RaspberryPi_Horizontal.jpg" alt="A Raspberry Pi on top of a tiny wooden tower in a white box. A SSD is connected via USB-A 3. Ethernet and power (USB-C) are connected and go through the back of the white box." caption="This is my Raspberry Pi where it's all running on." %}

Selfhosting is great! Not always. I really like selfhosting, but it can be a lot of work and especially time consuming.

I'm selfhosting on a Raspberry Pi, it runs a GoToSocial (Fediverse), Prosody (XMPP) and Radicale (Cal- & CardDAV) server. A 1T Samsung SSD is attached via USB-A 3 to the Raspberry Pi.

There are just two things which I don't self-host: this website and my mail because both shouldn't suffer from outages and shouldn't be limit by my home internet and my Raspberry Pi's hardware. Both are done by my domain provider.

## Hardware

I have got 3 main computers in my life. My phone, my laptop and my Raspberry Pi.

My phone is a Fairphone 4.

My laptop is a [TUXEDO Aura 15 Gen2](https://web.archive.org/web/20220315161215/https://www.tuxedocomputers.com/en/Linux-Hardware/Linux-Notebooks/15-16-inch/TUXEDO-Aura-15-Gen2.tuxedo). I configured it with 32 GB memory (2x16, 3200MHz), an AMD Ryzen 7 5700U (8 cores -> 16 threads, 1.8-4.3GHz) and a 1T NVMe PCIe 4.0 SSD (Samsung 980 Pro). I own a powerful desktop too, but it is on top of a shelf because I have stopped using it.

Last is the Raspberry Pi (4B, 8GB memory).

## Software

- My phone runs [CalyxOS](https://web.archive.org/web/20230723163708/https://calyxos.org/).
- My laptop runs [Gentoo Linux](https://web.archive.org/web/20221104101835/https://www.gentoo.org/) with GNOME. 
- My Rasberry Pi runs Debian.
