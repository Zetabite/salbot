until python3 bot2.py sc;do
    git stash push
    git fetch --all
    git reset --hard origin/deploy
    cd salbot-secrets
    git stash push
    git fetch --all
    git reset --hard origin/deploy
    cd ..
    python3 -m pip install -r requirements.txt
done
