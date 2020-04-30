#! /bin/bash

cd ~/covid
git add .
git status

git commit -m "$(date +%d-%b-%H_%M)"
git push origin master


