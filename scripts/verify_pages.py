#!/usr/bin/env python3
"""Automated structural verification of site pages."""
import urllib.request
import re
import sys

BASE = "http://localhost:8086"

# VIS-01: Sample pages (adjusted - no niches/industries dirs exist, using stacks and tools)
SAMPLE_PAGES = [
    ("/", "Homepage"),
    ("/best/crm/", "CRM Category"),
    ("/hubspot-pricing/", "Tool Pricing Page"),
    ("/stacks/lean-startup/", "Stack Guide"),
    ("/tools/hubspot/", "Tool Review"),
    ("/tools/", "Tools Index"),
]

# VIS-02: New category pages
NEW_CATEGORY_PAGES = [
    ("/best/ai-sdr/", "AI SDR", "AI SDR"),
    ("/best/sales-engagement/", "Sales Engagement", "Sales Engagement"),
    ("/best/conversation-intelligence/", "Conversation Intelligence", "Conversation Intelligence"),
    ("/best/data-enrichment/", "Data Enrichment", "Data Enrichment"),
]

failures = 0

def check_page(url, label, extra_checks=None):
    global failures
    full_url = BASE + url
    print(f"\n--- {label} ({url}) ---")

    try:
        req = urllib.request.Request(full_url)
        resp = urllib.request.urlopen(req)
        status = resp.status
        body = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  FAIL: Could not fetch: {e}")
        failures += 1
        return

    checks = [
        ("HTTP 200", status == 200),
        ("Body > 1000 bytes", len(body) > 1000),
        ("Has <nav", "<nav" in body.lower()),
        ("Has <h1", "<h1" in body.lower()),
        ("Has <footer", "<footer" in body.lower()),
        ("Has non-empty <title>", bool(re.search(r"<title>[^<]+</title>", body, re.I))),
        ("Contains 'Sultan'", "Sultan" in body or "sultan" in body.lower()),
    ]

    if extra_checks:
        checks.extend(extra_checks(body))

    for name, passed in checks:
        status_str = "PASS" if passed else "FAIL"
        print(f"  {status_str}: {name}")
        if not passed:
            failures += 1

def category_extra_checks(category_name):
    def checker(body):
        # Check for tool card elements
        has_cards = bool(re.search(r'class="[^"]*card[^"]*"', body, re.I))

        # Check category name in h1 or title
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.I | re.DOTALL)
        title_match = re.search(r'<title>(.*?)</title>', body, re.I)
        h1_text = h1_match.group(1) if h1_match else ""
        title_text = title_match.group(1) if title_match else ""
        has_cat_name = (category_name.lower() in h1_text.lower() or
                       category_name.lower() in title_text.lower())

        # Check for at least 3 tool links (links to /tools/ pages)
        tool_links = re.findall(r'href="[^"]*/(tools/|[a-z]+-pricing|[a-z]+-vs-)[^"]*"', body, re.I)
        # Also count links to individual tool review paths
        tool_links2 = re.findall(r'href="/tools/[^"]+/"', body, re.I)
        total_tool_refs = len(set(tool_links + tool_links2))

        return [
            ("Has card elements", has_cards),
            (f"Category name '{category_name}' in h1/title", has_cat_name),
            (f"At least 3 tool references (found {total_tool_refs})", total_tool_refs >= 3),
        ]
    return checker

print("=" * 60)
print("VIS-01: Sample Page Checks")
print("=" * 60)

for url, label in SAMPLE_PAGES:
    check_page(url, label)

print("\n" + "=" * 60)
print("VIS-02: New Category Page Checks")
print("=" * 60)

for url, label, cat_name in NEW_CATEGORY_PAGES:
    check_page(url, label, extra_checks=category_extra_checks(cat_name))

print("\n" + "=" * 60)
if failures == 0:
    print(f"RESULT: ALL CHECKS PASSED")
else:
    print(f"RESULT: {failures} CHECK(S) FAILED")
print("=" * 60)

sys.exit(1 if failures > 0 else 0)
