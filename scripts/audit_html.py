#!/usr/bin/env python3
"""
Comprehensive site-wide HTML audit for SultanOfSaaS.

Audits every rendered page in output/ against:
  1. WRITING_GUIDE.md hard-banned phrases (zero tolerance)
  2. marketingskills/ai-writing-detection.md AI tells
  3. SEO checks: title/meta length, single H1, internal links, schema
  4. Content depth: word count thresholds by page type
  5. Structural checks: nav/footer/breadcrumbs presence

Run: python3 scripts/audit_html.py [--strict]

Severities:
  ERROR    - Hard violations of writing/SEO rules. Must fix.
  WARN     - Soft AI-tell or borderline issue. Review.
  INFO     - Metric for tracking only.
"""

import os
import re
import sys
import glob
import html
import json
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT = os.path.join(ROOT, "output")

# Treat these page paths as nav-hub pages (looser word count threshold)
HUB_PAGES = {"about", "stacks", "best", "for", "guides", "tools"}

# ---------- BANNED PHRASES (ERROR severity) ----------
# WRITING_GUIDE.md zero-tolerance list + marketingskills overlap
HARD_BANNED = [
    "robust", "leverage", "synergy", "holistic", "cutting-edge",
    "game-changer", "best-in-class", "world-class", "frictionless",
    "end-to-end", "paradigm shift", "navigate the landscape",
    "in today's market", "spoiler alert", "without further ado",
    # marketingskills additions
    "delve into", "delving into", "shed light on", "pave the way",
    "in the realm of", "in the landscape of", "in an era of",
    "in the ever-evolving",
]

# Phrases that should not appear ANYWHERE
HARD_BANNED_PHRASES = [
    "in today's fast-paced", "in today's digital age",
    "let's dive in", "let's delve",
    "here's the thing", "the kicker",
    "at the end of the day", "it's worth noting that",
    "when it comes to", "imagine a world where",
    "with that in mind", "at its core",
    "to put it simply", "in essence",
    "this begs the question",
    "in conclusion", "to sum up",
    "in the final analysis", "all things considered",
    "let that sink in", "you read that right",
]

# ---------- FALSE REFRAMES (ERROR) ----------
FALSE_REFRAME_PATTERNS = [
    re.compile(r"\bisn'?t\s+(?:just\s+)?(?:about\s+)?\w+[,\.]?\s+it'?s\b", re.IGNORECASE),
    re.compile(r"\bnot\s+\w+[,\.]\s+it'?s\b", re.IGNORECASE),
    re.compile(r"\bless\s+about\s+\w+\s+and\s+more\s+about\b", re.IGNORECASE),
    re.compile(r"\bthe\s+pattern\s+isn'?t\b", re.IGNORECASE),
    re.compile(r"\bit'?s\s+not\s+just\s+\w+[,\.]\s+it'?s\b", re.IGNORECASE),
]

# ---------- WARN-LEVEL AI TELLS (advisory) ----------
SOFT_AI_PHRASES = [
    "furthermore", "moreover", "notwithstanding",
    "that being said", "by understanding",
    "delve", "leverage", "facilitate", "underscore",
    "unveil", "endeavour", "ascertain", "elucidate",
    "pivotal", "crucial", "transformative",
    "groundbreaking", "intricate", "nuanced", "multifaceted",
    "myriad of", "plethora of", "paramount",
    "pertaining to", "prior to", "subsequent to",
    "in light of", "with respect to", "in terms of",
    "the fact that",
]

# ---------- HELPERS ----------

def strip_chrome(h):
    """Remove nav, footer, scripts, styles, newsletter section."""
    h = re.sub(r"<script.*?</script>", "", h, flags=re.S)
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    h = re.sub(r"<nav[^>]*>.*?</nav>", "", h, flags=re.S)
    h = re.sub(r"<footer[^>]*>.*?</footer>", "", h, flags=re.S)
    h = re.sub(r'<section class="nl-section".*?</section>', "", h, flags=re.S)
    return h

def text_only(h):
    return html.unescape(re.sub(r"<[^>]+>", " ", h))

def get_paragraphs(h):
    """Extract <p> contents from chrome-stripped HTML."""
    return [text_only(p).strip() for p in re.findall(r"<p[^>]*>(.*?)</p>", h, re.S)]

def get_title(h):
    m = re.search(r"<title>(.*?)</title>", h, re.S)
    return html.unescape(m.group(1)).strip() if m else ""

def get_meta_desc(h):
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', h)
    return m.group(1) if m else ""

def count_h1(h):
    return len(re.findall(r"<h1[^>]*>", h))

def has_canonical(h):
    return bool(re.search(r'<link\s+rel="canonical"', h))

def has_breadcrumb_schema(h):
    return "BreadcrumbList" in h

def has_robots_meta(h):
    return bool(re.search(r'<meta\s+name="robots"', h))

def get_internal_links(h):
    """Count internal href anchors in main content (chrome stripped)."""
    return len(re.findall(r'href="(?:/[^"]*|https?://(?:www\.)?sultanofsaas\.com[^"]*)"', h))

