# Architecture Patterns

**Domain:** Content quality audit system for a Python static site generator
**Researched:** 2026-03-13

## Current System Architecture

Before defining the audit system, here is what it operates on:

```
scripts/
  build.py          (3,423 lines) — Tool data (T() registrations), categories, niches,
                                     industries, comparisons, alternatives, stack guides,
                                     and all HTML generation functions
  templates.py      (331 lines)  — Shared HTML wrappers, schema helpers, page writer
  nav_config.py     (93 lines)   — Site name, nav items, footer columns
  content/
    __init__.py     (98 lines)   — Content loader (get_tool_content, has_deep_content)
    tools_crm.py    (863 lines)  — Deep editorial content per CRM tool
    tools_*.py      (9 files, 7,655 lines total) — One file per category

assets/css/styles.css (1,461 lines)
output/               (334 generated pages)
```

**Data flow during build:**
1. `build.py` registers 90 tools via `T()` into `TOOLS` dict
2. `content/__init__.py` lazy-loads all `TOOL_CONTENT` dicts from 9 category files
3. `build_tool_pages()` calls `get_tool_content(slug)` to merge T() data with deep content
4. 16 `build_*()` functions generate HTML into `output/`

## Recommended Audit Architecture

The audit system is a standalone Python script that imports the same data structures build.py uses, runs checks, and produces a report. It does NOT modify any content. It reads and reports.

```
scripts/
  audit.py              — Main entry point. Orchestrates all checkers, produces report.
  audit/
    __init__.py
    writing_checks.py   — Writing guideline violations (false reframes, em-dashes, banned words)
    structure_checks.py  — Content schema completeness (all sections present, min lengths)
    data_checks.py       — Niche/industry data consistency (winners differ, all categories covered)
    seo_checks.py        — SEO elements (meta desc length, title patterns, schema markup)
    report.py            — Formats findings into terminal output and optional HTML report
```

### Component Boundaries

| Component | Responsibility | Reads From | Outputs |
|-----------|---------------|------------|---------|
| `audit.py` | Orchestrator. Loads data, runs each checker, collects findings. | `build.py` (TOOLS, CATEGORIES, NICHES, INDUSTRIES), `content/` | Passes data to checkers, collects results, passes to reporter |
| `writing_checks.py` | Scans all string content for writing guideline violations | Content dicts from `content/*.py` | List of `Finding(tool, section, rule, snippet, severity)` |
| `structure_checks.py` | Verifies every tool has all required content sections at minimum length | `TOOLS` dict + content dicts | List of `Finding(tool, section, issue, severity)` |
| `data_checks.py` | Cross-references niche winners vs Sultan's Picks, industry category coverage | `TOOLS`, `NICHES`, `INDUSTRIES`, `CATEGORIES` | List of `Finding(entity, issue, severity)` |
| `seo_checks.py` | Validates generated HTML files for SEO completeness | Files in `output/` | List of `Finding(page, issue, severity)` |
| `report.py` | Formats findings into readable output | List of all Findings | Terminal summary + optional `audit-report.html` |

### Data Flow

```
                    build.py data
                    (TOOLS, CATEGORIES, NICHES, INDUSTRIES)
                         |
                    content/*.py data
                    (TOOL_CONTENT dicts)
                         |
                    +----+----+
                    |         |
               audit.py loads both
                    |
        +-----------+-----------+-----------+
        |           |           |           |
   writing_    structure_   data_       seo_
   checks      checks      checks      checks
        |           |           |           |
        +-----+-----+-----+----+
              |
         List[Finding]
              |
         report.py
              |
    +---------+---------+
    |                   |
  Terminal           audit-report.html
  (summary)          (detailed, browsable)
```

