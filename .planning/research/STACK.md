# Technology Stack: SultanOfSaaS Quality Audit

**Project:** SultanOfSaaS content quality audit and expansion
**Researched:** 2026-03-13
**Mode:** Ecosystem research for content auditing at scale

## The Core Problem

SultanOfSaaS has 90 tool reviews across 9 Python content files (~7,750 lines). The content lives in Python dicts (strings inside `TOOL_CONTENT["tool_name"]` structures), not in markdown or HTML files. This shapes the entire tool selection: traditional prose linters like Vale expect markup files on disk. Here, the audit tool must parse Python source, extract string values, then analyze them.

The right approach is a **custom Python audit script** that imports the content modules, iterates every tool's content dict, and runs checks. External tools like Vale add complexity without matching the data format.

## Recommended Stack

### Primary: Custom Python Audit Script (no external deps for core checks)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python `re` (stdlib) | 3.11+ | Pattern matching for banned words, false reframes, em-dashes | All writing rules are pattern-matchable. No dependency needed. The content is already in Python dicts, so `re` operates directly on extracted strings. |
| Python `ast` (stdlib) | 3.11+ | Parse Python content files to extract string literals | Can validate structure (every tool has all 9 required sections) without importing the modules. Alternative to direct import. |
| `html.parser` (stdlib) | 3.11+ | Parse generated HTML for SEO checks | Handles meta tags, heading structure, link validation without external deps. |
| `json` (stdlib) | 3.11+ | Validate JSON-LD schema markup in generated pages | Parse and check structured data blocks. |

**Confidence: HIGH** -- stdlib, zero dependencies, matches the data format exactly.

### Secondary: Readability and Sentence Analysis

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| textstat | 0.7.13 | Flesch-Kincaid readability, sentence count, word count per section | Lightweight (no ML models), gives readability grade and word count per section. Validates the 2,000-4,000 word target and catches overly complex prose. Released Feb 2026, actively maintained. |

**Confidence: HIGH** -- textstat 0.7.13 released Feb 2026, pure Python, no heavy dependencies.

Use textstat only if readability scoring is wanted beyond word/sentence counts. The stdlib `re` + `split()` handles word counting and basic sentence detection fine for the structural checks. textstat adds value for Flesch-Kincaid grade and reading ease scores, which help catch dense or dumbed-down prose.

### Optional: HTML Auditing at Scale

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| beautifulsoup4 | 4.12+ | Parse generated HTML pages for deeper SEO audit | More ergonomic API than stdlib `html.parser` for complex queries (find all H1s, check heading hierarchy, extract all internal links). Worth it if the SEO audit grows beyond basic meta tag checks. |
| lxml | 5.x | HTML parser backend for BS4 | Faster than html.parser for 334 pages. |

**Confidence: HIGH** -- BS4 is the standard Python HTML parser.

For the initial audit, stdlib `html.parser` is sufficient. Add BS4 only if the SEO checks become complex enough to justify it (e.g., crawling all 334 pages for cross-page duplicate detection, link graph analysis).

### Not Recommended

| Technology | Why Not |
|------------|---------|
| **Vale** (v3.14.0) | Designed for markdown/RST/HTML files on disk. SultanOfSaaS content is Python strings in dicts. You'd have to export every string to temp files, run Vale, then parse results back. Adds a Go binary dependency and file I/O overhead for something regex handles directly. Vale is excellent for docs-as-code teams writing markdown; it's the wrong tool when content lives in Python source. |
| **proselint** | Effectively unmaintained. Vale absorbed its rules. Same file-format mismatch problem. |
| **textlint** | Node.js ecosystem. Adds npm dependency chain to a pure-Python project. Same file-format problem as Vale. |
| **spaCy** (v3.8) | 500MB+ model download for sentence segmentation that textstat handles in 50KB. Overkill for word/sentence counting and readability scoring. Would be justified if doing NER or semantic analysis, but writing quality checks are pattern-based. |
| **Grammarly API / LanguageTool API** | External API dependency for a build-time audit. Adds network latency, rate limits, and cost. The writing rules are specific and codified (banned words list, false reframe patterns) -- regex catches them faster and offline. |
| **pylint / ruff / flake8** | These lint Python code quality, not prose quality inside strings. |
| **pytest** | Overhead for a one-pass audit. Plain assertions with a summary report and exit codes are cleaner. The audit is a single linear scan, not a test suite with fixtures and parametrization. |
| **Selenium / Playwright** | Visual spot-check is faster done manually in a browser. The audit checks structure, not rendering. |
| **Screaming Frog / Sitebulb** | External GUI tools, not scriptable into the build pipeline. |

## Audit Architecture

The audit is a single Python script (`scripts/audit.py`) that:

1. **Imports** each `scripts/content/tools_*.py` module
2. **Iterates** `TOOL_CONTENT` dicts
3. **Runs checks** on each string value
4. **Optionally** scans `output/` HTML after build

### Check Categories

#### Writing Rules (regex, stdlib only)

