#!/bin/bash

if [[ "${PWD##*/}" != "website" ]]
then
    echo "Not in root of the website's source. Exiting …"
    exit 1
fi

PREPEND_URL="https://konstantintutsch.com/blog/"

# All available tags
TAGS=("layout" "title" "description" "tags" "date"                      "index")
VALUES=("post" ""      ""            ""     "1970-01-01T00:00:00+00:00" "")

# Set values of tags if not already set
for i in ${!TAGS[@]}
do
    if [[ ${VALUES[$i]} == "" ]]
    then
        read -p "${TAGS[$i]}: " "VALUES[$i]"
    fi
done

# set url
read -p "Choose the URL to your new post (without a following /): ${PREPEND_URL}" "URL"
FILE="./src/blog/${URL}.md"

# create file with tags and values
appendf() {
    echo "$1" >> "$FILE" || echo "Could not append line “${1}” to “${FILE}”"
}
touch "$FILE"
appendf "---"
for i in ${!TAGS[@]}
do
    if [[ ${TAGS[$i]} == "tags" ]]
    then
        for TAG in ${VALUES[$i]}
        do
            printf -v YAML_TAGS ', "%s"%s' "${TAG}" "${YAML_TAGS}" 
        done
        printf -v YAML_TAGS '"post"%s' "${YAML_TAGS}"
        appendf "${TAGS[$i]}: [${YAML_TAGS}]"
    else
        appendf "${TAGS[$i]}: ${VALUES[$i]}"
    fi
done
appendf "---"

# enter editing and wait for deploying, testing or deleting
flatpak run org.gnome.gitlab.somas.Apostrophe ${FILE} &
DEPLOY=""
while [[ ${DEPLOY} != "deploy" ]]
do
    read -p "Dou you want to [deploy/test/delete] your site?: " "DEPLOY"
    if [[ ${DEPLOY} == "test" ]]
    then
        npm start
    elif [[ ${DEPLOY} == "delete" ]]
    then
        rm "${FILE}" || echo "Failed to delete post “${VALUES[1]}”"
        exit
    fi
done
# apply time
sed -i -e "s/date: 1970-01-01T00:00:00+00:00/date: $(date +"%Y-%m-%dT%H:%M:%S%:z")/g" "${FILE}" || echo "Could not apply current time to post “${VALUES[1]}”"

# deploy new post with git post-commit hook
git add "${FILE}"
git add "./src/assets/images"
git commit -m "New post: ${VALUES[1]}"
git push -u origin main

for TAG in ${VALUES[3]}
do
    HASHTAG="${TAG//-/}"
    if [[ ${HASHTAG} != "Blog" ]]
    then
        printf -v HASHTAGS '%s#%s ' "${HASHTAGS}" "${HASHTAG}"
    fi
done
printf -v toot_content '%s #blog\n\n%s%s/\n\n%s' "${VALUES[1]}" "${PREPEND_URL}" "${URL}" "${HASHTAGS}"
toot post "${toot_content}"