def is_tool_name_match(text, start, end):
    """Suppress matches inside known tool names."""
    # Get 30-char context
    snippet = text[max(0, start-15):end+15].lower()
    # If 'seamless' is part of 'seamless.ai', ignore
    if "seamless.ai" in snippet:
        return True
    return False

def categorize(path):
    """Determine page type from URL path."""
    name = os.path.basename(os.path.dirname(path))
    if name in HUB_PAGES or any(seg in path for seg in ["/stacks/index", "/about/index", "/best/index", "/for/index", "/guides/index", "/tools/index"]):
        return "hub"
    # Check guides BEFORE list so guides/best-* gets categorized as guide
    if "/guides/" in path:
        return "guide"
    if name.endswith("-pricing"):
        return "pricing"
    if "-vs-" in name:
        return "comparison"
    if name.endswith("-alternatives"):
        return "alternatives"
    if name.startswith("best-"):
        return "list"
    if "/tools/" in path:
        return "tool_review"
    if "/stacks/" in path:
        return "stack"
    if "/best/" in path:
        return "category"
    if "/for/" in path:
        return "industry"
    return "other"

# Word count thresholds per page type (ERROR if below)
MIN_WORDS = {
    "hub": 700,
    "pricing": 800,
    "comparison": 800,
    "alternatives": 800,
    "list": 1500,
    "tool_review": 1200,
    "guide": 800,
    "stack": 400,
    "category": 500,
    "industry": 400,
    "other": 500,
}

# ---------- AUDIT CORE ----------

class Finding:
    __slots__ = ("severity", "rule", "page", "msg", "snippet")
    def __init__(self, severity, rule, page, msg, snippet=""):
        self.severity = severity
        self.rule = rule
        self.page = page
        self.msg = msg
        self.snippet = snippet
    def __repr__(self):
        s = self.snippet[:80] + ("..." if len(self.snippet) > 80 else "")
        return f"[{self.severity}] {self.rule} {self.page}: {self.msg} | {s}"


def audit_page(path):
    findings = []
    rel = path.replace(OUTPUT + "/", "").rstrip("/index.html")
    cat = categorize(path)

    with open(path) as f:
        full = f.read()

    chrome = strip_chrome(full)
    body_text = text_only(chrome)
    paragraphs = get_paragraphs(chrome)
    body_lower = body_text.lower()

    # ---- META / SEO ----
    title = get_title(full)
    if not title:
        findings.append(Finding("error", "missing_title", rel, "No <title> tag"))
    else:
        # Title strips brand suffix " | SultanOfSaaS" for length check
        title_clean = re.sub(r"\s*\|\s*SultanOfSaaS$", "", title)
        if len(title) > 70:
            findings.append(Finding("warn", "title_too_long", rel, f"Title is {len(title)} chars (target <60)", title))
        if len(title_clean) < 15:
            findings.append(Finding("warn", "title_too_short", rel, f"Title-only is {len(title_clean)} chars", title))

    meta = get_meta_desc(full)
    if not meta:
        findings.append(Finding("error", "missing_meta_desc", rel, "No meta description"))
    else:
        if len(meta) > 165:
            findings.append(Finding("warn", "meta_too_long", rel, f"Meta is {len(meta)} chars", meta))
        if len(meta) < 70:
            findings.append(Finding("warn", "meta_too_short", rel, f"Meta is {len(meta)} chars", meta))

    if not has_canonical(full):
        findings.append(Finding("error", "missing_canonical", rel, "No canonical link"))
    if not has_robots_meta(full):
        findings.append(Finding("warn", "missing_robots", rel, "No robots meta tag"))
    if not has_breadcrumb_schema(full):
        findings.append(Finding("warn", "missing_bc_schema", rel, "No BreadcrumbList schema"))

    h1_count = count_h1(full)
    if h1_count == 0:
        findings.append(Finding("error", "no_h1", rel, "No H1 on page"))
    elif h1_count > 1:
        findings.append(Finding("error", "multiple_h1", rel, f"{h1_count} H1 tags"))

    # ---- WORD COUNT ----
    words = len(body_text.split())
    threshold = MIN_WORDS.get(cat, 500)
    if words < threshold:
        findings.append(Finding("error", "thin_content", rel, f"{words} words (cat={cat}, min={threshold})"))

    # ---- WRITING: HARD BANNED ----
    for word in HARD_BANNED:
        pat = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
        for m in pat.finditer(body_text):
            if is_tool_name_match(body_text, m.start(), m.end()):
                continue
            snip = body_text[max(0, m.start()-30):m.end()+50].strip()
            findings.append(Finding("error", "banned_word", rel, f"Banned: '{word}'", snip[:120]))
            break  # one per word per page

    for phrase in HARD_BANNED_PHRASES:
        if phrase.lower() in body_lower:
            idx = body_lower.find(phrase.lower())
            snip = body_text[max(0, idx-20):idx+len(phrase)+40].strip()
            findings.append(Finding("error", "banned_phrase", rel, f"Banned phrase: '{phrase}'", snip[:120]))

    # ---- FALSE REFRAMES (only check paragraphs to avoid false positives in titles) ----
    for para in paragraphs:
        for pat in FALSE_REFRAME_PATTERNS:
            m = pat.search(para)
            if m:
                findings.append(Finding("error", "false_reframe", rel, "False reframe", m.group(0)[:120]))
                break

    # ---- EM-DASH IN BODY PARAGRAPHS ----
    for para in paragraphs:
        if "\u2014" in para:
            idx = para.find("\u2014")
            findings.append(Finding("error", "em_dash", rel, "Em-dash in body paragraph", para[max(0,idx-30):idx+40]))
            break

    # ---- SOFT AI TELLS (warn) ----
    soft_hits = Counter()
    for word in SOFT_AI_PHRASES:
        pat = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
        n = len(pat.findall(body_text))
        if n:
            soft_hits[word] = n
    if sum(soft_hits.values()) >= 3:
        # Cluster of AI tells = warn
        top = ", ".join(f"{k}({v})" for k, v in soft_hits.most_common(5))
        findings.append(Finding("warn", "ai_tell_cluster", rel, f"AI-tell cluster: {top}"))

    # ---- INTERNAL LINKING ----
    internal = get_internal_links(chrome)
    if cat in ("pricing", "comparison", "alternatives", "list", "tool_review", "guide") and internal < 3:
        findings.append(Finding("warn", "few_internal_links", rel, f"Only {internal} internal links in main content"))

    # ---- IMAGES (check for missing alt text) ----
    imgs = re.findall(r"<img[^>]*>", chrome)
    for img in imgs:
        if "alt=" not in img:
            findings.append(Finding("error", "img_missing_alt", rel, "Image missing alt attribute", img[:100]))

    return findings


