exitcode=69
while [ exitcode -eq 69 ]:
do
    git stash push
    git fetch --all
    git reset --hard origin/deploy
    python3 bot2.py sc
    exitcode=${?}
done
