#!/usr/bin/env python3
"""
Generate the SaaS review resources page with native SultanOfSaaS branding.
Canonical points to thegtmindex.com/saas-reviews/.
"""

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from templates import get_page_wrapper, write_page, breadcrumb_html, OUTPUT_DIR
import templates

PROJECT_ROOT = os.path.dirname(script_dir)

# Resource data
NICHE = "saas-reviews"
CANONICAL_URL = "https://thegtmindex.com/saas-reviews/"
TITLE = "Best SaaS Review Sites & Resources in 2026"
DESCRIPTION = "Curated list of the best SaaS review platforms, comparison sites, newsletters, and resources for evaluating business software."
INTRO = """Choosing the right SaaS tools for your business shouldn't require reading 50 sponsored blog posts. The review landscape is dominated by pay-to-play platforms and affiliate-driven content.

This list highlights the review sites, communities, and newsletters that provide genuinely useful evaluations. Places where real users share real experiences, and where the editorial process isn't compromised by vendor payments."""

SECTIONS = [
    {"title": "Newsletters", "items": [
        {"name": "Growth Unhinged", "url": "https://www.growthunhinged.com/", "desc": "80K+ subscriber newsletter on SaaS pricing, packaging, PLG, and GTM benchmarks."},
        {"name": "Lenny's Newsletter", "url": "https://www.lennysnewsletter.com/", "desc": "Deep product strategy and SaaS growth research with data from 100+ companies."},
    ]},
    {"title": "Blogs & Websites", "items": [
        {"name": "SaaStr", "url": "https://www.saastr.com/", "desc": "Leading B2B SaaS content hub and annual conference. Jason Lemkin covers growth from $0 to $100M ARR."},
        {"name": "All That SaaS", "url": "https://www.allthatsaas.com/", "desc": "SaaS product reviews, comparisons, and roundups from a team of software and UX professionals."},
        {"name": "Sultan of SaaS", "url": "https://sultanofsaas.com/", "desc": "Opinionated SaaS reviews for SMBs and founders. Picks winners, no 'it depends' answers.", "owned": True},
        {"name": "B2B Sales Tools", "url": "https://b2bsalestools.com/", "desc": "Independent reviews and comparisons of 130+ B2B sales tools across 22 categories.", "owned": True},
        {"name": "MOPs Report", "url": "https://mopsreport.com/", "desc": "Marketing operations tool reviews, salary data, and career intelligence for MOps professionals.", "owned": True},
    ]},
    {"title": "Tools Worth Knowing", "items": [
        {"name": "G2", "url": "https://www.g2.com/", "desc": "Largest review database (3.3M+ reviews). The G2 Grid is the most recognized SaaS evaluation framework."},
        {"name": "TrustRadius", "url": "https://www.trustradius.com/", "desc": "Highest review integrity. No incentivized reviews, no pay-to-play. Reviews average 400+ words."},
        {"name": "Gartner Peer Insights", "url": "https://www.gartner.com/peer-insights/home", "desc": "Enterprise-grade software reviews with verified peer ratings and Customers' Choice distinctions."},
        {"name": "Product Hunt", "url": "https://www.producthunt.com/", "desc": "Product launch platform for discovering new SaaS tools. Built around launch events and early adopter feedback."},
        {"name": "Capterra", "url": "https://www.capterra.com/", "desc": "Software comparison platform with user reviews. Acquired by G2 in Feb 2026."},
    ]},
    {"title": "Podcasts", "items": [
        {"name": "The SaaS Podcast (Omer Khan)", "url": "https://saasclub.io/", "desc": "500+ founder interviews targeting SaaS companies at $0-$5M ARR."},
        {"name": "SaaStr Podcast", "url": "https://www.saastr.com/podcast/", "desc": "Harry Stebbings and Jason Lemkin interview CEOs and founders on scaling SaaS companies."},
    ]},
]


