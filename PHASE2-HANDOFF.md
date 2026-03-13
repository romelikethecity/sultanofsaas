# SultanOfSaaS Phase 2 — Niches, Industries & Filters

## What's Built (Phase 1 Complete)

Working static site generator producing 145 pages from inline data.

### Files
```
scripts/nav_config.py    — Site metadata, nav structure, footer columns
scripts/templates.py     — HTML generators (head, nav, footer, page wrapper, schema helpers)
scripts/build.py         — Tool data (50 tools), page generators, all inline
assets/css/tokens.css    — CSS variables, base styles, utilities (DO NOT EDIT)
assets/css/components.css — Component styles: verdict cards, tool cards, comparison tables, etc. (DO NOT EDIT)
assets/css/styles.css    — Page layouts, responsive design, nav, footer
```

### Current Data
- **50 tools** across 5 categories (10 tools each)
- **5 categories:** CRM, Project Management, Email Marketing, SEO Tools, Help Desk
- **20 comparisons** with declared winners
- **10 alternatives** pages
- **50 pricing** pages (one per tool)
- **6 stack guides** ($0 Founder, Lean Startup, Sales Team, Agency, Content Creator, E-Commerce)
- **Sultan's Picks:** HubSpot (CRM), Asana (PM), ConvertKit (Email), Semrush (SEO), Freshdesk (Help Desk)

### Current Page Types & URLs
```
/                              Homepage
/tools/{slug}/                 Tool review (50 pages)
/best/{category}/              Category guide (5 pages)
/best/                         Category index
/{tool}-vs-{tool}/             Comparison (20 pages)
/{tool}-alternatives/          Alternatives (10 pages)
/{tool}-pricing/               Pricing breakdown (50 pages)
/stacks/{slug}/                Stack guide (6 pages)
/stacks/                       Stacks index
/about/                        About page
```

### Hero Copy (final)
- **Title:** Every review site says "it depends." We pick winners.
- **Subtitle:** Scores, winners, and stack guides for founders who buy their own tools.

### Build & Preview
```bash
cd /Users/rome/Documents/projects/sultanofsaas && python3 scripts/build.py
cd /Users/rome/Documents/projects/sultanofsaas/output && python3 -m http.server 8086
```

---

## Phase 2: What To Build

### 1. Niche Category Pages (`/best/{category}/{niche}/`)

Cross-cutting niches that apply to EVERY category. Each niche page re-ranks the tools and picks a DIFFERENT winner for that audience.

**6 universal niches × 5 categories = 30 pages:**

| Niche Slug | Page Title Pattern | Key Criteria |
|------------|-------------------|--------------|
| `solo-founders` | Best {Category} for Solo Founders | Simplest, cheapest, least setup |
| `small-teams` | Best {Category} for Small Teams (2-10) | Balance of features and simplicity |
| `free` | Best Free {Category} | Free tiers only, ranked by what you actually get |
| `agencies` | Best {Category} for Agencies | Client management, multi-account, white-label |
| `ecommerce` | Best {Category} for E-Commerce | Shopify/WooCommerce integration, purchase data |
| `startups` | Best {Category} for Startups on a Budget | Best value under $50/mo |

**Category-specific niches (~12 more pages):**

| Category | Niche | Why winner changes |
|----------|-------|-------------------|
| CRM | `outbound-sales` | Close wins (built-in dialer) |
| CRM | `google-workspace` | Copper wins (native integration) |
| Email Marketing | `newsletters` | ConvertKit/Beehiiv win |
| Email Marketing | `shopify` | Klaviyo wins (purchase data) |
| SEO Tools | `beginners` | Mangools/Ubersuggest win (simplicity) |
| SEO Tools | `content-teams` | Surfer SEO wins (on-page optimization) |
| PM | `engineering` | Linear wins (built for devs) |
| PM | `remote-teams` | Basecamp or Notion win (async-first) |
| Help Desk | `saas` | Intercom wins (chat-first, in-app) |
| Help Desk | `one-person` | Groove wins (simplest, cheapest) |

**Data structure to add to build.py:**

```python
NICHES = {
    # Universal niches (apply to all categories)
    'solo-founders': {
        'name': 'Solo Founders',
        'title_pattern': 'Best {category} for Solo Founders ({year})',
        'description': 'The best {category_lower} for one-person businesses. Prioritizing simplicity, free tiers, and fast setup.',
        'applies_to': ['crm', 'project-management', 'email-marketing', 'seo-tools', 'help-desk'],
        'rankings': {
            'crm': ['hubspot', 'less-annoying-crm', 'zoho-crm', 'pipedrive', 'freshsales'],
            'project-management': ['notion', 'trello', 'clickup', 'asana', 'linear'],
            'email-marketing': ['mailerlite', 'convertkit', 'brevo', 'beehiiv', 'mailchimp'],
            'seo-tools': ['mangools', 'ubersuggest', 'se-ranking', 'screaming-frog', 'ahrefs'],
            'help-desk': ['groove-helpdesk', 'freshdesk', 'zoho-desk', 'help-scout', 'hubspot-service'],
        },
        'winners': {
            'crm': 'hubspot',
            'project-management': 'notion',
            'email-marketing': 'mailerlite',
            'seo-tools': 'mangools',
            'help-desk': 'groove-helpdesk',
        },
    },
    # ... more niches
}
```

**URL structure:** `/best/{category}/{niche}/`
- `/best/crm/solo-founders/`
- `/best/email-marketing/free/`
- `/best/seo-tools/beginners/`

### 2. Industry Pages (`/for/{industry}/`)

