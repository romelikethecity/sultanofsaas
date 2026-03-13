#!/usr/bin/env python3
"""
Content quality audit for sultanofsaas.com

Scans all tool reviews for writing rule violations, structural issues,
and data integrity problems. Exits with code 1 if any errors found.

Run:  python3 scripts/audit.py
      python3 scripts/audit.py --verbose
"""

import os
import sys
import re
from dataclasses import dataclass, field
from collections import Counter

# Add scripts dir to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from build import TOOLS, CATEGORIES, NICHES, INDUSTRIES
from content import get_tool_content, has_deep_content


# =============================================================================
# FINDING
# =============================================================================

@dataclass
class Finding:
    severity: str       # "error" | "warning"
    category: str       # "writing" | "structure" | "data"
    entity: str         # tool slug, niche slug, or industry name
    section: str        # content section name or ""
    rule: str           # short rule ID
    message: str        # human-readable description
    snippet: str = ""   # offending text (first 120 chars)


# =============================================================================
# STRING EXTRACTION
# =============================================================================

def extract_strings(obj, path=""):
    """Recursively yield (path, text) for every string value in nested dicts/lists."""
    if isinstance(obj, str):
        yield (path, obj)
    elif isinstance(obj, dict):
        for key, val in obj.items():
            child_path = f"{path}.{key}" if path else key
            yield from extract_strings(val, child_path)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            child_path = f"{path}[{i}]"
            yield from extract_strings(item, child_path)


# =============================================================================
# TOOL NAME EXCLUSION
# =============================================================================

def _build_tool_names_lower():
    """Build a set of lowercase tool names for banned word exclusion."""
    names = set()
    for t in TOOLS.values():
        names.add(t['name'].lower())
    return names

_TOOL_NAMES_LOWER = None

def _get_tool_names():
    global _TOOL_NAMES_LOWER
    if _TOOL_NAMES_LOWER is None:
        _TOOL_NAMES_LOWER = _build_tool_names_lower()
    return _TOOL_NAMES_LOWER


def _is_tool_name_context(text, match_start, match_end, word):
    """Check if a banned word match is actually part of a tool name."""
    # Get surrounding context (40 chars each side)
    ctx_start = max(0, match_start - 40)
    ctx_end = min(len(text), match_end + 40)
    context = text[ctx_start:ctx_end].lower()

    tool_names = _get_tool_names()
    for name in tool_names:
        if word.lower() in name and name in context:
            return True

    # Also check for partial tool name references (e.g., "Seamless" for "Seamless.AI")
    # Look at immediate context around the match
    near_start = max(0, match_start - 5)
    near_end = min(len(text), match_end + 10)
    near_context = text[near_start:near_end].lower()
    for name in tool_names:
        # Check if the matched word is the beginning of a tool name
        name_lower = name.lower()
        if name_lower.startswith(word.lower()) and word.lower() != name_lower:
            # This banned word is a prefix of a tool name
            # Check if the next chars after match look like the tool name continuation
            after_match = text[match_end:match_end+20].lower().lstrip()
            remaining = name_lower[len(word.lower()):].lstrip()
            if after_match.startswith(remaining[:3]) if remaining else False:
                return True
        # Also check if the word appears as standalone but refers to the tool
        # (e.g., "Seamless searches the web" referring to Seamless.AI)
        if word.lower() in name_lower:
            # Check if it's capitalized like a proper noun (tool name usage)
            matched_text = text[match_start:match_end]
            if matched_text[0].isupper():
                # At start of string or after whitespace/punctuation = proper noun
                if match_start == 0 or text[match_start-1] in ' \n\t"\'(,.:;':
                    return True

    return False


# =============================================================================
# WRITING CHECKS
# =============================================================================

# False reframe patterns (AUDIT-01)
FALSE_REFRAME_PATTERNS = [
    (re.compile(r"\bnot\s+[\w'-]+[,.]?\s*it'?s\b", re.IGNORECASE), "not X, it's Y"),
    (re.compile(r"\bisn'?t\s+[\w'-]+\.\s*It'?s\b", re.IGNORECASE), "isn't X. It's Y"),
    (re.compile(r"\bless\s+about\b.*?\bmore\s+about\b", re.IGNORECASE), "less about X, more about Y"),
    (re.compile(r"\bnot\s+so\s+much\b.*?\bas\b", re.IGNORECASE), "not so much X as Y"),
    (re.compile(r"\bthe\s+pattern\s+isn'?t\b", re.IGNORECASE), "The pattern isn't"),
    (re.compile(r"\bstop\s+thinking\s+of\s+it\s+as\b", re.IGNORECASE), "stop thinking of it as"),
]

