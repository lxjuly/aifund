# Cloudflare Pages Website

## Recommendation

Use Cloudflare Pages as the default public website host for AI Fund.

## Initial Website Positioning

The first public version should present AI Fund as an AI trading research and paper-trading system, not as an investable fund offering.

Avoid public claims such as:

- invest with us
- guaranteed returns
- market-beating AI
- live strategy performance without audited methodology
- personalized trade recommendations

## First Site Scope

- Home page
- Methodology page
- System architecture page
- Research journal or selected reports
- Paper-trading status page
- Disclosures page

## Hosting Shape

```text
GitHub repo
  -> web app under apps/web
  -> Cloudflare Pages
  -> custom domain and HTTPS
```

The site should not directly control broker execution. Operator controls should remain private and separate from the public website.

## Compliance Notes

Any public investment-related website can create marketing and regulatory risk. Keep claims fair, balanced, and substantiated. Treat performance, testimonials, endorsements, and hypothetical returns as compliance-sensitive content.

## Sources

- Cloudflare Pages pricing: https://developers.cloudflare.com/pages/functions/pricing/
- Cloudflare Pages limits: https://developers.cloudflare.com/pages/platform/limits/
- SEC Investment Adviser Marketing: https://www.sec.gov/investment/investment-adviser-marketing
