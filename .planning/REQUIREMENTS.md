# Requirements: SultanOfSaaS Phase 3 Quality Audit & Deploy

**Defined:** 2026-03-13
**Core Value:** Every review picks a winner with evidence. Ship a site where all 334 pages pass writing quality standards.

## v1 Requirements

### Audit Script

- [x] **AUDIT-01**: Audit script scans all 9 content files for false reframes (multiple regex patterns covering "not X, it's Y", "isn't X. It's Y.", "less about X, more about Y")
- [x] **AUDIT-02**: Audit script detects all em-dashes in content strings
- [x] **AUDIT-03**: Audit script flags banned words (robust, leverage, synergy, holistic, cutting-edge, seamless, frictionless, genuinely, truly, really, actually, game-changer, paradigm shift, best-in-class)
- [x] **AUDIT-04**: Audit script validates word count per tool review (2,000-4,000 target range)
- [x] **AUDIT-05**: Audit script checks all 9 content sections are present per tool (overview, expanded_pros, expanded_cons, pricing_detail, who_should_buy, who_should_skip, stage_guidance, alternatives_detail, verdict_long, faqs)
- [x] **AUDIT-06**: Audit script validates niche winners differ from Sultan's Pick for every niche/category combo
- [x] **AUDIT-07**: Audit script validates all 17 industry pages have picks for all 9 categories
- [x] **AUDIT-08**: Audit script generates a clear report with findings grouped by severity (ERROR/WARNING)

### Content Fixes

- [x] **FIX-01**: All false reframes removed or rewritten across all content files
- [x] **FIX-02**: All em-dashes replaced with periods, commas, or parentheses
- [x] **FIX-03**: All banned words replaced with appropriate alternatives
- [ ] **FIX-04**: All 7 niche winner conflicts resolved (different winner assigned with new rationale)
- [ ] **FIX-05**: Any missing content sections filled in
- [ ] **FIX-06**: Industry picks added for any missing category/industry combinations

### SEO Validation

- [x] **SEO-01**: All 334 pages have unique meta title and description
- [x] **SEO-02**: All inner pages have BreadcrumbList JSON-LD schema
- [x] **SEO-03**: All tool review pages with FAQs have FAQPage JSON-LD schema
- [x] **SEO-04**: No broken internal links across all pages

### Visual & Deploy

- [ ] **VIS-01**: Sample pages render correctly in browser (homepage, category, tool review, niche, industry, tools index)
- [ ] **VIS-02**: New category pages (AI SDR, Sales Engagement, Conversation Intelligence, Data Enrichment) have correct CSS styling
- [ ] **DEPLOY-01**: Site deployed to GitHub Pages at sultanofsaas.com

## v2 Requirements

### Content Polish

- **POLISH-01**: Readability scoring (Flesch-Kincaid 8-12 range) across all reviews
- **POLISH-02**: Template homogeneity reduction (diversify transition phrases, vary section lengths)
- **POLISH-03**: Pricing accuracy verification against current vendor pricing pages (top 30 tools)
- **POLISH-04**: Unearned declaration removal ("The pattern here is clear:", "Here's the thing:")

### Analytics

- **ANALYTICS-01**: Google Analytics integration
- **ANALYTICS-02**: Google Search Console setup
- **ANALYTICS-03**: Rank tracking for target keywords

## Out of Scope

| Feature | Reason |
|---------|--------|
| Automated screenshot testing | One-time visual check, manual is faster |
| spaCy/NLP-based content analysis | Overkill for regex-solvable writing rules |
| External prose linters (Vale, textlint) | Content is in Python dicts, not markup files |
| Pricing page re-verification | Defer to v2, current prices are close enough for launch |
| Blog/content marketing | Separate initiative |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUDIT-01 | Phase 1 | Complete |
| AUDIT-02 | Phase 1 | Complete |
| AUDIT-03 | Phase 1 | Complete |
| AUDIT-04 | Phase 1 | Complete |
| AUDIT-05 | Phase 1 | Complete |
| AUDIT-06 | Phase 1 | Complete |
| AUDIT-07 | Phase 1 | Complete |
| AUDIT-08 | Phase 1 | Complete |
| FIX-01 | Phase 2 | Complete |
| FIX-02 | Phase 2 | Complete |
| FIX-03 | Phase 2 | Complete |
| FIX-04 | Phase 2 | Pending |
| FIX-05 | Phase 2 | Pending |
| FIX-06 | Phase 2 | Pending |
| SEO-01 | Phase 1 | Complete |
| SEO-02 | Phase 1 | Complete |
| SEO-03 | Phase 1 | Complete |
| SEO-04 | Phase 1 | Complete |
| VIS-01 | Phase 3 | Pending |
| VIS-02 | Phase 3 | Pending |
| DEPLOY-01 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0

---
*Requirements defined: 2026-03-13*
*Last updated: 2026-03-13 after roadmap creation*