**Key design decision:** The audit imports data from `build.py` and `content/` directly via Python imports, NOT by parsing generated HTML (except for SEO checks). This means:
- Writing and structure checks run against source data (the Python dicts), which is faster, more reliable, and catches issues before they reach HTML.
- SEO checks run against output HTML, because that is what search engines see.
- The audit can run before or after `build.py`. If run before, SEO checks are skipped. If run after, all checks run.

## Component Details

### 1. Finding Data Class

Every checker returns the same structure:

```python
@dataclass
class Finding:
    severity: str       # "error" | "warning" | "info"
    category: str       # "writing" | "structure" | "data" | "seo"
    entity: str         # Tool slug, niche slug, page path
    section: str        # "overview", "expanded_pros", etc.
    rule: str           # Short rule name ("false_reframe", "missing_section")
    message: str        # Human-readable description
    snippet: str = ""   # Offending text excerpt (first 120 chars)
```

### 2. Writing Checks (`writing_checks.py`)

Scans every string value in every tool's content dict. Rules implemented as regex patterns or string searches:

| Rule | Detection Method | Severity |
|------|-----------------|----------|
| False reframe | Regex: `not\s+\w+[,.]?\s+it'?s`, `isn't\s+\w+\.\s+It's`, `less about.*more about` | error |
| Em-dash | String search: `\u2014` (the unicode em-dash character) | error |
| Banned words | Case-insensitive search for each word in banned list (robust, leverage, synergy, holistic, cutting-edge, seamless, frictionless, end-to-end, genuinely, truly, really, actually, game-changer, paradigm shift, best-in-class) | error |
| Unearned declarations | Regex: `The pattern here is clear`, `Here's the thing`, `The bottom line:` | warning |
| Commentary after stats | Regex: `Let that sink in`, `You read that right`, `That's impressive` | warning |
| Forced casual | Regex: `Spoiler alert`, `Plot twist`, `Here's the kicker`, `Let's dive in` | warning |
| Tautologies | String search: `Time will tell`, `Success depends on execution` | warning |
| Missing contractions | Regex: `\bit is\b`, `\bdo not\b`, `\bcannot\b`, `\bwill not\b`, `\bdoes not\b` (context-aware, skip when used for emphasis) | warning |

**Implementation:** Iterate all content files, extract every string value (recursively walk dicts and lists), apply each rule. Return `List[Finding]`.

### 3. Structure Checks (`structure_checks.py`)

Verifies completeness of the content schema for all 90 tools:

| Check | Rule | Severity |
|-------|------|----------|
| Required sections present | overview, expanded_pros, expanded_cons, pricing_detail, who_should_buy, who_should_skip, stage_guidance, alternatives_detail, verdict_long, faqs | error if missing |
| Minimum pros/cons | At least 3 expanded_pros and 3 expanded_cons | error |
| Pros/cons have detail | Each pro/con has both `title` and `detail` keys with content | error |
| Stage guidance complete | All 4 stages present: solo, small_team, mid_market, enterprise | warning |
| FAQ count | At least 5 FAQs | warning |
| FAQ structure | Each FAQ has both `question` and `answer` keys | error |
| Who should buy/skip count | At least 2 entries each | warning |
| Alternatives count | At least 3 alternatives_detail entries | warning |
| Word count range | Total content 2,000-4,000 words (configurable) | warning if outside |

**Implementation:** For each tool slug in `TOOLS`, call `get_tool_content(slug)`. If `None`, report error (no deep content). Otherwise validate each field.

### 4. Data Checks (`data_checks.py`)

Cross-references structural data in build.py:

| Check | Rule | Severity |
|-------|------|----------|
| Niche winner differs from Sultan's Pick | For each niche + category combo, rank[0] must not be the Sultan's Pick tool | error |
| Industry coverage | Each industry has picks for all 9 categories | error if missing |
| Industry tools exist | Every tool slug referenced in INDUSTRIES exists in TOOLS | error |
| Niche tools exist | Every tool slug referenced in NICHES rankings exists in TOOLS | error |
| Niche applies_to valid | Every category in applies_to exists in CATEGORIES | error |
| No duplicate rankings | No tool appears twice in the same niche ranking list | warning |

