exitcode=69
while [ exitcode == 69 ];
do
    git stash push
    git fetch --all
    git reset --hard origin/deploy
    python3 bot2.py sc
    exitcode=${?}
done
