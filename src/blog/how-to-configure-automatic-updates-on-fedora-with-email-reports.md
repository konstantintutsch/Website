---
layout: post
title: How to configure automatic updates on Fedora with e-mail reports
description: How to use DNF Automatic and Postfix for automatically updating your Fedora server and sending reports via e-mail about the update.
tags: ["post", "self-hosting"]
date: 2023-12-05T20:03:09+01:00
---

### Requirements

You first need to install `dnf-automatic`, `postfix` and `mailx`:

```
dnf install -y dnf-automatic postfix mailx
```

After all programms have been installed, you can start configuring the e-mail server.

### E-Mail Server

---

Notice as of May 7th, 2024: Alternatively, [send DNF Automatic's email reports via an already existing server.](/blog/dnf-automatic-send-email-via-smtp-auth)

---

Postfix's configuration is located at `/etc/postfix/main.cf`. These are the values that should be set:

- `myhostname`: This value is used for various settings regarding, amongs other things, your e-mail domain.
- `mydomain`: *see myhostname*
- `mynetworks_style` *(or `mynetworks`)*: This defines which *places* in your network are authorized to send e-mails.

I have configured Postfix like this:

```
myhostname = server.example.com
mydomain = server.example.com

mynetworks_style = host
```

To test your Postfix configuration, you can execute this command:

```
echo "Hi, I'm your e-mail's body!" | mailx -r "test@server.example.com" -s "A test e-mail from Postfix!" "you@example.com"
```

Now that your e-mail server is working fine, you can configure DNF Automatic! 🤩

### DNF Automatic

Automatic is a component of DNF. It's configuration file is located at `/etc/dnf/automatic.conf`.

Here are all the necessary configuration parameters:

#### [commands]

- `random_sleep`: The interval *(in seconds)* between searching for new updates. — e. g. `3600`
- `download_updates`: If packages that can be updated should be downloaded automatically. — `yes` / `no`
- `apply_updates`: If updates for packages should be installed automatically. — `yes` / `no`
- `reboot`: Whether to reboot after updates. — `never` / `when-changed` / `when-needed`

#### [emitters]

- `emit_via`: How to inform the system administrator on activities. — `email` / `command_email` / `command`

#### [command_email]

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

email_from = dnf@server.example.com
email_to = you@example.com
```

Finally, you need to enable one of DNF Automatic's systemd timers.

#### SystemD

If you have set e. g. `download_updates` to `yes` in your configuration, the timers settings will be overritten by the parameter(s).

You can choose between these three timers:

- `dnf-automatic-notifyonly.timer`: Notify via the selected emitter, that updates are available.
- `dnf-automatic-download.timer`: Also download the updates
- `dnf-automatic-install.timer`: And install them

I chose the installer timer:

```
systemctl enable --now dnf-automatic-install.timer
```

### Done

Next time there are updates due, you will receive an e-mail telling you to not worry about it! 🥳

If you want to have a closer look at DNF Automatic, check out it's [documentation](https://dnf.readthedocs.io/en/latest/automatic.html).
