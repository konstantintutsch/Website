---
layout: post
title: "A single webserver serving multiple domains"
---

## My setup and the importance to me

So, I'm pretty sure that an introduction is always helpful.

I've a got Raspberry Pi, 8G memory and 4 cores @ 1.8GHz, running at home. It was used for **only** a single service with a web interface.

I have to use a reverse proxy on some VPS, because the router I'm using isn't reliable with allowing port 80 and 443 from the outside for some reason.

I always wanted to use my Raspberry Pi for more, but only if the services looked "normal" from the outside, that is: no special ports needed to access them, just a simple subdomain.

## My (not so) special discovery

What I realized wasn't that surprising after all. I saw a video about a homeserver and that all the services had their own local domains. But how?

That isn't different from domain names on the internet. So I must be able to reproduce it and my "selfhosting dream" would come true!

I remembered that a webserver also knows which domain the client accessed / typed into the URL bar. A quick search, about how the Nginx webserver handles such, gave me the solution: in an Nginx configuration file for a site, you always specify the `server_name` parameter with the hosts' domain.

But if I point two domains, lets just say example1.com and example1.com to my VPS, creating two `server {}`s with different values in the `server_name` but listening on the same port, each of those domains would get it's own unique website.

This is how it could look like. Each configuration has their respective site.

**example1.com**

```
server {
  listen 443 ssl;
  listen [::]:443 ssl;
  server_name example1.com;
 
  ssl_certificate /etc/letsencrypt/live/example1.com/fullchain.pem; # managed by Certbot
  ssl_certificate_key /etc/letsencrypt/live/example1.com/privkey.pem; # managed by Certbot
  include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

  location / {
    proxy_pass https://router:60000;
  }
}
```
**example2.com**
```
server {
  listen 443 ssl;
  listen [::]:443 ssl;
  server_name example2.com;
 
  ssl_certificate /etc/letsencrypt/live/example2.com/fullchain.pem; # managed by Certbot
  ssl_certificate_key /etc/letsencrypt/live/example2.com/privkey.pem; # managed by Certbot
  include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

  location / {
    proxy_pass https://router:60000;
  }
}
```

## Conclusion

That's it, a really handy trick to save money and use resources more efficiently for me and my self-hosting.

This, of course, only works with web apps. If your app isn't web-based, then you should look into SRV records. But they only work with applications and protocols who intend to use them.

Hope you enjoyed reading this post and that the information from here helps you at some point somewhere 😄
