#! /bin/bash


cd ~/covid
python final_url.py
git add .
git status
git commit -m "$(date +%d-%b-%H_%M)"
git push origin master


