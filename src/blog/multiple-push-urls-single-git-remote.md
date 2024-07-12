---
layout: post
title: Multiple Push URLs for a Single Git Remote
description: A note to my furutre self on how to add multiple push URLs to a single git remote.
tags: ["post", "open-source", "git"]
date: 2024-07-12T10:23:00+02:00
index: true
---

This post is just a note to my future self on how to add multiple push URLs to a single git remote.

### Adding The URLs

First, add a new remote to your git repository.

```
git remote add all git@server1:repo.git
```

Then, redefine the push URL of the remote.

```
git remote set-url --add --push all git@server1:repo.git
```

Finally, add the URL of your second remote.

```
git remote set-url --add --push all git@server2:repo.git
```

### Confirming The Changes

At the end, confirm that all URLs were set correctly.

```
git remote -v
```

The output should now be similar to this:

```
all	git@server1:repo.git (fetch)
all	git@server1:repo.git (push)
all	git@server2:repo.git (push)
```