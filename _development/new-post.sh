#!/bin/bash

if [[ "${PWD##*/}" != "Website" ]]
then
    echo "Not in root of the website's source. Exiting …"
    exit 1
fi

# All available tags
TAGS=("layout" "image" "title" "description" "tags" "time")
VALUES=("post" ""      ""      ""            ""     "$(date +"%H:%M:%S %z")")

# Set values of tags if not already set
for i in ${!TAGS[@]}
do
    if [[ ${VALUES[$i]} == "" ]]
    then
        read -p "${TAGS[$i]}: " "VALUES[$i]"
    fi
done

# define filename with slugified title
FILE="./_posts/$(date +%Y-%m-%d)-$(echo ${VALUES[2]} | tr -dc "[:alnum:]\n\r\ " | tr "[:upper:]" "[:lower:]" | tr "\ " "-" | sed "s/--/-/g" ).md"
appendf() {
    echo "$1" >> "$FILE"
}

# create file with tags and values
touch "$FILE"
appendf "---"
for i in ${!TAGS[@]}
do
    appendf "${TAGS[$i]}: ${VALUES[$i]}"
done
appendf "---"

# enter editing and wait for deploying, testing or deleting
DEPLOY=""
while [[ ${DEPLOY} != "deploy" ]]
do
    ${EDITOR} ${FILE}
    read -p "Dou you want to [deploy/test/delete] your site?: " "DEPLOY"
    if [[ ${DEPLOY} == "test" ]]
    then
        jekyll serve
    elif [[ ${DEPLOY} == "delete" ]]
    then
        rm "${FILE}"
        exit
    fi
done

# deploy new post with git post-commit hook
git add "${FILE}"
git commit -m "New post: ${VALUES[2]}"
