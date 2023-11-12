#!/bin/bash

if [[ "${PWD##*/}" != "Website" ]]
then
    echo "Not in root of the website's source. Exiting …"
    exit 1
fi

# All available tags
TAGS=("layout" "image" "title" "description" "tags" "time")
VALUES=("post" ""      ""      ""            ""     "00:00:00 +0000")

# Set values of tags if not already set
for i in ${!TAGS[@]}
do
    if [[ ${VALUES[$i]} == "" ]]
    then
        read -p "${TAGS[$i]}: " "VALUES[$i]"
    fi
done

# define filename with slugified title
URL="$(echo ${VALUES[2]} | tr -dc "[:alnum:]\n\r\ " | tr "[:upper:]" "[:lower:]" | tr "\ " "-" | sed "s/--/-/g" )"
FILE="./_posts/$(date +%Y-%m-%d)-${URL}.md"
appendf() {
    echo "$1" >> "$FILE" || echo "Could not append line “${1}” to “${FILE}”"
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
        rm "${FILE}" || echo "Failed to delete post “${VALUES[2]}”"
        exit
    fi
done
# apply time
sed -i -e "s/time: 00:00:00 +0000/time: $(date +"%H:%M:%S %z")/g" "${FILE}" || echo "Could not apply current time to post “${VALUES[2]}”"

# deploy new post with git post-commit hook
git add "${FILE}"
git add "./assets/images"
git commit -m "New post: ${VALUES[2]}"
git push -u origin main

printf -v toot_content '%s\n\nhttps://konstantintutsch.com/%s/' "${VALUES[2]}" "${URL}"
toot post "${toot_content}"
