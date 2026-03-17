# Requirements: SultanOfSaaS

**Defined:** 2026-03-16
**Core Value:** Every review picks a winner with evidence. Founders get decisive recommendations backed by real pricing, specific use cases, and honest trade-offs.

## v2.0 Requirements

Requirements for v2.0 — Audience Growth & Content Scaling. Each maps to roadmap phases.

### Newsletter Capture

- [ ] **NEWS-01**: Email signup form embedded across all page types using existing D1 newsletter worker
- [ ] **NEWS-02**: sultanofsaas.com added to CORS allowed origins in newsletter worker (`subscribe.js`)
- [ ] **NEWS-03**: "sultan-of-saas" list seeded in D1 database (name: "The Sultan's Pick", from: insights@sultanofsaas.com)
- [ ] **NEWS-04**: Signup form styled to match SultanOfSaaS brand (gold/dark theme)

### Versus/Alternative Scaling

- [ ] **VERSUS-01**: 50+ new "[Tool A] vs [Tool B]" comparison pages using existing build.py patterns and data structure
- [ ] **VERSUS-02**: 30+ new "[Tool] alternatives" pages using existing build.py patterns and data structure
- [ ] **VERSUS-03**: All new versus/alternative pages pass audit.py with 0 errors

### Pricing Changelogs

- [ ] **PRICE-01**: "Last updated" date displayed on each of 90 existing pricing pages
- [ ] **PRICE-02**: Changelog section on each pricing page showing historical price changes
- [ ] **PRICE-03**: Changelog data stored inline in build.py following existing data patterns

### Comparison Matrices

- [ ] **MATRIX-01**: One filterable side-by-side comparison table per category (9 categories total)
- [ ] **MATRIX-02**: Matrix displays pricing, ratings, and best-for tags for all tools in each category
- [ ] **MATRIX-03**: Client-side filtering with vanilla JS (no frameworks)

### Stack Expansion

- [ ] **STACK-01**: 12+ new stack pages covering additional ICPs (RevOps, PLG, ABM, SDR manager, CS, founder, etc.)
- [ ] **STACK-02**: Total stack pages reach 20+ (currently 8)

### Switched Teardowns

- [ ] **SWITCH-01**: 20-30 "Why teams switch from [Tool A] to [Tool B]" pages targeting high-intent keywords
- [ ] **SWITCH-02**: Content built from existing review data (pros, cons, pricing comparisons)

## Future Requirements

None deferred — all proposed features scoped into v2.0.

## Out of Scope

| Feature | Reason |
|---------|--------|
| New backend/API for newsletter | Existing D1 worker handles everything |
| JavaScript frameworks | Vanilla JS only, per v1.0 constraint |
| User-generated content or comments | Content site, not community |
| Affiliate link integration | Separate initiative, not this milestone |
| Blog/content marketing | Separate initiative |
| Tool data in external JSON files | All data stays inline in build.py |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| NEWS-01 | — | Pending |
| NEWS-02 | — | Pending |
| NEWS-03 | — | Pending |
| NEWS-04 | — | Pending |
| VERSUS-01 | — | Pending |
| VERSUS-02 | — | Pending |
| VERSUS-03 | — | Pending |
| PRICE-01 | — | Pending |
| PRICE-02 | — | Pending |
| PRICE-03 | — | Pending |
| MATRIX-01 | — | Pending |
| MATRIX-02 | — | Pending |
| MATRIX-03 | — | Pending |
| STACK-01 | — | Pending |
| STACK-02 | — | Pending |
| SWITCH-01 | — | Pending |
| SWITCH-02 | — | Pending |

**Coverage:**
- v2.0 requirements: 17 total
- Mapped to phases: 0
- Unmapped: 17 ⚠️

---
*Requirements defined: 2026-03-16*
*Last updated: 2026-03-16 after initial definition*
