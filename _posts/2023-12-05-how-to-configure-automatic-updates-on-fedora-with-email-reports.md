---
layout: post
image: 
title: How to configure automatic updates on Fedora with e-mail reports
description: How to use DNF Automatic and Postfix for automatically updating your Fedora server and sending reports via e-mail about the update.
tags: Self-hosting
time: 2023-12-05 20:03:09 +0100
---

{% include heading.html level=3 text="Requirements" %}

You first need to install `dnf-automatic`, `postfix` and `mailx`:

```
dnf install -y dnf-automatic postfix mailx
```

After all programms have been installed, you can start configuring the e-mail server.

{% include heading.html level=3 text="E-Mail Server" %}

Postfix's configuration is located at `/etc/postfix/main.cf`. These are the values that should be set:

- `myhostname`: This value is used for various settings regarding, amongs other things, your e-mail domain.
- `mydomain`: *see myhostname*
- `mynetworks_style` *(or `mynetworks`)*: This defines which *places* in your network are authorized to send e-mails.

I have configured Postfix like this:

```
myhostname = notmalware.info
mydomain = notmalware.info

mynetworks_style = host
```

To test your Postfix configuration, you can execute this command:

```
echo "Hi, I'm your e-mail's body!" | mailx -r "test@server" -s "A test e-mail from Postfix!" "you@example.com"
```

Now that your e-mail server is working fine, you can configure DNF Automatic! 🤩

{% include heading.html level=3 text="DNF Automatic" %}

Automatic is a component of DNF. It's configuration file is located at `/etc/dnf/automatic.conf`.

Here are all the necessary configuration parameters:

{% include heading.html level=4 text="[commands]" %}

- `random_sleep`: The interval *(in seconds)* between searching for new updates. — `yes` / `no`
- `download_updates`: If packages that can be updated should be downloaded automatically. — `yes` / `no`
- `apply_updates`: If updates for packages should be installed automatically. — `yes` / `no`
- `reboot`: Whether to reboot after updates. — `never` / `when-changed` / `when-needed`

{% include heading.html level=4 text="[emitters]" %}

- `emit_via`: How to inform the system administrator on activities. — `email` / `command_email` / `command`

{% include heading.html level=4 text="[command_email]" %}

- `command_format`: Which command and parameters to execute when sending an e-mail.
- `email_from`: Which e-mail to use for sending a report.
- `email_to`: Where to send a report via e-mail.

This is my configuration:

```
[commands]
# Check for updates daily
random_sleep = 86400

download_updates = yes
apply_updates = yes
reboot = when-needed

[emitters]
emit_via = command_email

[command_email]
command_format = "mailx -s {subject} -r {email_from} {email_to}"

email_from = dnf@notmalware.info
email_to = me@example.com
```

Finally, you need to enable one of DNF Automatic's systemd timers.

{% include heading.html level=4 text="SystemD" %}

If you have set e. g. `download_updates` to `yes` in your configuration, the timers settings will be overritten by the parameter(s).

You can choose between these three timers:

- `dnf-automatic-notifyonly.timer`: Notify via the selected emitter, that updates are available.
- `dnf-automatic-download.timer`: Also download the updates
- `dnf-automatic-install.timer`: And install them

I chose the installer timer:

```
systemctl enable --now dnf-automatic-install.timer
```

{% include heading.html level=3 text="Done" %}

Next time there are updates due, you will receive an e-mail telling you to not worry about it! 🥳

If you want to have a closer look at DNF Automatic, check out it's [documentation](https://dnf.readthedocs.io/en/latest/automatic.html).
