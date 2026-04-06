#!/usr/bin/env python3
"""
Shared HTML generation module for SultanOfSaaS.

Provides all common HTML template functions used by build.py:
- get_html_head() — meta tags, OG, fonts, CSS
- get_nav_html() — responsive navigation with category dropdown
- get_footer_html() — multi-column footer
- get_page_wrapper() — wraps everything into a complete page
- write_page() — writes file and registers for sitemap
- Schema helpers for BreadcrumbList, FAQPage, Product, Review
"""

import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import (
    NAV_ITEMS,
    FOOTER_COLUMNS,
    SITE_NAME,
    SITE_URL,
    SITE_TAGLINE,
    COPYRIGHT_YEAR,
    CSS_VERSION,
)

# Track all pages for sitemap
ALL_PAGES = []

# Output directory (set by build.py before calling)
OUTPUT_DIR = ""


# =============================================================================
# INLINE SVG CONSTANTS
# =============================================================================

LOGO_MARK_SMALL = '''<svg viewBox="0 0 18 24" width="18" height="24" xmlns="http://www.w3.org/2000/svg" class="logo-mark">
  <rect x="1" y="0" width="8" height="8" rx="2" transform="rotate(45, 5, 4)" fill="#D4A054"/>
  <rect x="4" y="7.5" width="8" height="8" rx="2" transform="rotate(45, 8, 11.5)" fill="#D4A054" opacity="0.55"/>
  <rect x="1" y="15" width="8" height="8" rx="2" transform="rotate(45, 5, 19)" fill="#D4A054" opacity="0.25"/>
</svg>'''

DIAMOND_SINGLE = '''<svg viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg" class="diamond-icon">
  <rect x="1" y="1" width="5.5" height="5.5" rx="1" transform="rotate(45, 3.75, 3.75)" fill="currentColor"/>
</svg>'''

DIAMONDS_TRIPLE = '''<svg viewBox="0 0 18 24" xmlns="http://www.w3.org/2000/svg" class="diamonds-triple">
  <rect x="1" y="0" width="8" height="8" rx="2" transform="rotate(45, 5, 4)" fill="currentColor"/>
  <rect x="4" y="7.5" width="8" height="8" rx="2" transform="rotate(45, 8, 11.5)" fill="currentColor" opacity="0.55"/>
  <rect x="1" y="15" width="8" height="8" rx="2" transform="rotate(45, 5, 19)" fill="currentColor" opacity="0.25"/>
</svg>'''

CHEVRON_DOWN = '<svg viewBox="0 0 12 12" fill="currentColor" class="chevron"><path d="M2 4l4 4 4-4"/></svg>'


# =============================================================================
# HTML HEAD
# =============================================================================

