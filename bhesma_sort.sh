#!/bin/bash
while read line
do
    if [[ $line == *"URLs for"* ]]; then
        # Extract URL from line and remove path
        url=$(echo $line | awk '{print $NF}' | cut -d'/' -f1-3)
    fi    

    if [[ $line == *"/"* ]]; then
        # Extract endpoint from line and append to URL
        endpoint=$(echo $line | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' | awk '{print $1}' | grep -v URLs)
        echo $url$endpoint
    fi
done < temp.txt