**Implementation:** Import TOOLS, CATEGORIES, NICHES, INDUSTRIES from build.py. Cross-reference dictionaries. Pure data validation, no string scanning.

### 5. SEO Checks (`seo_checks.py`)

Parses generated HTML files in `output/`:

| Check | Rule | Severity |
|-------|------|----------|
| Title tag present and non-empty | Every HTML file has `<title>` | error |
| Meta description present | Every HTML file has `<meta name="description">` | error |
| Meta description length | Between 120-160 characters | warning |
| H1 tag present | Exactly one `<h1>` per page | warning |
| Canonical URL present | `<link rel="canonical">` exists | warning |
| Schema markup present | At least one `<script type="application/ld+json">` | info |
| No broken internal links | All `href="/..."` paths resolve to existing files | error |

**Implementation:** Use Python's `html.parser` (stdlib) to parse HTML. No external dependencies. Walk `output/` directory recursively.

### 6. Report (`report.py`)

Two output modes:

**Terminal (default):** Summary table with counts by severity and category, then grouped findings. Errors first, then warnings.

```
AUDIT RESULTS: 334 pages, 90 tools
================================================
Errors:   12  (7 writing, 3 structure, 2 data)
Warnings: 28  (15 writing, 8 structure, 5 seo)
Info:      4

ERRORS
------
[writing] hubspot / overview: False reframe detected
  "...not a CRM, it's a platform..."

[structure] persana-ai: Missing section "faqs"
...
```

**HTML report (`--html`):** Browsable single-file HTML report with the same data, filterable by severity/category/tool. Written to `audit-report.html` (gitignored, not deployed).

## Patterns to Follow

### Pattern 1: Import, Don't Parse
**What:** Import `TOOLS`, `CATEGORIES`, `NICHES`, `INDUSTRIES` directly from `build.py` and content dicts from `content/`. Do not parse Python files as text.
**Why:** The data is already structured in Python dicts. Parsing text is fragile and misses context. Direct import is faster and catches type errors.
**How:**
```python
# In audit.py
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from build import TOOLS, CATEGORIES, NICHES, INDUSTRIES
from content import get_tool_content
```

### Pattern 2: Recursive String Extraction
**What:** For writing checks, recursively walk any nested dict/list structure and yield all string values with their path.
**Why:** Content dicts have varied nesting (lists of strings, lists of dicts with string values, plain strings, dicts of strings). A recursive walker handles all cases without special-casing each section.
```python
def extract_strings(obj, path=""):
    """Yield (path, text) for all string values in nested structure."""
    if isinstance(obj, str):
        yield (path, obj)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            yield from extract_strings(item, f"{path}[{i}]")
    elif isinstance(obj, dict):
        for key, val in obj.items():
            yield from extract_strings(val, f"{path}.{key}" if path else key)
```