def get_html_head(title, description, canonical_path, extra_head=""):
    """Generate complete <head> section."""
    canonical = f"{SITE_URL}{canonical_path}"
    full_title = f"{title} | {SITE_NAME}" if title != SITE_NAME else SITE_NAME

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#0C0E12">
    <title>{full_title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{full_title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:image" content="{SITE_URL}/assets/logos/logo-wordmark.svg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{full_title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{SITE_URL}/assets/logos/logo-wordmark.svg">

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/assets/favicons/favicon-gold.svg">

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="/assets/css/tokens.css">
    <link rel="stylesheet" href="/assets/css/components.css">
    <link rel="stylesheet" href="/assets/css/styles.css?v={CSS_VERSION}">

    <!-- Google Search Console -->
    <!-- Google Search Console verification pending -->

    <!-- Google Analytics (GA4) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-0SBNZZYM4Y"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-0SBNZZYM4Y');
    </script>
{extra_head}
</head>'''


# =============================================================================
# NAVIGATION
# =============================================================================

def get_nav_html(active_page=""):
    """Generate responsive navigation with logo wordmark and category dropdown."""
    # Build nav items
    nav_items_html = ""
    for item in NAV_ITEMS:
        children = item.get("children")
        if children:
            dropdown_links = ""
            for child in children:
                dropdown_links += f'<a href="{child["href"]}" class="nav-dropdown-link">{child["label"]}</a>\n'
            nav_items_html += f'''<li class="nav-item nav-item--dropdown">
                <button class="nav-dropdown-toggle">{item["label"]} {CHEVRON_DOWN}</button>
                <div class="nav-dropdown">{dropdown_links}</div>
            </li>'''
        else:
            active_cls = " nav-link--active" if active_page == item["href"] else ""
            nav_items_html += f'<li class="nav-item"><a href="{item["href"]}" class="nav-link{active_cls}">{item["label"]}</a></li>'

    return f'''<nav class="site-nav">
    <div class="nav-container">
        <a href="/" class="nav-logo">
            {LOGO_MARK_SMALL}
            <span class="nav-wordmark"><span class="wm-sultan">Sultan</span><span class="wm-of">Of</span><span class="wm-saas">SaaS</span></span>
        </a>
        <ul class="nav-links">{nav_items_html}</ul>
        <button class="nav-mobile-toggle" aria-label="Menu">
            <span></span><span></span><span></span>
        </button>
    </div>
</nav>'''


# =============================================================================
# FOOTER
# =============================================================================

def get_footer_html():
    """Generate multi-column footer."""
    columns_html = ""
    for col_title, links in FOOTER_COLUMNS.items():
        links_html = ""
        for link in links:
            ext_attrs = ' target="_blank" rel="noopener"' if link.get("external") else ""
            links_html += f'<li><a href="{link["href"]}"{ext_attrs}>{link["label"]}</a></li>\n'
        columns_html += f'''<div class="footer-col">
            <h4>{col_title}</h4>
            <ul>{links_html}</ul>
        </div>\n'''

    return f'''<footer class="site-footer">
    <div class="footer-container">
        <div class="footer-grid">{columns_html}</div>
        <div class="footer-bottom">
            <div class="footer-brand">
                {LOGO_MARK_SMALL}
                <span class="nav-wordmark"><span class="wm-sultan">Sultan</span><span class="wm-of">Of</span><span class="wm-saas">SaaS</span></span>
            </div>
            <p class="footer-tagline">{SITE_TAGLINE}</p>
            <p class="footer-copy">&copy; {COPYRIGHT_YEAR} {SITE_NAME}. All rights reserved.</p>
        </div>
    </div>
</footer>'''


# =============================================================================
# NEWSLETTER SIGNUP
# =============================================================================

def get_newsletter_html():
    """Generate newsletter signup section for every page."""
    return '''<section class="nl-section">
  <div class="container">
    <div class="nl-card">
      <div class="nl-content">
        <h3 class="nl-title">The Sultan's Pick</h3>
        <p class="nl-desc">One email per week. The best SaaS tool I reviewed, why it won, and who should buy it.</p>
      </div>
      <form class="nl-form" id="nl-form" data-list="sultan-of-saas">
        <div class="nl-form-row">
          <input type="email" name="email" placeholder="you@company.com" required class="nl-input" id="nl-email">
          <button type="submit" class="nl-btn">Subscribe Free</button>
        </div>
        <p class="nl-msg" id="nl-msg"></p>
        <p class="nl-fine">No spam. Unsubscribe anytime.</p>
      </form>
    </div>
  </div>
</section>
<script>
(function() {
  var form = document.getElementById('nl-form');
  var msg = document.getElementById('nl-msg');
  var btn = form.querySelector('.nl-btn');
  var emailInput = document.getElementById('nl-email');
  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var email = emailInput.value.trim();
    var list = form.getAttribute('data-list');
    if (!email) return;
    btn.disabled = true;
    btn.textContent = 'Subscribing...';
    msg.textContent = '';
    msg.className = 'nl-msg';
    fetch('https://newsletter-subscribe.rome-workers.workers.dev/subscribe', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: email, list: list})
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.ok) {
        form.style.display = 'none';
        msg.textContent = "You're in. Watch your inbox.";
        msg.className = 'nl-msg success';
        msg.style.display = 'block';
      } else {
        msg.textContent = data.error || 'Something went wrong.';
        msg.className = 'nl-msg error';
        btn.disabled = false;
        btn.textContent = 'Subscribe Free';
      }
    })
    .catch(function() {
      msg.textContent = 'Connection error. Try again.';
      msg.className = 'nl-msg error';
      btn.disabled = false;
      btn.textContent = 'Subscribe Free';
    });
  });
})();
</script>'''


# =============================================================================
# PAGE WRAPPER
# =============================================================================

def get_page_wrapper(title, description, canonical_path, body_content, active_page="", extra_head=""):
    """Wrap body content in a complete HTML page."""
    return f'''{get_html_head(title, description, canonical_path, extra_head)}
