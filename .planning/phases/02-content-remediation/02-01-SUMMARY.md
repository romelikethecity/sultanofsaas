---
phase: 02-content-remediation
plan: 01
subsystem: content
tags: [writing-quality, banned-words, false-reframe, editorial]

# Dependency graph
requires:
  - phase: 01-automated-quality-audit
    provides: audit script and baseline error counts
provides:
  - Zero writing errors in CRM, PM, email, SEO, and help desk content files
affects: [02-content-remediation]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Context-dependent word replacement over mechanical find-replace"
    - "False reframes rewritten to direct voice, not deleted"

key-files:
  created: []
  modified:
    - scripts/content/tools_crm.py
    - scripts/content/tools_project_management.py
    - scripts/content/tools_email_marketing.py
    - scripts/content/tools_seo_tools.py
    - scripts/content/tools_help_desk.py

key-decisions:
  - "Dropped banned words (genuinely, actually, really, truly, best-in-class) by deletion or minimal rewording rather than thesaurus swaps"
  - "Trello false reframe rewritten to describe Atlassian's retention strategy directly"

patterns-established:
  - "Banned word removal: prefer deletion when the sentence reads naturally without it"

requirements-completed: [FIX-01, FIX-02, FIX-03]

# Metrics
duration: 12min
completed: 2026-03-13
---

# Phase 2 Plan 1: Original Content Remediation Summary

**Removed ~120 banned words and 1 false reframe from 5 content files (CRM, PM, email, SEO, help desk) to pass audit with zero writing errors**

## Performance

- **Duration:** 12 min
- **Started:** 2026-03-13T22:35:46Z
- **Completed:** 2026-03-13T22:48:31Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- Eliminated all banned word violations (genuinely, actually, really, truly, best-in-class) across 50 tools in 5 categories
- Rewrote trello false reframe in stage_guidance.enterprise from "not because it's the right tool" to direct statement about Atlassian's retention play
- All 5 content files now pass audit check_writing with zero ERROR-level findings
- Replacements maintain The Sultan's opinionated voice throughout

## Task Commits

Each task was committed atomically:

1. **Task 1: Fix banned words and em-dashes in CRM, PM, and email content files** - `bfef8fe` (fix)
2. **Task 2: Fix banned words and em-dashes in SEO and help desk content files** - `8d85239` (fix)

## Files Created/Modified
- `scripts/content/tools_crm.py` - Removed ~32 banned words across 10 CRM tools
- `scripts/content/tools_project_management.py` - Removed ~28 banned words + 1 false reframe across 10 PM tools
- `scripts/content/tools_email_marketing.py` - Removed ~22 banned words across 10 email tools
- `scripts/content/tools_seo_tools.py` - Removed ~19 banned words across 10 SEO tools
- `scripts/content/tools_help_desk.py` - Removed ~21 banned words across 10 help desk tools

## Decisions Made
- Most banned words (genuinely, actually, really, truly) were removed by simple deletion since sentences read naturally without them
- "best-in-class" replaced with "Top-tier" (Notion documentation section)
- No em-dashes were found in these 5 files (audit confirmed zero em-dash violations)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Case-sensitive "Genuinely" (capitalized at start of title) was missed in initial grep pass; caught by audit verification and fixed before commit

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- 5 original content files clean; remaining plans (02-02, 02-03) cover additional content files
- Audit script verified zero errors across all 5 target categories

---
*Phase: 02-content-remediation*
*Completed: 2026-03-13*