# Banned words (AUDIT-03)
BANNED_WORDS = [
    "robust", "leverage", "synergy", "holistic", "cutting-edge",
    "seamless", "frictionless", "end-to-end", "genuinely", "truly",
    "really", "actually", "game-changer", "paradigm shift",
    "best-in-class", "world-class",
]

# Unearned declarations (warning)
UNEARNED_PATTERNS = [
    re.compile(r"\bThe pattern here is clear\b", re.IGNORECASE),
    re.compile(r"\bHere'?s the thing\b", re.IGNORECASE),
    re.compile(r"\bThe bottom line:", re.IGNORECASE),
    re.compile(r"\bIt'?s worth noting\b", re.IGNORECASE),
    re.compile(r"\bWhen it comes to\b", re.IGNORECASE),
    re.compile(r"\bWithout further ado\b", re.IGNORECASE),
]

# Commentary after stats (warning)
COMMENTARY_PATTERNS = [
    re.compile(r"\bLet that sink in\b", re.IGNORECASE),
    re.compile(r"\bYou read that right\b", re.IGNORECASE),
    re.compile(r"\bThat'?s impressive\b", re.IGNORECASE),
]

# Forced casual (warning)
CASUAL_PATTERNS = [
    re.compile(r"\bSpoiler alert\b", re.IGNORECASE),
    re.compile(r"\bPlot twist\b", re.IGNORECASE),
    re.compile(r"\bHere'?s the kicker\b", re.IGNORECASE),
    re.compile(r"\bLet'?s dive in\b", re.IGNORECASE),
    re.compile(r"\bAt the end of the day\b", re.IGNORECASE),
]

# Tautologies (warning)
TAUTOLOGY_PATTERNS = [
    re.compile(r"\bTime will tell\b", re.IGNORECASE),
    re.compile(r"\bSuccess depends on execution\b", re.IGNORECASE),
]

# Missing contractions (warning) - word boundary match, case-insensitive
CONTRACTION_PATTERNS = [
    (re.compile(r"\bit is\b", re.IGNORECASE), "it's"),
    (re.compile(r"\bdo not\b", re.IGNORECASE), "don't"),
    (re.compile(r"\bcannot\b", re.IGNORECASE), "can't"),
    (re.compile(r"\bwill not\b", re.IGNORECASE), "won't"),
    (re.compile(r"\bdoes not\b", re.IGNORECASE), "doesn't"),
    (re.compile(r"\bthey are\b", re.IGNORECASE), "they're"),
    (re.compile(r"\bwe are\b", re.IGNORECASE), "we're"),
    (re.compile(r"\byou are\b", re.IGNORECASE), "you're"),
]


