until python3 bot2.py sc;do   
    git stash push
    git fetch --all
    git reset --hard origin/deploy
done
