# 令和ドロー

New era version of https://github.com/walkingmask/heiseidraw .


## Requirements

* Git
* Node.js
* pnpm
* GitHub Repository
* Cloudflare Account


## Development

```bash
pnpm add -D wrangler
pnpm approve-builds
pnpm install
pnpm wrangler --version
pnpm wrangler login
pnpm wrangler pages dev .  # http://localhost:8788
```


## Depoly

```bash
pnpm wrangler deploy
```