def check_writing(tool_slug, content_dict):
    """Check all writing rules against a tool's content. Returns list of Findings."""
    findings = []

    for section_path, text in extract_strings(content_dict):
        # --- ERRORS ---

        # False reframes (AUDIT-01)
        for pattern, desc in FALSE_REFRAME_PATTERNS:
            for m in pattern.finditer(text):
                snippet = text[max(0, m.start()-20):m.end()+20][:120]
                findings.append(Finding(
                    severity="error",
                    category="writing",
                    entity=tool_slug,
                    section=section_path,
                    rule="false_reframe",
                    message=f"False reframe pattern: {desc}",
                    snippet=snippet.strip(),
                ))

        # Em-dashes (AUDIT-02)
        for m in re.finditer("\u2014", text):
            snippet = text[max(0, m.start()-30):m.end()+30][:120]
            findings.append(Finding(
                severity="error",
                category="writing",
                entity=tool_slug,
                section=section_path,
                rule="em_dash",
                message="Em-dash character found (use -- or rewrite)",
                snippet=snippet.strip(),
            ))

        # Banned words (AUDIT-03)
        for word in BANNED_WORDS:
            # Use word boundary for single words, but handle hyphenated ones
            pat = re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
            for m in pat.finditer(text):
                # Check if this match is part of a tool name
                if _is_tool_name_context(text, m.start(), m.end(), word):
                    continue
                snippet = text[max(0, m.start()-20):m.end()+20][:120]
                findings.append(Finding(
                    severity="error",
                    category="writing",
                    entity=tool_slug,
                    section=section_path,
                    rule="banned_word",
                    message=f"Banned word: '{word}'",
                    snippet=snippet.strip(),
                ))

        # --- WARNINGS ---

        # Unearned declarations
        for pattern in UNEARNED_PATTERNS:
            for m in pattern.finditer(text):
                snippet = text[max(0, m.start()-10):m.end()+30][:120]
                findings.append(Finding(
                    severity="warning",
                    category="writing",
                    entity=tool_slug,
                    section=section_path,
                    rule="unearned_declaration",
                    message=f"Unearned declaration: '{m.group()}'",
                    snippet=snippet.strip(),
                ))

        # Commentary after stats
        for pattern in COMMENTARY_PATTERNS:
            for m in pattern.finditer(text):
                snippet = text[max(0, m.start()-10):m.end()+20][:120]
                findings.append(Finding(
                    severity="warning",
                    category="writing",
                    entity=tool_slug,
                    section=section_path,
                    rule="commentary_after_stats",
                    message=f"Commentary after stats: '{m.group()}'",
                    snippet=snippet.strip(),
                ))

        # Forced casual
        for pattern in CASUAL_PATTERNS:
            for m in pattern.finditer(text):
                snippet = text[max(0, m.start()-10):m.end()+20][:120]
                findings.append(Finding(
                    severity="warning",
                    category="writing",
                    entity=tool_slug,
                    section=section_path,
                    rule="forced_casual",
                    message=f"Forced casual: '{m.group()}'",
                    snippet=snippet.strip(),
                ))

        # Tautologies
        for pattern in TAUTOLOGY_PATTERNS:
            for m in pattern.finditer(text):
                snippet = text[max(0, m.start()-10):m.end()+20][:120]
                findings.append(Finding(
                    severity="warning",
                    category="writing",
                    entity=tool_slug,
                    section=section_path,
                    rule="tautology",
                    message=f"Tautology: '{m.group()}'",
                    snippet=snippet.strip(),
                ))

        # Missing contractions
        for pattern, contraction in CONTRACTION_PATTERNS:
            for m in pattern.finditer(text):
                # Skip if at start of sentence (deliberate emphasis)
                pos = m.start()
                if pos == 0 or text[pos-1] in '.!?\n':
                    continue
                if pos >= 2 and text[pos-2:pos] in '. ':
                    continue
                snippet = text[max(0, m.start()-15):m.end()+15][:120]
                findings.append(Finding(
                    severity="warning",
                    category="writing",
                    entity=tool_slug,
                    section=section_path,
                    rule="missing_contraction",
                    message=f"Consider contraction: '{m.group()}' -> '{contraction}'",
                    snippet=snippet.strip(),
                ))

    return findings


# =============================================================================
# STRUCTURE CHECKS
# =============================================================================

REQUIRED_SECTIONS = [
    "overview", "expanded_pros", "expanded_cons", "pricing_detail",
    "who_should_buy", "who_should_skip", "stage_guidance",
    "alternatives_detail", "verdict_long", "faqs",
]

STAGE_KEYS = ["solo", "small_team", "mid_market", "enterprise"]


def _count_words(content_dict):
    """Count total words across all string values in content."""
    total = 0
    for _, text in extract_strings(content_dict):
        total += len(text.split())
    return total