def main():
    paths = sorted(glob.glob(os.path.join(OUTPUT, "*/index.html"))) + \
            sorted(glob.glob(os.path.join(OUTPUT, "*/*/index.html")))

    all_findings = []
    cat_counts = Counter()
    word_stats = defaultdict(list)

    for path in paths:
        cat_counts[categorize(path)] += 1
        page_findings = audit_page(path)
        all_findings.extend(page_findings)

        # Collect word counts
        with open(path) as f:
            full = f.read()
        chrome = strip_chrome(full)
        words = len(text_only(chrome).split())
        word_stats[categorize(path)].append(words)

    # Summary
    by_severity = Counter(f.severity for f in all_findings)
    by_rule = Counter(f.rule for f in all_findings)

    print(f"\n{'='*70}")
    print(f"SULTANOFSAAS SITE AUDIT — {len(paths)} pages")
    print(f"{'='*70}")
    print(f"\nPage type breakdown:")
    for cat, n in sorted(cat_counts.items(), key=lambda x: -x[1]):
        if word_stats[cat]:
            avg = sum(word_stats[cat]) // len(word_stats[cat])
            mn = min(word_stats[cat])
            mx = max(word_stats[cat])
            print(f"  {cat:14} {n:4} pages   words: avg={avg:5} min={mn:5} max={mx:5}")

    print(f"\nFindings by severity:")
    for sev in ["error", "warn", "info"]:
        n = by_severity.get(sev, 0)
        print(f"  {sev:7} {n}")

    print(f"\nTop rules triggered:")
    for rule, n in by_rule.most_common(20):
        print(f"  {rule:25} {n}")

    # Print first N errors per rule
    print(f"\n{'='*70}")
    print("ERRORS (sample, max 5 per rule):")
    print(f"{'='*70}")
    by_rule_findings = defaultdict(list)
    for f in all_findings:
        if f.severity == "error":
            by_rule_findings[f.rule].append(f)
    for rule, fs in sorted(by_rule_findings.items(), key=lambda x: -len(x[1])):
        print(f"\n--- {rule} ({len(fs)} occurrences) ---")
        for f in fs[:5]:
            print(f"  {f.page}: {f.msg}")
            if f.snippet:
                print(f"    > {f.snippet[:100]}")

    print(f"\n{'='*70}")
    print("WARNINGS (sample, max 3 per rule):")
    print(f"{'='*70}")
    by_rule_warns = defaultdict(list)
    for f in all_findings:
        if f.severity == "warn":
            by_rule_warns[f.rule].append(f)
    for rule, fs in sorted(by_rule_warns.items(), key=lambda x: -len(x[1])):
        print(f"\n--- {rule} ({len(fs)} occurrences) ---")
        for f in fs[:3]:
            print(f"  {f.page}: {f.msg}")

    # Write JSON for programmatic fixing
    json_out = os.path.join(ROOT, "audit_findings.json")
    with open(json_out, "w") as fp:
        json.dump([{
            "severity": f.severity, "rule": f.rule, "page": f.page,
            "msg": f.msg, "snippet": f.snippet
        } for f in all_findings], fp, indent=2)
    print(f"\nFull findings written to {json_out}")

    return 1 if by_severity.get("error", 0) > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
