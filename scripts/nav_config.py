#!/usr/bin/env python3
"""
Centralized navigation and site configuration for SultanOfSaaS.

Edit this file to update navigation across ALL pages on the site.
After editing, regenerate all pages by running:
    python3 scripts/build.py
"""

# Site info
SITE_NAME = "SultanOfSaaS"
SITE_URL = "https://sultanofsaas.com"
SITE_TAGLINE = "Opinionated SaaS Reviews for Founders"
COPYRIGHT_YEAR = "2026"
CURRENT_YEAR = 2026

# CSS cache busting
CSS_VERSION = "4"

# Category slugs used in nav dropdown (must match CATEGORIES keys in build.py)
NAV_CATEGORIES = [
    {"href": "/best/crm/", "label": "CRM Software"},
    {"href": "/best/project-management/", "label": "Project Management"},
    {"href": "/best/email-marketing/", "label": "Email Marketing"},
    {"href": "/best/seo-tools/", "label": "SEO Tools"},
    {"href": "/best/help-desk/", "label": "Help Desk"},
    {"href": "/best/ai-sdr/", "label": "AI SDR"},
    {"href": "/best/sales-engagement/", "label": "Sales Engagement"},
    {"href": "/best/conversation-intelligence/", "label": "Conversation Intelligence"},
    {"href": "/best/data-enrichment/", "label": "Data Enrichment"},
]

# Industry links for nav dropdown
NAV_INDUSTRIES = [
    {"href": "/for/ecommerce/", "label": "E-Commerce"},
    {"href": "/for/saas/", "label": "SaaS Companies"},
    {"href": "/for/agencies/", "label": "Agencies"},
    {"href": "/for/startups/", "label": "Startups"},
    {"href": "/for/real-estate/", "label": "Real Estate"},
    {"href": "/for/", "label": "All Industries \u2192"},
]

# Main navigation items
NAV_ITEMS = [
    {
        "href": "/best/",
        "label": "Categories",
        "children": NAV_CATEGORIES,
    },
    {
        "href": "/for/",
        "label": "By Industry",
        "children": NAV_INDUSTRIES,
    },
    {"href": "/tools/", "label": "Tools"},
    {"href": "/stacks/", "label": "Stacks"},
    {"href": "/guides/", "label": "Guides"},
    {"href": "/voices/", "label": "Top Voices"},
    {"href": "/about/", "label": "About"},
]

# Footer link columns
FOOTER_COLUMNS = {
    "Top Categories": [
        {"href": "/best/crm/", "label": "Best CRM Software"},
        {"href": "/best/project-management/", "label": "Best Project Management"},
        {"href": "/best/email-marketing/", "label": "Best Email Marketing"},
        {"href": "/best/seo-tools/", "label": "Best SEO Tools"},
        {"href": "/best/help-desk/", "label": "Best Help Desk"},
        {"href": "/best/ai-sdr/", "label": "Best AI SDR"},
        {"href": "/best/sales-engagement/", "label": "Best Sales Engagement"},
        {"href": "/best/conversation-intelligence/", "label": "Best Conversation Intelligence"},
        {"href": "/best/data-enrichment/", "label": "Best Data Enrichment"},
    ],
    "By Industry": [
        {"href": "/for/ecommerce/", "label": "E-Commerce Tools"},
        {"href": "/for/saas/", "label": "SaaS Tools"},
        {"href": "/for/agencies/", "label": "Agency Tools"},
        {"href": "/for/startups/", "label": "Startup Tools"},
        {"href": "/for/real-estate/", "label": "Real Estate Tools"},
        {"href": "/for/", "label": "All Industries"},
    ],
    "Resources": [
        {"href": "/tools/", "label": "All Tools"},
        {"href": "/stacks/zero-dollar-founder/", "label": "The $0/mo Stack"},
        {"href": "/stacks/lean-startup/", "label": "The Lean Startup Stack"},
        {"href": "/stacks/", "label": "All Stack Guides"},
        {"href": "/hubspot-vs-salesforce/", "label": "HubSpot vs Salesforce"},
        {"href": "/semrush-vs-ahrefs/", "label": "Semrush vs Ahrefs"},
        {"href": "/guides/", "label": "Founder Guides"},
    ],
    "Site": [
        {"href": "/about/", "label": "About The Sultan"},
        {"href": "/", "label": "Home"},
    ],
    "Sales Intelligence": [
        {"href": "https://b2bsalestools.com", "label": "B2B Sales Tools", "external": True},
        {"href": "https://thecroreport.com", "label": "CRO Report", "external": True},
        {"href": "https://datastackguide.com", "label": "DataStack Guide", "external": True},
    ],
}
