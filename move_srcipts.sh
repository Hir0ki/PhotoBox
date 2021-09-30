#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

cp  ./rsync/rsync.service /lib/systemd/system/

cp  ./rsync/rsync.sh /usr/bin/

cp ./GUI-App/photobox.service /lib/systemd/system/