#! /bin/bash

cd ~/covid
git add .
git status

# time= $(date +%d-%b-%H_%M)    
git commit -m "$time+check"
git push origin master


