---
layout: post
title: Using Fail2Ban With an External Firewall
description: Do you want to use your hosting providers firewall and Fail2Ban? Here's a simple solution.
tags: ["post", "security", "linux", "self-hosting"]
date: 2024-07-24T20:59:59+02:00
index: true
---

The VPS that now hosts this exact website received a flood of malicious SSH login attempts today. A great opportunity to set up Fail2Ban, I thought.

That's a pretty easy task. Until someone has any silly preferences. And in that case, that someone was me.

### An Overly Complicated Introduction

I really like the integrated firewall of my hosting provider. A beautiful, user-friendly and also powerful interface, no stupid iptables of firewalld shenanigans and probably located somewhere in the virtualization layer of the VPS so that no computing power of my box will ever be wasted on blocking nonsense requests.

The problem with Fail2Ban is, that it isn't responsible for blocking. Just for identifying malicious IPs and relaying them to, 
in the majority of cases, a firewall. And in this case, the firewall is not located on the system itself and definitely not supported by any of the premade configurations for Fail2Ban.

One could now create a configuration for that external firewall and go mad about all the specifics of whatever API the external firewall provides. Or you could keep the external firewall for static rules, set up an internal firewall on the server itself that allows all traffic and then use this internal firewall to block all the IPs that are being so impolite towards your system.

I know that I'm betraying myself, because I'm now definitely _wasting computing power of my box for blocking nonsense requests_, but I don't care. It is illogical. Accept it.

Now that I've wasted your time, here's how I implemented whatever I just described. I'll be using FirewallD as my internal firewall as it is the default on Fedora Linux. And I like Fedora Linux.

### The Internal Firewall

First, create a custom zone in `/etc/firewalld/zones/all.xml`:

```xml
<zone target="ACCEPT"> 
    <short>All</short> 
    <description>This zone accepts all traffic</description>
</zone>
```

Then, enable and start FirewallD, select the zone as default, save the changes and reload just to be sure:

```
systemctl enable --now firewalld
firewall-cmd --set-default-zone=all
firewall-cmd --runtime-to-permanent
firewall-cmd --reload
```

### Fail2Ban

Finally, select FirewallD as Fail2Ban's “backend” in `/etc/fail2ban/jail.local` under `[DEFAULT]`:

```
…
[DEFAULT]
banaction = firewallcmd-rich-rules[actiontype=]
banaction_allports = firewallcmd-rich-rules[actiontype=]
…
```

### Overcomplicated

That's it! A lot of words for a really limited amount of actual instructions.