### Pattern 3: Rule Registry
**What:** Each writing rule is a function or data tuple. Rules are registered in a list, not hardcoded in a loop.
**Why:** Makes adding/removing rules trivial. Each rule is independently testable.
```python
RULES = [
    Rule("false_reframe", "error", r"(?i)\bnot\s+\w+[,.]?\s*it'?s\b", "False reframe detected"),
    Rule("em_dash", "error", "\u2014", "Em-dash found (use period, comma, or colon)"),
    # ... all banned words, forced casual, etc.
]
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Parsing Content Files as Raw Text for Schema Validation
**What:** Using regex on `.py` source files to find content strings.
**Why bad:** Python source includes comments, variable names, function defs, and string delimiters. You get false positives on comments and miss multi-line strings. The data is already loaded into clean dicts at runtime.
**Instead:** Import the modules and work with the data structures.

### Anti-Pattern 2: Auto-Fixing Content
**What:** Having the audit script replace em-dashes, rewrite false reframes, or otherwise modify content.
**Why bad:** Content is hand-written editorial copy. Auto-fixes corrupt voice, introduce new AI artifacts, and bypass human judgment. The whole point of the quality audit is to surface issues for human review.
**Instead:** Report only. Fix manually or in a separate, explicitly invoked step.

### Anti-Pattern 3: Over-Engineering (Plugin System, Config Files, etc.)
**What:** Building a reusable testing framework with YAML config, plugin loading, or abstract base classes.
**Why bad:** This audit runs against one site with one content schema. The rules are defined in PROJECT.md and won't change weekly. A clear, readable Python script is the right level of abstraction.
**Instead:** Simple Python module per concern. Add rules by editing a list.

### Anti-Pattern 4: Running SEO Checks Without Build Output
**What:** Running `audit.py` and having SEO checks fail because `output/` is empty or stale.
**Why bad:** Confusing errors that mix real content issues with stale-build artifacts.
**Instead:** Detect whether `output/` exists and has recent files. If stale or missing, skip SEO checks with an info-level message: "SEO checks skipped: run build.py first."

## Suggested Build Order (Dependencies)

```
Phase 1: Finding dataclass + report.py
    No dependencies. Define the output format first.
    Everything else produces Findings; report.py consumes them.

Phase 2: writing_checks.py
    Depends on: Finding, content/ imports
    Highest value. Catches the most user-visible quality issues.
    The banned patterns list is already defined in PROJECT.md.

Phase 3: structure_checks.py
    Depends on: Finding, content/ imports, TOOLS import
    Second highest value. Catches missing sections before
    you browse 90 pages manually.

Phase 4: data_checks.py
    Depends on: Finding, build.py imports (TOOLS, NICHES, INDUSTRIES, CATEGORIES)
    Cross-reference checks are simple dict lookups.

Phase 5: seo_checks.py
    Depends on: Finding, output/ directory (requires build.py to have run)
    Lower priority because build.py templates are consistent.
    Only catches issues if template logic has bugs.

Phase 6: audit.py orchestrator + CLI
    Depends on: All checkers + report.py
    Wire everything together. Add argparse for filtering
    (--severity, --category, --tool, --html).
```

**Why this order:**
- Phase 1 establishes the contract (Finding + report) that all checkers implement against. Build this first so you can test each checker in isolation with visible output.
- Phases 2-3 are the core value. Writing violations and missing sections are the quality issues that prompted this audit. Ship these first, run them, fix content, then add the rest.
- Phases 4-5 are validation layers. They catch real bugs but are less likely to surface new issues.
- Phase 6 is the CLI wrapper. Until then, each checker can be run standalone for testing.

**Implication for roadmap:** Phases 1-3 can be a single milestone (the audit script that catches content quality issues). Phases 4-6 are a second pass that adds completeness. The biggest value is in writing + structure checks.

## Scalability Considerations

| Concern | Current (90 tools, 334 pages) | At 200 tools, 800 pages | At 500 tools, 2000 pages |
|---------|-------------------------------|------------------------|--------------------------|
| Audit runtime | Under 2 seconds | Under 5 seconds | Under 15 seconds |
| Memory | Trivial (~50MB) | Trivial (~100MB) | Still trivial (~200MB) |
| Report readability | Simple list | Filter by category/tool | Needs search/filter in HTML report |
| Maintainability | 9 content files | ~20 content files | Consider splitting by subcategory |

This is a static site with Python dicts. Performance is not a concern at any realistic scale. The bottleneck is human review time, which the report's filtering and severity levels address.

## Sources

- Direct codebase analysis of `/Users/rome/Documents/projects/sultanofsaas/scripts/`
- Content schema from `scripts/content/__init__.py`
- Writing guidelines from `.planning/PROJECT.md` (lines 61-101)
- Build function inventory from `scripts/build.py` (16 `build_*()` functions)
