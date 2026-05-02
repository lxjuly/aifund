# AI Fund Web

Public website for AI Fund, built as a static Astro app for Cloudflare Pages.

## Local Development

```bash
cd /Users/youmiss/workplace/aifund/apps/web
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Cloudflare Pages

Use these settings when importing the GitHub repository into Cloudflare Pages:

- Root directory: `apps/web`
- Framework preset: `Astro`
- Build command: `npm run build`
- Build output directory: `dist`
- Production branch: `main`

This app also includes `wrangler.toml` with `pages_build_output_dir = "dist"`.

Cloudflare's Astro Pages guide documents the same build command and output directory.

## Cloudflare Workers Static Assets

If the Cloudflare project is configured to run a deploy command such as `npx wrangler deploy`, use this instead:

- Root directory: `apps/web`
- Deploy command: `npm run deploy`

The `deploy` script builds Astro first, then runs `wrangler deploy` against the static asset directory configured in `wrangler.toml`.

## Positioning

The site should present AI Fund as an AI trading research and paper-trading system. Avoid investment-offering language, public performance claims, personalized trade recommendations, or anything that implies visitors can invest in a managed fund.
