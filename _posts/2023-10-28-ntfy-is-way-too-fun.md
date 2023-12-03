---
layout: post
title: Ntfy is way too fun
description: I have begun to self-host Ntfy on my Raspberry Pi. This post is about all the possibilities of such a notification service and all I have now automated.
tags: Self-hosting
time: 18:38:00 +0200
---

{% include heading.html level=3 text="What Ntfy is" %}

[Ntfy](https://ntfy.sh/) is a self-hosted push notification service. It allows to send notifications via HTTP with REST API specifications. This makes it extremly compatible. For example, you can easily send a notification from the commandline with `curl`:

{% highlight shell %}
curl -d "Hi from the commandline 👋" "https://ntfy.example.com/test"
{% endhighlight %}

{% include image.html file="ntfy-hi-cmd.webp" alt="A notification with the content: 'Hi from the commandline 👋'" caption="This is how it looks in the Web UI" %}

or with a title, tag (the wave emoji) and a priority:

```
curl \
    -H "Title: Greeting" \
    -H "Priority: urgent" \
    -H "Tags: wave" \
    -d "Hi from the commandline. Answer immediately!" \
    "https://ntfy.example.com/test"
```

{% include image.html file="ntfy-hi-with-title-cmd.webp" alt="A notification with the title: '👋 Greeting', content: 'Hi from the commandline. Answer immediately!' and three red arrows point up" caption="And again, a screenshot from the Web UI" %}

Ntfy also has mobile apps, a CLI and more. Additionally, notifications can have file attachments. Moreover, Ntfy can send you emails or even call you and send text messages.

{% include heading.html level=4 text="Configuring" %}

If you want to self-host Ntfy, [their documentation](https://docs.ntfy.sh/install/) is great. I am running it on my Raspberry Pi with a simple Nginx reverse proxy. It is almost unnoticable in terms of resource usage.

{% include heading.html level=3 text="All I have automated" %}

Then, after I had discovered and done all that, the service *had* to be implemented. 😁

{% include heading.html level=4 text="Outages" %}

A use case that comes to mind immediately is probably the reporting of downtime. This is also exactly what I did:

```
#!/bin/bash

ntfy-msg() {
    curl \
        -H "Title: ${1}" \
        -H "Priority: ${2}" \
        -H "Tags: ${3}" \
        -d "${4}" \
        "https://ntfy.example.com/status"
}

# Web services

WebService=("https://dav.example.com" "https://example.com" "https://social.example.com" "http://192.168.178.49:58080")
WebName=("Radicale" "Website" "GoToSocial" "Pi-hole Web interface")

for i in $(seq 0 $((${#WebService[@]}-1)))
do
    http_status="$(curl -f -LI ${WebService[i]} -o /dev/null -s -w %{http_code})"

    if [[ $http_status != "200" ]] && [[ $http_status != "405" ]]
    then
        ntfy-msg \
            "Service error" \
            "default" \
            "warning" \
            "There was an error for ${WebName[i]} (${WebService[i]}) with an HTTP Status Code ${http_status}."
    fi
done
```

Finally, I added this line to my crontab to let the script run every 5 minutes:

```
*/5   *   *   *   *     bash /root/check_status
```

{% include heading.html level=4 text="Updating" %}

Now that I knew when a service hosted on my Raspberry Pi was not running, I had to keep these services up-to-date too.

I had always updated manually every Friday, but why bother with that?

So I added another cronjob:

```
  0   0   *   *   Fri   ntfy pub --title "Update executed" --priority low --tags arrow_double_up --wait-cmd hosting bash -c "apt update && apt upgrade -y"; sleep 5; ntfy pub --title "Reboot" --priority low --tags repeat_one hosting "System is rebooting after an update …"; sleep 5; reboot
```

`--wait-cmd`: ntfy waits until the `bash -c "…"` is done running and the reports if it failed or succeeded

The first ntfy CLI command waits for `apt` to update all repositories and then upgrade all packages. Once finished, a notification is send and waited five seconds.

Then, ntfy CLI sends another notification announcing a reboot. Another five seconds is waited until the system actually reboots.

{% include heading.html level=4 text="Post-commit deploy hook" %}

Another cool little thing I added, a post-commit hook to re-deploy this website once I've commit something, e. g. a new post.

```
#!/bin/bash -i

shopt -s expand_aliases

ntfy-msg() {
    curl \
        -H "Title: $1" \
        -H "Priority: $2" \
        -H "Tags: $3" \
        -d "$4" \
        "https://ntfy.example.com/status"
    exit
}

web-deploy || ntfy-msg "Deploying failed" "default" "x" "An error occurred while deploying the new version of konstantintutsch.de."

ntfy-msg "Deploying successful" "low" "white_check_mark" "The new version of konstantintutsch.de was deployed successfully 🔥"
```

`web-deploy` is an alias in my `.bashrc` to build the site with Jekyll and the copy it to the webdir.

This only saves me a single command, but is really cool.

Imagine this, you just finished writing a new blog posts. You then look at your phone and there is this cool message with a flame at the end of it! (*I may be a bit **too** excited abou this*)

{% include heading.html level=3 text="Final thoughts" %}

In my opinion, Ntfy is really fun but also a serious tool. Discovering all the possibilities I can take advantage of was really exciting.

Writing this post has been a blast too! 😄
