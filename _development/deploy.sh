#!/bin/bash

# .git/hooks/pre-push (770):
#
# #!/bin/bash
#
# ./_development/deploy.sh
#

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ $BRANCH != "main" ]]
then
    echo "Not in branch “main”. Deployment skipped."
    exit 0
fi

DOMAIN="konstantintutsch.com"
SERVER="rpi-homeserver"

JEKYLL_ENV=production jekyll build

cd "./_site"

rsync -rvz --progress --delete ./ "root@${SERVER}:/mnt/storage/${DOMAIN}"

# Uncomment this line for Apache2 or Nginx. httpd has root access and does not require this
# ssh "root@${SERVER}" "chown -R www-data:www-data /mnt/storage/${DOMAIN}"

if [[ "${PWD##*/}" == "_site" ]]
then 
    cd ..
fi
