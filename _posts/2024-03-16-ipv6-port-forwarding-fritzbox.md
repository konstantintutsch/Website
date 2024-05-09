---
title: IPv6 Port Forwarding on a FritzBOX
description: How to set-up IPv6 port forwarding on an AVM FritzBOX router.
tags: Linux Self-hosting
time: 2024-03-16 11:38:31 +0100
index: true
---

I have just setup IPv6 for this website. It was not as straight forward as I though and that is why I decided to sum up all necessary steps here.

### Permanent IPv6 address

There are two commonly used systems for generating IPv6 addresses.

1. Random: Good for privacy, but impractical for servers. *(temporary)*
2. EUI-64: Based on the MAC address of the interface. *(static)*

You should enable EUI-64 for your server. If it runs a Linux system that is using NetworkManager, execute this command:

```
nmcli con modify "Connection name" ipv6.addr-gen-mode eui64
```

If you do not know what the connection is called, use this command to check which interface uses which connection:

```
nmcli --fields NAME,DEVICE con show
```

{% include image.html file="ipv6-port-forwarding-fritzbox-nm-connection.webp" alt="Wired connection 1 - end0" caption="Output is formatted like a table" %}

Hence, I would need to replace `"Connection name"` with `"Wired connection 1"` in the command above.

The server must be rebooted to use it's new static IPv6 address.

### Checking address

Login to your server and check it's public IPv6 address. On Linux, use the `ip addr` command:

{% include image.html file="ipv6-port-forwarding-fritzbox-ip-addr.webp" alt="The ip addr command output. A lot of IP address, network interfaces and other information." caption="`ip addr` executed on my server" %}

The AAAA record of your domain should point to this address.

If you do not know which IPv6 address is the right one, use the address that does not begin with `fe80::`.

I am aware that this method is not foolproof: this just excludes the local IPv6 address. But it works most of the time! 🤪

An alternative is to use the local address of your server. The FritzBOX will then generate a public IPv6 address accordingly. But that will mess with your DDClient *(DynDNS)* configuration and other services running on your server. You would also need to manually assign the generated IPv6 address to your domain.

### FritzBOX Configuration

Login to your FritzBOX and access the port configuration site for the server you want to expose. Feed the last four numbers of your IPv6 address into the `IPv6 Interface-ID` fields.

{% include image.html file="ipv6-port-forwarding-fritzbox-ipv6-interface-id.webp" alt="FritzBOX webinterface for port forwarding" caption="Make sure to also tick the second checkbox below the IPv6 settings heading" %}

Just save and apply the changes. Your server is now accessible via IPv6! 🥳
