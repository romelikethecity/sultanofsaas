# Roadmap: SultanOfSaaS

## Milestones

- ✅ **v1.0 Quality Audit & Deploy** — Phases 1-3 (shipped 2026-03-13)
- 🚧 **v2.0 Audience Growth & Content Scaling** — Phases 4-9 (in progress)

## Phases

<details>
<summary>✅ v1.0 Quality Audit & Deploy (Phases 1-3) — SHIPPED 2026-03-13</summary>

- [x] **Phase 1: Automated Quality Audit** - Build audit.py to catch writing violations and data integrity issues across all 90 tools and 334 pages
- [x] **Phase 2: Content Remediation** - Fix all errors found by audit (banned words, em-dashes, false reframes, niche winner conflicts, schema markup)
- [x] **Phase 3: Visual Verification & Deploy** - Verify generated pages render correctly and deploy to GitHub Pages

</details>

### v2.0 Audience Growth & Content Scaling

- [ ] **Phase 4: Newsletter Capture** - Email signup across all pages using existing D1 worker infrastructure
- [ ] **Phase 5: Versus/Alternative Scaling** - 80+ new comparison and alternative pages targeting high-intent search queries
- [ ] **Phase 6: Pricing Changelogs** - Freshness signals and historical pricing data on all 90 pricing pages
- [ ] **Phase 7: Comparison Matrices** - Filterable side-by-side category tables for all 9 categories
- [ ] **Phase 8: Stack Expansion** - Grow stack guides from 8 to 20+ covering additional ICPs
- [ ] **Phase 9: Switched Teardowns** - 20-30 "Why teams switch from X to Y" pages targeting migration keywords

## Phase Details

### Phase 4: Newsletter Capture
**Goal**: Visitors on any page can subscribe to the Sultan's Pick newsletter with zero friction
**Depends on**: Nothing (independent of other v2.0 phases)
**Requirements**: NEWS-01, NEWS-02, NEWS-03, NEWS-04
**Success Criteria** (what must be TRUE):
  1. Visitor sees a branded signup form on every page type (tool review, category, niche, industry, comparison, alternative, pricing, stack, tools index, homepage)
  2. Visitor submits email and receives confirmation (form posts to existing D1 worker, no errors)
  3. Submitted emails appear in D1 database under "sultan-of-saas" list
  4. Signup form matches SultanOfSaaS gold/dark brand (not generic newsletter styling)
**Plans**: TBD

### Phase 5: Versus/Alternative Scaling
**Goal**: SultanOfSaaS covers the long tail of "[Tool A] vs [Tool B]" and "[Tool] alternatives" searches with 80+ new pages
**Depends on**: Nothing (uses existing build.py patterns)
**Requirements**: VERSUS-01, VERSUS-02, VERSUS-03
**Success Criteria** (what must be TRUE):
  1. At least 50 new versus pages exist with opinionated winners, pricing comparisons, and use-case recommendations
  2. At least 30 new alternative pages exist with ranked alternatives and "choose X if..." framing
  3. All new pages pass audit.py with 0 errors (writing rules, data integrity, SEO structure)
  4. New pages appear in site navigation and are linked from relevant tool/category pages
**Plans**: TBD

### Phase 6: Pricing Changelogs
**Goal**: Every pricing page shows when it was last verified and how pricing has changed over time
**Depends on**: Nothing (modifies existing pricing pages)
**Requirements**: PRICE-01, PRICE-02, PRICE-03
**Success Criteria** (what must be TRUE):
  1. Every pricing page displays a "Last verified" date visible above the fold
  2. Pricing pages with historical changes show a changelog section listing what changed and when
  3. Changelog data is stored inline in build.py following existing T() data patterns
**Plans**: TBD

### Phase 7: Comparison Matrices
**Goal**: Each category has a filterable comparison table so visitors can compare all tools side-by-side
**Depends on**: Nothing (new page type)
**Requirements**: MATRIX-01, MATRIX-02, MATRIX-03
**Success Criteria** (what must be TRUE):
  1. Each of the 9 categories has a dedicated comparison matrix page accessible from category navigation
  2. Matrix displays pricing tiers, Sultan's rating, and best-for tags for every tool in that category
  3. Visitor can filter/sort the table by price range, rating, or best-for tag using client-side vanilla JS
**Plans**: TBD

### Phase 8: Stack Expansion
**Goal**: Stack guides cover 20+ ICPs so visitors find a recommended tool stack for their specific role
**Depends on**: Nothing (extends existing stack page pattern)
**Requirements**: STACK-01, STACK-02
**Success Criteria** (what must be TRUE):
  1. At least 12 new stack pages exist covering ICPs like RevOps lead, PLG founder, ABM manager, SDR manager, CS leader, solo founder, and others
  2. Total stack page count reaches 20 or more (up from 8)
  3. Each stack page recommends specific tools with reasoning tied to that ICP's workflow
**Plans**: TBD

### Phase 9: Switched Teardowns
**Goal**: High-intent "switching from X to Y" searches land on dedicated teardown pages with migration reasoning
**Depends on**: Phase 5 (benefits from expanded versus data, but can use existing review data)
**Requirements**: SWITCH-01, SWITCH-02
**Success Criteria** (what must be TRUE):
  1. 20-30 "Why teams switch from [Tool A] to [Tool B]" pages exist targeting real migration patterns
  2. Each teardown page cites specific pricing, feature, and workflow differences drawn from existing review data
  3. Teardown pages pass audit.py with 0 errors
**Plans**: TBD

## Progress

**Execution Order:**
Phases 4-8 are independent and can execute in any order. Phase 9 benefits from Phase 5 data but can proceed with existing review data.

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Automated Quality Audit | v1.0 | 2/2 | Complete | 2026-03-13 |
| 2. Content Remediation | v1.0 | 3/3 | Complete | 2026-03-13 |
| 3. Visual Verification & Deploy | v1.0 | 1/1 | Complete | 2026-03-13 |
| 4. Newsletter Capture | v2.0 | 0/? | Not started | - |
| 5. Versus/Alternative Scaling | v2.0 | 0/? | Not started | - |
| 6. Pricing Changelogs | v2.0 | 0/? | Not started | - |
| 7. Comparison Matrices | v2.0 | 0/? | Not started | - |
| 8. Stack Expansion | v2.0 | 0/? | Not started | - |
| 9. Switched Teardowns | v2.0 | 0/? | Not started | - |