<body>
{get_nav_html(active_page)}
<main class="main-content">
{body_content}
</main>
{get_newsletter_html()}
{get_footer_html()}
<script>
// Mobile nav toggle
document.querySelector('.nav-mobile-toggle')?.addEventListener('click', function() {{
    this.classList.toggle('active');
    document.querySelector('.nav-links').classList.toggle('open');
}});
// Dropdown toggles
document.querySelectorAll('.nav-dropdown-toggle').forEach(btn => {{
    btn.addEventListener('click', function(e) {{
        e.stopPropagation();
        const parent = this.parentElement;
        parent.classList.toggle('open');
    }});
}});
document.addEventListener('click', () => {{
    document.querySelectorAll('.nav-item--dropdown.open').forEach(el => el.classList.remove('open'));
}});
</script>
</body>
</html>'''


# =============================================================================
# FILE WRITING
# =============================================================================

def write_page(rel_path, content):
    """Write an HTML file and register it for sitemap."""
    full_path = os.path.join(OUTPUT_DIR, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    ALL_PAGES.append(rel_path)


# =============================================================================
# SCHEMA HELPERS
# =============================================================================

def get_breadcrumb_schema(items):
    """Generate BreadcrumbList JSON-LD. items = [(label, url), ...]"""
    list_items = []
    for i, (label, url) in enumerate(items, 1):
        list_items.append({
            "@type": "ListItem",
            "position": i,
            "name": label,
            "item": f"{SITE_URL}{url}" if url else None,
        })
    # Remove 'item' from last entry (current page)
    if list_items:
        list_items[-1].pop("item", None)

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": list_items,
    }
    return f'    <script type="application/ld+json">{json.dumps(schema)}</script>\n'


def get_faq_schema(faqs):
    """Generate FAQPage JSON-LD. faqs = [(question, answer), ...]"""
    entities = []
    for q, a in faqs:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a,
            },
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities,
    }
    return f'    <script type="application/ld+json">{json.dumps(schema)}</script>\n'


def get_article_schema(title, description, url, date_str, author="The Sultan"):
    """Generate Article JSON-LD for guide/editorial pages."""
    from datetime import datetime
    # Parse "March 2026" or "April 2026" style dates
    try:
        parsed = datetime.strptime(date_str, "%B %Y")
        iso_date = parsed.strftime("%Y-%m-01")
    except ValueError:
        iso_date = "2026-03-01"

    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": f"{SITE_URL}{url}",
        "datePublished": iso_date,
        "dateModified": iso_date,
        "author": {
            "@type": "Person",
            "name": author,
        },
        "publisher": {
            "@type": "Organization",
            "name": SITE_NAME,
            "url": SITE_URL,
        },
    }
    return f'    <script type="application/ld+json">{json.dumps(schema)}</script>\n'


def get_product_schema(name, description, url, rating, review_count=1):
    """Generate Product + AggregateRating JSON-LD."""
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "description": description,
        "url": url,
        "applicationCategory": "BusinessApplication",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(rating),
            "bestRating": "10",
            "worstRating": "1",
            "reviewCount": str(review_count),
        },
    }
    return f'    <script type="application/ld+json">{json.dumps(schema)}</script>\n'


# =============================================================================
# COMPONENT HELPERS
# =============================================================================

def get_verdict_color(score):
    """Return CSS variable name for verdict score color."""
    if score >= 9.0:
        return "var(--verdict-excellent)"
    elif score >= 7.0:
        return "var(--verdict-good)"
    elif score >= 5.0:
        return "var(--verdict-mid)"
    elif score >= 3.0:
        return "var(--verdict-poor)"
    return "var(--verdict-bad)"


def get_verdict_word(score):
    """Return verdict word from score."""
    if score >= 9.0:
        return "Excellent"
    elif score >= 7.0:
        return "Solid Pick"
    elif score >= 5.0:
        return "Situational"
    elif score >= 3.0:
        return "Avoid"
    return "Hard Pass"


def get_price_tier_class(tier):
    """Return CSS class for price tier tag."""
    return f"price-tag price-tag--{tier}"


def breadcrumb_html(crumbs):
    """Generate visual breadcrumb navigation. crumbs = [(label, url), ...]"""
    parts = []
    for i, (label, url) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<span class="breadcrumb-current">{label}</span>')
        else:
            parts.append(f'<a href="{url}" class="breadcrumb-link">{label}</a><span class="breadcrumb-sep">/</span>')
    return f'<nav class="breadcrumb" aria-label="Breadcrumb">{"".join(parts)}</nav>'
