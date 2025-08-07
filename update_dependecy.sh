#!/bin/bash
#Update denpendecy in requirements.txt

for i in $@; do
    echo "Updating $i..."
    echo "$i" >> requirements.txt
    done