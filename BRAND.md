# SultanOfSaaS.com — Brand Reference

> Opinionated SaaS tool reviews for SMBs and founders.
> Anonymous persona: "The Sultan" — decisive expert who picks winners.

---

## File Structure

```
sultanofsaas-brand/
├── css/
│   ├── tokens.css          # All CSS variables, base styles, utilities
│   └── components.css      # Sultan-specific component styles
├── logos/
│   ├── logo-mark.svg       # Flow Diamonds mark only (gold on transparent)
│   ├── logo-mark-white.svg # Flow Diamonds mark only (white on transparent)
│   ├── logo-wordmark.svg   # Diamonds + "SultanOfSaaS" text (dark bg)
│   └── logo-wordmark-light.svg # Diamonds + text (light bg)
├── favicons/
│   ├── favicon-gold.svg    # Gold fill, dark diamonds (primary)
│   ├── favicon-outline.svg # Dark fill, gold outline + diamonds
│   └── favicon-dark.svg    # Dark fill, white diamonds
├── icons/
│   ├── diamond-single.svg  # Single diamond (uses currentColor)
│   └── diamonds-triple.svg # Three cascading diamonds (uses currentColor)
└── docs/
    └── BRAND.md            # This file
```

---

## Logo: Flow Diamonds

Three rotated squares in an S-curve with cascading opacity:
- **Top diamond**: 100% opacity (#D4A054) — the winner
- **Middle diamond**: 55% opacity — the runner-up
- **Bottom diamond**: 25% opacity — the rest

### Inline SVG (copy-paste)

**Primary mark:**
```html
<svg viewBox="0 0 72 96" xmlns="http://www.w3.org/2000/svg">
  <rect x="16" y="6" width="24" height="24" rx="5" transform="rotate(45, 28, 18)" fill="#D4A054"/>
  <rect x="24" y="32" width="24" height="24" rx="5" transform="rotate(45, 36, 44)" fill="#D4A054" opacity="0.55"/>
  <rect x="16" y="58" width="24" height="24" rx="5" transform="rotate(45, 28, 70)" fill="#D4A054" opacity="0.25"/>
</svg>
```

**Small mark (nav, cards):**
```html
<svg viewBox="0 0 18 24" xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="0" width="8" height="8" rx="2" transform="rotate(45, 5, 4)" fill="#D4A054"/>
  <rect x="4" y="7.5" width="8" height="8" rx="2" transform="rotate(45, 8, 11.5)" fill="#D4A054" opacity="0.55"/>
  <rect x="1" y="15" width="8" height="8" rx="2" transform="rotate(45, 5, 19)" fill="#D4A054" opacity="0.25"/>
</svg>
```

**Single diamond icon (inline with scores, badges):**
```html
<svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
  <rect x="1" y="1" width="5.5" height="5.5" rx="1" transform="rotate(45, 3.75, 3.75)" fill="currentColor"/>
</svg>
```

### Logo Rules
- ✅ Gold (#D4A054) on dark backgrounds
- ✅ White (#F0F0F0) on dark when gold isn't appropriate
- ✅ Maintain opacity cascade: 100% / 55% / 25%
- ✅ Minimum height: 20px
- ✅ Clear space: 1 diamond-width on all sides
- ❌ Don't make all diamonds equal opacity
- ❌ Don't rotate the overall mark
- ❌ Don't change the diamond order
- ❌ Don't use on busy/patterned backgrounds

---

## Color Palette

### Core
| Name | Hex | CSS Variable | Usage |
|------|-----|-------------|-------|
| Primary Gold | `#D4A054` | `--color-primary` | Logo, accents, Sultan's Pick, links |
| Gold Light | `#E8C078` | `--color-primary-light` | Hover states, highlights |
| Gold Muted | `#A67B3D` | `--color-primary-dim` | Active states, borders |
| Gold Subtle | `rgba(212,160,84,0.12)` | `--color-primary-subtle` | Background tints |
| Electric Blue | `#3B82F6` | `--color-secondary` | Secondary actions, "Good" scores |
| Hot Pink | `#F472B6` | `--color-accent` | CTAs, attention moments |

### Backgrounds (darkest → lightest)
| Hex | CSS Variable | Usage |
|-----|-------------|-------|
| `#0C0E12` | `--bg-primary` | Page background |
| `#12151B` | `--bg-secondary` | Cards, panels |
| `#1A1D25` | `--bg-tertiary` | Elevated surfaces, table headers |
| `#1F2330` | `--bg-hover` | Hover states |
| `#252936` | `--bg-active` | Active/pressed states |

### Text
| Hex | CSS Variable | Usage |
|-----|-------------|-------|
| `#F0F0F0` | `--text-primary` | Headlines, primary content |
| `#9CA3AF` | `--text-secondary` | Body text, descriptions |
| `#6B7280` | `--text-tertiary` | Metadata, captions |
| `#0C0E12` | `--text-inverse` | Text on gold/light backgrounds |

### Verdict Scores
| Score Range | Label | Color | CSS Variable |
|-------------|-------|-------|-------------|
| 9.0 – 10 | Excellent | `#34D399` | `--verdict-excellent` |
| 7.0 – 8.9 | Solid Pick | `#60A5FA` | `--verdict-good` |
| 5.0 – 6.9 | Situational | `#FBBF24` | `--verdict-mid` |
| 3.0 – 4.9 | Avoid | `#F87171` | `--verdict-poor` |
| 1.0 – 2.9 | Hard Pass | `#EF4444` | `--verdict-bad` |

### Pricing Tiers
| Tier | Range | Color | CSS Variable |
|------|-------|-------|-------------|
| Free | $0 | `#34D399` | `--price-free` |
| Budget | <$30/mo | `#60A5FA` | `--price-budget` |
| Mid | $30–100/mo | `#FBBF24` | `--price-mid` |
| Premium | $100–300/mo | `#F472B6` | `--price-premium` |
| Enterprise | $300+/mo | `#A78BFA` | `--price-enterprise` |

---

## Typography

### Font Stack
| Role | Font | Weight Range | CSS Variable |
|------|------|-------------|-------------|
| Display | Outfit | 300–900 | `--font-display` |
| Body | Source Serif 4 | 400, 600, 700 + italic | `--font-body` |
| Mono | JetBrains Mono | 400, 500, 600 | `--font-mono` |

### Google Fonts Import
```html
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

### Usage Rules
- **Outfit** → Headlines, UI labels, navigation, buttons, badges, card titles
- **Source Serif 4** → Review body copy, tool descriptions, long-form editorial
- **JetBrains Mono** → Scores, prices, specs, data tables, technical attributes

### Wordmark Typography
The "SultanOfSaaS" wordmark uses Outfit weight 800:
- "Sultan" in `--text-primary` (#F0F0F0)
- "Of" in `--color-primary` (#D4A054)
- "SaaS" in `--text-primary` (#F0F0F0)
- Letter-spacing: -0.03em

---

## Key Components

### Sultan's Verdict Badge
Used on every tool review page and in tool cards. Shows score + label.
- Container: `--bg-tertiary` background, `--border-default` border, `--radius-md`
- Score: `--font-display` weight 900, sized `--text-2xl`, color from verdict scale
- Label: "Sultan's Verdict" in `--text-tertiary`, uppercase, `--text-xs`
- Word: "Excellent" / "Solid Pick" / etc in `--text-primary`
- Bar: 3px height, fill color matches verdict score

### Sultan's Verdict Card (Full)
The signature element on review pages.
- Gold border: `--border-gold`
- Gold glow shadow: `--shadow-gold`
- Header: Flow Diamonds icon + "THE SULTAN'S VERDICT" text
- Score: 3.2rem weight 900
- Sub-scores in 2-column grid, `--bg-hover` backgrounds

### Tool Profile Card
- Default: `--bg-tertiary`, `--border-default`, `--radius-lg`
- Hover: `--border-strong`, `--shadow-elevated`
- Sultan's Pick variant: `--sultans-pick-bg` gradient, gold border, gold glow
- Score inline uses single diamond icon + number

### Sultan's Pick Badge
- Gold text on gold-tinted background
- Uses triple-diamond icon (diamonds-triple.svg)
- Font: 0.6rem, weight 700, uppercase, letter-spacing 0.08em

### Comparison Table
- Winner column: gold top-border (2px), subtle gold background tint
- Winner tag: inline badge next to tool name
- Scores in `--font-mono`
- Check/cross use `--verdict-excellent` / `--verdict-poor`

### Winner Banner
- Background: `--winner-bg` gradient (gold → green)
- Gold border
- Flow Diamonds icon on left
- Tool name + reason in center
- Score badge on right with green tint

### Category Navigation
- Pills: `--bg-tertiary`, `--border-subtle`, `--radius-sm`
- Active: `--color-primary-subtle` bg, `--color-primary-dim` border, gold text
- Includes tool count per category

### Price Tier Tags
Colored pill badges. Each tier has its own color:
- Free (green), Budget (blue), Mid (yellow), Premium (pink), Enterprise (purple)

---

## Semantic Patterns

### Sultan's Pick (endorsed tools)
- Card gets gradient background + gold border + gold glow
- Triple-diamond badge appears
- These are the tools the Sultan recommends above all others in a category

### Winner (comparison pages)
- Table column gets gold top-border + subtle background
- Winner banner appears above/below table
- Winner tag inline with tool name

### Verdict Score Coloring
Always use the verdict color scale consistently:
- 9+ = green (`--verdict-excellent`)
- 7-8.9 = blue (`--verdict-good`)
- 5-6.9 = yellow (`--verdict-mid`)
- 3-4.9 = red-light (`--verdict-poor`)
- <3 = red (`--verdict-bad`)

---

## Page Types

The site has these programmatic page types:
1. **Tool Reviews** — individual review with Sultan's Verdict card
2. **Comparisons (X vs Y)** — side-by-side with comparison table + winner banner
3. **Alternatives** — "Best [Tool] Alternatives" with ranked tool cards
4. **Category Guides** — "Best [Category] Tools" with filtered tool cards
5. **Stack Guides** — curated bundles by role/budget

---

## Editorial Voice

- **Decisive**: Always picks a winner. Never says "it depends" without saying what it depends ON.
- **Direct**: Short sentences. No filler. Gets to the point.
- **Opinionated**: Has strong takes but backs them with reasoning.
- **Helpful**: The goal is saving founders time and money.
- **Not snarky**: Confident, not mean. Calls out overpriced tools, doesn't mock them.
- **"The Sultan's Verdict"**: The signature sign-off on every review.
