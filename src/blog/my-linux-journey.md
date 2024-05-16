---
layout: post
title: My Linux journey
description: My Linux journey. The distributions I've used and what I think about them.
tags: ["post", "linux"]
date: "2023-09-14T01:00:00+02:00"
---

### The beginning

My first touching points with Linux were somewhere in autumn of 2020.

I had a lot of free time because of the first corona lockdown. So I replaced my Windows 10 install with Linux. No dual-booting. I only had one backup of my data back then. Risky.

It was Ubuntu 20.04 LTS. The first thing I did was a search about how to "run" a .deb file. I literally had no idea.

But the linux machine, a Dell laptop, died. I was definetly not the one who killed it. Noooo. I drilled a screw through the mainboard while adding extra storage.

### A new device

I got a desktop (without an external graphics card). But luckily with everything else. I already had a display, keyboard and mouse because I was a "gamer". So they all were happily blinking in too many colors.

The first thing I did was to reinstall Ubuntu. The desktop is a custom configuration from a local computer store which had good reputation. I was able to buy it without a windows key too. No money wasted.

But a problem occured. The desktop has RGB memory sticks. I was able to find [OpenRGB](https://web.archive.org/web/20220927155955/https://openrgb.org/). But it was a nightmare to get it to work because the only thing I used the command line before were copy-past wine/proton commands to get all my games running at the time. And I didn't understand the Linux permission system and all the services running in the background. It eventually worked.

### The distrohopping fever

I don't remember the distros. But there were a lot.

### openSUSE Tumbleweed

I used it for like 3 months. It is a good distro. I still don't understand why there are so many Linux users who hate it.

### Gentoo Linux

The distro that made me a Linux power user. And also the distro that made me angry, **really** angry. I really like Gentoo. It gives the user a lot of power. I really like that mentality of an absolutly perfect system for the user's needs.

I've used it from April 2021 untill now.

I had a lot of problems getting it to run first. I got better and even so good, that I configured the kernels for my devices (the desktop and the [laptop](https://web.archive.org/web/20220315161215/https://www.tuxedocomputers.com/en/Linux-Hardware/Linux-Notebooks/15-16-inch/TUXEDO-Aura-15-Gen2.tuxedo), which I bought in 2022).

I started editing the [Gentoo Wiki](https://web.archive.org/web/20220922101556/https://wiki.gentoo.org/wiki/Main_Page) and started an [entry](https://web.archive.org/web/20220929134523/https://wiki.gentoo.org/wiki/TUXEDO_Aura_15_%28Gen2%29) about just mentioned laptop. Gentoo made me try lots of different Linux things. Different desktop enviroments, window managers and command line utilities.

But it also made me experience bad stuff for the first time. I broke my Gentoo install, of course, multiple times. That's not the problem. I'll write the storie a bit more dramatic, in present.

I broke my install again. Sad but something I could fix. After a few hours of reinstalling the OS, I'm at the point of restoring from my backup. I have two scripts. Both are using rsync. Without any confirmation dialogue or warning. One overrides the home directory with the backup and the other overrides the backup with my home directory. The home directory is empty, I execute the script to override my backup accidentally. Everything is gone. I didn't have a second medium with my data. Pure pain.

I was able to recover photos and all other important stuff. Only one thing was gone: my KDBX database (used for password managing). The only way I could access my mail was through my phone where a token to my account was in cache. I restored all of my accounts somehow. Even the 2FA ones.

### Debian (on my servers only)

Stable, really stable. My Raspberry Pi and VPSs run it. I never broke a Debian install and consider myself a experienced Debian user, **not** a power user. That's it, lucky.

The best distros don't have a lot to say about them. (except Gentoo, I'm 100% biased about it 😉)
