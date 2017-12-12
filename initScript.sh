#!/bin/bash

echo "URL $1"

cd Data

rm -rf .git/

git init

git remote add origin $1

git pull
