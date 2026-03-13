---
phase: 02-content-remediation
plan: 02
subsystem: content
tags: [writing-quality, banned-words, em-dashes, content-audit]

# Dependency graph
requires:
  - phase: 01-automated-quality-audit
    provides: audit script with check_writing function and banned word detection
provides:
  - Zero writing errors in AI SDR, sales engagement, conversation intelligence, and data enrichment content files
  - Zero writing errors in build.py TOOLS/NICHES/INDUSTRIES text data
affects: [02-content-remediation]

# Tech tracking
tech-stack:
  added: []
  patterns: [banned-word replacement patterns established in Plan 01 reused here]

key-files:
  created: []
  modified:
    - scripts/content/tools_ai_sdr.py
    - scripts/content/tools_sales_engagement.py
    - scripts/content/tools_conversation_intelligence.py
    - scripts/content/tools_data_enrichment.py
    - scripts/build.py

key-decisions:
  - "Preserved Seamless.AI tool name references (capitalized) while replacing lowercase 'seamless' adjective usage"
  - "HTML template text in build.py left out of scope (not TOOLS/NICHES/INDUSTRIES data)"
  - "Em-dashes replaced with context-appropriate punctuation: colons for lists/explanations, periods for full stops, commas for light pauses, parentheses for asides"

patterns-established:
  - "Banned word replacements: genuinely/actually/truly/really -> delete adverb; best-in-class -> top-tier/strongest/category-leading; seamless/frictionless -> smooth/effortless; robust -> solid/capable; leverage -> use"

requirements-completed: [FIX-01, FIX-02, FIX-03]

# Metrics
duration: 17min
completed: 2026-03-13
---

# Phase 2 Plan 2: Content File Remediation Summary

**Eliminated 174 writing violations (95 banned words + 79 em-dashes) across 4 content files and build.py inline text data**

## Performance

- **Duration:** 17 min
- **Started:** 2026-03-13T22:35:47Z
- **Completed:** 2026-03-13T22:52:47Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Removed all banned words from 4 new category content files (AI SDR: 19, sales engagement: 15, conversation intelligence: 42, data enrichment: 19)
- Removed all banned words and em-dashes from build.py TOOLS/NICHES/INDUSTRIES data (53 fixes)
- Preserved all Seamless.AI tool name references without false replacements
- Writing errors reduced from 312 to 12 (remaining 12 are data/SEO errors, zero writing errors)

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix writing violations in 4 content files** - `75fcfa7` (fix)
2. **Task 2: Fix writing violations in build.py TOOLS/NICHES/INDUSTRIES** - `9369ddf` (fix)

## Files Created/Modified
- `scripts/content/tools_ai_sdr.py` - 19 banned word replacements
- `scripts/content/tools_sales_engagement.py` - 15 banned word replacements
- `scripts/content/tools_conversation_intelligence.py` - 42 banned word replacements
- `scripts/content/tools_data_enrichment.py` - 19 banned word replacements
- `scripts/build.py` - 53 fixes (24 TOOLS banned words/em-dashes, 18 NICHES, 11 INDUSTRIES)

## Decisions Made
- Preserved Seamless.AI tool name references: the audit script excludes capitalized tool names, so only lowercase "seamless" as adjective was replaced
- HTML template text in build.py (homepage headings, about page scoring criteria) left untouched as out of scope for this plan
- Em-dash replacements chosen by context: colons before lists, periods between independent clauses, commas for light pauses

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All writing violations (banned words + em-dashes) eliminated from content files and build.py data
- Remaining 12 audit errors are data integrity (7 niche/pick conflicts) and SEO (5 missing BreadcrumbList schemas), covered by Plan 03
- Ready for Plan 03 (final fixes + build verification)

---
*Phase: 02-content-remediation*
*Completed: 2026-03-13*
