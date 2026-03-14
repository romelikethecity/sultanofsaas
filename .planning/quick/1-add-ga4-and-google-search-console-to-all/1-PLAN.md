---
phase: quick
plan: 1
type: execute
wave: 1
depends_on: []
files_modified:
  - scripts/templates.py
autonomous: true
requirements: [ANALYTICS-01, ANALYTICS-02]
must_haves:
  truths:
    - "Every page includes the GA4 gtag.js snippet with measurement ID G-0SBNZZYM4Y"
    - "Every page includes the Google Search Console verification meta tag"
    - "Build still produces 334 pages with 0 audit errors"
  artifacts:
    - path: "scripts/templates.py"
      provides: "GA4 and GSC tags in shared head template"
      contains: "G-0SBNZZYM4Y"
  key_links:
    - from: "scripts/templates.py"
      to: "all 334 output pages"
      via: "get_html_head() called by get_page_wrapper()"
      pattern: "gtag.*G-0SBNZZYM4Y"
---

<objective>
Add GA4 tracking (G-0SBNZZYM4Y) and Google Search Console verification to all 334 pages of sultanofsaas.com.

Purpose: Enable traffic analytics and search indexing for the live site.
Output: Updated templates.py, rebuilt output/, deployed to gh-pages.
</objective>

<execution_context>
@/Users/rome/.claude/get-shit-done/workflows/execute-plan.md
@/Users/rome/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@scripts/templates.py — The `get_html_head()` function (line 63) generates the `<head>` section for ALL pages. GA4 and GSC tags go here, before the closing `</head>` tag (line 104). The function accepts an `extra_head` parameter but the tags should be baked into the base template, not passed per-page.

<interfaces>
From scripts/templates.py:
```python
def get_html_head(title, description, canonical_path, extra_head=""):
    """Generate complete <head> section."""
    # Returns <!DOCTYPE html><html><head>...</head> string
    # extra_head is injected just before </head> (line 103)
    # GA4 + GSC tags should go AFTER the CSS links, BEFORE {extra_head}
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add GA4 and GSC tags to head template</name>
  <files>scripts/templates.py</files>
  <action>
In `get_html_head()` (line 63 of scripts/templates.py), add two blocks between the CSS link (line 102) and the `{extra_head}` injection (line 103):

1. Google Search Console verification meta tag:
```html
    <!-- Google Search Console -->
    <meta name="google-site-verification" content="PLACEHOLDER">
```
NOTE: The actual verification content value must come from Google Search Console. Add PLACEHOLDER for now — the user will provide the real value after verifying ownership. If the user has already provided it in context, use that instead.

2. GA4 gtag.js snippet:
```html
    <!-- Google Analytics (GA4) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-0SBNZZYM4Y"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-0SBNZZYM4Y');
    </script>
```
IMPORTANT: The curly braces in the JS function body must be doubled (`{{` and `}}`) because this is inside an f-string. The gtag config and dataLayer references use standard JS syntax — only the braces need escaping.

Do NOT modify any other part of templates.py.
  </action>
  <verify>
    <automated>cd /Users/rome/Documents/projects/sultanofsaas && python3 -c "from scripts.templates import get_html_head; h = get_html_head('Test', 'desc', '/test'); assert 'G-0SBNZZYM4Y' in h; assert 'gtag' in h; assert 'google-site-verification' in h; print('OK: GA4 and GSC tags present in head output')"</automated>
  </verify>
  <done>get_html_head() output contains GA4 gtag.js snippet with G-0SBNZZYM4Y and Google Search Console meta tag</done>
</task>

<task type="auto">
  <name>Task 2: Rebuild site and verify tags in output</name>
  <files>output/</files>
  <action>
1. Run `python3 scripts/build.py` to rebuild all 334 pages.
2. Run `python3 scripts/audit.py` to confirm 0 errors still.
3. Spot-check 3 output files (index.html, a tool page, a niche page) to confirm the GA4 script tag and GSC meta tag appear in each.
4. Deploy: push output/ to gh-pages branch using the existing deployment method (orphan gh-pages branch pattern from Phase 03).
  </action>
  <verify>
    <automated>cd /Users/rome/Documents/projects/sultanofsaas && python3 scripts/build.py 2>&1 | tail -5 && python3 scripts/audit.py 2>&1 | grep -E "errors|PASS" && grep -l "G-0SBNZZYM4Y" output/index.html output/tools/hubspot-sales-hub/index.html output/niches/ai-powered-sales-tools/index.html | wc -l | xargs -I{} test {} -eq 3 && echo "OK: 3/3 pages verified"</automated>
  </verify>
  <done>334 pages rebuilt with GA4+GSC tags, 0 audit errors, deployed to gh-pages</done>
</task>

</tasks>

<verification>
- All 334 output pages contain `G-0SBNZZYM4Y` in their head section
- Audit passes with 0 errors
- Site is deployed and live at sultanofsaas.com with tracking active
</verification>

<success_criteria>
- GA4 tag fires on every page load (verify in GA4 Realtime after deploy)
- Google Search Console can verify site ownership via meta tag
- Build produces same 334 pages, 0 errors
</success_criteria>

<output>
After completion, create `.planning/quick/1-add-ga4-and-google-search-console-to-all/1-SUMMARY.md`
</output>
