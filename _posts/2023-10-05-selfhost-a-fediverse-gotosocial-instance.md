---
title: "Self-hosting on a Raspberry Pi: GoToSocial 🦥"
description: How to self-host GoToSocial, a light-weight fediverse server. GoToSocial is compatible with most Mastodon clients.
tags: Self-hosting Linux
---
{% include heading.html level=3 text="Prerequisites" %}

- a domain or subdomain (e. g. social.example.com)
- a Linux system (this post uses a Raspberry Pi running Debian Bookworm as an example)

Before you continue, ensure that your host is accessible from the outside of it's local network and that your domain is set to the host system. Open ports 443 and 80 too.

We will use Nginx for a local reverse proxy to not dedicate ports 80 and 443 to GoToSocial alone in order to [allow other services to run besides GoToSocial]({% link _posts/2023-09-14-one-webserver-multiple-domains.md %}). The reverse proxy also strengthens security.

{% include heading.html level=4 text="Installing dependencies" %}

For Debian systems, you can install these packages:

```
apt install \
            nginx certbot python3-certbot-nginx \
            sudo postgresql \
            wget
```

{% include heading.html level=3 text="Database setup" %}

You need to setup a database and database user first. GoToSocial will store most of it's user data here. The only exception are image files for posts (they are stored in a media directory).

To gurantee that PostgreSQL is always running, enable it's service:

```
systemctl enable --now postgresql
```

The `--now` flag also starts the service.

You can now enter the PostgreSQL shell:

```
sudo -u postgres psql
```

{% include heading.html level=4 text="SQL" %}

Create a new user for GoToSocial first:

```
CREATE USER gotosocial WITH PASSWORD 'password';
```

Now, you can also create a new database for GtS:

```
CREATE DATABASE gotosocial WITH OWNER gotosocial ENCODING 'utf-8';
```

Last, grant all rights on that database to the GoToSocial user:

```
GRANT ALL ON DATABASE gotosocial TO gotosocial;
```

{% include heading.html level=3 text="Bare metal" %}

{% include heading.html level=4 text="User" %}

To increase security, use a seperate user and group for GoToSocial.

Create a Linux user for GoToSocial:

```
useradd -r -b /mnt/storage -m -s /bin/bash gotosocial
```

`-r`: system user

`-b` and `-m`: create and use `/mnt/storage/gotosocial` as home

`-s`: use shell `/bin/bash`

… also the group:

```
groupadd gotosocial
usermod -a -G gotosocial gotosocial
```

Once finished, log into the user and enter it's home directory:

```
su - gotosocial
```

{% include heading.html level=4 text="Resources" %}

