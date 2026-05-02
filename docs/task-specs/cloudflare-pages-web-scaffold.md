# Cloudflare Pages Web Scaffold

## Goal

Create the first public AI Fund website under `apps/web`, optimized for Cloudflare Pages and careful public positioning.

## Implementation

- Framework: Astro
- App path: `apps/web`
- Deployment target: Cloudflare Pages
- Site type: static public research site

## Pages

- `/`: public overview and current system status
- `/methodology`: TradingAgents, replay harnesses, and risk-policy flow
- `/research`: selected paper-trading run notes and system milestones
- `/disclosures`: non-advice and paper-trading disclosures

## Cloudflare Pages Settings

- Root directory: `apps/web`
- Framework preset: `Astro`
- Build command: `npm run build`
- Build output directory: `dist`
- Production branch: `main`

## Guardrails

- Position AI Fund as a research and paper-trading system.
- Use original AI Fund styling and generated/local code assets rather than upstream TradingAgents visual assets.
- Do not present the site as a fund offering.
- Do not publish live trading recommendations.
- Do not publish performance claims without a separate review process.
- Keep broker execution controls out of the public site.

## Sources

- Cloudflare Pages Astro guide: https://developers.cloudflare.com/pages/framework-guides/deploy-an-astro-site/
- Cloudflare Pages build configuration: https://developers.cloudflare.com/pages/configuration/build-configuration/
- Astro on Cloudflare Workers note: https://developers.cloudflare.com/workers/frameworks/framework-guides/astro/
