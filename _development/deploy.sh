#!/bin/bash

# .git/hooks/pre-push (770):
#
# #!/bin/bash
#
# export SFTPUN_STRATO="username"
# export SFTPPW_STRATO="password"
#
# ./_development/deploy.sh
#

DOMAIN="konstantintutsch.com"

USERNAME="${SFTPUN_STRATO}"
PASSWORD="${SFTPPW_STRATO}" 

JEKYLL_ENV=production jekyll build

cd "./_site"

# Tidy up Liquid's access blank spaces and wrong indentation
TIDY="/usr/bin/tidy"
TIDY_ARGS="\-modify \-indent \-utf8 \-quiet"
if [[ -f "${TIDY}" ]]
then
    eval "find . -name \"*.html\" -exec ${TIDY} ${TIDY_ARGS} {} \;"
    eval "find . -name \"*.xml\" -exec ${TIDY} \-xml ${TIDY_ARGS} {} \;"
fi

if [ ! -d "${HOME}/.mnt/website" ]
then
    mkdir -p "${HOME}/.mnt/website"
fi
sshfs -o reconnect,password_stdin "${USERNAME}@ssh.strato.de:/${DOMAIN}" "${HOME}/.mnt/website" <<< "$PASSWORD"
rsync -rvz --progress --delete ./ "${HOME}/.mnt/website"
umount "${HOME}/.mnt/website"

if [[ "${PWD##*/}" == "_site" ]]
then 
    cd ..
fi
