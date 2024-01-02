#!/bin/bash

FILE="${1}"

ffmpeg -i "${FILE}" -quality 50 -compression_level 6 -vf scale=512:-1 "${FILE}-thumbnail.webp"
