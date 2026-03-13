# SultanOfSaaS.com — Build Handoff

## What This Is

Opinionated SaaS tool reviews for SMBs and founders (1-200 person companies). Anonymous persona: "The Sultan" — a decisive expert who picks winners and calls out overpriced tools. Programmatic SEO site generating 1,000+ pages at launch.

**Domain:** sultanofsaas.com
**Local:** `/Users/rome/Documents/projects/sultanofsaas/`

---

## Positioning

- **Voice:** Opinionated expert. Always picks a winner. Backs opinions with reasoning. Confident, not snarky. Direct and helpful.
- **Audience:** SMB founders, ops leads, and team leads (1-200 employees) who pick their own tools without a procurement process.
- **Identity:** Anonymous "The Sultan" persona. No real name. Publication feel.
- **Signature element:** "The Sultan's Verdict" — appears on every tool review with a score and one-line take.
- **Differentiator from G2/Capterra:** Has opinions. Picks winners. Doesn't say "it depends" without saying what it depends ON.

### Editorial Rules
- NEVER use false reframes: "not X, it's Y" / "isn't X. It's Y." / "less about X and more about Y" — ZERO TOLERANCE
- Always pick a winner on comparison pages
- Keep descriptions short and direct — no filler
- Scores are 1-10, always justified with reasoning
- "Sultan's Pick" = the top recommendation in a category
- Stack guides should include specific dollar amounts

---

## Brand System

All brand files are in place. See `BRAND.md` for the complete reference.

### Colors (dark theme)
- **Primary Gold:** `#D4A054` — logo, accents, Sultan's Pick, links
- **Backgrounds:** `#0C0E12` (page) → `#12151B` (cards) → `#1A1D25` (elevated) → `#1F2330` (hover)
- **Text:** `#F0F0F0` (primary) → `#9CA3AF` (body) → `#6B7280` (metadata)
- **Verdict scores:** Green (9+) → Blue (7-8.9) → Yellow (5-6.9) → Red (3-4.9) → Dark Red (<3)
- **Price tiers:** Green (Free) → Blue (Budget) → Yellow (Mid) → Pink (Premium) → Purple (Enterprise)

### Typography
- **Outfit** — Headlines, UI, nav, buttons, badges (weight 300-900)
- **Source Serif 4** — Review body copy, descriptions (400, 600, 700 + italic)
- **JetBrains Mono** — Scores, prices, specs, data tables (400, 500, 600)

### Logo: Flow Diamonds
Three rotated squares in an S-curve with cascading opacity (100% / 55% / 25%). Wordmark: "Sultan" (white) + "Of" (gold) + "SaaS" (white) in Outfit 800.

### CSS Files
- `assets/css/tokens.css` — All CSS variables, base styles, utilities (ready to use)
- `assets/css/components.css` — Sultan-specific component styles (verdict badges, tool cards, comparison tables, etc.)

### Asset Locations
```
assets/
├── css/
│   ├── tokens.css
│   └── components.css
├── logos/
│   ├── logo-mark.svg            # Gold diamonds (dark bg)
│   ├── logo-mark-white.svg      # White diamonds (dark bg)
│   ├── logo-wordmark.svg        # Diamonds + text (dark bg)
│   └── logo-wordmark-light.svg  # Diamonds + text (light bg)
├── favicons/
│   ├── favicon-gold.svg         # Gold fill, dark diamonds (primary)
│   ├── favicon-outline.svg      # Dark fill, gold outline
│   └── favicon-dark.svg         # Dark fill, white diamonds
├── icons/
│   ├── diamond-single.svg       # Single diamond (currentColor)
│   └── diamonds-triple.svg      # Triple cascade (currentColor)
└── social/
    (generate OG image from brand colors + wordmark)
```

---

## Architecture (How To Build This)

### Pattern
This follows the same programmatic SEO pattern as:
- **b2bsalestools** (`/Users/rome/Documents/projects/b2bsalestools/build.py`) — 196 pages, single-file build
- **provyx-website** (`/Users/rome/Documents/projects/provyx-website/scripts/build.py`) — 346 pages, modular build

Use a **hybrid approach:**
- `scripts/build.py` — Main build script with all tool data inline (b2bsalestools pattern)
- `scripts/nav_config.py` — Site metadata, nav items, footer columns (provyx pattern)
- `scripts/templates.py` — Shared HTML generators: head, nav, footer, page wrapper, schema (provyx pattern)
- Output to `output/` directory
- CSS version param for cache busting (`styles.css?v=1`)

