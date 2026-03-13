# Feature Landscape: SaaS Review Site Quality Audit

**Domain:** Content quality verification for a 334-page static SaaS review site
**Researched:** 2026-03-13

## Table Stakes

Features that must work or the audit is incomplete. Missing any of these means content ships with known defects.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Writing rules scanner | The site has 15+ explicit writing rules (false reframes, em-dashes, banned words, forced casual, tautologies). Manual checking across 7,655 lines of content is error-prone. | Medium | Regex-based pattern matching across all 9 content files. Each rule maps to a specific regex or string match. |
| Content completeness checker | Every tool (90 total) needs all 9 sections filled: overview, expanded_pros, expanded_cons, pricing_detail, who_should_buy, who_should_skip, stage_guidance, alternatives_detail, verdict_long, faqs. Missing sections = thin review page. | Low | Parse each TOOL_CONTENT dict, check for missing or empty keys against the schema in `__init__.py`. |
| Word count validator | Reviews target 2,000-4,000 words. Under 2,000 = too thin. Over 4,000 = padding. Both violate the spec. | Low | Sum text across all sections per tool. Flag outliers. |
| Niche winner uniqueness check | Each niche page must pick a different winner than the Sultan's Pick for that category. Same winner = the niche page adds no editorial value. | Low | Compare `rankings[cat][0]` against the `sultans_pick=True` tool per category across all 64 niche pages. Data is in build.py. |
| Industry completeness check | All 17 industries must have picks for all 9 categories. Missing picks = broken page layout or empty sections. | Low | Iterate INDUSTRIES dict, verify each has a `picks` entry for every key in CATEGORIES. |
| SEO meta validation | Every page needs title tag, meta description, canonical URL, and appropriate schema markup (BreadcrumbList, FAQPage, Product). Missing = invisible to search. | Medium | Run against the 334 generated HTML files in `output/`. Check for required meta tags and valid JSON-LD. |
| Internal link integrity | All internal links must resolve to actual generated pages. Broken links = dead ends and wasted crawl budget. | Medium | Extract all `<a href>` from generated HTML, verify each internal path maps to a file in `output/`. |
| Build success verification | `python3 scripts/build.py` must complete without errors and produce exactly 334 pages. | Low | Run the build, count output files, capture any warnings or errors. |

## Differentiators

Features that elevate audit quality beyond "did it break?" into "is it good?"

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Prose quality scoring | Detect AI writing patterns beyond the explicit banned list: repetitive sentence structures, formulaic transitions, paragraphs that all start the same way. The site's brand depends on sounding human. | High | Harder to automate. Semi-manual review of a sample (e.g., 10 tools across categories) for patterns not caught by regex. |
| Pricing accuracy spot-check | Verify pricing numbers against actual vendor websites. Wrong pricing numbers destroy credibility for a review site. | High | Manual or semi-automated (WebFetch against vendor pricing pages). High value but time-intensive. Sample 10-15 tools. |
| Cross-page consistency check | Same tool should have consistent pricing, scores, and verdict across its review page, comparison pages, alternatives pages, pricing page, niche pages, and industry pages. Data comes from one source (T() function) but content files add detail that could contradict. | Medium | Compare pricing_detail text in content files against pricing_start/pricing_tiers in T() data. Flag contradictions. |
| Sentence length variance analysis | The writing guidelines demand "4-word punches mixed with 25-word explanations." Measure actual sentence length distribution per review. Flag reviews that are monotonously mid-length. | Medium | Split content on sentence boundaries, compute length stats (mean, std dev, min, max). Flag low-variance reviews. |
| Contraction compliance | Guidelines say "contractions always." Scan for uncontracted forms: "it is," "do not," "you will," "they are," etc. | Low | Simple regex for common uncontracted pairs. Low effort, catches a common AI writing tell. |
| FAQ search query relevance | FAQs should target real search queries, not generic filler. Verify FAQ questions match patterns people actually search. | Medium | Cross-reference FAQ questions against keyword patterns (e.g., "how much does X cost," "is X worth it," "X vs Y"). Flag overly generic questions. |
| Visual rendering spot-check | Verify CSS renders correctly: verdict badges, score colors, price tier tags, comparison tables, responsive layout. | Medium | Open 5-10 representative pages in browser, check key visual elements. Automated screenshot testing is overkill for a one-time audit. |
| Schema markup validation | Beyond existence, validate that JSON-LD is actually valid (parseable, correct types, no missing required fields). | Low | Parse JSON-LD blocks, validate against schema.org specs. Can use a JSON parser. |