def build_body():
    """Build the body HTML for the resource page."""
    html = []

    # Breadcrumb
    html.append(breadcrumb_html([("Home", "/"), (TITLE, None)]))

    # Hero
    html.append(f'''
<section style="max-width:800px;margin:0 auto;padding:2rem 1.5rem 1rem;">
  <h1 style="font-size:2.25rem;font-weight:800;margin-bottom:1rem;line-height:1.15;">{TITLE}</h1>
''')
    for para in INTRO.strip().split("\n\n"):
        html.append(f'  <p style="color:var(--text-secondary,#94a3b8);font-size:1.05rem;line-height:1.7;margin-bottom:1rem;">{para}</p>')
    html.append('</section>')

    # Sections
    for section in SECTIONS:
        html.append(f'''
<section style="max-width:800px;margin:0 auto;padding:1rem 1.5rem 2rem;">
  <h2 style="font-size:1.5rem;font-weight:700;margin-bottom:1.25rem;padding-bottom:0.5rem;border-bottom:2px solid rgba(212,160,84,0.3);">{section["title"]}</h2>
  <ol style="list-style:none;padding:0;margin:0;">
''')
        for i, item in enumerate(section["items"], 1):
            owned_badge = ' <span style="display:inline-block;background:rgba(212,160,84,0.15);color:#D4A054;font-size:0.7rem;font-weight:700;padding:2px 8px;border-radius:4px;margin-left:8px;vertical-align:middle;letter-spacing:0.5px;">OUR PICK</span>' if item.get("owned") else ""
            html.append(f'''    <li style="margin-bottom:1.25rem;padding:1rem;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:8px;">
      <span style="color:#D4A054;font-weight:700;margin-right:0.5rem;">{i}.</span>
      <a href="{item["url"]}" target="_blank" rel="noopener" style="color:#D4A054;font-weight:600;text-decoration:none;">{item["name"]}</a>{owned_badge}
      <p style="color:var(--text-secondary,#94a3b8);font-size:0.95rem;margin:0.5rem 0 0;line-height:1.6;">{item["desc"]}</p>
    </li>''')
        html.append('  </ol>\n</section>')

    # How We Curated
    html.append('''
<section style="max-width:800px;margin:0 auto;padding:1rem 1.5rem 2rem;">
  <div style="background:rgba(212,160,84,0.06);border:1px solid rgba(212,160,84,0.2);border-radius:12px;padding:1.5rem 2rem;">
    <h3 style="font-size:1.1rem;font-weight:700;margin-bottom:0.75rem;">How We Curated This List</h3>
    <p style="color:var(--text-secondary,#94a3b8);font-size:0.95rem;line-height:1.7;margin-bottom:0.75rem;">Every resource on this page was evaluated based on editorial independence, content depth, community engagement, and practitioner recommendations. We prioritize sources that provide original analysis over aggregated content.</p>
    <p style="color:var(--text-secondary,#94a3b8);font-size:0.95rem;line-height:1.7;">This page is part of <a href="https://thegtmindex.com/" target="_blank" rel="noopener" style="color:#D4A054;">The GTM Index</a>, a curated directory of the best resources across go-to-market disciplines.</p>
  </div>
</section>
''')

    return "\n".join(html)


def main():
    # Set output dirs
    output_dir = os.path.join(PROJECT_ROOT, "output")
    pages_dir = os.path.join(PROJECT_ROOT, "pages")
    templates.OUTPUT_DIR = output_dir

    body = build_body()

    page = get_page_wrapper(
        title=TITLE,
        description=DESCRIPTION,
        canonical_path="/best-saas-review-resources/",
        body_content=body,
    )

    # Replace the auto-generated canonical with our cross-site canonical
    import re
    page = re.sub(
        r'<link rel="canonical" href="https://sultanofsaas\.com/best-saas-review-resources/">',
        f'<link rel="canonical" href="{CANONICAL_URL}">',
        page
    )

    # Write to output/
    out_path = os.path.join(output_dir, "best-saas-review-resources", "index.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  Wrote {out_path}")

    # Write to pages/ (for gh-pages deployment)
    pages_path = os.path.join(pages_dir, "best-saas-review-resources", "index.html")
    os.makedirs(os.path.dirname(pages_path), exist_ok=True)
    with open(pages_path, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  Wrote {pages_path}")

    print("Done: SultanOfSaaS resource page generated.")


if __name__ == "__main__":
    main()