### Build Command
```bash
cd /Users/rome/Documents/projects/sultanofsaas && python3 scripts/build.py
```

### Preview
```bash
cd /Users/rome/Documents/projects/sultanofsaas/output && python3 -m http.server 8086
```
→ http://localhost:8086/

---

## Page Types

### 1. Tool Reviews (`/tools/{slug}/`)
- Individual review page for each SaaS tool
- Sultan's Verdict Card (full) with score, sub-scores, summary
- Pros/cons list
- Pricing breakdown
- "Best for" description
- Link to tool website (affiliate link when available)
- **Target: 500-1,000 tools**

### 2. Category Guides (`/best/{category}/`)
- "Best {Category} Tools for SMBs" pages
- Grid of tool cards sorted by score
- Sultan's Pick highlighted at top
- Category description and buying advice
- **Target: 50-80 categories**

### 3. Comparisons (`/{tool}-vs-{tool}/`)
- Side-by-side comparison with table
- Winner Banner at top declaring the winner
- Feature-by-feature breakdown
- Pricing comparison
- Sultan's final verdict on which to pick and why
- **Target: 200-400 comparison pages**

### 4. Alternatives (`/{tool}-alternatives/`)
- "Best {Tool} Alternatives" pages
- Ranked list of alternatives with scores
- Why someone might leave the original tool
- **Target: 200-400 alternatives pages**

### 5. Pricing Pages (`/{tool}-pricing/`)
- "{Tool} Pricing Breakdown" pages
- Tier-by-tier analysis
- Price tier tag (Free/Budget/Mid/Premium/Enterprise)
- Sultan's take on whether it's worth the price
- **Target: 300-500 pricing pages**

### 6. Stack Guides (`/stacks/{slug}/`)
- Curated tool bundles by role and budget
- Examples: "The $0/mo Founder Stack", "The $200/mo Sales Team Stack", "The Agency Stack Under $500/mo"
- Each tool in the stack with price and verdict
- Total monthly cost calculated
- **Target: 30-50 stack guides**

### 7. Homepage (`/`)
- Hero with tagline and search/browse CTA
- Featured Sultan's Picks (top tools across categories)
- Popular comparisons
- Recent stack guides
- Category navigation grid

---

## Data Structure

Tools defined inline in `build.py` using a helper function:

```python
TOOLS = {}

def T(slug, name, category, url, score, verdict_word, verdict_line,
      best_for, pricing_start, pricing_tier, pros, cons,
      features=None, pricing_tiers=None, subscores=None,
      sultans_pick=False, affiliate_url=None):
    """Register a tool."""
    TOOLS[slug] = {
        'slug': slug,
        'name': name,
        'category': category,          # primary category slug
        'url': url,                     # tool's website
        'score': score,                 # 1.0-10.0
        'verdict_word': verdict_word,   # "Excellent" / "Solid Pick" / etc
        'verdict_line': verdict_line,   # One-line Sultan's Verdict
        'best_for': best_for,           # "Solo founders who need..."
        'pricing_start': pricing_start, # "Free" / "$25/mo" / "$99/user/mo"
        'pricing_tier': pricing_tier,   # "free" / "budget" / "mid" / "premium" / "enterprise"
        'pros': pros,                   # list of strings
        'cons': cons,                   # list of strings
        'features': features or [],     # list of feature strings for comparison tables
        'pricing_tiers': pricing_tiers or [],  # list of {name, price, features}
        'subscores': subscores or {},   # {ease_of_use: 8.5, value: 7.0, ...}
        'sultans_pick': sultans_pick,   # bool — top pick in category
        'affiliate_url': affiliate_url, # affiliate link (if any)
    }

CATEGORIES = {
    'crm': {
        'slug': 'crm',
        'name': 'CRM Software',
        'description': 'Customer relationship management tools...',
        'tools': ['hubspot', 'salesforce', 'pipedrive', 'close', ...],
    },
    # ...
}

COMPARISONS = [
    {'slug': 'hubspot-vs-salesforce', 'tools': ['hubspot', 'salesforce'], 'winner': 'hubspot'},
    # ...
]

ALTERNATIVES = [
    {'slug': 'salesforce-alternatives', 'tool': 'salesforce', 'alts': ['hubspot', 'pipedrive', ...]},
    # ...
]

STACKS = [
    {
        'slug': 'zero-dollar-founder',
        'name': 'The $0/mo Founder Stack',
        'description': '...',
        'tools': [
            {'slug': 'hubspot', 'use': 'CRM', 'plan': 'Free'},
            {'slug': 'notion', 'use': 'Docs & Wiki', 'plan': 'Free'},
            # ...
        ],
        'total_cost': '$0/mo',
    },
    # ...
]
```