Pages that recommend the best tool from EACH category for a specific industry. Think of it as a curated stack guide by industry.

**17 industries in 3 tiers:**

**Tier 1 (full content, high search volume):**
- `ecommerce` — E-Commerce & Online Stores
- `saas` — SaaS Companies
- `agencies` — Agencies & Consultancies
- `real-estate` — Real Estate
- `professional-services` — Professional Services (Lawyers, Accountants, Consultants)
- `startups` — Startups & Early-Stage Companies

**Tier 2 (solid content, moderate volume):**
- `nonprofits` — Nonprofits & Charities
- `healthcare` — Healthcare & Wellness
- `education` — Education & Coaching
- `creators` — Creators & Media
- `financial-services` — Financial Services
- `construction` — Construction & Trades

**Tier 3 (lighter content, lower volume but worth generating):**
- `restaurants` — Restaurants & Hospitality
- `manufacturing` — Manufacturing & Wholesale
- `fitness` — Fitness & Gyms
- `legal` — Legal
- `accounting` — Accounting & Bookkeeping

**Data structure:**

```python
INDUSTRIES = {
    'ecommerce': {
        'name': 'E-Commerce & Online Stores',
        'slug': 'ecommerce',
        'tier': 1,
        'description': 'SaaS tools optimized for online stores. Shopify and WooCommerce integrations, purchase-based segmentation, and order management.',
        'picks': {
            'crm': {'tool': 'hubspot', 'why': 'Free CRM with strong Shopify integration and contact tracking.'},
            'email-marketing': {'tool': 'klaviyo', 'why': 'Best purchase-based segmentation and Shopify-native workflows.'},
            'seo-tools': {'tool': 'ahrefs', 'why': 'Best for product page optimization and competitor keyword research.'},
            'project-management': {'tool': 'asana', 'why': 'Handles product launches, inventory planning, and marketing campaigns.'},
            'help-desk': {'tool': 'freshdesk', 'why': 'Affordable omnichannel support with e-commerce integrations.'},
        },
    },
    # ... more industries
}
```

**URL structure:** `/for/{industry}/`
- `/for/ecommerce/`
- `/for/agencies/`
- `/for/real-estate/`

**Page layout:** Hero with industry name → "Sultan's Picks for {Industry}" grid showing one recommended tool per category → category-specific buying advice → link to deeper category niche pages.

### 3. Tools Index with Filters (`/tools/`)

A browsable index of all tools with client-side filtering. No JavaScript framework — vanilla JS with data attributes.

**Filters:**
- **Category** — dropdown (CRM, PM, Email Marketing, SEO, Help Desk)
- **Price Tier** — pills (Free, Budget, Mid, Premium, Enterprise)
- **Best For** — pills (Solo Founders, Small Teams, Agencies, E-Commerce)
- **Sort** — Sultan's Score (default), Price low→high, Name A→Z

**Implementation:**

Each tool card gets data attributes:
```html
<div class="tool-card" data-category="crm" data-price="free" data-score="8.9" data-name="HubSpot CRM">
```

Filter JS (~30 lines):
```javascript
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Toggle active state
        // Filter cards by matching data attributes
        // Show/hide based on combined filters
    });
});
```

**CSS needed:** Add filter bar styles to styles.css — pill buttons, active states, filter container.

**URL:** `/tools/` (not `/tools/index.html` — directory-based like all other pages)

### 4. Nav Updates

Update `nav_config.py` to add:
- "Tools" link to nav (the filterable index)
- More categories in dropdown as they're added
- Industry dropdown or "By Industry" link
- Footer columns updated with industry and niche links

---

## Page Count Target

| Page Type | Current | Phase 2 | Total |
|-----------|---------|---------|-------|
| Homepage | 1 | — | 1 |
| Category guides | 6 | — | 6 |
| Niche category pages | 0 | ~42 | 42 |
| Industry pages | 0 | 17 | 17 |
| Tool reviews | 50 | — | 50 |
| Tools index (filterable) | 0 | 1 | 1 |
| Comparisons | 20 | — | 20 |
| Alternatives | 10 | — | 10 |
| Pricing | 50 | — | 50 |
| Stack guides | 7 | — | 7 |
| About | 1 | — | 1 |
| **Total** | **145** | **~60** | **~205** |

---

## Important Rules

- **All data stays inline in build.py.** No external JSON files.
- **NEVER use false reframes:** No "not X, it's Y" / "isn't X. It's Y." / "less about X and more about Y" — ZERO TOLERANCE.
- **Every niche page must pick a different winner** than the main category page (otherwise the page has no reason to exist).
- **Niche winners must be defensible.** Don't just shuffle the ranking — explain WHY the winner changes for that audience.
- **Keep verdict copy opinionated and specific.** "Best for solo founders who need zero setup" beats "Great for small businesses."
- **Scores don't change per niche.** The tool's score is absolute. What changes is the RANKING (which tools are most relevant) and the WINNER.
- **Use verdict score colors from tokens.css** consistently.
- **All pages need canonical URLs, breadcrumbs, meta descriptions.**

---

## File Reading Order (for new context)

1. `PHASE2-HANDOFF.md` (this file)
2. `BRAND.md` — brand reference
3. `scripts/build.py` — current data + page generators (the big file)
4. `scripts/templates.py` — HTML generators and helpers
5. `scripts/nav_config.py` — nav structure
6. `assets/css/styles.css` — current page layouts
7. `assets/css/tokens.css` — CSS variables (read-only reference)
8. `assets/css/components.css` — component styles (read-only reference)