| Check | Pattern | Severity |
|-------|---------|----------|
| False reframes | `not\s+\w+[,.]?\s+(it's\|it is)`, `isn't\s+\w+\.\s+It's`, `less about\s+.+more about` | ERROR |
| Em-dashes | `\u2014` (Unicode em-dash) | ERROR |
| Banned words | `\b(robust\|leverage\|synergy\|holistic\|cutting-edge\|seamless\|frictionless\|end-to-end\|genuinely\|truly\|really\|actually\|game-changer\|paradigm shift\|best-in-class)\b` | ERROR |
| Unearned declarations | `The pattern here is clear`, `Here's the thing`, `The bottom line` | WARNING |
| Commentary after stats | `Let that sink in`, `You read that right`, `That's impressive` | WARNING |
| Forced casual | `Spoiler alert`, `Plot twist`, `Here's the kicker`, `Let's dive in` | WARNING |
| Tautologies | `Time will tell`, `Success depends on execution` | WARNING |
| Missing contractions | `it is`, `do not`, `can not`, `will not`, `does not` (context-aware) | WARNING |

#### Content Structure (dict key validation)

| Check | Rule | Severity |
|-------|------|----------|
| Required sections present | All 9 schema keys exist per tool | ERROR |
| Overview length | 300-500 words (3 paragraphs) | WARNING |
| Expanded pros count | >= 3 items | ERROR |
| Expanded cons count | >= 3 items | ERROR |
| FAQ count | 5-7 items | WARNING |
| Total word count | 2,000-4,000 words across all sections | WARNING |
| Pricing specificity | Contains `$` character (actual dollar amounts) | WARNING |

#### Readability (textstat, optional)

| Check | Rule | Severity |
|-------|------|----------|
| Flesch-Kincaid grade | Target 8-12 (readable but not dumbed down) | INFO |
| Sentence length variance | Std dev > 5 words (catches monotonous rhythm) | INFO |
| Average sentence length | 12-22 words | INFO |

#### SEO on Generated HTML (html.parser or BS4)

| Check | Rule | Severity |
|-------|------|----------|
| Title tag length | 30-60 characters | WARNING |
| Meta description length | 120-160 characters | WARNING |
| H1 count | Exactly 1 per page | ERROR |
| Heading hierarchy | No skipped levels (H1 -> H3 without H2) | WARNING |
| Internal link validity | All internal hrefs resolve to files in `output/` | ERROR |
| Duplicate titles | No two pages share the same `<title>` | WARNING |
| Duplicate meta descriptions | No two pages share the same meta description | WARNING |

#### Structural Consistency (build data checks)

| Check | Rule | Severity |
|-------|------|----------|
| Niche winners differ | Every niche page picks a different winner than Sultan's Pick | ERROR |
| Industry coverage | All 17 industry pages have picks for all 9 categories | ERROR |
| Cross-reference | Tools in alternatives_detail exist in the tool registry | WARNING |

## Installation

```bash
# Core audit (stdlib only, no install needed)
python3 scripts/audit.py

# If readability scoring is wanted
pip install textstat==0.7.13

# If HTML audit grows beyond basic checks
pip install beautifulsoup4 lxml
```

Total new dependencies: 0-3 packages. No Node.js, no Go binaries, no ML models.

## Script Interface

```bash
# Run all checks on all content
python3 scripts/audit.py

# Run only writing checks
python3 scripts/audit.py --check writing

# Run only structural checks
python3 scripts/audit.py --check structure

# Run only on one category
python3 scripts/audit.py --category crm

# Run SEO checks on generated HTML (requires build first)
python3 scripts/audit.py --check seo

# Output as JSON (for reporting)
python3 scripts/audit.py --format json

# Exit code: 0 = pass, 1 = errors found
```

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Prose linting | Custom regex script | Vale v3.14 | Content is in Python dicts, not markup files. |
| Readability | textstat 0.7.13 | spaCy 3.8 | 500MB model vs 50KB library for sentence stats. |
| HTML auditing | html.parser (stdlib) | beautifulsoup4 | Stdlib sufficient for initial checks. Upgrade path exists. |
| Sentence analysis | textstat | Custom NLTK tokenizer | textstat wraps NLTK tokenization already. |
| Full SEO audit | Custom script on local files | Screaming Frog | Not scriptable into build pipeline. |

## Sources

- [Vale GitHub releases -- v3.14.0, Mar 2026](https://github.com/errata-ai/vale/releases) -- HIGH confidence
- [textstat PyPI -- v0.7.13, Feb 2026](https://pypi.org/project/textstat/) -- HIGH confidence
- [Vale vs proselint comparison](https://weesholapara.medium.com/to-proselint-or-to-vale-60ce731abd0e) -- MEDIUM confidence
- [Meilisearch: Prose linting with Vale](https://www.meilisearch.com/blog/prose-linting-with-vale) -- MEDIUM confidence
- [Python re module docs](https://docs.python.org/3/library/re.html) -- HIGH confidence
- [Grafana: Vale prose linter usage](https://grafana.com/docs/writers-toolkit/review/lint-prose/) -- MEDIUM confidence
- [textstat GitHub](https://github.com/textstat/textstat) -- HIGH confidence