---

## URL Structure

```
/                                    # Homepage
/tools/{slug}/                       # Tool review (e.g., /tools/hubspot/)
/best/{category}/                    # Category guide (e.g., /best/crm/)
/{tool}-vs-{tool}/                   # Comparison (e.g., /hubspot-vs-salesforce/)
/{tool}-alternatives/                # Alternatives (e.g., /salesforce-alternatives/)
/{tool}-pricing/                     # Pricing (e.g., /hubspot-pricing/)
/stacks/{slug}/                      # Stack guide (e.g., /stacks/zero-dollar-founder/)
/sitemap.xml                         # Sitemap
```

Comparison, alternatives, and pricing pages live at the root level (not nested) for cleaner URLs and better SEO.

---

## Monetization

### Affiliate Programs (primary revenue)
- HubSpot: 30% recurring up to 1 year (~$150+/signup)
- Semrush: $200/sale or $10/trial
- Monday.com: up to $150/sale
- Notion: 50% of first year
- Most SaaS tools have programs on PartnerStack, Impact, or direct

### Sponsored Placements (future)
- "Sultan's Pick" sponsorship in category pages
- Featured placement in stack guides

### Newsletter (list building)
- Weekly "Sultan's Stack" email — one tool recommendation per week
- Builds email list for predictable affiliate clicks

---

## Seed Data: Start With These Categories

Priority categories for launch (highest search volume + affiliate payouts):

1. CRM Software
2. Project Management
3. Email Marketing
4. Sales Engagement
5. Help Desk / Customer Support
6. Accounting / Invoicing
7. Marketing Automation
8. Team Communication
9. Video Conferencing
10. Website Builders
11. E-commerce Platforms
12. HR / People Management
13. Proposal / Contract Software
14. Social Media Management
15. SEO Tools
16. Analytics / BI
17. Design Tools
18. Form / Survey Tools
19. Scheduling / Booking
20. File Storage / Sharing

### Seed Tools Per Category
Start with 8-15 tools per category for launch. Prioritize:
- The market leader (Salesforce, HubSpot, etc.)
- The top 2-3 challengers
- The best free option
- The best value option
- 2-3 niche/underdog picks

---

## Technical Notes

- **Static site** — all HTML generated by build.py, no server needed
- **Deploy:** GitHub Pages, Cloudflare Pages, or Netlify (all free)
- **SEO:** Generate sitemap.xml, robots.txt, canonical URLs, structured data (BreadcrumbList, FAQPage, Product schema)
- **OG images:** Generate a default social card from brand colors + wordmark
- **No JavaScript required** for core pages — progressive enhancement only
- **CSS:** tokens.css + components.css handle all styling. May need a main styles.css for layout/page-specific styles.
- **Google Fonts:** Load Outfit, Source Serif 4, JetBrains Mono via `<link>` tag

---

## What To Build First

1. `scripts/nav_config.py` — site metadata, nav structure, footer columns
2. `scripts/templates.py` — HTML generators (head, nav, footer, page wrapper, schema helpers)
3. `assets/css/styles.css` — page layouts, responsive grid, page-type-specific styles (tokens.css and components.css are already done)
4. `scripts/build.py` — data + page generation for all page types
5. Seed data — start with 5 categories, 10 tools each = 50 tool pages + category pages + comparisons + alternatives
6. Homepage
7. sitemap.xml generation

---

## Reference Sites (for build pattern)
- **b2bsalestools:** `/Users/rome/Documents/projects/b2bsalestools/build.py` (single-file, 196 pages)
- **provyx-website:** `/Users/rome/Documents/projects/provyx-website/scripts/` (modular, 346 pages)
- **cannabisers:** `/Users/rome/Documents/projects/cannabisers/scripts/build.py` (713 pages)
