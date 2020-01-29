exitcode=69
while [ exitcode -eq 69 ]
do
    sudo git stash push
    sudo git fetch --all
    sudo git reset --hard origin/deploy
    python3 bot2.py sc
    exitcode=${?}
done