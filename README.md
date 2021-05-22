# 令和ドロー

令和〜素晴らしい旅の始まり〜♪


## Requirements

* nginx-proxy
* Visual Studio Code


## Depoly

Init.

```
git clone https://github.com/walkingmask/reiwadrawing.walkingmask.tk.git
cd reiwadrawing.walkingmask.tk
docker-compose up -d
```

Update.

```
cd reiwadrawing.walkingmask.tk
git pull
docker-compose build
docker-compose restart
```


## Develop

Use VS Code devcontainer.
