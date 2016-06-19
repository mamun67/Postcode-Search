#!/usr/bin/env bash
ls -1 *.json | sed 's/.json$//' | while read jsonfile; do
    echo ${jsonfile}
    mongoimport --db postcodes -c ${jsonfile} --file "${jsonfile}.json" --jsonArray
done