# Prompt for New Context Window

Copy everything below the line into a new Claude Code conversation:

---

I'm building sultanofsaas.com — an opinionated SaaS review site for SMB founders. Phase 1 is complete (50 tools, 145 pages, working build). Now I need Phase 2: niche pages, industry pages, and a filterable tools index.

**Read these files in this order:**

1. `/Users/rome/Documents/projects/sultanofsaas/PHASE2-HANDOFF.md` — Full spec for Phase 2 (what's built, what to build, data structures, URL patterns)
2. `/Users/rome/Documents/projects/sultanofsaas/BRAND.md` — Brand reference (colors, typography, components, voice)
3. `/Users/rome/Documents/projects/sultanofsaas/scripts/build.py` — Current build script with all 50 tools and page generators (THE BIG FILE — read all of it)
4. `/Users/rome/Documents/projects/sultanofsaas/scripts/templates.py` — HTML generators and component helpers
5. `/Users/rome/Documents/projects/sultanofsaas/scripts/nav_config.py` — Nav structure and footer
6. `/Users/rome/Documents/projects/sultanofsaas/assets/css/styles.css` — Page layouts (you'll add new styles here)

Reference `tokens.css` and `components.css` as needed but do NOT edit them.

**What to build:**

1. **NICHES data structure** in build.py — 6 universal niches (solo-founders, small-teams, free, agencies, ecommerce, startups) + ~10 category-specific niches. Each niche re-ranks the tools and picks a DIFFERENT winner for that audience. ~42 new pages at `/best/{category}/{niche}/`.

2. **INDUSTRIES data structure** in build.py — 17 industries in 3 tiers (ecommerce, saas, agencies, real-estate, professional-services, startups, nonprofits, healthcare, education, creators, financial-services, construction, restaurants, manufacturing, fitness, legal, accounting). Each industry page recommends the best tool from EACH category. 17 new pages at `/for/{industry}/`.

3. **Filterable tools index** at `/tools/` — All tools displayed as cards with client-side filtering via vanilla JS. Filters: category dropdown, price tier pills, "best for" pills, sort by score/price/name. Data attributes on each card, ~30 lines of JS.

4. **New CSS** in styles.css — niche page layout, industry page layout, filter bar styles, filter pill active states.

5. **Nav updates** in nav_config.py — Add "Tools" link, "By Industry" link or dropdown, update footer with new page links.

**Important rules:**
- All data stays inline in build.py (no external JSON)
- NEVER use false reframes: no "not X, it's Y" / "isn't X. It's Y." — ZERO TOLERANCE
- Every niche page must pick a different winner than the main category page (or the page has no reason to exist)
- Niche winners must be defensible with specific reasoning
- Scores don't change per niche — only the ranking and winner change
- Keep copy opinionated and specific to the niche audience
- All pages need canonical URLs, breadcrumbs, and meta descriptions
- Target: ~205 total pages after Phase 2

**Build and preview:**
```bash
cd /Users/rome/Documents/projects/sultanofsaas && python3 scripts/build.py
cd /Users/rome/Documents/projects/sultanofsaas/output && python3 -m http.server 8086
```

Read all 6 files first. Then add the data structures, page generators, CSS, and nav updates. Run the build after each major addition to catch errors early.