Then, download the [latest version](https://github.com/superseriousbusiness/gotosocial/releases):

> Don't forget to also select the correct architecture!

```
wget https://github.com/superseriousbusiness/gotosocial/releases/download/v0.11.1/gotosocial_0.11.1_linux_arm64.tar.gz
```

… and unpack it:

```
tar xf gotosocial_0.11.1_linux_arm64.tar.gz
```

{% include heading.html level=4 text="Configuration" %}

You can use the default configuration as a starting point:

```
cp ./example/config.yaml ./config.yaml
```

These are important values to change, but **not** the full configuration file:

```
host: "social.example.com"
account-domain: "social.example.com"

protocol: "http"
bind-address: "0.0.0.0"
port: 60000

db-type: "postgres"
db-address: "localhost"
db-port: "5432"
db-user: "gotosocial"
db-password: "password"
db-database: "gotosocial"

storage-backend: "local"
storage-local-base-path: "./storage"

letsencrypt-enabled: false
```

Don't worry about HTTP, the disabled Let's Encrypt and the weird port 60000. We will use Nginx as a reverse proxy, these settings are only for the host itself.

{% include heading.html level=4 text="Systemd" %}

Before deploying the service file, we need to change it a little bit. It, again, is **not** the whole unit file:

```
[Service]
WorkingDirectory=/mnt/storage/gotosocial
```

GoToSocial itself is ready now:

```
exit

cp /mnt/storage/gotosocial/gotosocial.service /etc/systemd/system/gotosocial.service

systemctl daemon-reload
systemctl enable --now gotosocial
```

{% include heading.html level=3 text="Reverse proxy" %}

Wait, didn't I just start GoToSocial?

Yes, but the reverse proxy is still missing and GoToSocial can't be accessed on default http(s) ports.

You can configure Nginx like this:

**/etc/nginx/sites-available/gotosocial**

```
server {
  listen 443 ssl;
  listen [::]:443 ssl;
  server_name social.example.com;

  ssl_certificate /etc/letsencrypt/live/social.example.com/fullchain.pem; # managed by Certbot
  ssl_certificate_key /etc/letsencrypt/live/social.example.com/privkey.pem; # managed by Certbot
  include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

  location / {
    proxy_pass http://127.0.0.1:60000;
    proxy_set_header Host $host;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  client_max_body_size 40M;
}

server {
    listen 80;
    listen [::]:80;
    server_name social.example.com;

    if ($host = social.example.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    return 404; # managed by Certbot
}
```

Just request the SSL certificate:

```
certbot --nginx -d social.example.com
```

… and start Nginx.

```
ln -s /etc/nginx/sites-available/gotosocial /etc/nginx/sites-enabled/gotosocial

systemctl enable --now nginx
```

You are finally live!

{% include heading.html level=3 text="User" %}

You want to start posting right now because your instance is live?

I'm sorry to tell you that I may have lied a bit when I said that. Your account is still missing.

Let's go back to GtS:

```
su - gotosocial
```

… and create a user:

```
gotosocial --config-path /path/to/config.yaml \
           admin account create \
           --username username \
           --email hey@example.com \
           --password "secretpassword"
```

I'm just guessing, but could you also be the admin of this instance? */s*

```
gotosocial --config-path /path/to/config.yaml \
           admin account promote \
           --username username
```

{% include heading.html level=3 text="GoToSocial" %}

You need a third-party client for posting from GtS. There is **no** web interface for that.

But you can still configure a few things though the web like custom emojis. Just head to `social.example.com/settings` and log in there.

GoToSocial is also in alpha. There are a lot of things not implemented yet. But I have been running my own instance and not had any problems with it!

If you want to try federation, why not ping me?

{% include social.html id="fediverse" %}

{% include heading.html level=3 text="Backup" %}

You might consider backup-ing your instance too. Here's how I do it:

```
echo "Creating GoToSocial PostgreSQL dump …"
ssh "root"@"$HOST" "sudo -iu postgres pg_dump gotosocial" > "${BKPDIR}/gotosocial-pgsqldump.txt"
if [ ! -d "${BKPDIR}/gotosocial-media" ]
then
  mkdir "${BKPDIR}/gotosocial-media"
fi
for media in $(ssh "root"@"$HOST" "cd /mnt/storage/gotosocial && sudo -u gotosocial ./gotosocial --config-path config.yaml admin media list-local | grep storage")
do
  path="${BKPDIR}/gotosocial-media/$(dirname "${media}")"
  if [ ! -d "$path" ]
  then
    mkdir -p "$path"
  fi
  scp "root"@"$HOST":"/mnt/storage/gotosocial/${media}" "${BKPDIR}/gotosocial-media/${media}"
done
scp "root"@"$HOST":"/mnt/storage/gotosocial/config.yaml" "${BKPDIR}/gotosocial-config.yaml"
scp "root"@"$HOST":"/mnt/storage/gotosocial/gotosocial.service" "${BKPDIR}/gotosocial.service"
scp "root"@"$HOST":"/etc/nginx/sites-available/gotosocial" "${BKPDIR}/gotosocial"
```

This is a really hacky method that works for me. But **don't trust it!**

Before using the script, you also need to set `HOST`: your server, `BKPDIR`: directory to put the backup in.

{% include heading.html level=3 text="Sources" %}

I took information and learned the stuff for this post from here:

- [GoToSocial Docs/Bare Metal](https://web.archive.org/web/20230815205415/https://docs.gotosocial.org/en/latest/getting_started/installation/metal/)
- [GoToSocial Docs/Reverse Proxy](https://web.archive.org/web/20230818081157/https://docs.gotosocial.org/en/latest/getting_started/reverse_proxy/nginx/)
- [GoToSocial Docs/User creation](https://web.archive.org/web/20230627023202/https://docs.gotosocial.org/en/latest/getting_started/user_creation/)
- [GoToSocial Docs/Backup](https://web.archive.org/web/20230627023220/https://docs.gotosocial.org/en/latest/admin/backup_and_restore/)
