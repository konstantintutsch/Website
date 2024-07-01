---
layout: post
title: Change MariaDB's Default Data Directory
description: How to change the default data directory of MariaDB (MySQL DB Server) to a new path. With SELinux permissions.
tags: ["post", "self-hosting", "linux"]
date: 2024-07-01T19:36:02+02:00
index: true
---

This post is intended as a quick guide to changing the MariaDB data directory. I have also added information for systems that already contain MariaDB data or on which SELinux is enforced.

*MariaDB is an open source MySQL database server. I've also written a [post for PostgreSQL](/blog/change-postgresql-default-data-directory).*

### A New Path

All of MariaDB's configuration is loaded from `/etc/my.cnf`.

To change MariaDB's data storage location, modify the file to include the lines shown below. I chose to store all data in `/mnt/storage/mysql` for this example.

```
[client-server]
socket=/mnt/storage/mysql/mysql.sock

[mysqld]
datadir=/mnt/storage/mysql
socket=/mnt/storage/mysql/mysql.sock
```

### Permissions

The MySQL user needs access to the directory containing MariaDB data.

```
chown mysql:mysql -R /mnt/storage/mysql
```

#### SELinux

If you run Fedora Server or another distribution employing SELinux, the MariaDB daemon in particular must also be granted access to the new data directory.

You can mirror all SELinux permissions from the default MariaDB data location to your new directory.

```
semanage fcontext -a -e /var/lib/mysql /mnt/storage/mysql
restorecon -RF /mnt/storage/mysql
```

### MariaDB

If you already have MariaDB data, copy it to the new location.

```
rsync -av /var/lib/mysql /mnt/storage/mysql
```

### Last Steps

You're almost finished! Restart the database server to apply all changes.

```
systemctl restart mariadb.service
```

… or enable it if you've just set the system up!

```
systemctl enable --now mariadb.service
```