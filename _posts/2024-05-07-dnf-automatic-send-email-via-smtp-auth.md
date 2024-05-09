---
title: DNF Automatic – Send Emails via a SMTP Authenticated Server
description: How to send DNF Automatic email reports via an email server that requires SMTP authentication.
tags: Linux Self-hosting
time: 2024-05-07 17:37:59 +0200
index: true
---

This short post explains how to use `curl` as an email client with SMTP Authentication support for DNF Automatic.

This can be useful when an email server does not accept emails from a self-hosted mail server.

### Curl

Create this script somewhere:

```
#!/bin/bash

FROM="${1}"
TO="${2}"
SUBJECT="${3}"
BODY="$(cat /dev/stdin)"

curl \
    --ssl-reqd \
    --url "smtps://smtp.example.com:465" \
    --user "username:password" \
    --mail-from "${FROM}" \
    --mail-rcpt "${TO}" \
    --header "Subject: ${SUBJECT}" \
    --header "From: ${HOSTNAME} <${FROM}>" \
    --header "To: Administrator <${TO}>" \
    --form '=(;type=multipart/mixed' --form "=$BODY;type=text/plain" --form '=)'
```

### DNF Automatic

Edit your DNF Automatic configuration to use `command_email` as it's emitter.

Define these options in `[command_email]`:

```
command_format = "/root/dnfmail.sh {email_from} {email_to} {subject}"
stdin_format = "{body}"
email_from = server@example.com
email_to = you@example.com
```

