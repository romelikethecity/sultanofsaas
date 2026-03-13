"""
Content loading system for SultanOfSaaS deep reviews.

Each category has its own content module (e.g., tools_crm.py) that exports
a TOOL_CONTENT dict keyed by tool slug. When content exists for a tool,
the review page renders expanded sections. When it doesn't, the page
falls back to the thin format (verdict + bullet pros/cons + pricing table).

To add content for a tool:
1. Open/create the category content file (e.g., tools_crm.py)
2. Add a TOOL_CONTENT["slug"] = { ... } entry
3. Rebuild: python3 scripts/build.py

Content schema per tool:

    TOOL_CONTENT["hubspot"] = {
        "overview": [
            "First paragraph of overview...",
            "Second paragraph...",
        ],
        "expanded_pros": [
            {"title": "Best free tier in CRM", "detail": "2-3 sentences..."},
        ],
        "expanded_cons": [
            {"title": "Paid tiers get expensive fast", "detail": "2-3 sentences..."},
        ],
        "pricing_detail": "Multi-paragraph pricing analysis with hidden costs...",
        "who_should_buy": [
            {"audience": "SMBs starting from zero", "reason": "Why..."},
        ],
        "who_should_skip": [
            {"audience": "Enterprise teams with 50+ reps", "reason": "Why..."},
        ],
        "stage_guidance": {
            "solo": "Advice for solo founders...",
            "small_team": "Advice for 2-10 person teams...",
            "mid_market": "Advice for 11-50...",
            "enterprise": "Advice for 50+...",
        },
        "alternatives_detail": [
            {"tool": "pipedrive", "reason": "Choose Pipedrive if..."},
        ],
        "verdict_long": "2-3 paragraph opinionated final verdict...",
        "faqs": [
            {"question": "Is HubSpot free CRM really free?", "answer": "Detailed answer..."},
        ],
    }

All fields are optional. If a field is missing, that section is skipped.
"""

import os
import importlib

# Category slug -> content module name
_CONTENT_MODULES = {
    'crm': 'tools_crm',
    'project-management': 'tools_project_management',
    'email-marketing': 'tools_email_marketing',
    'seo-tools': 'tools_seo_tools',
    'help-desk': 'tools_help_desk',
    'ai-sdr': 'tools_ai_sdr',
    'sales-engagement': 'tools_sales_engagement',
    'conversation-intelligence': 'tools_conversation_intelligence',
    'data-enrichment': 'tools_data_enrichment',
}

# Merged content from all modules, keyed by tool slug
_ALL_CONTENT = {}
_loaded = False


def _load_all():
    """Import all content modules and merge into _ALL_CONTENT."""
    global _loaded
    if _loaded:
        return
    content_dir = os.path.dirname(os.path.abspath(__file__))
    for cat_slug, mod_name in _CONTENT_MODULES.items():
        mod_path = os.path.join(content_dir, f"{mod_name}.py")
        if os.path.exists(mod_path):
            mod = importlib.import_module(f"content.{mod_name}")
            if hasattr(mod, 'TOOL_CONTENT'):
                _ALL_CONTENT.update(mod.TOOL_CONTENT)
    _loaded = True


def get_tool_content(slug):
    """Return deep content dict for a tool, or None if no content exists."""
    _load_all()
    return _ALL_CONTENT.get(slug)


def has_deep_content(slug):
    """Check if a tool has deep editorial content."""
    _load_all()
    return slug in _ALL_CONTENT
