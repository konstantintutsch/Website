#!/bin/bash

FILE="${1}"

ffmpeg -i "${FILE}" -quality 100 -compression_level 3 -vf scale=-1:1000 "${FILE}-thumbnail.jpg"