def check_structure(tool_slug, content_dict):
    """Validate content structure: required sections, min counts, word count."""
    findings = []

    # Required sections (AUDIT-05)
    for section in REQUIRED_SECTIONS:
        if section not in content_dict or content_dict[section] is None:
            findings.append(Finding(
                severity="error",
                category="structure",
                entity=tool_slug,
                section=section,
                rule="missing_section",
                message=f"Required section missing: {section}",
            ))

    # expanded_pros: min 3, each with title and detail
    pros = content_dict.get("expanded_pros", [])
    if isinstance(pros, list):
        if len(pros) < 3:
            findings.append(Finding(
                severity="error",
                category="structure",
                entity=tool_slug,
                section="expanded_pros",
                rule="min_count",
                message=f"Need at least 3 expanded_pros, found {len(pros)}",
            ))
        for i, item in enumerate(pros):
            if not isinstance(item, dict) or "title" not in item or "detail" not in item:
                findings.append(Finding(
                    severity="error",
                    category="structure",
                    entity=tool_slug,
                    section=f"expanded_pros[{i}]",
                    rule="missing_keys",
                    message="expanded_pros item missing 'title' or 'detail' key",
                ))

    # expanded_cons: min 3, each with title and detail
    cons = content_dict.get("expanded_cons", [])
    if isinstance(cons, list):
        if len(cons) < 3:
            findings.append(Finding(
                severity="error",
                category="structure",
                entity=tool_slug,
                section="expanded_cons",
                rule="min_count",
                message=f"Need at least 3 expanded_cons, found {len(cons)}",
            ))
        for i, item in enumerate(cons):
            if not isinstance(item, dict) or "title" not in item or "detail" not in item:
                findings.append(Finding(
                    severity="error",
                    category="structure",
                    entity=tool_slug,
                    section=f"expanded_cons[{i}]",
                    rule="missing_keys",
                    message="expanded_cons item missing 'title' or 'detail' key",
                ))

    # stage_guidance: all 4 keys
    guidance = content_dict.get("stage_guidance")
    if isinstance(guidance, dict):
        for key in STAGE_KEYS:
            if key not in guidance:
                findings.append(Finding(
                    severity="warning",
                    category="structure",
                    entity=tool_slug,
                    section=f"stage_guidance.{key}",
                    rule="missing_stage_key",
                    message=f"Stage guidance missing key: {key}",
                ))

    # FAQs: at least 5
    faqs = content_dict.get("faqs", [])
    if isinstance(faqs, list):
        if len(faqs) < 5:
            findings.append(Finding(
                severity="warning",
                category="structure",
                entity=tool_slug,
                section="faqs",
                rule="min_count",
                message=f"Need at least 5 FAQs, found {len(faqs)}",
            ))
        for i, item in enumerate(faqs):
            if not isinstance(item, dict) or "question" not in item or "answer" not in item:
                findings.append(Finding(
                    severity="warning",
                    category="structure",
                    entity=tool_slug,
                    section=f"faqs[{i}]",
                    rule="missing_keys",
                    message="FAQ item missing 'question' or 'answer' key",
                ))

    # who_should_buy: at least 2
    buyers = content_dict.get("who_should_buy", [])
    if isinstance(buyers, list) and len(buyers) < 2:
        findings.append(Finding(
            severity="warning",
            category="structure",
            entity=tool_slug,
            section="who_should_buy",
            rule="min_count",
            message=f"Need at least 2 who_should_buy, found {len(buyers)}",
        ))

    # who_should_skip: at least 2
    skippers = content_dict.get("who_should_skip", [])
    if isinstance(skippers, list) and len(skippers) < 2:
        findings.append(Finding(
            severity="warning",
            category="structure",
            entity=tool_slug,
            section="who_should_skip",
            rule="min_count",
            message=f"Need at least 2 who_should_skip, found {len(skippers)}",
        ))

    # alternatives_detail: at least 3
    alts = content_dict.get("alternatives_detail", [])
    if isinstance(alts, list) and len(alts) < 3:
        findings.append(Finding(
            severity="warning",
            category="structure",
            entity=tool_slug,
            section="alternatives_detail",
            rule="min_count",
            message=f"Need at least 3 alternatives_detail, found {len(alts)}",
        ))

    # Word count (AUDIT-04)
    word_count = _count_words(content_dict)
    if word_count < 2000:
        findings.append(Finding(
            severity="warning",
            category="structure",
            entity=tool_slug,
            section="",
            rule="word_count",
            message=f"Word count too low: {word_count} (minimum 2,000)",
        ))
    elif word_count > 4000:
        findings.append(Finding(
            severity="warning",
            category="structure",
            entity=tool_slug,
            section="",
            rule="word_count",
            message=f"Word count too high: {word_count} (maximum 4,000)",
        ))

    return findings


# =============================================================================
# DATA CHECKS
# =============================================================================