## Anti-Features

Things to deliberately NOT build for this audit.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Automated rewriting/fix tool | The audit should identify problems, not auto-fix them. Auto-fixes introduce new AI writing artifacts and bypass editorial judgment. | Report issues with file, line number, and the offending text. Human fixes each one. |
| Comprehensive pricing verification for all 90 tools | Checking every vendor's current pricing is 4+ hours of manual work and pricing changes constantly. Diminishing returns past a sample. | Spot-check 10-15 tools across categories. Flag any that look stale or suspiciously round. |
| Automated Lighthouse/PageSpeed audit | Performance optimization is a separate concern. The audit is about content quality, not page load time. | Note any obvious performance issues (massive inline CSS, missing image optimization) but don't run full performance audits. |
| Grammar/spell check tooling | The content was generated by Claude. Grammar errors are rare. The real risk is AI writing patterns (which grammar tools don't catch), not typos. | Read-through of sample reviews catches more real issues than automated grammar checking. |
| Comparison page winner re-evaluation | Auditing whether the "right" tool wins each comparison is editorial judgment that requires deep domain knowledge per category. Out of scope for a quality audit. | Verify winners are declared (not missing), consistent with scores, and have reasoning. Don't second-guess the editorial picks. |
| Mobile responsive testing suite | Setting up device emulation or BrowserStack for a pre-deploy audit is overhead. The CSS framework (tokens.css + components.css) handles responsive. | Quick manual check at 375px width in Chrome DevTools on 3-4 page types. |

## Feature Dependencies

```
Build success verification
  -> SEO meta validation (needs output/ files)
  -> Internal link integrity (needs output/ files)
  -> Visual rendering spot-check (needs output/ files)

Content completeness checker
  -> Word count validator (needs the same content parsing)
  -> Prose quality scoring (needs content text extracted)
  -> Sentence length variance analysis (needs content text extracted)
  -> Contraction compliance (needs content text extracted)

Writing rules scanner (independent -- runs on source .py files)

Niche winner uniqueness check (independent -- runs on build.py data)

Industry completeness check (independent -- runs on build.py data)

Cross-page consistency check
  -> requires both T() data (build.py) and content file data (scripts/content/*.py)
```

## MVP Recommendation (Audit Checklist Priority)

**Must complete before deploy:**

1. **Build success verification** -- 5 minutes, gates everything else
2. **Writing rules scanner** -- the ZERO TOLERANCE rules (false reframes, em-dashes, banned words). Highest risk of shipping embarrassing content. Run regex across all 9 content files.
3. **Content completeness checker** -- verify all 90 tools have all 9 sections populated. Missing sections = visibly broken pages.
4. **Word count validator** -- flag any reviews under 2,000 or over 4,000 words
5. **Niche winner uniqueness check** -- every niche's #1 must differ from Sultan's Pick. Data-only check, fast.
6. **Industry completeness check** -- all 17 industries need picks for all 9 categories. Data-only check, fast.
7. **Internal link integrity** -- no broken links
8. **SEO meta validation** -- titles, descriptions, canonical URLs, schema on every page

**Should complete before deploy:**

9. **Contraction compliance** -- quick regex pass, catches an obvious AI tell
10. **Cross-page consistency check** -- pricing numbers in content files should match T() data
11. **Visual rendering spot-check** -- open 5-10 pages, verify CSS

**Defer (do after initial deploy if time permits):**

12. Sentence length variance analysis
13. FAQ search query relevance
14. Pricing accuracy spot-check (sample 10 tools)
15. Prose quality scoring (sample review of 10 tools)

## Complexity Budget

| Priority | Feature Count | Estimated Effort |
|----------|--------------|-----------------|
| Must complete | 8 features | 2-3 hours (most are scriptable) |
| Should complete | 3 features | 1-2 hours |
| Defer | 4 features | 3-4 hours (includes manual review) |
| **Total** | **15 features** | **6-9 hours** |

The "must complete" features are mostly automatable with a Python audit script that parses the content files and scans the output directory. The biggest time sink is fixing whatever the scanner finds, not running the scanner itself.

## Sources

- Project context from `.planning/PROJECT.md` (writing guidelines, content schema, quality checklist)
- Content file structure from `scripts/content/__init__.py` (schema definition)
- Data structures from `scripts/build.py` (NICHES, INDUSTRIES, CATEGORIES, T() function)
- Existing content files: 9 category files, 7,655 total lines across 90 tools
