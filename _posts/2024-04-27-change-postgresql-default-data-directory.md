---
title: Changing PostgreSQL's default data directory
description: How to change the data directory of PostgreSQL on a Linux system with SystemD init system and SELinux.
tags: Linux Self-hosting
time: 2024-04-27 12:00:39 +0200
index: true
---

This post is supposed to be a small guide to changing PostgreSQL's data directory whether your system already contains a PostgreSQL cluster or not, runs SystemD or SELinux is enforced.

{% include heading.html level=3 text="Defining the new path" %}

The PostgreSQL server loads it's data path from an enviroment variable when starting.

If your distribution uses SystemD as it's init system, you can safely modify the enviroment of PostgreSQL with this command.

```
systemctl disable postgresql.service
systemctl edit --full postgresql.service
```

Edit the line containing `Environment=PGDATA=` to something like this.

```
Environment=PGDATA=/mnt/storage/postgresql/data
```

If you mess up PostgreSQL's service file, delete `/etc/systemd/system/postgresql.service` and run `systemctl daemon-reload`. This will revert back to the default service file provided by your package manager. Then repeat the steps above.

{% include heading.html level=3 text="Permissions" %}

The PostgreSQL user needs access to the directory containing the cluster data.

```
chown -R postgres:postgres /mnt/storage/postgresql
```

{% include heading.html level=4 text="SELinux" %}

If you run Fedora Server or another distribution implementing SELinux, the PostgreSQL SystemD service needs access to your new data directory.

You can just “copy” all SELinux configurations from the default PostgreSQL directory to your new path.

```
semanage fcontext -a -e /var/lib/pgsql /mnt/storage/postgresql
restorecon -RF /mnt/storage/postgresql
```

{% include heading.html level=3 text="PostgreSQL" %}

If you already have a PostgreSQL cluster, copy it's data to your new directory.

```
rsync -av /var/lib/pgsql/data /mnt/storage/postgresql
```

{% include heading.html level=4 text="New database cluster" %}

If you don't have an existing PostgreSQL database cluster, you also need to modify `/etc/postgresql-setup/upgrade/postgresql.conf`.

Then continue with initializing a PostgreSQL cluster.

{% include heading.html level=3 text="Done!" %}

That's it! You can now enable and start your PostgreSQL server.

```
systemctl enable --now postgresql.service
```