def check_data():
    """Check niche winner uniqueness, industry completeness, slug validity."""
    findings = []
    all_category_slugs = list(CATEGORIES.keys())

    # Build sultan's pick per category
    sultans_picks = {}
    for cat_slug, cat in CATEGORIES.items():
        for tool_slug in cat['tools']:
            tool = TOOLS.get(tool_slug)
            if tool and tool.get('sultans_pick'):
                sultans_picks[cat_slug] = tool_slug

    # Niche winner uniqueness (AUDIT-06)
    # For each niche+category, the #1 ranked tool should NOT be the sultan's pick
    for niche_slug, niche in NICHES.items():
        rankings = niche.get('rankings', {})
        for cat_slug, ranked_tools in rankings.items():
            if not ranked_tools:
                continue
            winner = ranked_tools[0]
            pick = sultans_picks.get(cat_slug)
            if pick and winner == pick:
                findings.append(Finding(
                    severity="error",
                    category="data",
                    entity=niche_slug,
                    section=cat_slug,
                    rule="niche_winner_conflict",
                    message=f"Niche winner '{winner}' is same as Sultan's Pick for {cat_slug}",
                ))

    # Verify niche ranking slugs exist in TOOLS
    for niche_slug, niche in NICHES.items():
        rankings = niche.get('rankings', {})
        for cat_slug, ranked_tools in rankings.items():
            for tool_slug in ranked_tools:
                if tool_slug not in TOOLS:
                    findings.append(Finding(
                        severity="error",
                        category="data",
                        entity=niche_slug,
                        section=cat_slug,
                        rule="invalid_slug",
                        message=f"Tool slug '{tool_slug}' in niche rankings not found in TOOLS",
                    ))

    # Industry completeness (AUDIT-07)
    for ind_slug, ind in INDUSTRIES.items():
        picks = ind.get('picks', {})
        for cat_slug in all_category_slugs:
            if cat_slug not in picks:
                findings.append(Finding(
                    severity="error",
                    category="data",
                    entity=ind_slug,
                    section=cat_slug,
                    rule="industry_missing_category",
                    message=f"Industry '{ind['name']}' missing pick for category '{cat_slug}'",
                ))

    # Verify industry pick slugs exist in TOOLS
    for ind_slug, ind in INDUSTRIES.items():
        picks = ind.get('picks', {})
        for cat_slug, pick_data in picks.items():
            tool_slug = pick_data.get('tool', '') if isinstance(pick_data, dict) else pick_data
            if tool_slug not in TOOLS:
                findings.append(Finding(
                    severity="error",
                    category="data",
                    entity=ind_slug,
                    section=cat_slug,
                    rule="invalid_slug",
                    message=f"Tool slug '{tool_slug}' in industry picks not found in TOOLS",
                ))

    return findings


# =============================================================================
# REPORT
# =============================================================================

def print_report(findings, verbose=False, tools_scanned=0):
    """Print audit report grouped by severity."""
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]

    # Count by category
    error_cats = Counter(f.category for f in errors)
    warning_cats = Counter(f.category for f in warnings)

    # Count by rule for errors
    error_rules = Counter(f.rule for f in errors)
    warning_rules = Counter(f.rule for f in warnings)

    print("=" * 72)
    print(f"  AUDIT RESULTS: {tools_scanned} tools scanned")
    print("=" * 72)
    print()

    # Summary line
    err_breakdown = ", ".join(f"{cat}: {cnt}" for cat, cnt in sorted(error_cats.items()))
    warn_breakdown = ", ".join(f"{cat}: {cnt}" for cat, cnt in sorted(warning_cats.items()))
    print(f"  Errors: {len(errors)} ({err_breakdown})")
    print(f"  Warnings: {len(warnings)} ({warn_breakdown})")
    print()

    # Error rule breakdown
    if error_rules:
        print("  Error breakdown:")
        for rule, cnt in error_rules.most_common():
            print(f"    {rule}: {cnt}")
        print()

    # Warning rule breakdown
    if warning_rules:
        print("  Warning breakdown:")
        for rule, cnt in warning_rules.most_common():
            print(f"    {rule}: {cnt}")
        print()

    # ERRORS section
    if errors:
        print("-" * 72)
        print("  ERRORS")
        print("-" * 72)

        # Group by category
        for cat in ["writing", "structure", "data"]:
            cat_findings = [f for f in errors if f.category == cat]
            if not cat_findings:
                continue
            print(f"\n  [{cat.upper()}] ({len(cat_findings)} errors)")
            print()
            for f in cat_findings:
                section_part = f" / {f.section}" if f.section else ""
                print(f"    [{f.category}] {f.entity}{section_part}: {f.message}")
                if f.snippet:
                    print(f"      -> \"{f.snippet}\"")

    # WARNINGS section
    if warnings:
        print()
        print("-" * 72)
        print("  WARNINGS")
        print("-" * 72)

        for cat in ["writing", "structure", "data"]:
            cat_findings = [f for f in warnings if f.category == cat]
            if not cat_findings:
                continue
            print(f"\n  [{cat.upper()}] ({len(cat_findings)} warnings)")
            print()
            for f in cat_findings:
                section_part = f" / {f.section}" if f.section else ""
                print(f"    [{f.category}] {f.entity}{section_part}: {f.message}")
                if f.snippet:
                    print(f"      -> \"{f.snippet}\"")

    print()
    print("=" * 72)
    if errors:
        print(f"  FAILED: {len(errors)} errors, {len(warnings)} warnings")
    elif warnings:
        print(f"  PASSED with {len(warnings)} warnings")
    else:
        print("  PASSED: clean")
    print("=" * 72)


