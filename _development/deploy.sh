#!/bin/bash

# .git/hooks/pre-push (770):
#
# #!/bin/bash
#
# ./_development/deploy.sh
#

DOMAIN="konstantintutsch.com"

JEKYLL_ENV=production jekyll build

cd "./_site"

rsync -rvz --progress --delete ./ "root@${DOMAIN}:/var/www/${DOMAIN}"

if [[ "${PWD##*/}" == "_site" ]]
then 
    cd ..
fi
