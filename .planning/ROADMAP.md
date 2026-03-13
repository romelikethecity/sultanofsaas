# Roadmap: SultanOfSaaS Phase 3 Quality Audit & Deploy

## Overview

Ship sultanofsaas.com with all 334 pages passing writing quality standards. Build an audit script to find every violation, fix what it finds, then visually verify and deploy. Three phases: detect, fix, ship.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Automated Quality Audit** - Build audit script covering writing rules, content completeness, SEO, and data integrity
- [ ] **Phase 2: Content Remediation** - Fix all violations found by the audit script
- [ ] **Phase 3: Visual Verification & Deploy** - Confirm pages render correctly and push to GitHub Pages

## Phase Details

### Phase 1: Automated Quality Audit
**Goal**: A single script surfaces every quality, content, and SEO issue across all 334 pages
**Depends on**: Nothing (first phase)
**Requirements**: AUDIT-01, AUDIT-02, AUDIT-03, AUDIT-04, AUDIT-05, AUDIT-06, AUDIT-07, AUDIT-08, SEO-01, SEO-02, SEO-03, SEO-04
**Success Criteria** (what must be TRUE):
  1. Running `python3 scripts/audit.py` scans all 9 content files and reports false reframes, em-dashes, and banned words with file/line references
  2. The audit report shows word count per tool review and flags any outside the 2,000-4,000 range
  3. The audit report identifies missing content sections, niche winner conflicts, and incomplete industry picks
  4. The audit report validates all 334 pages for unique meta titles, BreadcrumbList schema, FAQPage schema, and broken internal links
  5. Output is grouped by severity (ERROR/WARNING) with actionable location info
**Plans:** 2 plans

Plans:
- [x] 01-01-PLAN.md -- Content quality audit (writing rules, structure validation, data integrity checks)
- [x] 01-02-PLAN.md -- SEO validation (meta tags, schema markup, internal links across 334 pages)

### Phase 2: Content Remediation
**Goal**: Every violation from the audit is resolved and the audit script runs clean
**Depends on**: Phase 1
**Requirements**: FIX-01, FIX-02, FIX-03, FIX-04, FIX-05, FIX-06
**Success Criteria** (what must be TRUE):
  1. Re-running `python3 scripts/audit.py` produces zero ERROR-level findings
  2. All false reframes are rewritten (not just deleted) to preserve the original point in direct voice
  3. Every niche page picks a winner different from the main category Sultan's Pick
  4. All 17 industry pages have picks for all 9 categories
**Plans:** 3 plans

Plans:
- [x] 02-01-PLAN.md -- Fix writing violations in 5 original content files (CRM, PM, email, SEO, help desk)
- [x] 02-02-PLAN.md -- Fix writing violations in 4 new content files + build.py text (TOOLS/NICHES/INDUSTRIES)
- [x] 02-03-PLAN.md -- Fix data issues (niche winners, BreadcrumbList), rebuild, verify zero audit errors

### Phase 3: Visual Verification & Deploy
**Goal**: The site looks correct in a browser and is live at sultanofsaas.com
**Depends on**: Phase 2
**Requirements**: VIS-01, VIS-02, DEPLOY-01
**Success Criteria** (what must be TRUE):
  1. Homepage, a category page, a tool review, a niche page, an industry page, and the tools index all render correctly at localhost:8086
  2. New category pages (AI SDR, Sales Engagement, Conversation Intelligence, Data Enrichment) display with correct styling and layout
  3. Site is live and serving pages at sultanofsaas.com via GitHub Pages
**Plans**: TBD

Plans:
- [ ] 03-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Automated Quality Audit | 2/2 | Complete | 2026-03-13 |
| 2. Content Remediation | 3/3 | Complete | 2026-03-13 |
| 3. Visual Verification & Deploy | 0/? | Not started | - |
