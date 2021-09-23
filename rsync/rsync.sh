#!/bin/bash
set -euo pipefail
IFS=$'\n\t'


while true;
do
    echo "starting rsync";
    rsync --archive --compress --partial /home/photobox/Pictures/photobox/ root@cloud.techbeard.de:/root/docker/fotobox/data;
    sleep 5;

done;