# =============================================================================
# MAIN
# =============================================================================

def main():
    verbose = "--verbose" in sys.argv

    all_findings = []
    tools_with_content = []
    tools_without_content = []

    # Scan all tools
    for slug in sorted(TOOLS.keys()):
        tool_data = TOOLS[slug]
        content = get_tool_content(slug)

        # Build a combined dict of scannable text for writing checks
        # Always scan TOOLS data (pros, cons, verdict_line, best_for)
        tool_text_dict = {
            "verdict_line": tool_data.get("verdict_line", ""),
            "best_for": tool_data.get("best_for", ""),
            "pros": tool_data.get("pros", []),
            "cons": tool_data.get("cons", []),
        }

        # Writing checks on TOOLS data (always, for all 90 tools)
        tool_data_findings = check_writing(slug, tool_text_dict)
        all_findings.extend(tool_data_findings)

        if content is None:
            tools_without_content.append(slug)
            if verbose and not tool_data_findings:
                print(f"  CLEAN: {slug} (no deep content)")
            continue

        tools_with_content.append(slug)

        # Writing checks on deep content
        writing_findings = check_writing(slug, content)
        all_findings.extend(writing_findings)

        # Structure checks
        structure_findings = check_structure(slug, content)
        all_findings.extend(structure_findings)

        if verbose and not writing_findings and not structure_findings and not tool_data_findings:
            print(f"  CLEAN: {slug}")

    # Writing checks on NICHES text (intro, why_winners)
    for niche_slug, niche in NICHES.items():
        niche_text = {}
        if niche.get('intro'):
            niche_text['intro'] = niche['intro']
        if niche.get('why_winners'):
            niche_text['why_winners'] = niche['why_winners']
        if niche_text:
            niche_findings = check_writing(f"niche:{niche_slug}", niche_text)
            all_findings.extend(niche_findings)

    # Writing checks on INDUSTRIES text (intro, picks why)
    for ind_slug, ind in INDUSTRIES.items():
        ind_text = {}
        if ind.get('intro'):
            ind_text['intro'] = ind['intro']
        picks_text = {}
        for cat_slug, pick in ind.get('picks', {}).items():
            if isinstance(pick, dict) and pick.get('why'):
                picks_text[cat_slug] = pick['why']
        if picks_text:
            ind_text['picks'] = picks_text
        if ind_text:
            ind_findings = check_writing(f"industry:{ind_slug}", ind_text)
            all_findings.extend(ind_findings)

    # Data checks (across all tools, niches, industries)
    data_findings = check_data()
    all_findings.extend(data_findings)

    # Report
    total_scanned = len(TOOLS)
    print_report(all_findings, verbose=verbose, tools_scanned=total_scanned)

    if verbose:
        print(f"\n  Tools with content: {len(tools_with_content)}")
        print(f"  Tools without content: {len(tools_without_content)}")
        if tools_without_content:
            print(f"    {', '.join(tools_without_content[:20])}")
            if len(tools_without_content) > 20:
                print(f"    ... and {len(tools_without_content) - 20} more")

    # Exit code
    errors = [f for f in all_findings if f.severity == "error"]
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
