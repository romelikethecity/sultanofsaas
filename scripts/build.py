#!/usr/bin/env python3
"""
Build script for sultanofsaas.com
Generates 200+ static HTML pages from inline structured data.

Run:     python3 scripts/build.py
Preview: cd output && python3 -m http.server 8086
"""

import os
import sys
import json
import shutil
from datetime import datetime

# Add scripts dir to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from nav_config import SITE_NAME, SITE_URL, SITE_TAGLINE, CURRENT_YEAR, CSS_VERSION
from templates import (
    get_page_wrapper, write_page, get_verdict_color, get_verdict_word,
    get_price_tier_class, get_breadcrumb_schema, get_faq_schema,
    get_product_schema, breadcrumb_html, LOGO_MARK_SMALL, DIAMOND_SINGLE,
    DIAMONDS_TRIPLE, ALL_PAGES,
)
import templates
from content import get_tool_content

# =============================================================================
# PATHS
# =============================================================================

PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BUILD_DATE = datetime.now().strftime("%Y-%m-%d")

# Set output dir on templates module
templates.OUTPUT_DIR = OUTPUT_DIR


# =============================================================================
# TOOL DATA
# =============================================================================

TOOLS = {}

def T(slug, name, category, url, score, verdict_line,
      best_for, pricing_start, pricing_tier, pros, cons,
      features=None, pricing_tiers=None, subscores=None,
      sultans_pick=False):
    """Register a tool."""
    TOOLS[slug] = {
        'slug': slug,
        'name': name,
        'category': category,
        'url': url,
        'score': score,
        'verdict_word': get_verdict_word(score),
        'verdict_line': verdict_line,
        'best_for': best_for,
        'pricing_start': pricing_start,
        'pricing_tier': pricing_tier,
        'pros': pros,
        'cons': cons,
        'features': features or [],
        'pricing_tiers': pricing_tiers or [],
        'subscores': subscores or {},
        'sultans_pick': sultans_pick,
    }


# =============================================================================
# CATEGORIES (5 seed categories)
# =============================================================================

CATEGORIES = {
    'crm': {
        'slug': 'crm',
        'name': 'CRM Software',
        'description': 'Customer relationship management tools that track contacts, deals, and pipeline. The foundation of every sales stack.',
        'tools': ['hubspot', 'salesforce', 'pipedrive', 'close', 'freshsales',
                  'zoho-crm', 'copper', 'monday-sales-crm', 'nutshell', 'less-annoying-crm'],
    },
    'project-management': {
        'slug': 'project-management',
        'name': 'Project Management',
        'description': 'Tools for organizing tasks, tracking projects, and keeping teams aligned. Ranges from simple kanban boards to full-blown work operating systems.',
        'tools': ['asana', 'monday', 'clickup', 'notion', 'trello',
                  'basecamp', 'linear', 'wrike', 'teamwork', 'smartsheet'],
    },
    'email-marketing': {
        'slug': 'email-marketing',
        'name': 'Email Marketing',
        'description': 'Platforms for sending newsletters, building automations, and growing your email list. The highest-ROI marketing channel for most SMBs.',
        'tools': ['mailchimp', 'convertkit', 'activecampaign', 'constant-contact', 'brevo',
                  'drip', 'mailerlite', 'campaign-monitor', 'klaviyo', 'beehiiv'],
    },
    'seo-tools': {
        'slug': 'seo-tools',
        'name': 'SEO Tools',
        'description': 'Software for keyword research, rank tracking, backlink analysis, and technical site audits. Essential for organic traffic growth.',
        'tools': ['semrush', 'ahrefs', 'moz', 'se-ranking', 'ubersuggest',
                  'surfer-seo', 'mangools', 'spyfu', 'serpstat', 'screaming-frog'],
    },
    'help-desk': {
        'slug': 'help-desk',
        'name': 'Help Desk',
        'description': 'Customer support platforms with ticketing, live chat, and knowledge bases. Keep your customers happy without drowning in emails.',
        'tools': ['zendesk', 'freshdesk', 'intercom', 'help-scout', 'hubspot-service',
                  'zoho-desk', 'liveagent', 'happyfox', 'kayako', 'groove-helpdesk'],
    },
    'ai-sdr': {
        'slug': 'ai-sdr',
        'name': 'AI SDR',
        'description': 'AI-powered tools that automate outbound prospecting. From autonomous AI agents that write and send emails to coaching tools that make human reps sharper.',
        'tools': ['11x', 'artisan', 'aisdr', 'regie-ai', 'amplemarket',
                  'lavender', 'smartlead', 'salesrobot', 'nooks', 'outplay'],
    },
    'sales-engagement': {
        'slug': 'sales-engagement',
        'name': 'Sales Engagement',
        'description': 'Platforms for orchestrating multi-channel outbound sequences. Email, phone, LinkedIn, and task automation for sales teams running structured outreach.',
        'tools': ['outreach', 'salesloft', 'apollo', 'instantly', 'reply-io',
                  'mixmax', 'mailshake', 'woodpecker', 'lemlist', 'yesware'],
    },
    'conversation-intelligence': {
        'slug': 'conversation-intelligence',
        'name': 'Conversation Intelligence',
        'description': 'Tools that record, transcribe, and analyze sales calls. Surface coaching insights, deal risks, and competitive mentions automatically.',
        'tools': ['gong', 'chorus', 'clari', 'sybill', 'fireflies',
                  'otter-ai', 'avoma', 'fathom', 'jiminny', 'modjo'],
    },
    'data-enrichment': {
        'slug': 'data-enrichment',
        'name': 'Data Enrichment',
        'description': 'Platforms that find and verify contact data. Email addresses, phone numbers, firmographics, and intent signals for outbound prospecting.',
        'tools': ['zoominfo', 'clay', 'clearbit', 'lusha', 'cognism',
                  'seamless-ai', 'uplead', 'rocketreach', 'leadiq', 'kaspr'],
    },
}


# =============================================================================
# CRM TOOLS (10)
# =============================================================================

T("hubspot", "HubSpot CRM", "crm", "https://www.hubspot.com", 8.9,
  "The best free CRM on the market. Generous free tier, intuitive UI, and a massive ecosystem. The paid tiers get expensive fast, but the free version alone beats most paid competitors.",
  "SMBs who want a CRM they can start using today without paying a dime",
  "Free / $20/mo", "free",
  ["Best free tier in the CRM market", "Incredibly intuitive interface", "Massive integration ecosystem"],
  ["Paid tiers get expensive quickly", "Per-seat pricing adds up for larger teams", "Some features locked behind top tiers"],
  ["Contact management", "Deal pipeline", "Email tracking", "Meeting scheduler", "Live chat", "Reporting dashboard"],
  [("Free", "$0"), ("Starter", "$20/mo"), ("Professional", "$500/mo"), ("Enterprise", "$1,200/mo")],
  {"ease_of_use": 9.5, "value": 9.0, "features": 8.5, "support": 8.0},
  sultans_pick=True)

T("salesforce", "Salesforce", "crm", "https://www.salesforce.com", 7.8,
  "The 800-pound gorilla of CRM. Infinitely customizable, deeply powerful, and overkill for 90% of SMBs. You will need an admin. You will pay for consultants. You will wonder if it was worth it.",
  "Companies with 50+ reps and a dedicated Salesforce admin",
  "$25/user/mo", "premium",
  ["Infinitely customizable", "Largest third-party app ecosystem", "Scales to any team size"],
  ["Steep learning curve, you need a dedicated admin", "Expensive with add-ons", "UI feels dated compared to modern CRMs"],
  ["Contact & account management", "Opportunity tracking", "Workflow automation", "Custom objects", "Einstein AI", "AppExchange marketplace"],
  [("Essentials", "$25/user/mo"), ("Professional", "$80/user/mo"), ("Enterprise", "$165/user/mo"), ("Unlimited", "$330/user/mo")],
  {"ease_of_use": 5.5, "value": 6.0, "features": 9.5, "support": 7.0})

T("pipedrive", "Pipedrive", "crm", "https://www.pipedrive.com", 8.2,
  "A CRM built by salespeople, for salespeople. The visual pipeline is the best in the business. Lacks the depth of HubSpot or Salesforce, but that simplicity is the whole point.",
  "Small sales teams (2-20 reps) who want a pipeline-focused CRM",
  "$14/user/mo", "budget",
  ["Best visual pipeline in the market", "Clean, focused interface", "Good mobile app"],
  ["Marketing features are basic", "Reporting less powerful than HubSpot", "No free tier"],
  ["Visual pipeline", "Email integration", "Activity tracking", "Lead management", "Workflow automation", "Mobile app"],
  [("Essential", "$14/user/mo"), ("Advanced", "$39/user/mo"), ("Professional", "$49/user/mo"), ("Power", "$64/user/mo")],
  {"ease_of_use": 9.0, "value": 8.5, "features": 7.5, "support": 7.5})

T("close", "Close", "crm", "https://www.close.com", 8.0,
  "A CRM with a built-in power dialer, SMS, and email sequences. If your sales process runs on cold calls, Close is built for exactly that workflow.",
  "Inside sales teams running high-volume outbound",
  "$49/user/mo", "mid",
  ["Built-in calling, SMS, and email", "Designed for outbound sales", "Fast, modern interface"],
  ["More expensive than Pipedrive", "Less useful for non-phone-heavy teams", "Smaller integration ecosystem"],
  ["Built-in dialer", "Email sequences", "SMS messaging", "Pipeline management", "Power dialer", "Call coaching"],
  [("Startup", "$49/user/mo"), ("Professional", "$99/user/mo"), ("Enterprise", "$139/user/mo")],
  {"ease_of_use": 8.0, "value": 7.5, "features": 8.0, "support": 8.0})

T("freshsales", "Freshsales", "crm", "https://www.freshworks.com/crm/sales/", 7.5,
  "Part of the Freshworks suite. Solid mid-range CRM with decent AI features. Good value if you already use Freshdesk or Freshchat, but nothing that stands out on its own.",
  "Teams already using Freshworks products",
  "Free / $9/user/mo", "budget",
  ["Affordable entry point", "Built-in phone and email", "AI lead scoring (Freddy)"],
  ["AI features overpromised vs. delivered", "UI can feel cluttered", "Less polished than Pipedrive"],
  ["Contact management", "Deal pipeline", "Built-in phone", "AI scoring", "Workflow automation", "Territory management"],
  [("Free", "$0"), ("Growth", "$9/user/mo"), ("Pro", "$39/user/mo"), ("Enterprise", "$59/user/mo")],
  {"ease_of_use": 7.5, "value": 8.0, "features": 7.0, "support": 7.0})

T("zoho-crm", "Zoho CRM", "crm", "https://www.zoho.com/crm/", 7.3,
  "Feature-rich and affordable, but the UI feels like it was designed by committee. The free tier covers up to 3 users. If you can tolerate the interface, the value is hard to beat.",
  "Budget-conscious teams who prioritize features over polish",
  "Free / $14/user/mo", "budget",
  ["Very affordable for what you get", "Free tier for up to 3 users", "Part of massive Zoho ecosystem"],
  ["UI feels outdated and cluttered", "Steep learning curve", "Support can be slow"],
  ["Contact management", "Sales automation", "Analytics", "Multichannel communication", "Canvas design studio", "AI assistant (Zia)"],
  [("Free", "$0 (3 users)"), ("Standard", "$14/user/mo"), ("Professional", "$23/user/mo"), ("Enterprise", "$40/user/mo")],
  {"ease_of_use": 6.0, "value": 8.5, "features": 8.0, "support": 6.0})

T("copper", "Copper", "crm", "https://www.copper.com", 7.0,
  "A CRM that lives inside Google Workspace. If your team runs on Gmail and Google Calendar, Copper syncs everything automatically. Outside of Google, it has limited value.",
  "Google Workspace-heavy teams who hate switching between apps",
  "$23/user/mo", "budget",
  ["Seamless Google Workspace integration", "Auto-captures emails and contacts", "Clean, modern UI"],
  ["Useless without Google Workspace", "Limited customization", "Missing features at lower tiers"],
  ["Gmail integration", "Auto-contact creation", "Pipeline management", "Task automation", "Reporting", "Google Calendar sync"],
  [("Basic", "$23/user/mo"), ("Professional", "$59/user/mo"), ("Business", "$99/user/mo")],
  {"ease_of_use": 8.5, "value": 6.5, "features": 6.5, "support": 7.0})

T("monday-sales-crm", "Monday Sales CRM", "crm", "https://www.monday.com/crm", 7.2,
  "Monday.com repackaged its project management platform as a CRM. It works surprisingly well for teams already on Monday, but dedicated CRMs offer deeper sales functionality.",
  "Teams already using Monday.com who need basic CRM features",
  "$12/seat/mo", "budget",
  ["Familiar if you use Monday.com", "Highly visual and customizable", "Good for non-traditional sales workflows"],
  ["Sales-specific features feel bolted on", "Not as deep as dedicated CRMs", "Per-seat pricing adds up"],
  ["Custom pipelines", "Email tracking", "Activity management", "Automations", "Dashboards", "Integrations"],
  [("Basic", "$12/seat/mo"), ("Standard", "$17/seat/mo"), ("Pro", "$28/seat/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.0, "value": 7.0, "features": 6.5, "support": 7.0})

T("nutshell", "Nutshell", "crm", "https://www.nutshell.com", 6.8,
  "A straightforward CRM that does the basics well. Email marketing, pipeline tracking, and contact management in one tool. Lacks the power features of larger competitors.",
  "Very small teams wanting CRM + email marketing in one simple tool",
  "$16/user/mo", "budget",
  ["Simple and quick to set up", "Built-in email marketing", "Good customer support"],
  ["Limited customization", "Feature set is basic", "Reporting is shallow"],
  ["Contact management", "Pipeline tracking", "Email marketing", "Reporting", "Web forms", "Team collaboration"],
  [("Foundation", "$16/user/mo"), ("Pro", "$42/user/mo"), ("Power AI", "$52/user/mo"), ("Enterprise", "$67/user/mo")],
  {"ease_of_use": 8.0, "value": 7.0, "features": 6.0, "support": 8.0})

T("less-annoying-crm", "Less Annoying CRM", "crm", "https://www.lessannoyingcrm.com", 7.4,
  "One price. One plan. No upsells. Does exactly what it promises: a simple, affordable CRM that stays out of your way. Refreshingly honest in a market full of bait-and-switch pricing.",
  "Solo founders and micro-teams who want zero complexity",
  "$15/user/mo", "budget",
  ["One simple price: no tiers, no upsells", "Incredibly easy to learn", "Top-tier customer support"],
  ["Missing advanced features (automation, AI)", "No built-in email marketing", "Limited integrations"],
  ["Contact management", "Pipeline tracking", "Calendar", "Task management", "Email logging", "Custom fields"],
  [("Simple Pricing", "$15/user/mo")],
  {"ease_of_use": 9.5, "value": 8.5, "features": 5.0, "support": 9.5})


# =============================================================================
# PROJECT MANAGEMENT TOOLS (10)
# =============================================================================

T("asana", "Asana", "project-management", "https://www.asana.com", 8.4,
  "The best all-around project management tool for teams of 10-100. Strong workflows, good UI, and enough structure without being overbearing. The free tier is solid for small teams.",
  "Growing teams that need structure without rigidity",
  "Free / $10.99/user/mo", "budget",
  ["Best workflow automation in the category", "Clean, intuitive interface", "Generous free tier (up to 10 users)"],
  ["Gets expensive at scale", "Can feel slow with large projects", "Portfolio features locked behind Business tier"],
  ["Task management", "Timeline view", "Workflow builder", "Goals & portfolios", "Custom fields", "100+ integrations"],
  [("Personal", "$0"), ("Starter", "$10.99/user/mo"), ("Advanced", "$24.99/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.5, "value": 8.0, "features": 8.5, "support": 7.5},
  sultans_pick=True)

T("monday", "Monday.com", "project-management", "https://www.monday.com", 8.1,
  "The most visual project management platform. Color-coded boards make status tracking effortless. Great for non-technical teams, but the pricing model (minimum 3 seats) annoys solopreneurs.",
  "Non-technical teams who want visual project tracking",
  "$9/seat/mo (3-seat min)", "budget",
  ["Most visually appealing PM tool", "Highly customizable dashboards", "Strong automation features"],
  ["3-seat minimum on all plans", "Can feel overwhelming with too many boards", "Add-ons cost extra"],
  ["Visual boards", "Gantt charts", "Automations", "Dashboards", "Time tracking", "Integrations"],
  [("Basic", "$9/seat/mo"), ("Standard", "$12/seat/mo"), ("Pro", "$19/seat/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.5, "value": 7.5, "features": 8.0, "support": 7.0})

T("clickup", "ClickUp", "project-management", "https://www.clickup.com", 7.8,
  "Tries to be everything: project management, docs, whiteboards, chat, time tracking. It mostly succeeds, but the UI can buckle under its own ambition. The free plan is the most generous in the category.",
  "Teams who want one tool to replace everything",
  "Free / $7/user/mo", "free",
  ["Most generous free plan", "All-in-one: docs, whiteboards, chat", "Incredible feature density for the price"],
  ["UI can feel cluttered and slow", "Too many features can overwhelm new users", "Mobile app lags behind desktop"],
  ["Task management", "Docs", "Whiteboards", "Time tracking", "Goals", "Custom views"],
  [("Free Forever", "$0"), ("Unlimited", "$7/user/mo"), ("Business", "$12/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.5, "value": 9.0, "features": 9.0, "support": 6.5})

T("notion", "Notion", "project-management", "https://www.notion.so", 7.9,
  "A beautiful, flexible workspace for docs, wikis, and project tracking. Excels as a knowledge base. The project management features work but are a step behind dedicated PM tools.",
  "Small teams who value documentation as much as task management",
  "Free / $8/user/mo", "free",
  ["Strongest docs and wikis in the category", "Beautiful, flexible interface", "Strong template ecosystem"],
  ["Project management is secondary to docs", "No native time tracking or Gantt charts", "Can become disorganized without discipline"],
  ["Pages & databases", "Kanban boards", "Timeline view", "Wikis", "AI assistant", "Integrations"],
  [("Free", "$0"), ("Plus", "$8/user/mo"), ("Business", "$15/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.5, "value": 8.5, "features": 7.5, "support": 6.5})

T("trello", "Trello", "project-management", "https://www.trello.com", 7.0,
  "The original kanban board. Dead simple, easy to learn, and free for basic use. Outgrown by any team with more than a handful of projects, but still the fastest way to get started.",
  "Solopreneurs and tiny teams with simple project needs",
  "Free / $5/user/mo", "free",
  ["Simplest PM tool to learn", "Free tier handles basic needs", "Excellent mobile app"],
  ["Limited to kanban (no Gantt, timeline)", "Power-Ups add up in cost", "Outgrown quickly by growing teams"],
  ["Kanban boards", "Cards & checklists", "Power-Ups", "Butler automation", "Calendar view", "Mobile app"],
  [("Free", "$0"), ("Standard", "$5/user/mo"), ("Premium", "$10/user/mo"), ("Enterprise", "$17.50/user/mo")],
  {"ease_of_use": 9.5, "value": 7.5, "features": 5.5, "support": 6.0})

T("basecamp", "Basecamp", "project-management", "https://www.basecamp.com", 6.5,
  "Opinionated and proud of it. Flat monthly pricing, built-in chat, and a deliberate lack of features other tools treat as essential (no Gantt charts, no time tracking). You either love it or leave it.",
  "Teams who buy into Basecamp's less-is-more philosophy",
  "$15/user/mo", "budget",
  ["Flat, predictable pricing", "Built-in team chat", "Refreshingly simple"],
  ["Missing features most teams expect (Gantt, time tracking)", "Opinionated workflow doesn't fit everyone", "Limited integrations"],
  ["To-dos", "Message boards", "Chat (Campfire)", "Schedules", "Docs & files", "Check-ins"],
  [("Basecamp", "$15/user/mo"), ("Pro Unlimited", "$299/mo flat")],
  {"ease_of_use": 8.5, "value": 7.0, "features": 5.0, "support": 7.5})

T("linear", "Linear", "project-management", "https://www.linear.app", 8.6,
  "The fastest project management tool you will ever use. Built for software teams, optimized for keyboard shortcuts, and engineered for speed. If you ship software, Linear is the right choice.",
  "Engineering and product teams who care about speed and craft",
  "Free / $8/user/mo", "free",
  ["The fastest PM UI on the market", "Built for software development workflows", "Beautiful, opinionated design"],
  ["Only useful for software teams", "Limited outside of issue tracking", "Fewer integrations than Asana/Monday"],
  ["Issue tracking", "Cycles & sprints", "Roadmaps", "Project views", "Git integrations", "Triage"],
  [("Free", "$0 (up to 250 issues)"), ("Standard", "$8/user/mo"), ("Plus", "$14/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 9.0, "value": 8.5, "features": 7.5, "support": 7.5})

T("wrike", "Wrike", "project-management", "https://www.wrike.com", 7.2,
  "Enterprise-grade project management with strong resource planning and Gantt charts. Powerful but complex. Smaller teams will find it overwhelming; large teams will appreciate the depth.",
  "Mid-market and enterprise teams with complex project needs",
  "Free / $9.80/user/mo", "mid",
  ["Strong resource management", "Good Gantt charts and timelines", "Enterprise-grade permissions"],
  ["Steep learning curve", "UI feels heavy", "Gets expensive with add-ons"],
  ["Gantt charts", "Resource management", "Custom workflows", "Time tracking", "Proofing & approval", "Cross-tagging"],
  [("Free", "$0"), ("Team", "$9.80/user/mo"), ("Business", "$24.80/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.0, "value": 7.0, "features": 8.5, "support": 7.0})

T("teamwork", "Teamwork", "project-management", "https://www.teamwork.com", 6.9,
  "Built specifically for agencies and client services teams. Billable time tracking, client permissions, and project templates tailored to the agency workflow.",
  "Agencies managing multiple client projects with billable hours",
  "Free / $5.99/user/mo", "budget",
  ["Built for agency workflows", "Good time tracking and billing", "Client-facing permissions"],
  ["Less versatile than Asana or Monday", "UI feels dated", "Limited appeal outside agencies"],
  ["Project tracking", "Time tracking", "Client permissions", "Templates", "Resource scheduling", "Invoicing integrations"],
  [("Free", "$0 (5 users)"), ("Deliver", "$5.99/user/mo"), ("Grow", "$9.99/user/mo"), ("Scale", "$19.99/user/mo")],
  {"ease_of_use": 7.0, "value": 7.5, "features": 7.0, "support": 7.5})

T("smartsheet", "Smartsheet", "project-management", "https://www.smartsheet.com", 7.0,
  "A spreadsheet that grew into a project management platform. If your team thinks in rows and columns, Smartsheet feels natural. If they don't, everything feels clunky.",
  "Teams migrating from Excel-based project tracking",
  "$9/user/mo", "budget",
  ["Familiar spreadsheet interface", "Strong automation capabilities", "Good for data-heavy project tracking"],
  ["Feels like a spreadsheet, not a PM tool", "Mobile experience is poor", "Confusing pricing with sheets/user limits"],
  ["Grid view", "Gantt charts", "Automations", "Dashboards", "Forms", "Resource management"],
  [("Pro", "$9/user/mo"), ("Business", "$19/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.5, "value": 7.0, "features": 7.5, "support": 6.5})


# =============================================================================
# EMAIL MARKETING TOOLS (10)
# =============================================================================

T("mailchimp", "Mailchimp", "email-marketing", "https://www.mailchimp.com", 7.4,
  "The household name in email marketing. The free plan got gutted, the pricing got aggressive, and Intuit's acquisition added bloat. Still works, but the value equation has shifted.",
  "Small businesses wanting a familiar, established email platform",
  "Free / $13/mo", "budget",
  ["Brand recognition, everyone knows it", "Decent template builder", "Good analytics and A/B testing"],
  ["Free plan severely limited (500 contacts)", "Pricing jumps are steep", "Charges for unsubscribed contacts"],
  ["Email builder", "Automations", "Landing pages", "A/B testing", "Analytics", "100+ integrations"],
  [("Free", "$0 (500 contacts)"), ("Essentials", "$13/mo"), ("Standard", "$20/mo"), ("Premium", "$350/mo")],
  {"ease_of_use": 7.5, "value": 6.0, "features": 7.5, "support": 6.5})

T("convertkit", "Kit (ConvertKit)", "email-marketing", "https://kit.com", 8.3,
  "Built for creators, not corporations. The best email platform for newsletters, digital products, and audience building. Simple automations, excellent deliverability, and a creator-first business model.",
  "Creators, bloggers, and solopreneurs building an audience",
  "Free / $25/mo", "budget",
  ["Built specifically for creators", "Excellent email deliverability", "Visual automation builder"],
  ["Limited design options for emails", "No advanced segmentation at lower tiers", "More expensive than MailerLite for basic sending"],
  ["Visual automations", "Landing pages", "Digital product sales", "Subscriber tagging", "Creator network", "Paid newsletters"],
  [("Newsletter", "$0 (10K subscribers)"), ("Creator", "$25/mo"), ("Creator Pro", "$50/mo")],
  {"ease_of_use": 8.5, "value": 8.0, "features": 7.5, "support": 8.5},
  sultans_pick=True)

T("activecampaign", "ActiveCampaign", "email-marketing", "https://www.activecampaign.com", 8.5,
  "The most powerful email automation platform for SMBs. The automation builder handles complex multi-step workflows that would require enterprise tools elsewhere. Steeper learning curve, bigger payoff.",
  "Marketing teams who need sophisticated automation workflows",
  "$29/mo", "mid",
  ["Most powerful automation builder in the category", "Excellent deliverability", "CRM included on most plans"],
  ["Steeper learning curve than simpler tools", "Template design feels basic", "Pricing scales with contacts"],
  ["Advanced automations", "CRM", "Predictive sending", "Split automations", "Site tracking", "Machine learning"],
  [("Starter", "$29/mo"), ("Plus", "$49/mo"), ("Pro", "$149/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.0, "value": 8.0, "features": 9.0, "support": 8.0})

T("constant-contact", "Constant Contact", "email-marketing", "https://www.constantcontact.com", 6.3,
  "A legacy email platform coasting on brand recognition. The event management feature is useful, but the core email product is outclassed by newer competitors at every price point.",
  "Local businesses and nonprofits running event-driven email campaigns",
  "$12/mo", "budget",
  ["Event management integration", "Good for local businesses", "Long track record"],
  ["Overpriced for what you get", "Automation is basic", "Interface feels dated"],
  ["Email builder", "Event marketing", "Social posting", "Contact management", "Reporting", "Landing pages"],
  [("Lite", "$12/mo"), ("Standard", "$35/mo"), ("Premium", "$80/mo")],
  {"ease_of_use": 7.0, "value": 5.0, "features": 6.0, "support": 7.0})

T("brevo", "Brevo (Sendinblue)", "email-marketing", "https://www.brevo.com", 7.6,
  "All-in-one marketing platform with email, SMS, chat, and CRM at a fraction of HubSpot's price. The email builder is solid, and the pricing model (based on emails sent, not contacts) is founder-friendly.",
  "Budget-conscious teams wanting email + SMS + CRM without HubSpot pricing",
  "Free / $25/mo", "budget",
  ["Pricing based on emails sent, not contacts", "Includes SMS, chat, and CRM", "Generous free tier (300 emails/day)"],
  ["Deliverability historically inconsistent", "Automation less powerful than ActiveCampaign", "Brand awareness lower than competitors"],
  ["Email campaigns", "SMS marketing", "Chat", "CRM", "Automations", "Transactional email"],
  [("Free", "$0 (300 emails/day)"), ("Starter", "$25/mo"), ("Business", "$65/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.5, "value": 8.5, "features": 7.5, "support": 7.0})

T("drip", "Drip", "email-marketing", "https://www.drip.com", 7.8,
  "E-commerce email marketing done right. Deep Shopify and WooCommerce integrations, pre-built revenue-focused automations, and segmentation based on purchase behavior.",
  "E-commerce stores on Shopify or WooCommerce",
  "$39/mo", "mid",
  ["Deep e-commerce integrations", "Revenue-attributed reporting", "Pre-built e-commerce automations"],
  ["Only useful for e-commerce", "More expensive than generalist tools", "Limited outside of its niche"],
  ["E-commerce automations", "Revenue attribution", "Shopify integration", "Behavioral segmentation", "A/B testing", "Dynamic content"],
  [("Standard", "$39/mo (2,500 contacts)")],
  {"ease_of_use": 7.5, "value": 7.0, "features": 8.0, "support": 7.5})

T("mailerlite", "MailerLite", "email-marketing", "https://www.mailerlite.com", 8.0,
  "The best value in email marketing. Clean interface, solid deliverability, and a useful free tier with 1,000 subscribers. Does 80% of what ConvertKit does at 60% of the price.",
  "Bootstrapped founders and small teams who want great email without the premium price",
  "Free / $9/mo", "free",
  ["Best value in the category", "Clean, easy-to-use interface", "Good free tier (1,000 subscribers)"],
  ["Fewer advanced features than ActiveCampaign", "Account approval process can be strict", "Limited CRM functionality"],
  ["Email builder", "Automations", "Landing pages", "Websites", "A/B testing", "Paid newsletter support"],
  [("Free", "$0 (1K subscribers)"), ("Growing Business", "$9/mo"), ("Advanced", "$18/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 9.0, "value": 9.0, "features": 7.0, "support": 7.5})

T("campaign-monitor", "Campaign Monitor", "email-marketing", "https://www.campaignmonitor.com", 6.5,
  "Premium email templates and a solid visual builder. Agencies love the client management features. Everyone else should look at cheaper alternatives first.",
  "Agencies managing email campaigns for multiple clients",
  "$9/mo", "budget",
  ["Beautiful email templates", "Good agency/client features", "Link review and spam testing"],
  ["Expensive for the feature set", "Automation is basic", "No free tier"],
  ["Email builder", "Journey builder", "Templates", "Analytics", "Transactional email", "Client management"],
  [("Lite", "$9/mo"), ("Essentials", "$29/mo"), ("Premier", "$149/mo")],
  {"ease_of_use": 7.5, "value": 5.5, "features": 6.5, "support": 6.5})

T("klaviyo", "Klaviyo", "email-marketing", "https://www.klaviyo.com", 8.2,
  "The dominant email + SMS platform for e-commerce. Deep Shopify integration, powerful segmentation based on purchase data, and predictive analytics. The pricing climbs fast with your contact list.",
  "Shopify stores doing $1M+ in revenue who need advanced segmentation",
  "Free / $20/mo", "premium",
  ["Best Shopify email integration", "Powerful purchase-based segmentation", "Predictive analytics"],
  ["Expensive as your list grows", "Steep learning curve for advanced features", "Primarily e-commerce focused"],
  ["Email campaigns", "SMS", "Shopify integration", "Predictive analytics", "Segmentation", "Product recommendations"],
  [("Free", "$0 (250 contacts)"), ("Email", "$20/mo"), ("Email + SMS", "$35/mo")],
  {"ease_of_use": 7.0, "value": 7.5, "features": 8.5, "support": 7.0})

T("beehiiv", "Beehiiv", "email-marketing", "https://www.beehiiv.com", 8.0,
  "The newsletter platform built by ex-Morning Brew. Referral programs, ad monetization, and growth tools baked in. If you are building a media business around email, Beehiiv is purpose-built for it.",
  "Newsletter operators building a media business",
  "Free / $42/mo", "mid",
  ["Built-in referral program", "Ad network monetization", "Custom website included"],
  ["Only useful for newsletters", "Limited automation compared to ConvertKit", "Young platform, still maturing"],
  ["Newsletter editor", "Referral program", "Ad network", "Custom website", "Analytics", "Recommendations"],
  [("Launch", "$0 (2,500 subscribers)"), ("Scale", "$42/mo"), ("Max", "$100/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.0, "value": 8.0, "features": 7.5, "support": 7.0})


# =============================================================================
# SEO TOOLS (10)
# =============================================================================

T("semrush", "Semrush", "seo-tools", "https://www.semrush.com", 8.7,
  "The most complete SEO toolkit on the market. Keyword research, rank tracking, site audits, backlink analysis, and content tools all in one. Expensive, but it replaces 3-4 other tools.",
  "Marketing teams and agencies who need an all-in-one SEO platform",
  "$129.95/mo", "premium",
  ["Most comprehensive feature set", "Excellent competitive analysis", "Strong content marketing tools"],
  ["Expensive entry point", "Interface can feel overwhelming", "Keyword difficulty scores run high"],
  ["Keyword research", "Rank tracking", "Site audit", "Backlink analysis", "Content tools", "PPC research"],
  [("Pro", "$129.95/mo"), ("Guru", "$249.95/mo"), ("Business", "$499.95/mo")],
  {"ease_of_use": 7.0, "value": 8.0, "features": 9.5, "support": 7.5},
  sultans_pick=True)

T("ahrefs", "Ahrefs", "seo-tools", "https://www.ahrefs.com", 8.6,
  "The best backlink database in the industry and a keyword research tool that rivals Semrush. The site audit is excellent. Slightly less breadth than Semrush, but many SEOs prefer it.",
  "SEO professionals who prioritize backlink analysis and keyword research",
  "$99/mo", "mid",
  ["Best backlink index in the industry", "Content Explorer for content research", "Excellent keyword difficulty metric"],
  ["No free trial (paid only)", "Rank tracking on basic plan is limited", "Content tools less developed than Semrush"],
  ["Site Explorer", "Keyword Explorer", "Content Explorer", "Rank Tracker", "Site Audit", "Backlink analysis"],
  [("Lite", "$99/mo"), ("Standard", "$199/mo"), ("Advanced", "$399/mo"), ("Enterprise", "$999/mo")],
  {"ease_of_use": 7.5, "value": 7.5, "features": 9.0, "support": 7.0})

T("moz", "Moz Pro", "seo-tools", "https://www.moz.com", 7.0,
  "The OG of SEO tools. Domain Authority is still the industry standard metric. The toolset is solid but has fallen behind Semrush and Ahrefs in depth and data freshness.",
  "Teams who value Moz's educational content and community alongside their tools",
  "$99/mo", "mid",
  ["Domain Authority is the industry standard", "Strong SEO community and learning resources", "Good local SEO tools (Moz Local)"],
  ["Data freshness lags behind Ahrefs/Semrush", "Smaller keyword and backlink databases", "Interface feels dated"],
  ["Keyword Explorer", "Link Explorer", "Rank tracking", "Site audit", "On-page grader", "SERP analysis"],
  [("Standard", "$99/mo"), ("Medium", "$179/mo"), ("Large", "$299/mo"), ("Premium", "$599/mo")],
  {"ease_of_use": 7.5, "value": 6.5, "features": 7.0, "support": 7.0})

T("se-ranking", "SE Ranking", "seo-tools", "https://www.seranking.com", 7.8,
  "The best Semrush alternative for budget-conscious teams. Covers keyword research, rank tracking, and site audits at a fraction of Semrush's price. Database is smaller but sufficient for most SMBs.",
  "SMBs who want Semrush-like features without the Semrush price tag",
  "$44/mo", "mid",
  ["Fraction of Semrush/Ahrefs pricing", "Competitive feature set for the price", "Good rank tracking accuracy"],
  ["Smaller keyword database", "Less accurate traffic estimates", "Missing some advanced features"],
  ["Keyword research", "Rank tracking", "Site audit", "Backlink checker", "Competitor analysis", "Content marketing tools"],
  [("Essential", "$44/mo"), ("Pro", "$87.20/mo"), ("Business", "$191.20/mo")],
  {"ease_of_use": 8.0, "value": 8.5, "features": 7.5, "support": 7.0})

T("ubersuggest", "Ubersuggest", "seo-tools", "https://www.neilpatel.com/ubersuggest/", 6.2,
  "Neil Patel's SEO tool. The lifetime deal is appealing, and the basics work. Data accuracy and depth fall short of any paid competitor. You get what you pay for.",
  "Beginners learning SEO who want a cheap starting point",
  "$12/mo", "budget",
  ["Cheapest paid option", "Lifetime deal available", "Simple interface for beginners"],
  ["Data accuracy is questionable", "Limited backlink database", "Feature depth is shallow"],
  ["Keyword suggestions", "Content ideas", "Rank tracking", "Site audit", "Backlink data", "Traffic analysis"],
  [("Individual", "$12/mo"), ("Business", "$20/mo"), ("Enterprise", "$40/mo")],
  {"ease_of_use": 8.0, "value": 6.0, "features": 5.0, "support": 5.0})

T("surfer-seo", "Surfer SEO", "seo-tools", "https://www.surferseo.com", 7.5,
  "The leading on-page optimization tool. Analyzes top-ranking pages and gives you a content score with specific recommendations. Excellent for content teams; limited as a standalone SEO tool.",
  "Content teams optimizing articles for search rankings",
  "$89/mo", "mid",
  ["Best on-page content optimization", "SERP Analyzer with actionable insights", "Content planner for topic clusters"],
  ["Only handles on-page SEO", "Needs another tool for backlinks/rank tracking", "AI content writer is mediocre"],
  ["Content Editor", "SERP Analyzer", "Content Planner", "Keyword research", "Audit tool", "AI writing"],
  [("Essential", "$89/mo"), ("Scale", "$129/mo"), ("Scale AI", "$219/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.0, "value": 7.0, "features": 7.0, "support": 7.0})

T("mangools", "Mangools", "seo-tools", "https://www.mangools.com", 7.3,
  "Five simple SEO tools bundled together. KWFinder is the standout: one of the best keyword research UIs available. Lacks the depth of bigger tools but perfect for simpler SEO workflows.",
  "Bloggers and small sites who mostly need keyword research",
  "$29/mo", "budget",
  ["KWFinder has excellent keyword difficulty scoring", "Clean, simple interface", "Affordable all-in-one bundle"],
  ["Small backlink database", "Limited rank tracking", "Not suitable for agencies or large sites"],
  ["KWFinder", "SERPChecker", "SERPWatcher", "LinkMiner", "SiteProfiler"],
  [("Entry", "$29/mo"), ("Basic", "$44/mo"), ("Premium", "$89/mo")],
  {"ease_of_use": 9.0, "value": 8.0, "features": 6.5, "support": 7.0})

T("spyfu", "SpyFu", "seo-tools", "https://www.spyfu.com", 6.8,
  "Specializes in competitor keyword and PPC intelligence. Shows you every keyword your competitors rank for and every ad they run. Great for competitive research, limited for other SEO tasks.",
  "PPC managers and SEOs focused on competitive intelligence",
  "$39/mo", "mid",
  ["Excellent competitive keyword data", "Shows competitor PPC spend and ads", "Unlimited results on all plans"],
  ["Weak outside of competitive analysis", "Data accuracy varies", "Interface feels old"],
  ["Competitor keyword tracking", "PPC research", "Backlink analysis", "Rank tracking", "SERP analysis", "Domain comparison"],
  [("Basic", "$39/mo"), ("Professional", "$79/mo"), ("Team", "$299/mo")],
  {"ease_of_use": 7.0, "value": 7.0, "features": 6.5, "support": 6.0})

T("serpstat", "Serpstat", "seo-tools", "https://www.serpstat.com", 6.5,
  "Ukrainian-built SEO platform with decent keyword research and site auditing. Positioned as a budget alternative to Semrush. The data quality doesn't quite match the marketing claims.",
  "Budget-conscious teams in European markets",
  "$59/mo", "mid",
  ["Affordable vs. Semrush/Ahrefs", "Decent site audit tool", "Good for local European SEO"],
  ["Smaller database than competitors", "Data freshness can lag", "Limited English-language support"],
  ["Keyword research", "Rank tracking", "Site audit", "Backlink analysis", "Competitor analysis", "Content marketing"],
  [("Individual", "$59/mo"), ("Team", "$119/mo"), ("Agency", "$479/mo")],
  {"ease_of_use": 7.0, "value": 6.5, "features": 6.5, "support": 5.5})

T("screaming-frog", "Screaming Frog", "seo-tools", "https://www.screamingfrog.co.uk/seo-spider/", 8.0,
  "The industry-standard site crawler. Every technical SEO uses it. Desktop app that crawls your entire site and finds broken links, redirects, duplicate content, and metadata issues.",
  "Technical SEOs and developers doing site audits",
  "Free / $259/yr", "mid",
  ["Most thorough site crawler available", "Industry standard for technical SEO", "Free tier crawls up to 500 URLs"],
  ["Desktop-only (no cloud)", "Steep learning curve for non-technical users", "UI looks like it was built in 2005"],
  ["Site crawling", "Broken link detection", "Redirect chains", "Duplicate content", "Meta data analysis", "XML sitemap generation"],
  [("Free", "$0 (500 URLs)"), ("Paid", "$259/yr")],
  {"ease_of_use": 5.5, "value": 8.5, "features": 8.5, "support": 6.5})


# =============================================================================
# HELP DESK TOOLS (10)
# =============================================================================

T("zendesk", "Zendesk", "help-desk", "https://www.zendesk.com", 7.9,
  "The market leader in customer support. Mature, reliable, and deeply customizable. Also complex, expensive, and requires dedicated admin time. The right pick for teams outgrowing simpler tools.",
  "Growing support teams (10+ agents) who need enterprise-grade ticketing",
  "$19/agent/mo", "premium",
  ["Most mature help desk platform", "Massive integration ecosystem", "Strong reporting and analytics"],
  ["Complex setup and administration", "Gets expensive with add-ons", "UI modernization is slow"],
  ["Ticketing", "Live chat", "Knowledge base", "AI bot", "Reporting", "1,000+ integrations"],
  [("Support Team", "$19/agent/mo"), ("Suite Team", "$55/agent/mo"), ("Suite Professional", "$115/agent/mo"), ("Suite Enterprise", "$169/agent/mo")],
  {"ease_of_use": 6.5, "value": 6.5, "features": 9.0, "support": 7.0})

T("freshdesk", "Freshdesk", "help-desk", "https://www.freshdesk.com", 8.0,
  "The best Zendesk alternative. Same core features at a lower price point, with a more intuitive interface. The free tier supports up to 2 agents. The AI features (Freddy) are decent but not transformative.",
  "SMBs who want Zendesk-level features without Zendesk-level pricing",
  "Free / $15/agent/mo", "budget",
  ["Strong free tier (2 agents)", "More intuitive than Zendesk", "Good automation (Dispatch'r)"],
  ["AI features are overhyped", "Reporting less powerful than Zendesk", "Can feel limited at enterprise scale"],
  ["Ticketing", "Team inbox", "Knowledge base", "Automations", "Freddy AI", "Customer portal"],
  [("Free", "$0 (2 agents)"), ("Growth", "$15/agent/mo"), ("Pro", "$49/agent/mo"), ("Enterprise", "$79/agent/mo")],
  {"ease_of_use": 8.0, "value": 8.5, "features": 7.5, "support": 7.5},
  sultans_pick=True)

T("intercom", "Intercom", "help-desk", "https://www.intercom.com", 7.7,
  "The pioneer of chat-first customer support. Their AI chatbot (Fin) is one of the best in the industry. The pricing model is confusing and the costs add up fast with add-ons.",
  "SaaS companies who want AI-powered chat as the primary support channel",
  "$39/seat/mo", "premium",
  ["Best AI chatbot in the category (Fin)", "Excellent chat-first experience", "Strong product tours and onboarding"],
  ["Pricing is confusing and expensive", "Ticketing is secondary to chat", "Add-ons inflate costs quickly"],
  ["Chat widget", "Fin AI bot", "Inbox", "Product tours", "Help center", "Outbound messaging"],
  [("Essential", "$39/seat/mo"), ("Advanced", "$99/seat/mo"), ("Expert", "$139/seat/mo")],
  {"ease_of_use": 7.5, "value": 6.0, "features": 8.0, "support": 7.0})

T("help-scout", "Help Scout", "help-desk", "https://www.helpscout.com", 8.3,
  "Help desk that feels like email. No ticket numbers, no robotic auto-replies. Just clean, human support. The best choice for teams who believe customer support should feel personal.",
  "Small teams who want support to feel human, not corporate",
  "$20/user/mo", "budget",
  ["Feels like email, not a ticket system", "Excellent knowledge base (Docs)", "Strong for small teams"],
  ["Less powerful for high-volume support", "Limited reporting at lower tiers", "Fewer integrations than Zendesk"],
  ["Shared inbox", "Knowledge base", "Beacon widget", "Customer profiles", "Reporting", "Workflows"],
  [("Standard", "$20/user/mo"), ("Plus", "$40/user/mo"), ("Pro", "$65/user/mo")],
  {"ease_of_use": 9.0, "value": 8.0, "features": 7.5, "support": 9.0})

T("hubspot-service", "HubSpot Service Hub", "help-desk", "https://www.hubspot.com/products/service", 7.3,
  "HubSpot's help desk offering. Decent if you already use HubSpot CRM, but the service-specific features lag behind dedicated help desk tools. The free tier gives you basic ticketing.",
  "HubSpot CRM users who want support tools in the same ecosystem",
  "Free / $20/mo", "budget",
  ["Native HubSpot CRM integration", "Free tier includes basic ticketing", "Unified customer view"],
  ["Service features feel secondary", "Expensive at Professional tier", "Less capable than dedicated help desks"],
  ["Ticketing", "Knowledge base", "Live chat", "Customer portal", "Feedback surveys", "SLAs"],
  [("Free", "$0"), ("Starter", "$20/mo"), ("Professional", "$500/mo"), ("Enterprise", "$1,200/mo")],
  {"ease_of_use": 7.5, "value": 6.5, "features": 6.5, "support": 7.5})

T("zoho-desk", "Zoho Desk", "help-desk", "https://www.zoho.com/desk/", 7.0,
  "Affordable help desk from the Zoho ecosystem. Good feature set for the price, but the UI is a step behind Freshdesk. Best value if you are already invested in Zoho's suite.",
  "Teams using other Zoho products who want a unified ecosystem",
  "Free / $7/agent/mo", "free",
  ["Very affordable", "Good Zoho ecosystem integration", "AI assistant (Zia)"],
  ["UI lags behind Freshdesk", "Can feel clunky", "Limited outside Zoho ecosystem"],
  ["Ticketing", "Knowledge base", "AI assistant", "Community forums", "Telephony", "SLA management"],
  [("Free", "$0 (3 agents)"), ("Express", "$7/agent/mo"), ("Standard", "$14/agent/mo"), ("Professional", "$23/agent/mo")],
  {"ease_of_use": 6.5, "value": 8.0, "features": 7.0, "support": 6.5})

T("liveagent", "LiveAgent", "help-desk", "https://www.liveagent.com", 6.7,
  "Feature-packed help desk with a strong live chat widget and built-in call center. Tries to cover every channel. The UI reflects its age, but the functionality per dollar is solid.",
  "Teams wanting help desk + call center in one affordable platform",
  "$9/agent/mo", "budget",
  ["Built-in call center", "Fast live chat widget", "Good feature-to-price ratio"],
  ["Interface looks dated", "Setup can be complex", "Documentation could be better"],
  ["Ticketing", "Live chat", "Call center", "Knowledge base", "Social media integration", "Gamification"],
  [("Small", "$9/agent/mo"), ("Medium", "$29/agent/mo"), ("Large", "$49/agent/mo"), ("Enterprise", "$69/agent/mo")],
  {"ease_of_use": 6.0, "value": 7.5, "features": 7.5, "support": 6.5})

T("happyfox", "HappyFox", "help-desk", "https://www.happyfox.com", 6.5,
  "Mid-range help desk with clean UI and solid ticket management. Does the basics well but lacks the depth of Zendesk or the value of Freshdesk. A competent middle-of-the-road choice.",
  "Teams wanting a clean, no-frills help desk",
  "$29/agent/mo", "mid",
  ["Clean, organized interface", "Good ticket categorization", "Multi-brand support"],
  ["Pricing is mid-range with mid-range features", "Limited automation", "Smaller integration ecosystem"],
  ["Ticketing", "Knowledge base", "Canned responses", "Automations", "SLA management", "Reporting"],
  [("Mighty", "$29/agent/mo"), ("Fantastic", "$49/agent/mo"), ("Enterprise", "$69/agent/mo"), ("Enterprise Plus", "$89/agent/mo")],
  {"ease_of_use": 7.5, "value": 6.0, "features": 6.5, "support": 7.0})

T("kayako", "Kayako", "help-desk", "https://www.kayako.com", 5.8,
  "Once a strong contender, now struggling to keep up. The product has stagnated while competitors have innovated. Hard to recommend over Freshdesk or Help Scout at any price point.",
  "Existing Kayako users evaluating whether to migrate",
  "$15/agent/mo", "budget",
  ["Clean conversation view", "Affordable base pricing", "Self-service portal"],
  ["Product development has stagnated", "Missing modern features (AI, advanced automation)", "Support quality has declined"],
  ["Ticketing", "Live chat", "Help center", "Customer journey view", "Automations", "Reporting"],
  [("Essential", "$15/agent/mo"), ("Growth", "$30/agent/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.5, "value": 5.5, "features": 5.5, "support": 5.0})

T("groove-helpdesk", "Groove", "help-desk", "https://www.groovehq.com", 7.5,
  "A simple help desk built for small businesses. Shared inbox, knowledge base, and live chat without the complexity of enterprise tools. Gets out of your way and lets you focus on helping customers.",
  "Small teams (2-10 people) who want simple, affordable support",
  "$4.80/user/mo", "budget",
  ["Dead simple to set up and use", "Very affordable", "Good shared inbox experience"],
  ["Limited scalability", "Missing advanced features", "Reporting is basic"],
  ["Shared inbox", "Knowledge base", "Live chat", "Assignments & tags", "Collision detection", "Reporting"],
  [("Standard", "$4.80/user/mo"), ("Plus", "$9.60/user/mo"), ("Pro", "$15.60/user/mo")],
  {"ease_of_use": 9.0, "value": 8.5, "features": 6.0, "support": 8.0})


# =============================================================================
# AI SDR TOOLS (10)
# =============================================================================

T("11x", "11x", "ai-sdr", "https://www.11x.ai", 5.5,
  "Represents the AI SDR hype cycle at its peak. Fabricated customer testimonials, 75% churn within 3 months, and a $60K/yr minimum commitment. The AI outbound concept has merit. This execution doesn't justify the price or the risk.",
  "Well-funded teams with $60K+ to experiment and a human SDR team handling replies",
  "$5,000/mo", "premium",
  ["High-volume personalized outreach at scale", "Multi-channel prospecting (email + LinkedIn)", "Research-based personalization engine"],
  ["75% customer churn within 3 months", "Can't handle replies, still needs human SDRs", "$60K/yr minimum with 12-month lock-in"],
  ["AI email personalization", "LinkedIn automation", "Prospect research", "Multi-channel sequences", "CRM sync", "Custom AI training"],
  [("Standard", "$5,000/mo"), ("Growth", "$8,000/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.0, "value": 3.5, "features": 7.0, "support": 5.0})

T("artisan", "Artisan", "ai-sdr", "https://www.artisan.co", 7.2,
  "The best of a young and volatile category. Ava handles initial outreach well and the team is more transparent about what AI can and can't do. Still requires human oversight for replies and complex conversations, but the prospecting automation saves real SDR hours.",
  "B2B SaaS companies with a human SDR team that needs to scale outbound volume",
  "$2,000/mo", "premium",
  ["Better reply handling than most AI SDRs", "Transparent about AI limitations", "Solid email personalization"],
  ["Still needs human SDR backup for replies", "Expensive for unproven ROI", "Category is too young for long-term bets"],
  ["AI prospect research", "Personalized email writing", "Multi-step sequences", "LinkedIn integration", "Lead scoring", "CRM sync"],
  [("Starter", "$2,000/mo"), ("Growth", "$3,500/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.0, "value": 6.5, "features": 7.5, "support": 7.0})

T("aisdr", "AiSDR", "ai-sdr", "https://www.aisdr.com", 6.8,
  "A more affordable AI SDR option that gets the basics right. Handles prospect research and initial email outreach competently. The lower price point makes experimentation less painful, but you're still betting on a category that hasn't proven long-term value.",
  "SMBs testing AI outbound without a $5K/mo commitment",
  "$750/mo", "premium",
  ["Lower cost than 11x and Artisan", "Decent prospect research", "Quick setup"],
  ["Less sophisticated personalization than top-tier options", "Limited multi-channel support", "Smaller customer base means less proven"],
  ["AI email writing", "Prospect research", "Email sequences", "A/B testing", "CRM integrations", "Analytics"],
  [("Starter", "$750/mo"), ("Professional", "$1,500/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.0, "value": 7.0, "features": 6.5, "support": 6.5})

T("regie-ai", "Regie.ai", "ai-sdr", "https://www.regie.ai", 6.5,
  "Combines AI content generation with outbound sequencing. Better at writing sales copy than executing autonomous outreach. Useful if your SDR team's bottleneck is writing personalized emails, less useful if you want a fully autonomous AI agent.",
  "Sales teams wanting AI-assisted content creation alongside outbound automation",
  "Custom", "premium",
  ["Strong AI content generation", "Integrates with major sales engagement platforms", "Good for scaling personalization"],
  ["More content tool than autonomous SDR", "Complex pricing structure", "Requires existing engagement platform"],
  ["AI content generation", "Sequence writing", "Personalization at scale", "Content analytics", "Platform integrations", "Sales playbooks"],
  [("Pro", "Custom"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.5, "value": 6.0, "features": 7.0, "support": 6.5})

T("amplemarket", "Amplemarket", "ai-sdr", "https://www.amplemarket.com", 7.0,
  "An all-in-one AI outbound platform that combines prospecting data, AI writing, and multi-channel delivery. Does everything adequately, nothing exceptionally. The convenience of a single platform offsets the lack of top-tier depth in any single feature.",
  "B2B teams wanting a single platform for prospecting, sequencing, and AI writing",
  "Custom", "premium",
  ["All-in-one: data + sequencing + AI writing", "Multi-channel delivery", "Built-in prospect database"],
  ["Jack of all trades, master of none", "Custom pricing means no price transparency", "Less specialized than dedicated tools"],
  ["Prospect database", "AI email writer", "Multi-channel sequences", "Intent signals", "LinkedIn automation", "Analytics"],
  [("Growth", "Custom"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.0, "value": 6.5, "features": 7.5, "support": 7.0})

T("lavender", "Lavender", "ai-sdr", "https://www.lavender.ai", 7.8,
  "The practical choice in a hyped category. Instead of replacing your SDRs, Lavender makes them better. Real-time email coaching, data-backed suggestions, and measurable improvements in reply rates. At $29/mo per user, the ROI is obvious within weeks.",
  "Individual reps and small teams wanting to improve cold email response rates",
  "$29/mo", "budget",
  ["Real-time email scoring and coaching", "Data-backed writing suggestions", "Measurable reply rate improvement"],
  ["Email coaching only, not a full SDR replacement", "No built-in sending or sequencing", "Less useful for teams that don't do cold email"],
  ["Email scoring", "Writing assistant", "Reply rate analytics", "Personalization suggestions", "Team performance dashboard", "Gmail & Outlook integration"],
  [("Starter", "Free"), ("Individual", "$29/mo"), ("Team", "$49/mo/user"), ("Enterprise", "Custom")],
  {"ease_of_use": 9.0, "value": 8.5, "features": 7.0, "support": 8.0},
  sultans_pick=True)

T("smartlead", "Smartlead", "ai-sdr", "https://www.smartlead.ai", 7.5,
  "Cold email infrastructure done right. Unlimited mailbox rotation, AI warmup, and high-volume sending without deliverability headaches. The AI personalization is solid, and the pricing is aggressive. Best for teams sending thousands of cold emails monthly.",
  "Agencies and lead gen firms sending high-volume cold email",
  "$39/mo", "budget",
  ["Unlimited mailbox rotation", "AI warmup and deliverability tools", "Aggressive pricing for volume"],
  ["Email-only, no phone or LinkedIn", "UI is functional but not polished", "Support can be slow at lower tiers"],
  ["Unlimited mailboxes", "AI email warmup", "Sub-sequence logic", "AI personalization", "Unified inbox", "API + webhooks"],
  [("Basic", "$39/mo"), ("Pro", "$94/mo"), ("Custom", "$174/mo")],
  {"ease_of_use": 7.0, "value": 8.5, "features": 7.5, "support": 6.5})

T("salesrobot", "SalesRobot", "ai-sdr", "https://www.salesrobot.co", 6.0,
  "LinkedIn automation with AI message writing. Sends connection requests and follow-ups on autopilot. Gets the job done, but LinkedIn's crackdown on automation tools means you're always one policy update away from account restrictions.",
  "LinkedIn-first prospectors who want automated connection requests and follow-ups",
  "$99/mo", "mid",
  ["LinkedIn automation that mostly works", "AI-generated personalized messages", "Campaign management dashboard"],
  ["Constant risk of LinkedIn account restrictions", "Limited to LinkedIn + email", "AI personalization is hit-or-miss"],
  ["LinkedIn automation", "AI messaging", "Smart follow-ups", "Campaign analytics", "Email integration", "Team management"],
  [("Starter", "$99/mo"), ("Professional", "$179/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.5, "value": 5.5, "features": 6.5, "support": 5.5})

T("nooks", "Nooks", "ai-sdr", "https://www.nooks.ai", 7.0,
  "An AI-powered parallel dialer with a virtual sales floor. If your team's outbound motion runs on phone calls, Nooks dramatically increases connect rates by dialing multiple numbers simultaneously. The virtual sales floor feature keeps remote SDR teams energized.",
  "Phone-heavy SDR teams wanting AI-powered parallel dialing and a virtual sales floor",
  "Custom", "premium",
  ["Parallel dialing increases connects 3-5x", "Virtual sales floor for remote teams", "AI call summaries and coaching"],
  ["Phone-centric, doesn't help email-first teams", "Custom pricing is opaque", "Requires a team of callers to see ROI"],
  ["AI parallel dialer", "Virtual sales floor", "Call recording", "AI summaries", "CRM logging", "Battle cards"],
  [("Starter", "Custom"), ("Growth", "Custom"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.5, "value": 7.0, "features": 7.0, "support": 7.0})

T("outplay", "Outplay", "ai-sdr", "https://www.outplayhq.com", 6.8,
  "Multi-channel engagement with AI capabilities baked in. Handles email, phone, LinkedIn, and SMS in one platform. Positioned as a more affordable Outreach alternative. The AI features are useful additions rather than core differentiators.",
  "SMB sales teams wanting multi-channel outreach without enterprise pricing",
  "$79/mo", "mid",
  ["True multi-channel: email, phone, LinkedIn, SMS", "More affordable than Outreach or SalesLoft", "Built-in meeting scheduler"],
  ["AI features are additions, not core", "Less polished than enterprise competitors", "Smaller ecosystem and fewer integrations"],
  ["Email sequences", "Power dialer", "LinkedIn steps", "SMS outreach", "Meeting scheduler", "Analytics"],
  [("Growth", "$79/mo/user"), ("Enterprise", "$120/mo/user"), ("Custom", "Custom")],
  {"ease_of_use": 7.0, "value": 7.0, "features": 7.0, "support": 6.5})


# =============================================================================
# SALES ENGAGEMENT TOOLS (10)
# =============================================================================

T("outreach", "Outreach", "sales-engagement", "https://www.outreach.io", 8.0,
  "The market leader in sales engagement for a reason. The sequencing engine is the most powerful in the category, the AI insights are useful, and the platform handles everything from SDR prospecting to AE deal management. The price and complexity are real barriers for SMBs.",
  "Mid-market and enterprise sales teams (25+ reps) with dedicated RevOps support",
  "$100/user/mo", "premium",
  ["Most powerful sequencing engine in the category", "AI-driven insights on deal health", "Handles full sales cycle from prospecting to close"],
  ["Complex setup requires RevOps support", "Expensive at $100+/user/mo", "Overkill for small teams"],
  ["Multi-step sequences", "A/B testing", "AI deal insights", "Revenue intelligence", "Pipeline management", "Salesforce integration"],
  [("Standard", "$100/user/mo"), ("Professional", "$130/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.0, "value": 7.0, "features": 9.0, "support": 7.5})

T("salesloft", "SalesLoft", "sales-engagement", "https://www.salesloft.com", 7.5,
  "Outreach's main competitor, now merged with Clari. Strong sequencing and coaching features, slightly more intuitive than Outreach. The Clari merger adds forecasting but introduces uncertainty about product direction. A solid platform navigating a complex transition.",
  "Sales teams wanting engagement + forecasting in one platform",
  "$75/user/mo", "premium",
  ["More intuitive UI than Outreach", "Strong coaching and analytics", "Clari merger adds revenue forecasting"],
  ["Post-merger product direction is uncertain", "Still expensive for SMBs", "Some feature overlap with Clari creates confusion"],
  ["Email sequences", "Dialer", "Coaching", "Pipeline management", "Forecasting (Clari)", "Analytics"],
  [("Essentials", "$75/user/mo"), ("Advanced", "$125/user/mo"), ("Premier", "Custom")],
  {"ease_of_use": 7.5, "value": 7.0, "features": 8.0, "support": 7.0})

T("apollo", "Apollo.io", "sales-engagement", "https://www.apollo.io", 8.5,
  "The best value in B2B sales tools. Period. A contact database of 275M+ profiles, email sequencing, dialer, and LinkedIn integration, all starting at $49/user/mo. Apollo took the ZoomInfo + Outreach bundle and made it affordable. The data quality isn't ZoomInfo-level, but for most SMBs, it's good enough.",
  "SMBs and startups wanting prospecting data + engagement in one affordable platform",
  "$49/user/mo", "mid",
  ["275M+ contact database included", "Full engagement suite (email, phone, LinkedIn)", "Best value per dollar in B2B sales"],
  ["Data quality below ZoomInfo", "Can feel overwhelming, does a lot", "Email deliverability requires careful setup"],
  ["Contact database", "Email sequences", "Built-in dialer", "LinkedIn integration", "Intent signals", "AI email writing"],
  [("Free", "$0"), ("Basic", "$49/user/mo"), ("Professional", "$79/user/mo"), ("Organization", "$119/user/mo")],
  {"ease_of_use": 7.5, "value": 9.5, "features": 8.5, "support": 7.0},
  sultans_pick=True)

T("instantly", "Instantly", "sales-engagement", "https://www.instantly.ai", 7.8,
  "The cold email tool built for volume. Unlimited email accounts, built-in warmup, and lead finding, all at a price that undercuts every competitor. If your outbound motion is email-first and high-volume, Instantly delivers the infrastructure. Just don't expect phone or LinkedIn support.",
  "Agencies and founders running high-volume cold email campaigns",
  "$30/mo", "budget",
  ["Unlimited email accounts with warmup", "Built-in B2B lead database", "Very competitive pricing for volume senders"],
  ["Email only, no phone or LinkedIn", "UI is functional but basic", "Lead database quality varies"],
  ["Unlimited email accounts", "AI warmup", "Lead finder", "Email sequences", "A/B testing", "Inbox rotation"],
  [("Growth", "$30/mo"), ("Hypergrowth", "$77.60/mo"), ("Light Speed", "$286.30/mo")],
  {"ease_of_use": 8.0, "value": 8.5, "features": 7.5, "support": 6.5})

T("reply-io", "Reply.io", "sales-engagement", "https://www.reply.io", 7.2,
  "Multi-channel engagement with strong automation features. Handles email, LinkedIn, calls, and SMS in one platform. The Jason AI feature adds AI-powered prospect research and email writing. Solid mid-market tool that does everything competently without excelling at any single thing.",
  "Sales teams wanting multi-channel sequences with AI-assisted email writing",
  "$49/user/mo", "mid",
  ["True multi-channel sequences", "Jason AI for automated prospect research", "Good LinkedIn automation"],
  ["Interface feels cluttered", "AI features are decent but not leading", "Per-user pricing adds up for larger teams"],
  ["Email sequences", "LinkedIn automation", "Jason AI", "Phone dialer", "Meeting scheduler", "CRM sync"],
  [("Email Volume", "$49/mo"), ("Multichannel", "$89/user/mo"), ("Agency", "$166/mo")],
  {"ease_of_use": 6.5, "value": 7.0, "features": 7.5, "support": 7.0})

T("mixmax", "Mixmax", "sales-engagement", "https://www.mixmax.com", 7.0,
  "Gmail-native sales engagement. Lives inside your inbox instead of pulling you into a separate platform. Email tracking, sequences, and scheduling without leaving Gmail. If your team refuses to leave Gmail, Mixmax is the best option. If they're open to a dedicated platform, Outreach and Apollo are stronger.",
  "Gmail-heavy sales teams who want engagement tools without leaving their inbox",
  "$29/user/mo", "budget",
  ["Lives inside Gmail, zero context switching", "Easy to adopt (no new app to learn)", "Good meeting scheduling"],
  ["Gmail only, no Outlook support", "Less powerful sequencing than dedicated platforms", "Limited reporting compared to Outreach"],
  ["Gmail sidebar", "Email sequences", "Meeting scheduling", "Email tracking", "Templates", "Salesforce integration"],
  [("SMB", "$29/user/mo"), ("Growth", "$49/user/mo"), ("Growth + CRM", "$69/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.5, "value": 7.0, "features": 6.5, "support": 7.0})

T("mailshake", "Mailshake", "sales-engagement", "https://www.mailshake.com", 6.5,
  "Simple cold email outreach for small teams. Does the basics well: email sequences, follow-ups, A/B testing, without the complexity of Outreach or SalesLoft. The simplicity is a feature for teams doing their first outbound campaigns. You'll outgrow it.",
  "Small teams running their first outbound email campaigns",
  "$25/user/mo", "budget",
  ["Dead simple to set up and use", "Affordable for first-time outbound teams", "Built-in email warmup"],
  ["Limited multi-channel support", "Basic reporting", "You'll outgrow it quickly"],
  ["Email sequences", "A/B testing", "Lead catcher", "Phone dialer (add-on)", "LinkedIn automation (add-on)", "Analytics"],
  [("Email Outreach", "$25/user/mo"), ("Sales Engagement", "$75/user/mo")],
  {"ease_of_use": 8.5, "value": 7.0, "features": 5.5, "support": 7.0})

T("woodpecker", "Woodpecker", "sales-engagement", "https://www.woodpecker.co", 6.8,
  "Cold email automation built for agencies and B2B companies. Deliverability is the selling point: domain warmup, bounce detection, and sending throttling keep your emails out of spam. Functional and reliable, without trying to be a platform.",
  "B2B companies and agencies focused on cold email deliverability",
  "$25/mo", "budget",
  ["Excellent deliverability features", "Agency-friendly multi-client setup", "Clean, focused interface"],
  ["Email-centric, limited multi-channel", "Fewer integrations than larger platforms", "Growth beyond email requires a different tool"],
  ["Cold email sequences", "Domain warmup", "Bounce detection", "A/B testing", "Agency panel", "Condition-based campaigns"],
  [("Cold Email", "$25/mo"), ("Agency", "$35/mo"), ("Custom", "Custom")],
  {"ease_of_use": 7.5, "value": 7.5, "features": 6.5, "support": 7.0})

T("lemlist", "Lemlist", "sales-engagement", "https://www.lemlist.com", 7.5,
  "Personalization-first cold outreach. Custom images, landing pages, and liquid syntax make every email feel hand-written. The built-in B2B database is a nice addition. Strong for teams where personalization quality matters more than send volume.",
  "Outbound teams where email personalization quality drives response rates",
  "$32/user/mo", "budget",
  ["Best personalization features (custom images, landing pages)", "Built-in B2B lead database", "Multi-channel sequences (email + LinkedIn)"],
  ["Personalization features have a learning curve", "Smaller customer base than Outreach/SalesLoft", "Advanced features need higher tiers"],
  ["Custom image personalization", "Liquid syntax templates", "B2B lead finder", "LinkedIn steps", "Email warmup", "Campaign analytics"],
  [("Email Starter", "$32/user/mo"), ("Email Pro", "$55/user/mo"), ("Multichannel Expert", "$79/user/mo"), ("Outreach Scale", "$129/user/mo")],
  {"ease_of_use": 7.0, "value": 7.5, "features": 8.0, "support": 7.0})

T("yesware", "Yesware", "sales-engagement", "https://www.yesware.com", 6.0,
  "Email tracking and basic templates inside Gmail and Outlook. Was an early mover in sales engagement, now overshadowed by platforms with broader capabilities. Still useful for individual reps who just want email tracking and templates without committing to a full engagement platform.",
  "Individual reps wanting email tracking without a full engagement platform",
  "$15/user/mo", "budget",
  ["Works in both Gmail and Outlook", "Simple email tracking and templates", "Low price for basic functionality"],
  ["Feature set hasn't kept pace with competitors", "No multi-channel support", "Limited to email tracking and templates"],
  ["Email tracking", "Templates", "Meeting scheduler", "Reporting", "CRM sync", "Attachment tracking"],
  [("Free", "$0"), ("Pro", "$15/user/mo"), ("Premium", "$35/user/mo"), ("Enterprise", "$65/user/mo")],
  {"ease_of_use": 8.0, "value": 6.0, "features": 5.0, "support": 6.0})


# =============================================================================
# CONVERSATION INTELLIGENCE TOOLS (10)
# =============================================================================

T("gong", "Gong", "conversation-intelligence", "https://www.gong.io", 8.5,
  "The gold standard in conversation intelligence. Records every call, surfaces coaching insights, tracks deal health, and spots competitive mentions automatically. The platform earns its price when adoption is high (80%+ calls recorded). Below that threshold, you're paying enterprise pricing for a recording tool.",
  "Sales teams with 10+ reps where coaching and deal visibility drive revenue",
  "$100/user/mo", "premium",
  ["Top-tier conversation analytics", "AI-powered deal intelligence", "Competitive mention tracking"],
  ["Requires 80%+ adoption to justify ROI", "Expensive at $100-160/user/mo + platform fee", "Privacy concerns in some industries"],
  ["Call recording & transcription", "Deal intelligence", "Coaching scorecards", "Competitive intelligence", "Pipeline analytics", "CRM auto-logging"],
  [("Standard", "~$100/user/mo"), ("Premium", "~$130/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.0, "value": 7.5, "features": 9.5, "support": 8.0},
  sultans_pick=True)

T("chorus", "Chorus", "conversation-intelligence", "https://www.chorus.ai", 7.0,
  "ZoomInfo's conversation intelligence play. Acquired in 2021 and now bundled with ZoomInfo's higher tiers. The CI features are solid but innovation has slowed since the acquisition. Best for teams already paying for ZoomInfo who want CI included in their bundle.",
  "Teams already on ZoomInfo looking for bundled conversation intelligence",
  "$50/user/mo", "mid",
  ["Bundled with ZoomInfo at higher tiers", "Good transcription accuracy", "Solid ZoomInfo data integration"],
  ["Innovation has slowed post-acquisition", "Standalone pricing is less competitive", "Falling behind Gong on AI features"],
  ["Call recording", "AI transcription", "Deal intelligence", "Coaching tools", "ZoomInfo integration", "Market intelligence"],
  [("Business", "$50/user/mo"), ("Enterprise", "Custom"), ("ZoomInfo Bundle", "Included in Advanced+")],
  {"ease_of_use": 7.0, "value": 6.5, "features": 7.0, "support": 6.5})

T("clari", "Clari", "conversation-intelligence", "https://www.clari.com", 7.2,
  "Revenue intelligence and forecasting with conversation data. Clari's pipeline analytics are the strongest in the category: time-series trending and deal risk scoring that predict outcomes. The SalesLoft merger (Dec 2025) adds engagement capabilities but creates short-term product uncertainty.",
  "Revenue leaders wanting pipeline forecasting and deal risk scoring at scale",
  "$40/user/mo", "mid",
  ["Best pipeline forecasting in the market", "Time-series deal trending", "SalesLoft merger adds engagement"],
  ["Post-merger product direction is uncertain", "More forecasting platform than pure CI", "Enterprise complexity and pricing"],
  ["Pipeline analytics", "Revenue forecasting", "Deal inspection", "Conversation intelligence", "CRM auto-sync", "Revenue operations"],
  [("Standard", "$40/user/mo"), ("Professional", "$65/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.5, "value": 7.0, "features": 7.5, "support": 7.0})

T("sybill", "Sybill", "conversation-intelligence", "https://www.sybill.ai", 7.8,
  "AI CRM automation from your sales calls. Sybill records calls, generates summaries, drafts follow-up emails, and updates your CRM automatically. The thesis: reps should sell, not do data entry. Lighter and more focused than Gong, and priced for SMBs who want AI-powered CRM hygiene.",
  "SMB sales teams wanting AI that turns conversations into CRM data",
  "$49/user/mo", "mid",
  ["Automatic CRM updates from calls", "AI-generated follow-up emails", "Lighter and cheaper than Gong"],
  ["Shallower analytics than Gong", "Deal intelligence features are newer", "Smaller ecosystem and fewer integrations"],
  ["Call recording & transcription", "AI call summaries", "Auto CRM updates", "Follow-up email drafts", "Deal boards", "Slack integration"],
  [("Starter", "$49/user/mo"), ("Growth", "$79/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.5, "value": 8.0, "features": 7.5, "support": 7.5})

T("fireflies", "Fireflies.ai", "conversation-intelligence", "https://www.fireflies.ai", 7.5,
  "AI meeting notes that work. Joins Zoom, Teams, and Google Meet calls automatically, transcribes everything, and generates searchable summaries. The free tier is generous enough for individual use. Strong for meeting-heavy organizations that need institutional memory, not just sales coaching.",
  "Meeting-heavy teams wanting automatic transcription, notes, and search across all calls",
  "Free / $10/user/mo", "free",
  ["Generous free tier", "Works across Zoom, Teams, and Meet", "Searchable conversation database"],
  ["Sales-specific features are limited", "Transcription accuracy varies with accents", "Storage limits on lower tiers"],
  ["Auto-join meetings", "AI transcription", "Smart summaries", "Action items", "Conversation search", "CRM integrations"],
  [("Free", "$0"), ("Pro", "$10/user/mo"), ("Business", "$19/user/mo"), ("Enterprise", "$39/user/mo")],
  {"ease_of_use": 9.0, "value": 8.5, "features": 7.0, "support": 7.0})

T("otter-ai", "Otter.ai", "conversation-intelligence", "https://www.otter.ai", 6.8,
  "AI transcription for meetings with a focus on collaboration. Good for teams that need accurate transcripts and shared notes, less suited for sales-specific workflows. The OtterPilot auto-joins calls and generates summaries. Practical and affordable, but limited sales intelligence.",
  "Teams wanting accurate meeting transcription and shared notes",
  "Free / $8.33/user/mo", "free",
  ["Accurate real-time transcription", "Good free tier for individuals", "Strong collaboration features"],
  ["Limited sales-specific features", "Not designed for deal intelligence", "Storage caps on free tier"],
  ["Real-time transcription", "OtterPilot auto-join", "Meeting summaries", "Action items", "Shared workspaces", "Search across meetings"],
  [("Basic", "Free"), ("Pro", "$8.33/user/mo"), ("Business", "$20/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.5, "value": 7.5, "features": 6.5, "support": 6.5})

T("avoma", "Avoma", "conversation-intelligence", "https://www.avoma.com", 7.0,
  "An AI meeting assistant that covers the full meeting lifecycle: scheduling, recording, transcription, summaries, and coaching. Tries to be the all-in-one meeting platform. Does each piece adequately without leading in any single function.",
  "Revenue teams wanting meeting management and conversation intelligence in one platform",
  "$19/user/mo", "budget",
  ["Full meeting lifecycle coverage", "Competitive pricing vs. Gong", "Good AI summaries"],
  ["Jack of all trades, master of none", "Coaching features less sophisticated than Gong", "Smaller customer base"],
  ["AI scheduling", "Call recording", "Transcription", "AI summaries", "Coaching scorecards", "Revenue intelligence"],
  [("Starter", "$19/user/mo"), ("Plus", "$49/user/mo"), ("Business", "$79/user/mo"), ("Enterprise", "$129/user/mo")],
  {"ease_of_use": 7.5, "value": 7.5, "features": 7.0, "support": 7.0})

T("fathom", "Fathom", "conversation-intelligence", "https://www.fathom.video", 7.5,
  "Free AI notetaker that punches above its weight. Records Zoom calls, generates summaries, and highlights key moments. The free plan is usable with no time limits, unlimited recordings. The best entry point for teams trying conversation intelligence before committing to Gong's pricing.",
  "Individual reps and small teams wanting free AI meeting notes",
  "Free / $15/user/mo", "free",
  ["Useful free plan with unlimited recordings", "Fast, accurate AI summaries", "Clean, simple interface"],
  ["Limited coaching and analytics features", "Shallower than Gong for team-wide insights", "Zoom-first, other platforms are secondary"],
  ["AI recording", "Instant summaries", "Key moment highlights", "CRM auto-sync", "Action item tracking", "Clip sharing"],
  [("Free", "$0"), ("Premium", "$15/user/mo"), ("Team", "$19/user/mo"), ("Team Pro", "$29/user/mo")],
  {"ease_of_use": 9.0, "value": 9.0, "features": 6.5, "support": 7.0})

T("jiminny", "Jiminny", "conversation-intelligence", "https://www.jiminny.com", 6.5,
  "Revenue intelligence for mid-market teams. Call recording, coaching, and deal intelligence with a focus on adoption. The interface is cleaner than Gong's. Positioned as the CI platform that reps will use. Feature depth doesn't match Gong, but neither does the price.",
  "Mid-market sales teams wanting CI without Gong's pricing complexity",
  "$85/user/mo", "mid",
  ["Clean, rep-friendly interface", "Good coaching features for the price", "Deal intelligence dashboard"],
  ["Smaller ecosystem than Gong", "Analytics depth is limited", "Less brand recognition makes buy-in harder"],
  ["Call recording", "Coaching scorecards", "Deal intelligence", "Revenue analytics", "CRM integration", "Team dashboards"],
  [("Business", "$85/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.5, "value": 6.5, "features": 6.5, "support": 7.0})

T("modjo", "Modjo", "conversation-intelligence", "https://www.modjo.ai", 6.0,
  "European conversation intelligence platform. Strong in EU markets with GDPR-compliant architecture and multi-language transcription. In English-speaking markets, Gong and Sybill are stronger choices. Pick Modjo if you need native European language support and EU data residency.",
  "European sales teams needing GDPR-compliant CI with multi-language support",
  "Custom", "premium",
  ["GDPR-compliant European data residency", "Multi-language transcription", "Good coaching features for EU teams"],
  ["Weaker in English-only markets", "Smaller feature set than Gong", "Custom pricing is opaque"],
  ["Call recording", "Multi-language transcription", "Coaching", "Deal intelligence", "CRM integration", "EU data residency"],
  [("Business", "Custom"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.0, "value": 5.5, "features": 6.5, "support": 6.5})


# =============================================================================
# DATA ENRICHMENT TOOLS (10)
# =============================================================================

T("zoominfo", "ZoomInfo", "data-enrichment", "https://www.zoominfo.com", 7.5,
  "The most comprehensive B2B database in the market. 100M+ business profiles, intent data, and org charts. The data quality is measurably better than alternatives. The pricing will make you reconsider your life choices. Minimum $15K/yr contracts with aggressive renewal tactics.",
  "Mid-market and enterprise sales teams with $15K+ annual data budget",
  "$15,000/yr", "premium",
  ["Largest and most accurate B2B database", "Org charts and buyer intent signals", "Deep Salesforce and HubSpot integration"],
  ["$15K+/yr minimum with aggressive renewals", "Data credits system creates artificial scarcity", "Overkill for SMBs"],
  ["Contact database", "Company profiles", "Intent data", "Org charts", "Workflows", "Chrome extension"],
  [("Professional", "~$15,000/yr"), ("Advanced", "~$25,000/yr"), ("Elite", "~$40,000/yr")],
  {"ease_of_use": 7.0, "value": 5.5, "features": 9.0, "support": 7.5})

T("clay", "Clay", "data-enrichment", "https://www.clay.com", 8.2,
  "The data enrichment tool that changed the game. Clay doesn't have its own database. It waterfalls across 75+ providers to find the best data for each contact. The result: better coverage than any single provider. The spreadsheet-like interface handles complex enrichment workflows that would take an engineer to build elsewhere.",
  "RevOps teams and growth operators who want top-tier data enrichment with workflow flexibility",
  "$149/mo", "mid",
  ["Waterfalls across 75+ data providers", "Spreadsheet-like workflow builder", "Better coverage than any single database"],
  ["Learning curve is real, it's a power tool", "Credits get expensive at scale", "Not a plug-and-play solution for non-technical users"],
  ["Waterfall enrichment", "75+ data providers", "AI research agent", "Workflow builder", "CRM sync", "Integrations"],
  [("Starter", "$149/mo"), ("Explorer", "$349/mo"), ("Pro", "$800/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.0, "value": 8.0, "features": 9.0, "support": 7.5},
  sultans_pick=True)

T("clearbit", "Clearbit", "data-enrichment", "https://www.clearbit.com", 7.0,
  "Acquired by HubSpot in 2023. The API-first enrichment tool that marketing and product teams love. Strong company data and real-time website visitor identification. Post-acquisition, the standalone product is being absorbed into HubSpot. If you're on HubSpot, you might already have Clearbit features built in.",
  "HubSpot users wanting deeper company data and website visitor identification",
  "Custom", "mid",
  ["Strong company and firmographic data", "Real-time website visitor identification", "Deep HubSpot integration (post-acquisition)"],
  ["Being absorbed into HubSpot, standalone future uncertain", "Company-focused, weaker on personal contact data", "Custom pricing with no transparency"],
  ["Company enrichment", "Contact enrichment", "Website visitor ID", "Reveal (IP → company)", "API access", "HubSpot integration"],
  [("Free (HubSpot)", "$0 with HubSpot"), ("Business", "Custom"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.5, "value": 7.0, "features": 7.0, "support": 7.0})

T("lusha", "Lusha", "data-enrichment", "https://www.lusha.com", 7.2,
  "Simple contact data lookup that reps use. The Chrome extension finds emails and phone numbers from LinkedIn profiles in seconds. Less powerful than ZoomInfo or Clay, but the simplicity and per-seat pricing make it accessible for individual reps and small teams.",
  "Individual reps and small teams wanting quick contact lookups from LinkedIn",
  "$29/user/mo", "budget",
  ["Dead simple Chrome extension", "Good direct phone number coverage", "Affordable per-seat pricing"],
  ["Smaller database than ZoomInfo", "Limited enrichment beyond basic contact data", "Credit limits on lower tiers"],
  ["Contact finder", "Chrome extension", "Company profiles", "List building", "CRM enrichment", "API access"],
  [("Free", "$0 (5 credits/mo)"), ("Pro", "$29/user/mo"), ("Premium", "$51/user/mo"), ("Scale", "Custom")],
  {"ease_of_use": 9.0, "value": 7.5, "features": 6.5, "support": 7.0})

T("cognism", "Cognism", "data-enrichment", "https://www.cognism.com", 7.5,
  "The strongest B2B data provider for European markets. GDPR-compliant from the ground up with phone-verified mobile numbers (Diamond Data). If your ICP includes European companies, Cognism's coverage is unmatched. In the US, ZoomInfo and Apollo cover more ground.",
  "B2B teams prospecting into European markets who need GDPR-compliant data",
  "Custom", "premium",
  ["Best European B2B data coverage", "Phone-verified mobile numbers (Diamond Data)", "GDPR-compliant architecture"],
  ["Weaker US coverage than ZoomInfo", "Custom pricing is expensive", "Smaller integration ecosystem"],
  ["Contact database", "Diamond Data (verified mobiles)", "Chrome extension", "Intent data", "CRM enrichment", "Compliance tools"],
  [("Platinum", "Custom"), ("Diamond", "Custom"), ("Enterprise", "Custom")],
  {"ease_of_use": 7.0, "value": 7.0, "features": 7.5, "support": 7.5})

T("seamless-ai", "Seamless.AI", "data-enrichment", "https://www.seamless.ai", 5.5,
  "Real-time contact finder with aggressive marketing. The tool finds emails and phone numbers by searching the web in real-time rather than maintaining a static database. Results are hit-or-miss. The 50-credit free tier is bait for a hard sales pitch. Pushy upselling and mixed data quality undermine a decent concept.",
  "Budget-conscious teams willing to verify data quality manually",
  "$147/mo", "mid",
  ["Real-time data lookup (not a static database)", "Good when it finds accurate data", "Chrome extension for LinkedIn prospecting"],
  ["Data accuracy is inconsistent", "Extremely aggressive sales team and upselling", "50-credit free tier is misleading bait"],
  ["Real-time contact search", "Chrome extension", "List builder", "Buyer intent", "Data enrichment", "CRM integrations"],
  [("Free", "$0 (50 credits)"), ("Basic", "$147/mo"), ("Pro", "Custom"), ("Enterprise", "Custom")],
  {"ease_of_use": 6.5, "value": 5.0, "features": 6.0, "support": 4.0})

T("uplead", "UpLead", "data-enrichment", "https://www.uplead.com", 6.8,
  "A cleaner, more affordable alternative to ZoomInfo for basic contact lookup. 155M+ contacts with real-time email verification. The interface is simple, the pricing is transparent, and the data is decent. Won't match ZoomInfo's depth, but delivers 70% of the value at 20% of the price.",
  "SMBs wanting affordable B2B contact data without ZoomInfo pricing",
  "$74/mo", "mid",
  ["Transparent, affordable pricing", "Real-time email verification", "Clean, simple interface"],
  ["Smaller database than ZoomInfo or Apollo", "Limited intent data and advanced features", "Phone number coverage is weaker"],
  ["Contact search", "Email verification", "Company data", "Technographics", "Intent data (basic)", "CRM integrations"],
  [("Essentials", "$74/mo"), ("Plus", "$149/mo"), ("Professional", "$299/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.0, "value": 7.5, "features": 6.0, "support": 7.0})

T("rocketreach", "RocketReach", "data-enrichment", "https://www.rocketreach.co", 6.5,
  "Email and phone lookup across 700M+ professionals. The database is large, but accuracy is inconsistent. Good for finding hard-to-reach contacts when other tools fail. Think of it as a backup enrichment source, not your primary database.",
  "Teams needing a secondary data source for hard-to-find contacts",
  "$39/mo", "budget",
  ["Large database (700M+ profiles)", "Good for hard-to-find contacts", "Affordable starting price"],
  ["Accuracy is inconsistent", "Interface feels dated", "Limited features beyond basic lookup"],
  ["Email lookup", "Phone lookup", "Company search", "Chrome extension", "Bulk enrichment", "API access"],
  [("Essentials", "$39/mo"), ("Pro", "$99/mo"), ("Ultimate", "$249/mo")],
  {"ease_of_use": 7.0, "value": 6.5, "features": 5.5, "support": 6.0})

T("leadiq", "LeadIQ", "data-enrichment", "https://www.leadiq.com", 7.0,
  "Prospecting data capture built for SDRs. The Chrome extension captures contact data from LinkedIn and pushes it directly into your CRM and sequencer. Less powerful as a standalone database, but the prospecting workflow integration is excellent. Think of it as the bridge between LinkedIn and your CRM.",
  "SDR teams wanting smooth LinkedIn-to-CRM prospecting",
  "$36/user/mo", "budget",
  ["Excellent LinkedIn-to-CRM workflow", "One-click capture to sequences", "Good data on target accounts"],
  ["Limited standalone database search", "Works best as part of a larger stack", "Credit limits constrain heavy prospectors"],
  ["LinkedIn data capture", "One-click CRM push", "Sequence integration", "Job change alerts", "Salesforce enrichment", "Team analytics"],
  [("Free", "$0"), ("Essential", "$36/user/mo"), ("Pro", "$79/user/mo"), ("Enterprise", "Custom")],
  {"ease_of_use": 8.5, "value": 7.5, "features": 6.5, "support": 7.0})

T("kaspr", "Kaspr", "data-enrichment", "https://www.kaspr.io", 6.0,
  "LinkedIn contact data extraction. A Chrome extension that pulls phone numbers and emails from LinkedIn profiles. European-focused with GDPR compliance. Does one thing simply: you see a LinkedIn profile, you click, you get the data. Limited beyond that single function.",
  "European sales reps wanting quick LinkedIn contact extraction",
  "$45/user/mo", "mid",
  ["Simple LinkedIn data extraction", "GDPR-compliant", "Good European phone number coverage"],
  ["LinkedIn-only, no standalone database", "Limited functionality beyond contact extraction", "Credit limits at lower tiers"],
  ["LinkedIn Chrome extension", "Phone number finder", "Email finder", "CRM export", "Team management", "API access"],
  [("Free", "$0 (5 credits/mo)"), ("Starter", "$45/user/mo"), ("Business", "$79/user/mo"), ("Organization", "$99/user/mo")],
  {"ease_of_use": 8.0, "value": 6.0, "features": 5.0, "support": 6.0})


# =============================================================================
# COMPARISONS
# =============================================================================

COMPARISONS = [
    # CRM
    {"tools": ["hubspot", "salesforce"], "winner": "hubspot",
     "why": "HubSpot gives SMBs everything they need without the admin overhead. Salesforce is powerful, but most small teams will never use 70% of what they are paying for.",
     "summary": "Two CRM titans with fundamentally different philosophies. HubSpot prioritizes ease of use and a generous free tier. Salesforce prioritizes infinite customization at infinite complexity."},
    {"tools": ["hubspot", "pipedrive"], "winner": "hubspot",
     "why": "HubSpot's free tier outcompetes Pipedrive's cheapest paid plan. Pipedrive has a better visual pipeline, but HubSpot offers a complete platform.",
     "summary": "Both are excellent CRMs for small teams. Pipedrive wins on pipeline visualization and simplicity. HubSpot wins on breadth and free-tier value."},
    {"tools": ["pipedrive", "close"], "winner": "pipedrive",
     "why": "Pipedrive is more versatile and less expensive. Close wins if phone-heavy outbound is your primary motion, but Pipedrive covers more ground.",
     "summary": "Pipedrive is a visual pipeline CRM. Close is a calling-first CRM. Your sales motion determines the right pick."},
    {"tools": ["salesforce", "zoho-crm"], "winner": "salesforce",
     "why": "Salesforce offers deeper customization and a larger ecosystem. Zoho is a fraction of the cost but can't match Salesforce's depth at scale.",
     "summary": "The budget vs. premium CRM battle. Zoho CRM offers solid functionality at a fraction of Salesforce's price."},
    # PM
    {"tools": ["asana", "monday"], "winner": "asana",
     "why": "Asana has better workflow automation and a more generous free tier. Monday is more visual, but Asana is more functional for day-to-day project execution.",
     "summary": "The two most popular project management platforms for growing teams. Both are excellent. Asana edges Monday on workflow depth."},
    {"tools": ["clickup", "notion"], "winner": "clickup",
     "why": "ClickUp is a better project management tool. Notion is a better knowledge base. If you need PM first, ClickUp wins. If docs come first, Notion wins.",
     "summary": "Two all-in-one platforms with different strengths. ClickUp leads in task management. Notion leads in docs and wikis."},
    {"tools": ["asana", "clickup"], "winner": "asana",
     "why": "Asana is more polished and easier to adopt across a team. ClickUp has more features but the UI complexity works against it in practice.",
     "summary": "Feature density vs. polish. ClickUp does more things. Asana does the important things better."},
    {"tools": ["trello", "notion"], "winner": "notion",
     "why": "Notion does everything Trello does (kanban boards) plus docs, wikis, and databases. Trello is simpler, but Notion offers more value.",
     "summary": "Trello is a kanban board. Notion is a workspace. If you just need cards on a board, Trello is faster. For everything else, Notion."},
    {"tools": ["linear", "asana"], "winner": "linear",
     "why": "For software teams, Linear's speed and developer-focused design make it the clear winner. Asana is better for non-engineering teams managing broader projects.",
     "summary": "Linear is built for engineering. Asana is built for everyone. Pick based on your team composition."},
    # Email
    {"tools": ["mailchimp", "convertkit"], "winner": "convertkit",
     "why": "ConvertKit offers better deliverability, a more generous free tier, and a creator-friendly business model. Mailchimp's pricing has gotten aggressive while its free tier shrunk.",
     "summary": "The incumbent vs. the challenger. Mailchimp is bigger. ConvertKit is better for most small-list use cases."},
    {"tools": ["convertkit", "mailerlite"], "winner": "convertkit",
     "why": "ConvertKit has a stronger creator ecosystem and better automations. MailerLite is cheaper and a legitimate contender, but ConvertKit's edge in deliverability and community gives it the win.",
     "summary": "Two creator-friendly email platforms. MailerLite wins on price. ConvertKit wins on the overall creator experience."},
    {"tools": ["activecampaign", "mailchimp"], "winner": "activecampaign",
     "why": "ActiveCampaign's automation builder is leagues ahead of Mailchimp's. Any team that needs more than basic drip sequences will outgrow Mailchimp quickly.",
     "summary": "Basic email marketing vs. advanced automation. Mailchimp is easier. ActiveCampaign is far more powerful."},
    {"tools": ["klaviyo", "mailchimp"], "winner": "klaviyo",
     "why": "For e-commerce, Klaviyo's Shopify integration and purchase-based segmentation are unmatched. Mailchimp works for e-commerce, but Klaviyo was purpose-built for it.",
     "summary": "General email marketing vs. e-commerce email marketing. Klaviyo dominates if you sell products online."},
    # SEO
    {"tools": ["semrush", "ahrefs"], "winner": "semrush",
     "why": "Semrush offers broader functionality (content tools, PPC research, social media) alongside strong SEO. Ahrefs has a better backlink index, but Semrush provides more value as a complete toolkit.",
     "summary": "The two biggest SEO platforms. Semrush is wider. Ahrefs is deeper on backlinks. Most teams only need one."},
    {"tools": ["ahrefs", "moz"], "winner": "ahrefs",
     "why": "Ahrefs has a larger, fresher database and more powerful tooling. Moz pioneered the category but hasn't kept pace with Ahrefs' data infrastructure.",
     "summary": "The legacy vs. the modern challenger. Moz is good. Ahrefs is better in almost every measurable dimension."},
    {"tools": ["semrush", "se-ranking"], "winner": "semrush",
     "why": "Semrush has a larger database and more features. SE Ranking offers 70% of the value at 35% of the price. Budget teams should seriously consider SE Ranking.",
     "summary": "Premium vs. budget SEO. Semrush is the gold standard. SE Ranking is the best budget alternative."},
    # Help Desk
    {"tools": ["zendesk", "freshdesk"], "winner": "freshdesk",
     "why": "Freshdesk delivers 85% of Zendesk's functionality at a significantly lower price and with a better free tier. Zendesk wins on advanced features and scale, but most SMBs don't need that depth.",
     "summary": "The incumbent vs. the challenger in customer support. Zendesk is more powerful. Freshdesk is a better value."},
    {"tools": ["intercom", "zendesk"], "winner": "zendesk",
     "why": "Zendesk is a better traditional help desk. Intercom is a better chat-first platform. For ticket-based support, Zendesk wins. For conversational support, Intercom wins.",
     "summary": "Tickets vs. conversations. Zendesk excels at structured support. Intercom excels at real-time chat."},
    {"tools": ["help-scout", "freshdesk"], "winner": "help-scout",
     "why": "Help Scout's email-like experience creates a more personal support interaction. Freshdesk is more feature-rich, but Help Scout's simplicity is a competitive advantage for smaller teams.",
     "summary": "Personal support vs. feature-rich support. Help Scout feels human. Freshdesk feels powerful."},
    {"tools": ["freshdesk", "zoho-desk"], "winner": "freshdesk",
     "why": "Freshdesk has a more polished interface and better standalone value. Zoho Desk wins only if you are deeply invested in the Zoho ecosystem.",
     "summary": "Two affordable help desks. Freshdesk is better as a standalone product. Zoho Desk is better inside the Zoho ecosystem."},
    # AI SDR
    {"tools": ["11x", "artisan"], "winner": "artisan",
     "why": "Artisan is more transparent about AI limitations, has lower churn, and costs $3K/mo less. 11x's fabricated testimonial scandal and 75% churn rate make it a risky bet at any price.",
     "summary": "The two most-funded AI SDR startups. Artisan is more honest about what AI can and can't do. 11x has more hype and more red flags."},
    {"tools": ["artisan", "aisdr"], "winner": "artisan",
     "why": "Artisan has a more mature platform and larger customer base. AiSDR is cheaper and worth testing if budget is tight, but Artisan's execution is more polished.",
     "summary": "Premium vs. budget AI SDR. Artisan offers more features and reliability. AiSDR offers a lower-cost entry point."},
    {"tools": ["lavender", "regie-ai"], "winner": "lavender",
     "why": "Lavender proves ROI immediately by measuring and improving email response rates. Regie.ai's AI content is decent but harder to quantify. At $29/mo vs. custom pricing, the value gap is wide.",
     "summary": "Email coaching vs. AI content generation for sales. Lavender improves your writing. Regie.ai writes for you."},
    # Sales Engagement
    {"tools": ["outreach", "salesloft"], "winner": "outreach",
     "why": "Outreach has a more powerful sequencing engine and broader feature set. SalesLoft is easier to use and the Clari merger adds forecasting, but Outreach remains the category leader on raw capability.",
     "summary": "The two dominant sales engagement platforms. Outreach is more powerful. SalesLoft is more user-friendly."},
    {"tools": ["apollo", "outreach"], "winner": "apollo",
     "why": "Apollo delivers 80% of Outreach's engagement features plus a built-in contact database, all at a fraction of the price. Outreach wins on enterprise power. Apollo wins on value.",
     "summary": "The enterprise leader vs. the all-in-one challenger. Outreach is deeper. Apollo is a better value for most teams."},
    {"tools": ["instantly", "lemlist"], "winner": "instantly",
     "why": "Instantly's unlimited mailbox rotation and aggressive pricing make it the better pure cold email tool. Lemlist wins on personalization features, but Instantly wins on volume and infrastructure.",
     "summary": "Volume vs. personalization in cold email. Instantly handles more volume. Lemlist creates more personalized outreach."},
    # Conversation Intelligence
    {"tools": ["gong", "chorus"], "winner": "gong",
     "why": "Gong's analytics and AI capabilities have pulled ahead since ZoomInfo's acquisition of Chorus. Chorus is acceptable bundled with ZoomInfo. As a standalone CI tool, Gong is the clear leader.",
     "summary": "The CI category leader vs. ZoomInfo's bundled option. Gong leads on innovation. Chorus leads on ZoomInfo integration."},
    {"tools": ["gong", "sybill"], "winner": "gong",
     "why": "Gong is the more complete platform with deeper analytics and coaching. Sybill is lighter, cheaper, and better at automated CRM updates. For teams that can't justify Gong's pricing, Sybill is the best alternative.",
     "summary": "Enterprise CI vs. SMB-friendly CI. Gong has more depth. Sybill has better value for smaller teams."},
    {"tools": ["fireflies", "otter-ai"], "winner": "fireflies",
     "why": "Fireflies offers better CRM integration, stronger action item detection, and a more generous free tier. Otter's transcription is slightly more accurate, but Fireflies is the more useful business tool.",
     "summary": "Two affordable AI transcription tools. Fireflies is better for sales teams. Otter is better for general meeting notes."},
    # Data Enrichment
    {"tools": ["zoominfo", "clay"], "winner": "clay",
     "why": "Clay's waterfall enrichment across 75+ providers delivers better overall coverage than any single database, including ZoomInfo. ZoomInfo's data is higher quality on individual lookups. Clay's approach gives you more data for less money.",
     "summary": "The incumbent database vs. the waterfall innovator. ZoomInfo has the deepest single database. Clay aggregates across 75+ sources."},
    {"tools": ["clay", "clearbit"], "winner": "clay",
     "why": "Clay does everything Clearbit does and more. Clearbit's HubSpot acquisition means its standalone future is uncertain. Clay is independent, more powerful, and actively innovating.",
     "summary": "The rising star vs. the acquired player. Clay is independent and more powerful. Clearbit is being absorbed into HubSpot."},
    {"tools": ["lusha", "rocketreach"], "winner": "lusha",
     "why": "Lusha has better data accuracy, a cleaner Chrome extension, and stronger phone number coverage. RocketReach has a larger database but accuracy is inconsistent.",
     "summary": "Two contact lookup tools. Lusha is more accurate. RocketReach has more volume."},
]

# Generate comparison slugs
for c in COMPARISONS:
    c["slug"] = f'{c["tools"][0]}-vs-{c["tools"][1]}'


# =============================================================================
# ALTERNATIVES
# =============================================================================

ALTERNATIVES = [
    {"tool": "salesforce", "reason": "Salesforce is powerful but complex and expensive. These alternatives offer CRM functionality that most SMBs will find easier and more affordable.",
     "alts": ["hubspot", "pipedrive", "close", "zoho-crm", "freshsales", "less-annoying-crm"]},
    {"tool": "hubspot", "reason": "HubSpot's paid tiers can get expensive fast. If the free CRM isn't enough but the paid plans strain your budget, these alternatives deliver similar value.",
     "alts": ["pipedrive", "close", "freshsales", "zoho-crm", "copper", "nutshell"]},
    {"tool": "asana", "reason": "Asana works well for many teams, but its pricing model and feature gating frustrate some users. These alternatives offer different approaches to project management.",
     "alts": ["monday", "clickup", "notion", "linear", "basecamp", "wrike"]},
    {"tool": "monday", "reason": "Monday.com's 3-seat minimum and add-on pricing push some teams to look elsewhere. These alternatives offer similar visual project management.",
     "alts": ["asana", "clickup", "notion", "trello", "wrike", "teamwork"]},
    {"tool": "mailchimp", "reason": "Mailchimp's shrinking free tier and rising prices have pushed many users to explore alternatives. These platforms offer better value for most use cases.",
     "alts": ["convertkit", "mailerlite", "brevo", "activecampaign", "beehiiv", "constant-contact"]},
    {"tool": "semrush", "reason": "Semrush is comprehensive but expensive. If you need specific SEO capabilities rather than the full suite, these alternatives can save you significant money.",
     "alts": ["ahrefs", "se-ranking", "mangools", "moz", "ubersuggest", "surfer-seo"]},
    {"tool": "ahrefs", "reason": "Ahrefs is excellent but has no free trial and premium pricing. These alternatives offer overlapping functionality at various price points.",
     "alts": ["semrush", "se-ranking", "moz", "mangools", "spyfu", "ubersuggest"]},
    {"tool": "zendesk", "reason": "Zendesk's complexity and cost drive many teams to simpler, more affordable support platforms. These alternatives cover the essentials without the overhead.",
     "alts": ["freshdesk", "help-scout", "intercom", "zoho-desk", "groove-helpdesk", "liveagent"]},
    {"tool": "intercom", "reason": "Intercom's pricing model is confusing and expensive once you start adding features. These alternatives offer customer messaging and support at more predictable prices.",
     "alts": ["freshdesk", "help-scout", "zendesk", "groove-helpdesk", "zoho-desk", "liveagent"]},
    {"tool": "clickup", "reason": "ClickUp tries to do everything, and that ambition can make the UI overwhelming. These alternatives take a more focused approach.",
     "alts": ["asana", "monday", "notion", "linear", "trello", "basecamp"]},
    # AI SDR
    {"tool": "11x", "reason": "11x is expensive, controversial, and locks you into 12-month contracts. These alternatives offer AI-powered outbound at lower risk and lower cost.",
     "alts": ["artisan", "aisdr", "regie-ai", "lavender", "smartlead", "amplemarket"]},
    # Sales Engagement
    {"tool": "outreach", "reason": "Outreach's complexity and $100+/user pricing drive many teams to simpler, more affordable engagement platforms.",
     "alts": ["apollo", "salesloft", "instantly", "reply-io", "lemlist", "mixmax"]},
    {"tool": "salesloft", "reason": "SalesLoft's merger with Clari creates product uncertainty. These alternatives offer stable engagement platforms without the transition risk.",
     "alts": ["outreach", "apollo", "instantly", "reply-io", "lemlist", "mixmax"]},
    {"tool": "apollo", "reason": "Apollo tries to be everything — database + engagement + intelligence. If you want tools that specialize, these alternatives focus on doing one thing well.",
     "alts": ["outreach", "instantly", "lemlist", "salesloft", "mixmax", "reply-io"]},
    {"tool": "instantly", "reason": "Instantly is email-only. If you need phone, LinkedIn, or multi-channel outreach, these alternatives cover more ground.",
     "alts": ["apollo", "lemlist", "reply-io", "outreach", "woodpecker", "salesloft"]},
    # Conversation Intelligence
    {"tool": "gong", "reason": "Gong's $100+/user pricing puts it out of reach for many teams. These alternatives offer conversation intelligence at more accessible price points.",
     "alts": ["sybill", "fireflies", "fathom", "chorus", "avoma", "otter-ai"]},
    # Data Enrichment
    {"tool": "zoominfo", "reason": "ZoomInfo's $15K/yr minimum and aggressive renewal tactics push many teams to explore alternatives. These tools offer B2B data at more reasonable prices.",
     "alts": ["clay", "apollo", "lusha", "cognism", "uplead", "leadiq"]},
    {"tool": "clay", "reason": "Clay's learning curve is steep and credits get expensive at scale. These alternatives offer simpler enrichment for teams that don't need waterfall workflows.",
     "alts": ["apollo", "lusha", "zoominfo", "clearbit", "uplead", "leadiq"]},
]

# Generate alternative slugs
for a in ALTERNATIVES:
    a["slug"] = f'{a["tool"]}-alternatives'


# =============================================================================
# STACK GUIDES
# =============================================================================

STACKS = [
    {
        "slug": "zero-dollar-founder",
        "name": "The $0/mo Founder Stack",
        "description": "Everything a solo founder needs to run a business without spending a dime. Free tiers only.",
        "tools": [
            {"slug": "hubspot", "use": "CRM", "plan": "Free", "cost": "$0"},
            {"slug": "notion", "use": "Docs & Project Management", "plan": "Free", "cost": "$0"},
            {"slug": "mailerlite", "use": "Email Marketing", "plan": "Free (1K subs)", "cost": "$0"},
            {"slug": "trello", "use": "Task Management", "plan": "Free", "cost": "$0"},
            {"slug": "zoho-desk", "use": "Customer Support", "plan": "Free (3 agents)", "cost": "$0"},
        ],
        "total_cost": "$0/mo",
    },
    {
        "slug": "lean-startup",
        "name": "The Lean Startup Stack ($50/mo)",
        "description": "The best tools for early-stage startups with a small budget. Maximum value per dollar spent.",
        "tools": [
            {"slug": "hubspot", "use": "CRM", "plan": "Free", "cost": "$0"},
            {"slug": "clickup", "use": "Project Management", "plan": "Unlimited", "cost": "$7"},
            {"slug": "convertkit", "use": "Email Marketing", "plan": "Newsletter (Free)", "cost": "$0"},
            {"slug": "mangools", "use": "SEO", "plan": "Entry", "cost": "$29"},
            {"slug": "groove-helpdesk", "use": "Help Desk", "plan": "Standard", "cost": "$4.80"},
        ],
        "total_cost": "~$41/mo",
    },
    {
        "slug": "sales-team",
        "name": "The Sales Team Stack ($200/mo)",
        "description": "CRM, pipeline management, and outreach tools for a 5-person sales team scaling outbound.",
        "tools": [
            {"slug": "pipedrive", "use": "CRM", "plan": "Advanced", "cost": "$39/user/mo"},
            {"slug": "asana", "use": "Internal Projects", "plan": "Starter", "cost": "$10.99/user/mo"},
            {"slug": "activecampaign", "use": "Email Sequences", "plan": "Starter", "cost": "$29/mo"},
            {"slug": "freshdesk", "use": "Customer Support", "plan": "Growth", "cost": "$15/agent/mo"},
        ],
        "total_cost": "~$195/mo for a small team",
    },
    {
        "slug": "agency",
        "name": "The Agency Stack ($300/mo)",
        "description": "Project management, client communication, SEO tools, and billing for a growing agency.",
        "tools": [
            {"slug": "hubspot", "use": "CRM & Client Management", "plan": "Starter", "cost": "$20/mo"},
            {"slug": "asana", "use": "Project Management", "plan": "Starter", "cost": "$10.99/user/mo"},
            {"slug": "semrush", "use": "SEO & Reporting", "plan": "Pro", "cost": "$129.95/mo"},
            {"slug": "activecampaign", "use": "Email Marketing", "plan": "Starter", "cost": "$29/mo"},
            {"slug": "help-scout", "use": "Client Support", "plan": "Standard", "cost": "$20/user/mo"},
        ],
        "total_cost": "~$300/mo for a small agency",
    },
    {
        "slug": "content-creator",
        "name": "The Content Creator Stack ($80/mo)",
        "description": "Newsletter, SEO, and audience-building tools for bloggers, creators, and solo media operators.",
        "tools": [
            {"slug": "convertkit", "use": "Newsletter & Email", "plan": "Creator", "cost": "$25/mo"},
            {"slug": "notion", "use": "Content Calendar & Docs", "plan": "Plus", "cost": "$8/mo"},
            {"slug": "se-ranking", "use": "SEO & Rank Tracking", "plan": "Essential", "cost": "$44/mo"},
        ],
        "total_cost": "~$77/mo",
    },
    {
        "slug": "ecommerce",
        "name": "The E-Commerce Stack ($150/mo)",
        "description": "Email marketing, SEO, and support tools optimized for online stores.",
        "tools": [
            {"slug": "klaviyo", "use": "Email & SMS Marketing", "plan": "Email", "cost": "$20/mo"},
            {"slug": "hubspot", "use": "CRM", "plan": "Free", "cost": "$0"},
            {"slug": "ahrefs", "use": "SEO", "plan": "Lite", "cost": "$99/mo"},
            {"slug": "freshdesk", "use": "Customer Support", "plan": "Growth", "cost": "$15/agent/mo"},
        ],
        "total_cost": "~$134/mo",
    },
    {
        "slug": "outbound-engine",
        "name": "The Outbound Engine ($500/mo)",
        "description": "A full outbound sales stack for teams running cold email, calling, and LinkedIn outreach. Data, sequencing, AI, and call recording in one motion.",
        "tools": [
            {"slug": "apollo", "use": "Contact Data + Sequencing", "plan": "Professional", "cost": "$99/user/mo"},
            {"slug": "instantly", "use": "Cold Email at Scale", "plan": "Growth", "cost": "$30/mo"},
            {"slug": "lavender", "use": "AI Email Coaching", "plan": "Starter", "cost": "$29/mo"},
            {"slug": "clay", "use": "Data Enrichment + Waterfall", "plan": "Explorer", "cost": "$149/mo"},
            {"slug": "gong", "use": "Call Recording + Coaching", "plan": "Starter", "cost": "~$100/user/mo"},
            {"slug": "pipedrive", "use": "CRM + Pipeline", "plan": "Advanced", "cost": "$39/user/mo"},
        ],
        "total_cost": "~$446-550/mo for a 2-rep team",
    },
    {
        "slug": "data-driven-sales",
        "name": "The Data-Driven Sales Stack ($800/mo)",
        "description": "For revenue teams that make decisions on data. Enrichment, conversation analytics, CRM, and forecasting tools that turn every interaction into intelligence.",
        "tools": [
            {"slug": "clay", "use": "Data Enrichment + Workflows", "plan": "Professional", "cost": "$349/mo"},
            {"slug": "gong", "use": "Conversation Intelligence", "plan": "Business", "cost": "~$150/user/mo"},
            {"slug": "hubspot", "use": "CRM + Reporting", "plan": "Professional", "cost": "$500/mo"},
            {"slug": "sybill", "use": "AI Call Summaries + CRM Sync", "plan": "Starter", "cost": "$49/user/mo"},
            {"slug": "semrush", "use": "Competitive + Market Intel", "plan": "Pro", "cost": "$129.95/mo"},
        ],
        "total_cost": "~$1,180/mo for a 2-rep team",
    },
]


# =============================================================================
# NICHES — 6 universal + 10 category-specific
# Each niche re-ranks tools and picks a DIFFERENT winner than Sultan's Pick.
# Sultan's Picks: hubspot (CRM), asana (PM), convertkit (Email), semrush (SEO), freshdesk (Help Desk),
#   artisan (AI SDR), outreach (Sales Engagement), gong (CI), clay (Data Enrichment)
# =============================================================================

NICHES = {
    # ── Universal Niches (apply to all 5 categories) ──

    'solo-founders': {
        'name': 'Solo Founders',
        'title_pattern': 'Best {category} for Solo Founders ({year})',
        'meta_desc': 'The best {category_lower} for one-person businesses in {year}. Prioritizing simplicity, free tiers, and fast setup.',
        'intro': "You wear every hat. Your tools should be simple enough to set up in an afternoon and cheap enough to forget about. These are the {category_lower} tools that earn their place on a solo founder's screen.",
        'applies_to': ['crm', 'project-management', 'email-marketing', 'seo-tools', 'help-desk', 'ai-sdr', 'sales-engagement', 'conversation-intelligence', 'data-enrichment'],
        'rankings': {
            'crm': ['less-annoying-crm', 'hubspot', 'pipedrive', 'zoho-crm', 'freshsales'],
            'project-management': ['notion', 'trello', 'clickup', 'linear', 'asana'],
            'email-marketing': ['mailerlite', 'convertkit', 'brevo', 'beehiiv', 'mailchimp'],
            'seo-tools': ['mangools', 'ubersuggest', 'se-ranking', 'screaming-frog', 'ahrefs'],
            'help-desk': ['groove-helpdesk', 'help-scout', 'freshdesk', 'zoho-desk', 'hubspot-service'],
            'ai-sdr': ['smartlead', 'lavender', 'outplay', 'aisdr', 'salesrobot'],
            'sales-engagement': ['instantly', 'apollo', 'lemlist', 'mailshake', 'yesware'],
            'conversation-intelligence': ['fathom', 'fireflies', 'otter-ai', 'sybill', 'avoma'],
            'data-enrichment': ['lusha', 'apollo', 'leadiq', 'rocketreach', 'kaspr'],
        },
        'why_winners': {
            'crm': "One price, no tiers, no upsells. Less Annoying CRM is the anti-HubSpot: it does exactly what a solo founder needs and nothing more. Zero learning curve, zero surprise invoices.",
            'project-management': "Notion replaces your docs, your wiki, and your task manager in one free tool. Solo founders don't need Gantt charts. They need a flexible workspace that adapts to however they think.",
            'email-marketing': "MailerLite gives you automations, landing pages, and a clean email builder for free (up to 1,000 subscribers). It does 80% of what ConvertKit does at a fraction of the price.",
            'seo-tools': "Mangools packages five SEO tools into one affordable bundle. KWFinder alone is worth the price: the cleanest keyword difficulty scoring interface in the market.",
            'help-desk': "Groove is the simplest help desk you can buy. Shared inbox, knowledge base, and live chat at $4.80/user/mo. If you're the only person answering support emails, this is all you need.",
            'ai-sdr': "Smartlead gives solo founders unlimited mailbox rotation and AI warmup at $39/mo. You can run high-volume cold email campaigns without worrying about deliverability, and the setup takes an afternoon. Lavender coaches your writing, but Smartlead handles the entire sending infrastructure.",
            'sales-engagement': "Instantly gives you unlimited email accounts with built-in warmup at $30/mo. Solo founders doing cold outreach need volume and deliverability, not a complex multi-channel platform.",
            'conversation-intelligence': "Fathom records your Zoom calls and generates AI summaries for free. Unlimited recordings, no credit card. Every solo founder taking sales calls should be running Fathom.",
            'data-enrichment': "Lusha's Chrome extension finds emails and phone numbers from LinkedIn in seconds for $29/mo. Solo founders need quick lookups, not a $15K/yr database.",
        },
    },

    'small-teams': {
        'name': 'Small Teams (2-10)',
        'title_pattern': 'Best {category} for Small Teams ({year})',
        'meta_desc': 'The best {category_lower} for teams of 2-10 in {year}. Balancing features and simplicity without enterprise bloat.',
        'intro': "Your team is small enough to be nimble but big enough to need real tools. The picks here balance power and simplicity: enough features to grow into, without the bloat that slows you down.",
        'applies_to': ['crm', 'project-management', 'email-marketing', 'seo-tools', 'help-desk', 'ai-sdr', 'sales-engagement', 'conversation-intelligence', 'data-enrichment'],
        'rankings': {
            'crm': ['pipedrive', 'hubspot', 'close', 'freshsales', 'less-annoying-crm'],
            'project-management': ['monday', 'asana', 'clickup', 'notion', 'linear'],
            'email-marketing': ['activecampaign', 'convertkit', 'mailerlite', 'brevo', 'mailchimp'],
            'seo-tools': ['se-ranking', 'semrush', 'ahrefs', 'mangools', 'moz'],
            'help-desk': ['help-scout', 'freshdesk', 'zendesk', 'zoho-desk', 'intercom'],
            'ai-sdr': ['smartlead', 'lavender', 'outplay', 'amplemarket', 'nooks'],
            'sales-engagement': ['lemlist', 'apollo', 'instantly', 'reply-io', 'mixmax'],
            'conversation-intelligence': ['sybill', 'fireflies', 'fathom', 'avoma', 'gong'],
            'data-enrichment': ['apollo', 'lusha', 'clay', 'leadiq', 'uplead'],
        },
        'why_winners': {
            'crm': "Pipedrive's visual pipeline is the best in the business for small sales teams. Clean, focused, and built by salespeople. HubSpot has more features, but Pipedrive has less friction.",
            'project-management': "Monday.com's visual boards make status tracking effortless for small teams. Non-technical team members pick it up instantly, and the automation features scale well from 2 to 10 people.",
            'email-marketing': "ActiveCampaign has the most powerful automation builder in the category. Once your team is big enough to run multi-step workflows, ActiveCampaign pays for itself in saved time.",
            'seo-tools': "SE Ranking delivers 70% of Semrush's functionality at 35% of the price. For small teams watching their budget, the value per dollar is unbeatable.",
            'help-desk': "Help Scout makes customer support feel personal. No ticket numbers, no robotic auto-replies. Just clean, human conversations. Small teams who believe support is a differentiator belong here.",
            'ai-sdr': "Smartlead gives small outbound teams unlimited mailbox rotation and AI warmup at $39/mo. Your 2-5 person sales team gets enterprise-level cold email infrastructure at startup pricing.",
            'sales-engagement': "Lemlist's personalized images and liquid syntax make every cold email feel hand-written. Small teams sending hundreds of emails (not thousands) get better reply rates through personalization quality. The built-in B2B database covers basic prospecting without a separate data tool.",
            'conversation-intelligence': "Sybill automatically updates your CRM from call recordings and drafts follow-up emails. Small teams where reps wear multiple hats need AI that eliminates data entry, and Sybill does exactly that.",
            'data-enrichment': "Apollo's included contact database covers most small team prospecting needs at $49/user/mo. You get data + engagement in one tool instead of paying ZoomInfo $15K/yr for data alone.",
        },
    },

    'free': {
        'name': 'Free Tools',
        'title_pattern': 'Best Free {category} ({year})',
        'meta_desc': 'The best free {category_lower} in {year}. Ranked by what the free tier gives you: features, limits, and catches.',
        'intro': "Free tiers are marketing tools. Some are generous. Most are crippled demos designed to make you upgrade. These rankings cut through the marketing and tell you which free plans are worth using long-term.",
        'applies_to': ['crm', 'project-management', 'email-marketing', 'seo-tools', 'help-desk', 'ai-sdr', 'sales-engagement', 'conversation-intelligence', 'data-enrichment'],
        'rankings': {
            'crm': ['freshsales', 'hubspot', 'zoho-crm', 'monday-sales-crm', 'nutshell'],
            'project-management': ['clickup', 'notion', 'trello', 'asana', 'linear'],
            'email-marketing': ['mailerlite', 'brevo', 'beehiiv', 'convertkit', 'mailchimp'],
            'seo-tools': ['screaming-frog', 'ubersuggest', 'moz', 'mangools', 'se-ranking'],
            'help-desk': ['zoho-desk', 'freshdesk', 'hubspot-service', 'groove-helpdesk', 'liveagent'],
            'ai-sdr': ['outplay', 'lavender', 'smartlead', 'aisdr', 'salesrobot'],
            'sales-engagement': ['yesware', 'apollo', 'instantly', 'mailshake', 'reply-io'],
            'conversation-intelligence': ['fathom', 'fireflies', 'otter-ai', 'avoma', 'sybill'],
            'data-enrichment': ['apollo', 'lusha', 'kaspr', 'leadiq', 'rocketreach'],
        },
        'why_winners': {
            'crm': "Freshsales free includes a built-in phone dialer and email, features HubSpot charges for. For founders who want to make calls and send emails from their CRM without paying anything, Freshsales delivers more actionable features at $0.",
            'project-management': "ClickUp's free plan is the most generous in the category. Unlimited tasks, unlimited members, and access to docs, whiteboards, and chat. The UI takes getting used to, but no other free plan comes close in scope.",
            'email-marketing': "MailerLite's free tier gives you 1,000 subscribers with automations, landing pages, and a clean email builder. Most free tiers gut the features. MailerLite gives you enough to run a real email operation.",
            'seo-tools': "Screaming Frog's free tier crawls 500 URLs with full technical SEO analysis. Every technical SEO uses it. The free version handles most small-site audits without spending a cent.",
            'help-desk': "Zoho Desk's free tier supports 3 agents, one more than Freshdesk's free plan. For tiny teams stretching every dollar, that extra seat matters. The feature set covers ticketing, knowledge base, and basic automations.",
            'ai-sdr': "Outplay's free plan includes multi-channel outreach across email, phone, LinkedIn, and SMS. You get a full engagement platform at $0, covering more ground than Lavender's email-only coaching. For founders testing outbound channels, Outplay lets you experiment across all of them for free.",
            'sales-engagement': "Yesware's free plan adds email tracking and templates directly inside Gmail and Outlook. You can see who opens your emails and when, without paying anything or leaving your inbox. For free-tier users, that visibility into prospect engagement is more actionable than database access.",
            'conversation-intelligence': "Fathom records unlimited Zoom calls and generates AI summaries at no cost. No time limits, no credit card. The most generous free tier in conversation intelligence.",
            'data-enrichment': "Apollo's free plan includes contact database access and 50 export credits/month. You can prospect, find data, and send emails without paying anything. No other data provider comes close at $0.",
        },
    },

    'agencies': {
        'name': 'Agencies',
        'title_pattern': 'Best {category} for Agencies ({year})',
        'meta_desc': 'The best {category_lower} for agencies and consultancies in {year}. Multi-client management, white-label options, and scalable pricing.',
        'intro': "Agencies juggle multiple clients, multiple projects, and multiple billing cycles. Your tools need multi-account support, client-facing features, and pricing that doesn't destroy your margins as you scale.",
        'applies_to': ['crm', 'project-management', 'email-marketing', 'seo-tools', 'help-desk', 'ai-sdr', 'sales-engagement', 'conversation-intelligence', 'data-enrichment'],
        'rankings': {
            'crm': ['pipedrive', 'hubspot', 'salesforce', 'close', 'copper'],
            'project-management': ['teamwork', 'asana', 'monday', 'clickup', 'wrike'],
            'email-marketing': ['activecampaign', 'campaign-monitor', 'mailchimp', 'brevo', 'convertkit'],
            'seo-tools': ['ahrefs', 'semrush', 'se-ranking', 'moz', 'spyfu'],
            'help-desk': ['help-scout', 'zendesk', 'freshdesk', 'intercom', 'happyfox'],
            'ai-sdr': ['smartlead', 'instantly', 'outplay', 'lavender', 'amplemarket'],
            'sales-engagement': ['instantly', 'woodpecker', 'lemlist', 'apollo', 'reply-io'],
            'conversation-intelligence': ['fireflies', 'gong', 'fathom', 'sybill', 'avoma'],
            'data-enrichment': ['apollo', 'clay', 'lusha', 'uplead', 'leadiq'],
        },
        'why_winners': {
            'crm': "Pipedrive's visual pipeline scales cleanly across multiple client accounts. Agencies managing outbound for several clients at once get a clear view of every deal stage without the overhead of Salesforce.",
            'project-management': "Teamwork was built specifically for agencies. Billable time tracking, client permissions, and project templates tailored to agency workflows. Every other PM tool bolts these features on as an afterthought.",
            'email-marketing': "ActiveCampaign handles complex multi-client automation workflows that simpler tools can't touch. Agencies running drip campaigns across multiple accounts need this level of sophistication.",
            'seo-tools': "Ahrefs' Content Explorer and backlink index are essential for agencies managing SEO across multiple client sites. The project-based workflow makes client reporting cleaner than Semrush's dashboard.",
            'help-desk': "Help Scout's multi-mailbox setup lets agencies run separate support channels per client with distinct branding. The personal, email-like experience reflects well on both the agency and its clients.",
            'ai-sdr': "Smartlead's agency panel lets you manage cold email campaigns across multiple client accounts with separate mailbox pools. Unlimited mailbox rotation means your clients' domains stay clean.",
            'sales-engagement': "Instantly's multi-client workspace was built for agencies running cold outreach at scale. Separate campaigns, separate mailboxes, separate analytics per client. The pricing stays flat as you add accounts.",
            'conversation-intelligence': "Fireflies records and transcribes every client call, making institutional knowledge searchable. Agencies with high account manager turnover keep context alive when team members change.",
            'data-enrichment': "Apollo gives agencies a 275M+ contact database with built-in sequencing at $49/user/mo per client account. Agencies managing outbound for multiple clients get data + engagement in one platform, keeping per-client costs predictable. Clay's waterfall enrichment is more powerful, but Apollo's bundled pricing is easier to margin-stack across client retainers.",
        },
    },

    'ecommerce': {
        'name': 'E-Commerce',
        'title_pattern': 'Best {category} for E-Commerce ({year})',
        'meta_desc': 'The best {category_lower} for e-commerce and online stores in {year}. Shopify/WooCommerce integration, purchase data, and order management.',
        'intro': "E-commerce tools need to sync with your store, segment by purchase behavior, and handle order-related support tickets. Generic SaaS tools miss these requirements. These picks are built for businesses that sell products online.",
        'applies_to': ['crm', 'project-management', 'email-marketing', 'seo-tools', 'help-desk', 'ai-sdr', 'sales-engagement', 'conversation-intelligence', 'data-enrichment'],
        'rankings': {
            'crm': ['pipedrive', 'hubspot', 'freshsales', 'salesforce', 'zoho-crm'],
            'project-management': ['monday', 'asana', 'clickup', 'trello', 'notion'],
            'email-marketing': ['klaviyo', 'drip', 'activecampaign', 'mailchimp', 'brevo'],
            'seo-tools': ['ahrefs', 'semrush', 'surfer-seo', 'se-ranking', 'screaming-frog'],
            'help-desk': ['zendesk', 'freshdesk', 'intercom', 'help-scout', 'zoho-desk'],
            'ai-sdr': ['smartlead', 'lavender', 'amplemarket', 'outplay', 'salesrobot'],
            'sales-engagement': ['lemlist', 'apollo', 'instantly', 'reply-io', 'mailshake'],
            'conversation-intelligence': ['sybill', 'gong', 'fireflies', 'fathom', 'avoma'],
            'data-enrichment': ['apollo', 'clay', 'clearbit', 'lusha', 'uplead'],
        },
        'why_winners': {
            'crm': "Pipedrive's clean pipeline tracks wholesale accounts and B2B e-commerce deals more effectively than HubSpot's broader approach. The integrations with Shopify and WooCommerce pull purchase data directly into deal records.",
            'project-management': "Monday.com's visual boards handle product launches, inventory planning, and marketing campaigns in a format that non-technical e-commerce teams understand immediately.",
            'email-marketing': "Klaviyo is the dominant email platform for Shopify stores. Purchase-based segmentation, predictive analytics, and pre-built e-commerce automations generate measurable revenue. No other tool matches its Shopify integration depth.",
            'seo-tools': "Ahrefs excels at product page optimization and competitor keyword research, the two SEO tasks that directly drive e-commerce revenue. The Content Explorer finds link-building opportunities faster than Semrush.",
            'help-desk': "Zendesk's Shopify integration pulls order data directly into support tickets. Agents see purchase history, shipping status, and returns without switching tabs. For high-volume e-commerce support, that context saves hours daily.",
            'ai-sdr': "Smartlead handles the high-volume cold email that B2B e-commerce wholesale teams need. Unlimited mailboxes and AI warmup keep deliverability high when you're prospecting retail buyers at scale.",
            'sales-engagement': "Lemlist's personalized images and landing pages stand out in crowded e-commerce inboxes. Custom product images embedded in cold emails convert better than plain text for physical product businesses.",
            'conversation-intelligence': "Sybill's automatic CRM updates capture buyer signals from wholesale and partnership calls. E-commerce teams with long sales cycles to retail chains need this level of call documentation.",
            'data-enrichment': "Apollo's included database covers B2B buyer contacts at retail chains, distributors, and wholesale buyers. E-commerce brands doing outbound to retail partners get data + engagement in one platform.",
        },
    },

    'startups': {
        'name': 'Startups on a Budget',
        'title_pattern': 'Best {category} for Startups ({year})',
        'meta_desc': 'The best {category_lower} for startups and early-stage companies in {year}. Maximum value under $50/mo.',
        'intro': "Startups burn cash on tools they outgrow in six months or underpay for tools that hold them back. These picks maximize value per dollar: enough capability to scale, cheap enough to survive while you find product-market fit.",
        'applies_to': ['crm', 'project-management', 'email-marketing', 'seo-tools', 'help-desk', 'ai-sdr', 'sales-engagement', 'conversation-intelligence', 'data-enrichment'],
        'rankings': {
            'crm': ['pipedrive', 'hubspot', 'freshsales', 'less-annoying-crm', 'zoho-crm'],
            'project-management': ['clickup', 'linear', 'notion', 'asana', 'trello'],
            'email-marketing': ['brevo', 'mailerlite', 'convertkit', 'beehiiv', 'mailchimp'],
            'seo-tools': ['se-ranking', 'mangools', 'ubersuggest', 'screaming-frog', 'ahrefs'],
            'help-desk': ['groove-helpdesk', 'freshdesk', 'zoho-desk', 'help-scout', 'hubspot-service'],
            'ai-sdr': ['smartlead', 'lavender', 'outplay', 'aisdr', 'salesrobot'],
            'sales-engagement': ['instantly', 'apollo', 'lemlist', 'mailshake', 'yesware'],
            'conversation-intelligence': ['fathom', 'fireflies', 'otter-ai', 'sybill', 'avoma'],
            'data-enrichment': ['apollo', 'lusha', 'leadiq', 'kaspr', 'rocketreach'],
        },
        'why_winners': {
            'crm': "Pipedrive starts at $14/user/mo with a focused, fast interface. Startups need a CRM they can adopt in a day and afford for a year. HubSpot's free tier is tempting, but paid Pipedrive outperforms free HubSpot on pipeline management.",
            'project-management': "ClickUp's free plan is unlimited, and the $7/user/mo paid plan includes everything most startups need: docs, whiteboards, time tracking, and custom views. More functionality per dollar than any competitor.",
            'email-marketing': "Brevo charges by emails sent, not contacts stored. For startups growing their list fast, this pricing model saves real money. Email, SMS, chat, and CRM in one tool, all under $25/mo for most early-stage companies.",
            'seo-tools': "SE Ranking delivers Semrush-caliber features (keyword research, rank tracking, site audits) at $44/mo vs. Semrush's $130. Startups get 70% of the capability at 35% of the cost.",
            'help-desk': "Groove starts at $4.80/user/mo. That is cheaper than every competitor's lowest tier. For a startup handling 10-50 support tickets a day, Groove's shared inbox and knowledge base are all you need.",
            'ai-sdr': "Smartlead at $39/mo gives startups unlimited mailbox rotation and AI warmup for high-volume cold email. Early-stage companies sending thousands of outbound emails per month need deliverability infrastructure, and Smartlead's pricing stays flat as you scale sending volume.",
            'sales-engagement': "Instantly's unlimited email accounts and built-in warmup at $30/mo give startups cold email infrastructure at the lowest price in the category. When cash is tight, Instantly delivers volume and deliverability without the $49/user/mo per-seat cost of Apollo.",
            'conversation-intelligence': "Fathom is free. Unlimited call recordings and AI summaries with no credit card. Every startup founder taking sales calls should install Fathom today.",
            'data-enrichment': "Apollo's free tier includes database access and 50 credits/month. For startups pre-revenue, you get contact data without any financial commitment. Upgrade to $49/mo when you need more volume.",
        },
    },

    # ── Category-Specific Niches ──

    'outbound-sales': {
        'name': 'Outbound Sales Teams',
        'title_pattern': 'Best {category} for Outbound Sales ({year})',
        'meta_desc': 'The best {category_lower} for outbound sales teams in {year}. Built-in dialers, email sequences, and high-volume prospecting.',
        'intro': "Outbound sales runs on volume: calls made, emails sent, replies earned. Your CRM needs a built-in dialer, email sequences, and a UI that keeps reps in flow instead of clicking between tabs.",
        'applies_to': ['crm'],
        'rankings': {
            'crm': ['close', 'hubspot', 'pipedrive', 'salesforce', 'freshsales'],
        },
        'why_winners': {
            'crm': "Close has a built-in power dialer, SMS messaging, and email sequences, the three tools outbound teams use every hour. HubSpot makes you bolt these on. Close ships them in the box.",
        },
    },

    'google-workspace': {
        'name': 'Google Workspace Teams',
        'title_pattern': 'Best {category} for Google Workspace ({year})',
        'meta_desc': 'The best {category_lower} for Google Workspace teams in {year}. Native Gmail and Google Calendar integration.',
        'intro': "If your team lives in Gmail and Google Calendar, your CRM should too. These picks integrate natively with Google Workspace: no tab switching, no manual data entry, no sync headaches.",
        'applies_to': ['crm'],
        'rankings': {
            'crm': ['copper', 'hubspot', 'pipedrive', 'zoho-crm', 'freshsales'],
        },
        'why_winners': {
            'crm': "Copper lives inside Gmail. It auto-captures contacts, syncs calendar events, and surfaces deal information without leaving your inbox. For teams that refuse to leave Google Workspace, Copper eliminates the CRM-as-a-separate-app problem entirely.",
        },
    },

    'newsletters': {
        'name': 'Newsletter Operators',
        'title_pattern': 'Best {category} for Newsletters ({year})',
        'meta_desc': 'The best {category_lower} for newsletters and media businesses in {year}. Growth tools, monetization, and subscriber management.',
        'intro': "Newsletter operators need growth tools, monetization options, and subscriber analytics, features that general email platforms treat as afterthoughts. These picks are built for people building media businesses around email.",
        'applies_to': ['email-marketing'],
        'rankings': {
            'email-marketing': ['beehiiv', 'convertkit', 'mailerlite', 'mailchimp', 'campaign-monitor'],
        },
        'why_winners': {
            'email-marketing': "Beehiiv was built by the Morning Brew team specifically for newsletter operators. Built-in referral programs, ad network monetization, and custom websites come standard. ConvertKit is great for creators, but Beehiiv is purpose-built for newsletters as a business.",
        },
    },

    'shopify': {
        'name': 'Shopify Stores',
        'title_pattern': 'Best {category} for Shopify ({year})',
        'meta_desc': 'The best {category_lower} for Shopify stores in {year}. Native Shopify integration, purchase-based segmentation, and e-commerce workflows.',
        'intro': "Shopify stores need email tools that understand purchase behavior, abandoned carts, and product recommendations. Generic email platforms bolt these features on. These picks build them in.",
        'applies_to': ['email-marketing'],
        'rankings': {
            'email-marketing': ['klaviyo', 'drip', 'activecampaign', 'mailchimp', 'brevo'],
        },
        'why_winners': {
            'email-marketing': "Klaviyo is the default email platform for serious Shopify stores. Predictive analytics, purchase-based segmentation, and automated flows based on shopping behavior generate measurable revenue that justifies the premium pricing.",
        },
    },

    'beginners': {
        'name': 'SEO Beginners',
        'title_pattern': 'Best {category} for Beginners ({year})',
        'meta_desc': 'The best {category_lower} for SEO beginners in {year}. Simple interfaces, affordable pricing, and gentle learning curves.',
        'intro': "SEO tools can be intimidating. The best tools for beginners make keyword research, rank tracking, and site audits approachable without dumbing down the data. Start here, graduate to Semrush or Ahrefs later.",
        'applies_to': ['seo-tools'],
        'rankings': {
            'seo-tools': ['mangools', 'ubersuggest', 'se-ranking', 'moz', 'screaming-frog'],
        },
        'why_winners': {
            'seo-tools': "Mangools' KWFinder is the most approachable keyword research interface in the market. Color-coded keyword difficulty, clean SERP analysis, and five tools bundled at a starter-friendly price. You can learn SEO fundamentals without drowning in data.",
        },
    },

    'content-teams': {
        'name': 'Content Teams',
        'title_pattern': 'Best {category} for Content Teams ({year})',
        'meta_desc': 'The best {category_lower} for content marketing teams in {year}. Content optimization, topic clusters, and on-page scoring.',
        'intro': "Content teams need tools that go beyond keyword research. On-page optimization, content scoring, and topic cluster planning separate amateur content operations from professional ones.",
        'applies_to': ['seo-tools'],
        'rankings': {
            'seo-tools': ['surfer-seo', 'semrush', 'ahrefs', 'se-ranking', 'moz'],
        },
        'why_winners': {
            'seo-tools': "Surfer SEO's Content Editor scores your writing in real-time against top-ranking pages. It tells you exactly what terms to include, what word count to target, and how your content compares to the competition. Content teams ship better articles faster with Surfer.",
        },
    },

    'engineering': {
        'name': 'Engineering Teams',
        'title_pattern': 'Best {category} for Engineering Teams ({year})',
        'meta_desc': 'The best {category_lower} for software engineering teams in {year}. Git integration, sprint planning, and keyboard-first workflows.',
        'intro': "Engineering teams care about speed, keyboard shortcuts, and tight Git integration. Generic project management tools add friction that compounds across every sprint. These picks are built for people who ship software.",
        'applies_to': ['project-management'],
        'rankings': {
            'project-management': ['linear', 'asana', 'clickup', 'notion', 'wrike'],
        },
        'why_winners': {
            'project-management': "Linear is the fastest project management tool you will ever use. Sub-50ms interactions, keyboard-driven navigation, and Git integrations designed by engineers who care about craft. Asana works for engineering teams. Linear was built for them.",
        },
    },

    'remote-teams': {
        'name': 'Remote Teams',
        'title_pattern': 'Best {category} for Remote Teams ({year})',
        'meta_desc': 'The best {category_lower} for remote and distributed teams in {year}. Async communication, documentation, and timezone-friendly workflows.',
        'intro': "Remote teams can't tap someone on the shoulder. Documentation, async updates, and clear task ownership replace hallway conversations. Your project management tool should make remote collaboration feel natural.",
        'applies_to': ['project-management'],
        'rankings': {
            'project-management': ['notion', 'basecamp', 'asana', 'clickup', 'monday'],
        },
        'why_winners': {
            'project-management': "Notion combines docs, wikis, and task management in one workspace, the three things remote teams need most. Decisions get documented where work happens. Team members in different timezones can catch up by reading instead of scheduling another meeting.",
        },
    },

    'saas-support': {
        'name': 'SaaS Companies',
        'title_pattern': 'Best {category} for SaaS ({year})',
        'meta_desc': 'The best {category_lower} for SaaS companies in {year}. In-app messaging, product-led support, and developer-friendly integrations.',
        'intro': "SaaS support happens inside the product. Chat widgets, in-app guides, and AI-powered bots deflect tickets before they are created. These picks understand the SaaS support model.",
        'applies_to': ['help-desk'],
        'rankings': {
            'help-desk': ['intercom', 'zendesk', 'freshdesk', 'help-scout', 'hubspot-service'],
        },
        'why_winners': {
            'help-desk': "Intercom pioneered chat-first support for SaaS. The Fin AI chatbot resolves common questions before they become tickets. Product tours, in-app messaging, and conversation routing built specifically for software companies.",
        },
    },

    'one-person': {
        'name': 'One-Person Support',
        'title_pattern': 'Best {category} for One-Person Support ({year})',
        'meta_desc': 'The best {category_lower} for solo support operators in {year}. Simple setup, affordable pricing, and no enterprise bloat.',
        'intro': "When you are the entire support team, you need a help desk that stays out of your way. Fast setup, simple pricing, and just enough features to keep customers happy without building a support operation you don't need yet.",
        'applies_to': ['help-desk'],
        'rankings': {
            'help-desk': ['groove-helpdesk', 'help-scout', 'freshdesk', 'zoho-desk', 'kayako'],
        },
        'why_winners': {
            'help-desk': "Groove is the simplest, cheapest help desk on the market. $4.80/user/mo for shared inbox, knowledge base, and live chat. When you are the only person answering support emails, enterprise features are clutter. Groove gives you exactly what you need.",
        },
    },
}


# =============================================================================
# INDUSTRIES (Phase 2) — 17 industries in 3 tiers
# Each industry recommends the best tool from EACH category.
# =============================================================================

INDUSTRIES = {
    # ── Tier 1 (full content, high search volume) ──

    'ecommerce': {
        'name': 'E-Commerce & Online Stores',
        'tier': 1,
        'description': 'SaaS tools optimized for online stores. Shopify and WooCommerce integrations, purchase-based segmentation, and order management.',
        'intro': "E-commerce businesses need tools that sync with their store, segment customers by purchase behavior, and handle order-related support. Here are The Sultan's picks for online stores.",
        'picks': {
            'crm': {'tool': 'hubspot', 'why': "Free CRM with strong Shopify integration. Tracks every customer interaction from first visit to repeat purchase."},
            'email-marketing': {'tool': 'klaviyo', 'why': "The dominant email platform for Shopify stores. Purchase-based segmentation and automated flows that directly drive revenue."},
            'seo-tools': {'tool': 'ahrefs', 'why': "Best for product page optimization and competitor keyword research. Content Explorer finds link-building opportunities for e-commerce."},
            'project-management': {'tool': 'monday', 'why': "Visual boards handle product launches, inventory planning, and marketing campaigns in a format the whole team understands."},
            'help-desk': {'tool': 'freshdesk', 'why': "Affordable omnichannel support with Shopify integration. Pulls order data into tickets so agents have full context."},
            'ai-sdr': {'tool': 'smartlead', 'why': "High-volume cold email infrastructure for B2B wholesale prospecting. Unlimited mailboxes keep your domain reputation clean."},
            'sales-engagement': {'tool': 'lemlist', 'why': "Personalized product images in cold emails convert better for physical product businesses. Built-in B2B database finds retail buyers."},
            'conversation-intelligence': {'tool': 'sybill', 'why': "Auto-updates CRM from wholesale buyer calls. E-commerce brands with B2B sales channels need call documentation without manual data entry."},
            'data-enrichment': {'tool': 'apollo', 'why': "Contact data for retail buyers and distributors at $49/user/mo. Includes engagement features so you can prospect and sequence in one tool."},
        },
    },

    'saas': {
        'name': 'SaaS Companies',
        'tier': 1,
        'description': 'Tools built for software companies. Product-led support, developer-friendly integrations, and subscription lifecycle management.',
        'intro': "SaaS companies operate on recurring revenue. Every tool choice affects churn, activation, and expansion. These picks understand the SaaS business model.",
        'picks': {
            'crm': {'tool': 'hubspot', 'why': "The best free CRM for tracking leads through a SaaS funnel. Native integrations with every marketing and support tool you will need."},
            'email-marketing': {'tool': 'activecampaign', 'why': "Sophisticated automation workflows for onboarding sequences, trial nurtures, and expansion campaigns. The CRM integration handles the full lifecycle."},
            'seo-tools': {'tool': 'semrush', 'why': "Content marketing tools alongside keyword research make Semrush the complete SEO platform for SaaS companies investing in organic growth."},
            'project-management': {'tool': 'linear', 'why': "Built for software teams. Sub-50ms interactions, keyboard-first design, and tight Git integration for engineering-driven SaaS companies."},
            'help-desk': {'tool': 'intercom', 'why': "Chat-first support with an AI bot (Fin) that resolves common questions before they become tickets. In-app messaging keeps support inside the product."},
            'ai-sdr': {'tool': 'artisan', 'why': "The most polished AI SDR for SaaS outbound. Ava handles initial outreach well and integrates with standard SaaS sales stacks."},
            'sales-engagement': {'tool': 'outreach', 'why': "The deepest sequencing engine for SaaS sales cycles. Handles everything from SDR prospecting to AE deal management with AI-powered insights."},
            'conversation-intelligence': {'tool': 'gong', 'why': "The gold standard for SaaS sales coaching. Call analytics surface win/loss patterns across your sales org and track competitive mentions."},
            'data-enrichment': {'tool': 'clay', 'why': "Waterfall enrichment builds hyper-targeted prospect lists for SaaS ICP-driven outbound. The workflow builder handles complex enrichment logic."},
        },
    },

    'agencies': {
        'name': 'Agencies & Consultancies',
        'tier': 1,
        'description': 'Multi-client management, billable time tracking, and scalable project workflows for agencies of all sizes.',
        'intro': "Agencies manage multiple clients with different needs, timelines, and budgets. Your tools need to scale per-client without scaling your costs at the same rate.",
        'picks': {
            'crm': {'tool': 'pipedrive', 'why': "Visual pipeline management across multiple client accounts. Clean deal tracking without Salesforce overhead."},
            'email-marketing': {'tool': 'activecampaign', 'why': "Multi-client automation workflows with enough sophistication to serve demanding clients. Agency-friendly pricing as you scale."},
            'seo-tools': {'tool': 'semrush', 'why': "Client reporting, competitive analysis, and content tools in one platform. The agency features justify the premium pricing."},
            'project-management': {'tool': 'teamwork', 'why': "Built for agencies. Billable time tracking, client permissions, and project templates designed for client services work."},
            'help-desk': {'tool': 'help-scout', 'why': "Multi-mailbox setup with distinct branding per client. The personal support experience reflects well on your agency."},
            'ai-sdr': {'tool': 'smartlead', 'why': "Agency panel manages cold email campaigns across client accounts. Unlimited mailboxes per client with separate deliverability tracking."},
            'sales-engagement': {'tool': 'instantly', 'why': "Multi-workspace setup built for agencies running client outbound. Flat pricing as you scale across accounts."},
            'conversation-intelligence': {'tool': 'fireflies', 'why': "Records every client call and makes them searchable. Agencies preserve context when account managers change."},
            'data-enrichment': {'tool': 'clay', 'why': "Custom enrichment workflows per client ICP. Agencies build bespoke data pipelines instead of one-size-fits-all database exports."},
        },
    },

    'real-estate': {
        'name': 'Real Estate',
        'tier': 1,
        'description': 'Contact management for leads and listings, automated follow-ups, and client communication tools for agents and brokerages.',
        'intro': "Real estate runs on relationships and follow-up. Your CRM tracks leads for months before they close. Your email keeps you top-of-mind. Your help desk handles tenant and client inquiries.",
        'picks': {
            'crm': {'tool': 'pipedrive', 'why': "The visual pipeline maps perfectly to real estate deal stages: lead, showing, offer, inspection, closing. Agents see their entire book of business at a glance."},
            'email-marketing': {'tool': 'mailerlite', 'why': "Clean drip sequences for listing alerts and market updates. Affordable enough for solo agents, powerful enough for small brokerages."},
            'seo-tools': {'tool': 'se-ranking', 'why': "Local SEO tools and rank tracking for geographic keywords. Real estate agents need hyperlocal search visibility, and SE Ranking delivers at a fraction of Semrush's price."},
            'project-management': {'tool': 'trello', 'why': "Kanban boards for tracking listings, closings, and tasks. Dead simple. Agents who have never used PM software pick it up in minutes."},
            'help-desk': {'tool': 'help-scout', 'why': "Personal, email-like support for tenant inquiries and client follow-ups. The Beacon widget works on brokerage websites."},
            'ai-sdr': {'tool': 'lavender', 'why': "AI email coaching helps agents write better listing outreach and buyer follow-ups. At $29/mo, the ROI shows up in response rates."},
            'sales-engagement': {'tool': 'mailshake', 'why': "Simple cold email sequences for agent prospecting. Easy enough for real estate professionals without technical backgrounds."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free call recording for buyer consultations and listing presentations. Agents review conversations to improve their pitch."},
            'data-enrichment': {'tool': 'lusha', 'why': "Quick contact lookup for property owners and decision-makers. The Chrome extension finds numbers directly from LinkedIn profiles."},
        },
    },

    'professional-services': {
        'name': 'Professional Services',
        'tier': 1,
        'description': 'Tools for law firms, accounting firms, and consultancies. Client relationship management, project tracking, and communication.',
        'intro': "Professional services firms sell expertise and relationships. Your tools need to track client engagements, manage billable projects, and maintain the kind of communication that justifies premium fees.",
        'picks': {
            'crm': {'tool': 'less-annoying-crm', 'why': "Simple, affordable, and zero-complexity CRM for firms that need contact tracking without enterprise overhead. One flat price, no upsells."},
            'email-marketing': {'tool': 'convertkit', 'why': "Clean newsletters and drip sequences for thought leadership content. Professional services firms win clients by demonstrating expertise. ConvertKit makes that easy."},
            'seo-tools': {'tool': 'semrush', 'why': "Content marketing tools for publishing authoritative articles that attract high-intent clients searching for professional expertise."},
            'project-management': {'tool': 'asana', 'why': "Workflow automation for client engagements, deliverable tracking, and team coordination. Enough structure for complex projects without Wrike-level complexity."},
            'help-desk': {'tool': 'help-scout', 'why': "Client communication that feels personal. Professional services clients expect white-glove treatment. Help Scout's email-like interface delivers it."},
            'ai-sdr': {'tool': 'lavender', 'why': "Polishes outreach emails for consulting and advisory firms. Professional services firms live and die by written communication quality."},
            'sales-engagement': {'tool': 'mixmax', 'why': "Gmail-native engagement for firms that live in Google Workspace. Sequences and scheduling without leaving the inbox."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free call recording for client meetings and discovery sessions. Professional services firms document conversations for scope and compliance."},
            'data-enrichment': {'tool': 'leadiq', 'why': "LinkedIn-to-CRM prospecting for service firms targeting specific companies. One-click capture feeds contacts into business development pipelines."},
        },
    },

    'startups': {
        'name': 'Startups & Early-Stage',
        'tier': 1,
        'description': 'Maximum value on a startup budget. Tools that scale from 2-person founding team to 50-person growth stage.',
        'intro': "Startups need tools that are cheap enough to survive pre-revenue and capable enough to scale post-product-market-fit. These picks will not need replacing when you raise your Series A.",
        'picks': {
            'crm': {'tool': 'hubspot', 'why': "Start free, upgrade as you grow. The CRM, marketing hub, and service hub scale alongside your startup from day one to IPO."},
            'email-marketing': {'tool': 'brevo', 'why': "Pay by emails sent, not contacts stored. Startups growing fast save real money with this pricing model. Email, SMS, and CRM under one roof."},
            'seo-tools': {'tool': 'se-ranking', 'why': "Semrush features at startup-friendly pricing. Keyword research, rank tracking, and site audits for $44/mo instead of $130."},
            'project-management': {'tool': 'clickup', 'why': "The most generous free plan in PM. Unlimited tasks and members, plus docs, whiteboards, and chat. More functionality per dollar than any competitor."},
            'help-desk': {'tool': 'freshdesk', 'why': "Free for 2 agents, then scales affordably. Startups get Zendesk-level features without Zendesk-level pricing."},
            'ai-sdr': {'tool': 'lavender', 'why': "At $29/mo, the cheapest way to improve outbound email quality. Startups can't risk $2-5K/mo on unproven AI agents."},
            'sales-engagement': {'tool': 'apollo', 'why': "Prospecting data + engagement in one platform for $49/user/mo. Replaces a $15K/yr ZoomInfo + $100/user/mo Outreach stack."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free unlimited call recording. Every startup founder taking sales calls needs this installed yesterday."},
            'data-enrichment': {'tool': 'apollo', 'why': "Free tier includes database access. Upgrade to $49/mo when revenue supports it. Best data value for startups."},
        },
    },

    # ── Tier 2 (solid content, moderate volume) ──

    'nonprofits': {
        'name': 'Nonprofits & Charities',
        'tier': 2,
        'description': 'Donor management, volunteer coordination, and communication tools with nonprofit-friendly pricing.',
        'intro': "Nonprofits stretch every dollar. Many SaaS tools offer nonprofit discounts, but the right tool at full price beats the wrong tool at 50% off. These picks deliver value where nonprofits need it most.",
        'picks': {
            'crm': {'tool': 'hubspot', 'why': "Free CRM for donor and volunteer contact management. HubSpot offers nonprofit discounts on paid tiers."},
            'email-marketing': {'tool': 'mailerlite', 'why': "Best value in email marketing with a generous free tier. Landing pages and automations included, critical for donation campaigns."},
            'seo-tools': {'tool': 'mangools', 'why': "Affordable SEO tools for nonprofits building organic visibility. KWFinder identifies grant-related and cause-related search opportunities."},
            'project-management': {'tool': 'asana', 'why': "Free for up to 10 users with enough features for program management and volunteer coordination. Asana offers 50% nonprofit discounts."},
            'help-desk': {'tool': 'freshdesk', 'why': "Free tier for 2 agents handles most nonprofit support needs. Covers donor inquiries, volunteer questions, and general constituent support."},
            'ai-sdr': {'tool': 'lavender', 'why': "Improves fundraising outreach emails at $29/mo. Nonprofits with limited budgets get measurable improvements in donor response rates."},
            'sales-engagement': {'tool': 'apollo', 'why': "Free tier covers basic outreach needs. Nonprofits can prospect grant-giving foundations and corporate sponsors without paying."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free call recording for donor meetings and board calls. Zero-cost documentation for nonprofits watching every dollar."},
            'data-enrichment': {'tool': 'apollo', 'why': "Free database access for finding corporate contacts and foundation directors. Nonprofits get prospecting data at no cost."},
        },
    },

    'healthcare': {
        'name': 'Healthcare & Wellness',
        'tier': 2,
        'description': 'Patient communication, appointment management, and compliance-aware tools for healthcare practices.',
        'intro': "Healthcare practices handle sensitive data. Your tools need to be straightforward enough for non-technical staff and trustworthy enough for patient data. Compliance matters, but so does simplicity.",
        'picks': {
            'crm': {'tool': 'less-annoying-crm', 'why': "Dead simple patient relationship tracking for small practices. No complex setup, no steep learning curve. Just contact management that works."},
            'email-marketing': {'tool': 'mailerlite', 'why': "Clean appointment reminders and wellness newsletters. The drag-and-drop builder is simple enough for practice managers without marketing experience."},
            'seo-tools': {'tool': 'se-ranking', 'why': "Local SEO tracking for practice websites. Patients search for providers near them. SE Ranking monitors your local search performance affordably."},
            'project-management': {'tool': 'trello', 'why': "Simple kanban boards for tracking patient onboarding, operational tasks, and internal projects. No learning curve for clinical staff."},
            'help-desk': {'tool': 'help-scout', 'why': "Patient inquiries handled with personal, human communication. The email-like interface avoids the cold, corporate feel of ticket-based systems."},
            'ai-sdr': {'tool': 'lavender', 'why': "Email coaching for healthcare business development. Helps practice managers write better outreach to referral partners."},
            'sales-engagement': {'tool': 'mailshake', 'why': "Simple sequences for healthcare business development. Easy enough for practice managers without sales backgrounds."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free call documentation for provider consultations. Healthcare practices benefit from recorded conversations for compliance and quality."},
            'data-enrichment': {'tool': 'lusha', 'why': "Quick lookup for healthcare administrator contacts. Simple Chrome extension for finding decision-makers at hospitals and clinics."},
        },
    },

    'education': {
        'name': 'Education & Coaching',
        'tier': 2,
        'description': 'Student communication, course management, and audience building for educators, coaches, and online course creators.',
        'intro': "Educators and coaches build audiences, sell courses, and manage student relationships. Your stack needs to handle content delivery, email marketing, and student support in tools that educators can manage without a tech team.",
        'picks': {
            'crm': {'tool': 'hubspot', 'why': "Free CRM for tracking student leads, enrollment pipeline, and alumni relationships. The forms and landing pages convert course-curious visitors into students."},
            'email-marketing': {'tool': 'convertkit', 'why': "Built for creators and educators selling digital products. Course launch sequences, student onboarding emails, and paid newsletter support."},
            'seo-tools': {'tool': 'mangools', 'why': "Simple keyword research for course creators building organic traffic. Find what potential students are searching for without the complexity of Semrush."},
            'project-management': {'tool': 'notion', 'why': "Course outlines, lesson plans, and student resources all live in one flexible workspace. Notion's template ecosystem includes ready-made education workflows."},
            'help-desk': {'tool': 'groove-helpdesk', 'why': "Simple student support at the lowest price. Shared inbox handles enrollment questions, tech support, and course feedback without overcomplicating things."},
            'ai-sdr': {'tool': 'lavender', 'why': "AI coaching for student recruitment emails. Improves response rates on enrollment outreach."},
            'sales-engagement': {'tool': 'mailshake', 'why': "Simple sequences for course launches and student outreach. Educators don't need complex engagement platforms."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free recording for student consultation calls. Course creators document feedback and testimonials."},
            'data-enrichment': {'tool': 'apollo', 'why': "Free tier finds contacts at schools, districts, and corporate training departments."},
        },
    },

    'creators': {
        'name': 'Creators & Media',
        'tier': 2,
        'description': 'Audience building, newsletter monetization, and content management for creators, bloggers, and media operators.',
        'intro': "Creators monetize attention. Your tools need to grow your audience, monetize your content, and manage the business side without pulling you away from creating.",
        'picks': {
            'crm': {'tool': 'hubspot', 'why': "Free CRM tracks sponsorship deals, brand partnerships, and collaboration opportunities. The deal pipeline manages your creator business relationships."},
            'email-marketing': {'tool': 'convertkit', 'why': "The creator's email platform. Visual automations, digital product sales, and a creator-first business model. Built by creators, for creators."},
            'seo-tools': {'tool': 'ahrefs', 'why': "Content Explorer identifies trending topics and link-building opportunities. Creators who invest in SEO build sustainable organic traffic alongside social media."},
            'project-management': {'tool': 'notion', 'why': "Content calendars, editorial workflows, and knowledge bases in one beautiful workspace. The creator economy runs on Notion."},
            'help-desk': {'tool': 'help-scout', 'why': "Personal fan and customer support that maintains the creator's voice. Community members get human responses, not ticket numbers."},
            'ai-sdr': {'tool': 'lavender', 'why': "Email coaching for sponsorship outreach. Creators pitching brands need emails that stand out in crowded inboxes."},
            'sales-engagement': {'tool': 'lemlist', 'why': "Personalized outreach for brand partnerships. Custom images and landing pages make sponsorship pitches more engaging."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free call recording for brand meetings and podcast interviews. Creators capture content ideas from every conversation."},
            'data-enrichment': {'tool': 'apollo', 'why': "Free tier finds marketing manager and sponsorship contacts at target brands."},
        },
    },

    'financial-services': {
        'name': 'Financial Services',
        'tier': 2,
        'description': 'Client relationship management, compliance-aware communication, and lead nurturing for financial advisors and firms.',
        'intro': "Financial services firms manage high-value client relationships over long timeframes. Your tools need to track every touchpoint, nurture prospects for months, and maintain the level of professionalism your clients expect.",
        'picks': {
            'crm': {'tool': 'salesforce', 'why': "The depth of customization handles complex financial product portfolios. Compliance tracking, approval workflows, and audit trails built into the platform."},
            'email-marketing': {'tool': 'activecampaign', 'why': "Sophisticated drip campaigns for prospect nurturing across long sales cycles. Conditional workflows adapt messaging based on engagement signals."},
            'seo-tools': {'tool': 'semrush', 'why': "Content marketing tools for building authoritative financial content. Keyword research identifies high-intent search terms from prospects evaluating financial services."},
            'project-management': {'tool': 'asana', 'why': "Client onboarding workflows, compliance task tracking, and team coordination for financial advisory firms managing multiple client engagements."},
            'help-desk': {'tool': 'zendesk', 'why': "Enterprise-grade support with audit trails and SLA management. Financial services clients expect responsive, documented support interactions."},
            'ai-sdr': {'tool': 'amplemarket', 'why': "AI-powered outbound for financial advisory prospecting. Compliant, professional outreach at scale."},
            'sales-engagement': {'tool': 'outreach', 'why': "Enterprise-grade sequencing for long financial services sales cycles. Compliance-friendly with audit trails."},
            'conversation-intelligence': {'tool': 'gong', 'why': "Call analytics for financial advisor coaching. Tracks compliance language and client conversation quality."},
            'data-enrichment': {'tool': 'zoominfo', 'why': "The deepest firmographic data for identifying high-net-worth prospects and corporate finance decision-makers."},
        },
    },

    'construction': {
        'name': 'Construction & Trades',
        'tier': 2,
        'description': 'Project tracking, client communication, and lead management for contractors, builders, and trade businesses.',
        'intro': "Construction and trades businesses juggle bids, projects, subcontractors, and clients. Your tools need to work from a phone on a job site, track project milestones, and help you win more bids.",
        'picks': {
            'crm': {'tool': 'pipedrive', 'why': "Visual pipeline tracks bids from lead to signed contract. The mobile app lets contractors manage deals from the job site."},
            'email-marketing': {'tool': 'mailerlite', 'why': "Simple email campaigns for seasonal promotions, project showcases, and referral requests. Affordable enough for small contractors."},
            'seo-tools': {'tool': 'se-ranking', 'why': "Local SEO tracking for contractor websites. When homeowners search for contractors near them, SE Ranking helps you show up."},
            'project-management': {'tool': 'monday', 'why': "Visual boards track project milestones, subcontractor schedules, and material orders. Non-technical crews understand the interface immediately."},
            'help-desk': {'tool': 'freshdesk', 'why': "Handles homeowner inquiries, warranty claims, and project update requests. The free tier covers most small contractor needs."},
            'ai-sdr': {'tool': 'lavender', 'why': "Email coaching for bid proposals and contractor outreach. Helps construction professionals write cleaner business emails."},
            'sales-engagement': {'tool': 'mailshake', 'why': "Simple cold email for subcontractor and client prospecting. Construction teams don't need complex platforms."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free recording for client meetings and bid discussions. Captures scope details that prevent disputes."},
            'data-enrichment': {'tool': 'lusha', 'why': "Quick contact lookup for property developers and general contractors. Simple LinkedIn extension for the trades."},
        },
    },

    # ── Tier 3 (lighter content, lower volume) ──

    'restaurants': {
        'name': 'Restaurants & Hospitality',
        'tier': 3,
        'description': 'Guest communication, reservation management, and marketing for restaurants, hotels, and hospitality businesses.',
        'intro': "Restaurants and hospitality businesses thrive on repeat customers and local visibility. Simple tools that handle guest communication and local marketing outperform complex systems your staff will not use.",
        'picks': {
            'crm': {'tool': 'hubspot', 'why': "Free CRM for tracking catering leads, event inquiries, and VIP guest relationships. Simple enough for restaurant managers."},
            'email-marketing': {'tool': 'mailerlite', 'why': "Weekly specials, event announcements, and loyalty offers. Clean templates and an easy builder for marketing-light restaurant teams."},
            'seo-tools': {'tool': 'mangools', 'why': "Local keyword research for restaurant discovery searches. Simple enough for owners who are chefs first, marketers second."},
            'project-management': {'tool': 'trello', 'why': "Menu planning, event coordination, and opening checklists on simple kanban boards. Kitchen and floor staff learn it in minutes."},
            'help-desk': {'tool': 'freshdesk', 'why': "Free tier handles reservation inquiries, catering questions, and guest feedback. More structure than email, less overhead than Zendesk."},
            'ai-sdr': {'tool': 'lavender', 'why': "Email coaching for catering outreach and partnership emails. Helps restaurant operators communicate professionally."},
            'sales-engagement': {'tool': 'mailshake', 'why': "Simple email sequences for catering leads and event follow-ups. No complexity, just follow-up automation."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free recording for catering consultations and vendor negotiations. Captures details that prevent miscommunication."},
            'data-enrichment': {'tool': 'apollo', 'why': "Free tier finds corporate event planners and catering contacts. Restaurants doing B2B catering can prospect at no cost."},
        },
    },

    'manufacturing': {
        'name': 'Manufacturing & Wholesale',
        'tier': 3,
        'description': 'Order management, distributor relationships, and supply chain communication for manufacturers and wholesalers.',
        'intro': "Manufacturing and wholesale businesses manage complex distributor relationships and long sales cycles. Your CRM tracks accounts for years. Your PM tool coordinates production. Keep it simple and reliable.",
        'picks': {
            'crm': {'tool': 'pipedrive', 'why': "Visual pipeline for tracking wholesale accounts through long, multi-stage sales cycles. Deal values and close dates visible at a glance."},
            'email-marketing': {'tool': 'brevo', 'why': "Transactional email for order confirmations and shipping updates alongside marketing campaigns. Pay per email, not per contact."},
            'seo-tools': {'tool': 'se-ranking', 'why': "B2B keyword research for industrial product pages. Affordable monitoring of search visibility for product categories and part numbers."},
            'project-management': {'tool': 'smartsheet', 'why': "Spreadsheet-based project tracking for production schedules, quality checklists, and supply chain coordination. Manufacturing teams think in rows and columns."},
            'help-desk': {'tool': 'freshdesk', 'why': "Handles distributor support tickets, warranty claims, and technical inquiries. The ticketing system provides accountability for every issue."},
            'ai-sdr': {'tool': 'smartlead', 'why': "High-volume outbound for reaching distributors and wholesale buyers. Manufacturing sales cycles start with prospecting at scale."},
            'sales-engagement': {'tool': 'apollo', 'why': "Contact database plus engagement for reaching industrial buyers. One platform for finding and contacting distributors."},
            'conversation-intelligence': {'tool': 'fireflies', 'why': "Records and transcribes distributor calls. Manufacturing teams capture specifications and order details automatically."},
            'data-enrichment': {'tool': 'zoominfo', 'why': "Deep firmographic data for identifying manufacturing buyers, procurement managers, and supply chain decision-makers."},
        },
    },

    'fitness': {
        'name': 'Fitness & Gyms',
        'tier': 3,
        'description': 'Member communication, class scheduling support, and lead management for gyms, studios, and personal trainers.',
        'intro': "Fitness businesses run on member retention and local marketing. Your tools should keep members engaged, attract new leads through local search, and handle the day-to-day without a dedicated admin.",
        'picks': {
            'crm': {'tool': 'hubspot', 'why': "Free CRM for tracking leads from website forms, social media, and walk-ins. Automated follow-up sequences convert trial members into paying members."},
            'email-marketing': {'tool': 'mailerlite', 'why': "Class schedules, promotional offers, and member newsletters. Simple and affordable for gym owners who are trainers first, marketers second."},
            'seo-tools': {'tool': 'mangools', 'why': "Local keyword research for gym and fitness studio discovery. Tracks rankings for searches that drive foot traffic."},
            'project-management': {'tool': 'trello', 'why': "Class planning, equipment maintenance schedules, and staff task boards. Zero learning curve for fitness professionals."},
            'help-desk': {'tool': 'groove-helpdesk', 'why': "Simple member support for billing questions, class inquiries, and membership changes. The cheapest help desk that handles the basics."},
            'ai-sdr': {'tool': 'lavender', 'why': "Email coaching for membership outreach and corporate wellness proposals. Helps gym owners write professional business emails."},
            'sales-engagement': {'tool': 'mailshake', 'why': "Simple follow-up sequences for trial membership leads and corporate accounts. Easy for fitness professionals."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free recording for corporate wellness pitches and partnership calls. Captures commitments and action items."},
            'data-enrichment': {'tool': 'apollo', 'why': "Free tier finds HR directors and corporate wellness contacts. Gym owners prospecting corporate memberships get data at no cost."},
        },
    },

    'legal': {
        'name': 'Legal',
        'tier': 3,
        'description': 'Client intake, case management support, and communication tools for law firms and legal practices.',
        'intro': "Law firms manage long client relationships, track billable time, and handle sensitive communications. Your tools need to be reliable, organized, and simple enough that attorneys use them.",
        'picks': {
            'crm': {'tool': 'less-annoying-crm', 'why': "Simple contact management for client intake and referral tracking. Attorneys get a CRM that works without needing a CRM administrator."},
            'email-marketing': {'tool': 'convertkit', 'why': "Thought leadership newsletters and client update sequences. Legal professionals build authority by publishing. ConvertKit makes that workflow simple."},
            'seo-tools': {'tool': 'se-ranking', 'why': "Local SEO tracking for practice area keywords. Legal searches are hyperlocal. SE Ranking monitors visibility where it matters."},
            'project-management': {'tool': 'asana', 'why': "Case milestone tracking, deadline management, and team task coordination. Structured enough for legal workflows without requiring a project manager."},
            'help-desk': {'tool': 'help-scout', 'why': "Client communication that maintains professional standards. The personal, email-like experience aligns with how law firms communicate with clients."},
            'ai-sdr': {'tool': 'lavender', 'why': "Polishes business development emails for law firms. Legal professionals need precise, well-crafted outreach."},
            'sales-engagement': {'tool': 'mixmax', 'why': "Gmail-native sequences for law firms living in Google Workspace. Meeting scheduling and follow-ups without leaving the inbox."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free call documentation for client consultations and partner meetings. Creates searchable records of legal discussions."},
            'data-enrichment': {'tool': 'leadiq', 'why': "LinkedIn-to-CRM capture for identifying corporate counsel and in-house legal departments."},
        },
    },

    'accounting': {
        'name': 'Accounting & Bookkeeping',
        'tier': 3,
        'description': 'Client management, deadline tracking, and communication tools for accounting firms and bookkeeping services.',
        'intro': "Accounting firms operate on deadlines, client deliverables, and trust. Your tools need to track engagements, manage seasonal workload spikes, and maintain client communication year-round.",
        'picks': {
            'crm': {'tool': 'less-annoying-crm', 'why': "Simple client tracking for accounting firms. Tax season is stressful enough. Your CRM should be the easiest tool in your stack."},
            'email-marketing': {'tool': 'mailerlite', 'why': "Tax deadline reminders, financial tips, and client newsletters. Affordable and simple enough for bookkeepers who wear multiple hats."},
            'seo-tools': {'tool': 'mangools', 'why': "Keyword research for local accounting service searches. Most accounting clients find their accountant through search. Mangools helps you appear in those results."},
            'project-management': {'tool': 'asana', 'why': "Tax season workflows, monthly close checklists, and client engagement tracking. Templates for recurring accounting processes."},
            'help-desk': {'tool': 'groove-helpdesk', 'why': "Simple client support for billing questions and document requests. The cheapest way to get organized support without enterprise overhead."},
            'ai-sdr': {'tool': 'lavender', 'why': "Email coaching for client acquisition outreach. Helps accounting firms write polished business development emails."},
            'sales-engagement': {'tool': 'mailshake', 'why': "Simple sequences for tax season outreach and referral follow-ups. Accountants need automation without complexity."},
            'conversation-intelligence': {'tool': 'fathom', 'why': "Free call recording for client meetings. Captures scope discussions and advisory conversations."},
            'data-enrichment': {'tool': 'apollo', 'why': "Free tier finds CFOs and controllers at target companies. Accounting firms prospecting new clients get contacts at no cost."},
        },
    },
}


# =============================================================================
# HTML COMPONENT HELPERS
# =============================================================================

def verdict_color_style(score):
    """Return inline style with verdict color."""
    return f'color: {get_verdict_color(score)}'


def tool_card_html(slug, show_category=True, rank=0):
    """Generate a tool card component."""
    t = TOOLS[slug]
    cat = CATEGORIES.get(t['category'], {})

    pick_badge = ""
    pick_class = ""
    if t['sultans_pick']:
        pick_badge = f'<div class="sultans-pick-badge">{DIAMONDS_TRIPLE} Sultan\'s Pick</div>'
        pick_class = " sultans-pick"

    category_label = f'<span class="card-category">{cat.get("name", "")}</span>' if show_category else ""

    rank_html = ""
    if rank > 0:
        rank_html = f'<span class="card-rank">#{rank}</span>'

    return f'''<div class="tool-card{pick_class}">
    <div class="card-top">
        <div class="card-icon">{t["name"][0]}</div>
        <div class="card-info">
            <div class="card-name">{rank_html} {t["name"]}</div>
            {category_label}
            {pick_badge}
            <div class="card-score" style="{verdict_color_style(t["score"])}">
                {DIAMOND_SINGLE} {t["score"]}
            </div>
        </div>
    </div>
    <p class="card-description">{t["verdict_line"][:180]}{"..." if len(t["verdict_line"]) > 180 else ""}</p>
    <div class="card-footer">
        <span class="card-price {get_price_tier_class(t["pricing_tier"])}">{t["pricing_start"]}</span>
        <a href="/tools/{slug}/" class="card-cta">Read Review &rarr;</a>
    </div>
</div>'''


def winner_banner_html(winner_slug, reason):
    """Generate winner banner for comparison pages."""
    w = TOOLS[winner_slug]
    return f'''<div class="winner-banner">
    <div class="winner-icon">{LOGO_MARK_SMALL}</div>
    <div class="winner-text">
        <div class="winner-title">{w["name"]} wins this one</div>
        <div class="winner-reason">{reason}</div>
    </div>
    <div class="winner-score" style="{verdict_color_style(w["score"])}">{w["score"]}</div>
</div>'''


def faq_html_block(faqs):
    """Generate FAQ HTML + JSON-LD. faqs = [(question, answer), ...]"""
    items = ""
    for q, a in faqs:
        items += f'''<div class="faq-item">
    <h3 class="faq-q">{q}</h3>
    <p class="faq-a">{a}</p>
</div>\n'''
    schema = get_faq_schema(faqs)
    return f'''{schema}
<div class="faq-section">
<h2>Frequently Asked Questions</h2>
{items}
</div>'''


# =============================================================================
# PAGE GENERATORS
# =============================================================================

def build_homepage():
    """Generate the homepage."""
    # Sultan's picks from each category
    picks_html = ""
    for cat_slug, cat in CATEGORIES.items():
        for tool_slug in cat['tools']:
            t = TOOLS.get(tool_slug)
            if t and t['sultans_pick']:
                picks_html += tool_card_html(tool_slug, show_category=True)
                break

    # Category grid
    cat_cards = ""
    for slug, cat in CATEGORIES.items():
        count = len(cat['tools'])
        cat_cards += f'''<a href="/best/{slug}/" class="category-card">
    <h3>{cat["name"]}</h3>
    <p>{cat["description"][:120]}{"..." if len(cat["description"]) > 120 else ""}</p>
    <span class="tool-count">{count} tools reviewed</span>
</a>\n'''

    # Popular comparisons
    comp_html = ""
    for c in COMPARISONS[:8]:
        ta = TOOLS[c["tools"][0]]
        tb = TOOLS[c["tools"][1]]
        comp_html += f'''<a href="/{c["slug"]}/" class="comparison-link">
    <span class="vs-badge">VS</span>
    <span class="comp-names">{ta["name"]} vs {tb["name"]}</span>
</a>\n'''

    body = f'''<div class="container">
    <div class="hero">
        <h1>SaaS reviews that actually pick a winner.</h1>
        <p class="hero-subtitle">Scores, winners, and stack guides for founders who buy their own tools.</p>
        <a href="/best/crm/" class="hero-cta">Browse Reviews &rarr;</a>
        <div class="hero-stats">
            <div class="hero-stat"><div class="hero-stat-value">{len(TOOLS)}</div><div class="hero-stat-label">Tools Reviewed</div></div>
            <div class="hero-stat"><div class="hero-stat-value">{len(CATEGORIES)}</div><div class="hero-stat-label">Categories</div></div>
            <div class="hero-stat"><div class="hero-stat-value">{len(COMPARISONS)}</div><div class="hero-stat-label">Comparisons</div></div>
        </div>
    </div>

    <div class="section">
        <div class="section-header">
            <h2>Sultan's Picks</h2>
            <p>The top tool in each category, chosen by The Sultan.</p>
        </div>
        <div class="picks-grid">{picks_html}</div>
    </div>

    <div class="section">
        <div class="section-header">
            <h2>Browse by Category</h2>
            <p>{len(CATEGORIES)} categories of SaaS tools reviewed and ranked for {CURRENT_YEAR}.</p>
        </div>
        <div class="category-grid">{cat_cards}</div>
    </div>

    <div class="section">
        <div class="section-header">
            <h2>Popular Comparisons</h2>
            <p>Side-by-side breakdowns of the tools founders ask about most.</p>
        </div>
        <div class="comparison-grid">{comp_html}</div>
    </div>
</div>'''

    page = get_page_wrapper(
        SITE_NAME,
        f"SaaS reviews that pick winners. Scores, comparisons, and stack guides for founders who buy their own tools. Updated {CURRENT_YEAR}.",
        "/",
        body
    )
    write_page("index.html", page)


def _render_deep_sections(t, content, cat):
    """Render expanded review sections from deep content data.
    Returns HTML string for all deep sections, or empty string if no content.
    """
    sections = []

    # Overview
    if content.get('overview'):
        paras = "\n".join(f"<p>{p}</p>" for p in content['overview'])
        sections.append(f'''<div class="review-section">
    <h2>{t["name"]}: What You Need to Know</h2>
    <div class="review-body">{paras}</div>
</div>''')

    # Expanded Pros
    if content.get('expanded_pros'):
        items = ""
        for pro in content['expanded_pros']:
            items += f'''<div class="expanded-item expanded-pro">
    <h3>{pro["title"]}</h3>
    <p>{pro["detail"]}</p>
</div>\n'''
        sections.append(f'''<div class="review-section">
    <h2>What The Sultan Likes</h2>
    <div class="expanded-grid">{items}</div>
</div>''')

    # Expanded Cons
    if content.get('expanded_cons'):
        items = ""
        for con in content['expanded_cons']:
            items += f'''<div class="expanded-item expanded-con">
    <h3>{con["title"]}</h3>
    <p>{con["detail"]}</p>
</div>\n'''
        sections.append(f'''<div class="review-section">
    <h2>Where It Falls Short</h2>
    <div class="expanded-grid">{items}</div>
</div>''')

    # Pricing Detail
    if content.get('pricing_detail'):
        detail = content['pricing_detail']
        if isinstance(detail, list):
            detail = "\n".join(f"<p>{p}</p>" for p in detail)
        else:
            detail = f"<p>{detail}</p>"
        sections.append(f'''<div class="review-section">
    <h2>What You'll Actually Pay</h2>
    <div class="review-body pricing-detail">{detail}</div>
</div>''')

    # Who Should Buy / Skip
    buy_skip = ""
    if content.get('who_should_buy'):
        items = ""
        for entry in content['who_should_buy']:
            items += f'''<div class="audience-item audience-buy">
    <h4>{entry["audience"]}</h4>
    <p>{entry["reason"]}</p>
</div>\n'''
        buy_skip += f'<div class="audience-col"><h3>Buy {t["name"]} If&hellip;</h3>{items}</div>\n'
    if content.get('who_should_skip'):
        items = ""
        for entry in content['who_should_skip']:
            items += f'''<div class="audience-item audience-skip">
    <h4>{entry["audience"]}</h4>
    <p>{entry["reason"]}</p>
</div>\n'''
        buy_skip += f'<div class="audience-col"><h3>Skip {t["name"]} If&hellip;</h3>{items}</div>\n'
    if buy_skip:
        sections.append(f'''<div class="review-section">
    <h2>Should You Buy {t["name"]}?</h2>
    <div class="audience-grid">{buy_skip}</div>
</div>''')

    # Stage Guidance
    if content.get('stage_guidance'):
        sg = content['stage_guidance']
        stage_labels = {
            'solo': ('Solo Founder', 'Running lean, doing everything yourself'),
            'small_team': ('Small Team (2-10)', 'Growing past founder-led sales'),
            'mid_market': ('Mid-Market (11-50)', 'Scaling with dedicated teams'),
            'enterprise': ('Enterprise (50+)', 'Complex org, multiple divisions'),
        }
        cards = ""
        for key in ['solo', 'small_team', 'mid_market', 'enterprise']:
            if key in sg:
                label, subtitle = stage_labels[key]
                cards += f'''<div class="stage-card">
    <div class="stage-card-header">
        <h4>{label}</h4>
        <span class="stage-subtitle">{subtitle}</span>
    </div>
    <p>{sg[key]}</p>
</div>\n'''
        if cards:
            sections.append(f'''<div class="review-section">
    <h2>Stage-by-Stage Guidance</h2>
    <div class="stage-grid">{cards}</div>
</div>''')

    # Alternatives Detail
    if content.get('alternatives_detail'):
        items = ""
        for alt in content['alternatives_detail']:
            alt_tool = alt.get('tool', '')
            alt_slug = alt_tool.lower().replace(' ', '-').replace('.', '-')
            link = f' <a href="/tools/{alt_slug}/">Read review &rarr;</a>' if alt_slug in TOOLS else ''
            items += f'''<div class="alt-card">
    <h4>{alt_tool}</h4>
    <p>{alt["reason"]}{link}</p>
</div>\n'''
        sections.append(f'''<div class="review-section">
    <h2>Alternatives Worth Considering</h2>
    <div class="alt-grid">{items}</div>
</div>''')

    # Sultan's Bottom Line
    if content.get('verdict_long'):
        vl = content['verdict_long']
        if isinstance(vl, list):
            vl = "\n".join(f"<p>{p}</p>" for p in vl)
        else:
            vl = f"<p>{vl}</p>"
        sections.append(f'''<div class="review-section bottom-line">
    <h2>The Sultan's Bottom Line</h2>
    <div class="bottom-line-content">{vl}</div>
</div>''')

    # FAQ
    if content.get('faqs'):
        faq_items = ""
        for faq in content['faqs']:
            faq_items += f'''<div class="faq-item">
    <h3>{faq["question"]}</h3>
    <p>{faq["answer"]}</p>
</div>\n'''
        sections.append(f'''<div class="review-section">
    <h2>Frequently Asked Questions</h2>
    <div class="faq-list">{faq_items}</div>
</div>''')

    return "\n\n".join(sections)


def build_tool_pages():
    """Generate individual tool review pages."""
    for slug, t in TOOLS.items():
        cat = CATEGORIES.get(t['category'], {})
        content = get_tool_content(slug)

        # Subscores breakdown
        subscores_html = ""
        if t['subscores']:
            items = ""
            for label, val in t['subscores'].items():
                display_label = label.replace("_", " ").title()
                items += f'<div class="breakdown-item"><span class="bl">{display_label}</span><span class="bv" style="{verdict_color_style(val)}">{val}</span></div>\n'
            subscores_html = f'<div class="verdict-breakdown">{items}</div>'

        # Verdict card
        verdict_html = f'''<div class="verdict-card">
    <div class="verdict-header">
        {LOGO_MARK_SMALL}
        <span class="verdict-header-text">The Sultan's Verdict</span>
    </div>
    <div class="verdict-main">
        <span class="verdict-score-large" style="{verdict_color_style(t["score"])}">{t["score"]}</span>
        <div class="verdict-summary">
            <div class="verdict-summary-word">{t["verdict_word"]}</div>
            <p>{t["verdict_line"]}</p>
        </div>
    </div>
    {subscores_html}
</div>'''

        # Pros/Cons — thin format (always rendered as quick glance)
        pros_items = "\n".join(f"<li>{p}</li>" for p in t['pros'])
        cons_items = "\n".join(f"<li>{c}</li>" for c in t['cons'])

        # Pricing table
        pricing_html = ""
        if t['pricing_tiers']:
            rows = ""
            for tier in t['pricing_tiers']:
                name, price = tier[0], tier[1]
                features = tier[2] if len(tier) > 2 else ""
                rows += f'<tr><td class="plan-name">{name}</td><td class="plan-price">{price}</td></tr>\n'
            pricing_html = f'''<div class="pricing-section">
    <h2>Pricing</h2>
    <table class="pricing-table">
        <thead><tr><th>Plan</th><th>Price</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
</div>'''

        # Features list
        features_html = ""
        if t['features']:
            feat_items = "\n".join(f"<li>{f}</li>" for f in t['features'])
            features_html = f'''<div class="features-section">
    <h2>Key Features</h2>
    <ul class="features-list">{feat_items}</ul>
</div>'''

        # Breadcrumbs
        bc = breadcrumb_html([("Home", "/"), (cat.get("name", ""), f'/best/{t["category"]}/'), (t['name'], "")])
        bc_schema = get_breadcrumb_schema([("Home", "/"), (cat.get("name", ""), f'/best/{t["category"]}/'), (t['name'], f'/tools/{slug}/')])
        product_schema = get_product_schema(t['name'], t['verdict_line'], t['url'], t['score'])

        # Sultan's Pick badge
        pick_html = ""
        if t['sultans_pick']:
            pick_html = f'<div class="sultans-pick-badge">{DIAMONDS_TRIPLE} Sultan\'s Pick in {cat.get("name", "")}</div>'

        # CTA bar
        cta_html = f'''<div class="review-cta-bar">
    <a href="{t["url"]}" class="cta-btn" target="_blank" rel="noopener">Visit {t["name"]} &rarr;</a>
    <span class="cta-info">Starting at {t["pricing_start"]}</span>
</div>'''

        # Deep content sections (conditionally rendered)
        deep_html = ""
        faq_schema = ""
        if content:
            deep_html = _render_deep_sections(t, content, cat)
            # FAQ schema for rich snippets
            if content.get('faqs'):
                faq_schema = get_faq_schema(content['faqs'])

        # Choose pros/cons format: if deep content has expanded pros, use label "At a Glance"
        pros_heading = "At a Glance" if content and content.get('expanded_pros') else "What The Sultan Likes"
        cons_heading = "" if content and content.get('expanded_cons') else "Where It Falls Short"
        if content and (content.get('expanded_pros') or content.get('expanded_cons')):
            # Combined quick-glance box instead of separate pros/cons
            pros_cons_html = f'''<div class="pros-cons">
        <div class="pros-list"><h3>Pros</h3><ul>{pros_items}</ul></div>
        <div class="cons-list"><h3>Cons</h3><ul>{cons_items}</ul></div>
    </div>'''
        else:
            pros_cons_html = f'''<div class="pros-cons">
        <div class="pros-list"><h3>What The Sultan Likes</h3><ul>{pros_items}</ul></div>
        <div class="cons-list"><h3>Where It Falls Short</h3><ul>{cons_items}</ul></div>
    </div>'''

        body = f'''<div class="review-page{"  has-deep-content" if content else ""}">
    {bc}
    <div class="review-header">
        <h1>{t["name"]} Review ({CURRENT_YEAR})</h1>
        <div class="review-meta">
            <span class="review-category">{cat.get("name", "")}</span>
            <span class="{get_price_tier_class(t["pricing_tier"])}">{t["pricing_start"]}</span>
            {pick_html}
        </div>
    </div>

    <p class="review-best-for"><strong>Best for:</strong> {t["best_for"]}</p>

    <div class="review-verdict">{verdict_html}</div>

    {cta_html}

    {pros_cons_html}

    {deep_html}

    {features_html}
    {pricing_html}
</div>'''

        extra_head = bc_schema + product_schema + faq_schema
        page = get_page_wrapper(
            f"{t['name']} Review ({CURRENT_YEAR}) - Score: {t['score']}/10",
            f"The Sultan's verdict on {t['name']}: {t['verdict_word']} ({t['score']}/10). {t['verdict_line'][:120]}",
            f"/tools/{slug}/",
            body,
            extra_head=extra_head
        )
        write_page(f"tools/{slug}/index.html", page)


def build_category_pages():
    """Generate category guide pages."""
    for slug, cat in CATEGORIES.items():
        # Tool cards
        tool_cards = ""
        for i, tool_slug in enumerate(cat['tools'], 1):
            if tool_slug in TOOLS:
                tool_cards += tool_card_html(tool_slug, show_category=False, rank=i)

        # Related comparisons
        related_comps = [c for c in COMPARISONS if c['tools'][0] in cat['tools'] or c['tools'][1] in cat['tools']]
        comp_html = ""
        if related_comps:
            comp_links = ""
            for c in related_comps[:6]:
                ta = TOOLS[c["tools"][0]]
                tb = TOOLS[c["tools"][1]]
                comp_links += f'''<a href="/{c["slug"]}/" class="comparison-link">
    <span class="vs-badge">VS</span>
    <span class="comp-names">{ta["name"]} vs {tb["name"]}</span>
</a>\n'''
            comp_html = f'''<div class="section">
    <div class="section-header"><h2>Comparisons</h2></div>
    <div class="comparison-grid">{comp_links}</div>
</div>'''

        # Breadcrumbs
        bc = breadcrumb_html([("Home", "/"), (cat['name'], "")])
        bc_schema = get_breadcrumb_schema([("Home", "/"), (cat['name'], f'/best/{slug}/')])

        body = f'''<div class="category-page">
    {bc}
    <div class="category-header">
        <h1>Best {cat["name"]} for SMBs ({CURRENT_YEAR})</h1>
        <p class="category-desc">{cat["description"]}</p>
    </div>
    <div class="tool-grid">{tool_cards}</div>
    {comp_html}
</div>'''

        extra_head = bc_schema
        page = get_page_wrapper(
            f"Best {cat['name']} for SMBs ({CURRENT_YEAR})",
            f"Compare the best {cat['name'].lower()} for small businesses. {len(cat['tools'])} tools scored, ranked, and reviewed by The Sultan.",
            f"/best/{slug}/",
            body,
            active_page="/best/",
            extra_head=extra_head
        )
        write_page(f"best/{slug}/index.html", page)


def build_comparison_pages():
    """Generate comparison pages."""
    for c in COMPARISONS:
        ta = TOOLS[c["tools"][0]]
        tb = TOOLS[c["tools"][1]]
        winner = TOOLS[c["winner"]]
        loser = ta if c["winner"] == c["tools"][1] else tb

        # Comparison table rows
        features_set = set(ta.get('features', []) + tb.get('features', []))
        table_rows = ""
        for feat in sorted(features_set):
            a_has = "Yes" if feat in ta.get('features', []) else "No"
            b_has = "Yes" if feat in tb.get('features', []) else "No"
            a_class = "verdict-excellent" if a_has == "Yes" else "text-tertiary"
            b_class = "verdict-excellent" if b_has == "Yes" else "text-tertiary"
            winner_col_a = ' class="winner-col"' if c["winner"] == c["tools"][0] else ""
            winner_col_b = ' class="winner-col"' if c["winner"] == c["tools"][1] else ""
            table_rows += f'<tr><td>{feat}</td><td{winner_col_a}><span class="{a_class}">{a_has}</span></td><td{winner_col_b}><span class="{b_class}">{b_has}</span></td></tr>\n'

        # Pricing row
        winner_col_a = ' class="winner-col"' if c["winner"] == c["tools"][0] else ""
        winner_col_b = ' class="winner-col"' if c["winner"] == c["tools"][1] else ""
        table_rows += f'<tr><td><strong>Starting Price</strong></td><td{winner_col_a}><span class="plan-price">{ta["pricing_start"]}</span></td><td{winner_col_b}><span class="plan-price">{tb["pricing_start"]}</span></td></tr>\n'
        table_rows += f'<tr><td><strong>Sultan\'s Score</strong></td><td{winner_col_a}><span style="{verdict_color_style(ta["score"])}" class="font-mono"><strong>{ta["score"]}</strong></span></td><td{winner_col_b}><span style="{verdict_color_style(tb["score"])}" class="font-mono"><strong>{tb["score"]}</strong></span></td></tr>\n'

        winner_tag_a = ' <span class="winner-tag">Winner</span>' if c["winner"] == c["tools"][0] else ""
        winner_tag_b = ' <span class="winner-tag">Winner</span>' if c["winner"] == c["tools"][1] else ""
        winner_th_a = ' class="winner-col"' if c["winner"] == c["tools"][0] else ""
        winner_th_b = ' class="winner-col"' if c["winner"] == c["tools"][1] else ""

        # Breadcrumbs
        bc = breadcrumb_html([("Home", "/"), (f"{ta['name']} vs {tb['name']}", "")])
        bc_schema = get_breadcrumb_schema([("Home", "/"), (f"{ta['name']} vs {tb['name']}", f"/{c['slug']}/")])

        body = f'''<div class="comparison-page">
    {bc}
    <div class="comparison-header">
        <h1>{ta["name"]} vs {tb["name"]} ({CURRENT_YEAR})</h1>
        <p>{c["summary"]}</p>
    </div>

    {winner_banner_html(c["winner"], c["why"])}

    <div class="comparison-scores">
        <div class="comparison-score-card {"is-winner" if c["winner"] == c["tools"][0] else ""}">
            <h3>{ta["name"]}</h3>
            <div class="score-value" style="{verdict_color_style(ta["score"])}">{ta["score"]}</div>
        </div>
        <div class="comparison-score-card {"is-winner" if c["winner"] == c["tools"][1] else ""}">
            <h3>{tb["name"]}</h3>
            <div class="score-value" style="{verdict_color_style(tb["score"])}">{tb["score"]}</div>
        </div>
    </div>

    <table class="comparison-table">
        <thead>
            <tr>
                <th>Feature</th>
                <th{winner_th_a}>{ta["name"]}{winner_tag_a}</th>
                <th{winner_th_b}>{tb["name"]}{winner_tag_b}</th>
            </tr>
        </thead>
        <tbody>{table_rows}</tbody>
    </table>

    <div class="verdict-section">
        <h2>The Sultan's Verdict</h2>
        <p>{c["why"]}</p>
    </div>

    <div class="comparison-grid" style="margin-top: var(--space-8)">
        <a href="/tools/{c["tools"][0]}/" class="comparison-link"><span class="comp-names">Read full {ta["name"]} review &rarr;</span></a>
        <a href="/tools/{c["tools"][1]}/" class="comparison-link"><span class="comp-names">Read full {tb["name"]} review &rarr;</span></a>
    </div>
</div>'''

        extra_head = bc_schema
        page = get_page_wrapper(
            f"{ta['name']} vs {tb['name']} ({CURRENT_YEAR})",
            f"{ta['name']} vs {tb['name']}: The Sultan picks {winner['name']}. Side-by-side comparison of features, pricing, and scores.",
            f"/{c['slug']}/",
            body,
            extra_head=extra_head
        )
        write_page(f"{c['slug']}/index.html", page)


def build_alternatives_pages():
    """Generate alternatives pages."""
    for a in ALTERNATIVES:
        original = TOOLS[a["tool"]]

        # Alt list
        alt_items = ""
        for i, alt_slug in enumerate(a["alts"], 1):
            alt = TOOLS[alt_slug]
            alt_items += f'''<a href="/tools/{alt_slug}/" class="alt-item">
    <div class="alt-rank {"rank-1" if i == 1 else ""}">{i}</div>
    <div class="alt-info">
        <h3>{alt["name"]}</h3>
        <p>{alt["verdict_line"][:140]}{"..." if len(alt["verdict_line"]) > 140 else ""}</p>
        <span class="{get_price_tier_class(alt["pricing_tier"])}" style="margin-top: 8px; display: inline-block;">{alt["pricing_start"]}</span>
    </div>
    <div class="alt-score" style="{verdict_color_style(alt["score"])}">{alt["score"]}</div>
</a>\n'''

        # Breadcrumbs
        bc = breadcrumb_html([("Home", "/"), (f"{original['name']} Alternatives", "")])
        bc_schema = get_breadcrumb_schema([("Home", "/"), (f"{original['name']} Alternatives", f"/{a['slug']}/")])

        body = f'''<div class="alternatives-page">
    {bc}
    <div class="alternatives-header">
        <h1>Best {original["name"]} Alternatives ({CURRENT_YEAR})</h1>
    </div>
    <div class="alt-reason">{a["reason"]}</div>
    <div class="alt-list">{alt_items}</div>
</div>'''

        extra_head = bc_schema
        page = get_page_wrapper(
            f"Best {original['name']} Alternatives ({CURRENT_YEAR})",
            f"Looking for {original['name']} alternatives? The Sultan ranks the {len(a['alts'])} best options with scores, pricing, and honest verdicts.",
            f"/{a['slug']}/",
            body,
            extra_head=extra_head
        )
        write_page(f"{a['slug']}/index.html", page)


def build_pricing_pages():
    """Generate pricing breakdown pages for each tool."""
    for slug, t in TOOLS.items():
        if not t['pricing_tiers']:
            continue

        cat = CATEGORIES.get(t['category'], {})

        # Pricing table
        rows = ""
        for tier in t['pricing_tiers']:
            name, price = tier[0], tier[1]
            rows += f'<tr><td class="plan-name">{name}</td><td class="plan-price">{price}</td></tr>\n'

        # Pricing verdict
        tier_word = t['pricing_tier'].title()
        if t['pricing_tier'] == 'free':
            price_take = f"{t['name']} offers a free tier that handles the basics. Worth starting here before spending money elsewhere."
        elif t['pricing_tier'] == 'budget':
            price_take = f"{t['name']} is competitively priced for its category. Good value for small teams watching their spend."
        elif t['pricing_tier'] == 'mid':
            price_take = f"{t['name']} sits at the mid-range price point. Fair pricing if you use the features, but make sure you need this tier before committing."
        elif t['pricing_tier'] == 'premium':
            price_take = f"{t['name']} commands premium pricing. The feature set justifies it for teams who use it fully, but there are cheaper alternatives that cover 80% of the functionality."
        else:
            price_take = f"{t['name']} targets enterprise budgets. Unless your team has outgrown mid-market alternatives, start with something cheaper."

        # Breadcrumbs
        bc = breadcrumb_html([("Home", "/"), (t['name'], f"/tools/{slug}/"), ("Pricing", "")])
        bc_schema = get_breadcrumb_schema([("Home", "/"), (t['name'], f"/tools/{slug}/"), ("Pricing", f"/{slug}-pricing/")])

        body = f'''<div class="pricing-page">
    {bc}
    <div class="pricing-page-header">
        <h1>{t["name"]} Pricing ({CURRENT_YEAR})</h1>
        <div class="review-meta">
            <span class="{get_price_tier_class(t["pricing_tier"])}">Starting at {t["pricing_start"]}</span>
        </div>
    </div>

    <table class="pricing-table">
        <thead><tr><th>Plan</th><th>Price</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>

    <div class="pricing-verdict">
        <h3>The Sultan's Take on {t["name"]} Pricing</h3>
        <p>{price_take}</p>
    </div>

    <div class="review-cta-bar">
        <a href="/tools/{slug}/" class="cta-btn">Read Full Review &rarr;</a>
        <a href="{t["url"]}" class="cta-btn" target="_blank" rel="noopener">Visit {t["name"]} &rarr;</a>
    </div>
</div>'''

        extra_head = bc_schema
        page = get_page_wrapper(
            f"{t['name']} Pricing Breakdown ({CURRENT_YEAR})",
            f"{t['name']} pricing starts at {t['pricing_start']}. Full tier-by-tier breakdown with The Sultan's take on value.",
            f"/{slug}-pricing/",
            body,
            extra_head=extra_head
        )
        write_page(f"{slug}-pricing/index.html", page)


def build_stack_pages():
    """Generate stack guide pages."""
    for stack in STACKS:
        # Tool list
        items_html = ""
        for st in stack['tools']:
            t = TOOLS.get(st['slug'], {})
            score_html = ""
            if t:
                score_html = f'<div class="stack-item-score" style="{verdict_color_style(t["score"])}">{t["score"]}/10</div>'

            items_html += f'''<div class="stack-item">
    <div class="stack-item-info">
        <h3><a href="/tools/{st["slug"]}/">{t.get("name", st["slug"])}</a></h3>
        <div class="stack-use">{st["use"]}</div>
        <div class="stack-plan">Plan: {st["plan"]}</div>
    </div>
    <div>
        <div class="stack-item-price">{st["cost"]}</div>
        {score_html}
    </div>
</div>\n'''

        # Breadcrumbs
        bc = breadcrumb_html([("Home", "/"), ("Stack Guides", "/stacks/"), (stack['name'], "")])
        bc_schema = get_breadcrumb_schema([("Home", "/"), ("Stack Guides", "/stacks/"), (stack['name'], f'/stacks/{stack["slug"]}/')])

        body = f'''<div class="stack-page">
    {bc}
    <div class="stack-header">
        <h1>{stack["name"]}</h1>
        <p class="category-desc">{stack["description"]}</p>
    </div>
    <div class="stack-total">
        <span class="stack-total-label">Total Monthly Cost</span>
        <span class="stack-total-value">{stack["total_cost"]}</span>
    </div>
    <div class="stack-list">{items_html}</div>
</div>'''

        extra_head = bc_schema
        page = get_page_wrapper(
            f'{stack["name"]} - SaaS Stack Guide ({CURRENT_YEAR})',
            f'{stack["name"]}: {stack["description"]} Total cost: {stack["total_cost"]}.',
            f'/stacks/{stack["slug"]}/',
            body,
            active_page="/stacks/",
            extra_head=extra_head
        )
        write_page(f'stacks/{stack["slug"]}/index.html', page)


def build_stacks_index():
    """Generate /stacks/ index page."""
    cards = ""
    for stack in STACKS:
        cards += f'''<a href="/stacks/{stack["slug"]}/" class="stack-card">
    <h3>{stack["name"]}</h3>
    <p>{stack["description"][:140]}{"..." if len(stack["description"]) > 140 else ""}</p>
    <span class="stack-card-cost">{stack["total_cost"]}</span>
</a>\n'''

    body = f'''<div class="container">
    <div class="category-header">
        <h1>SaaS Stack Guides ({CURRENT_YEAR})</h1>
        <p class="category-desc">Curated tool bundles by role and budget. Each stack includes specific plans and a total monthly cost.</p>
    </div>
    <div class="stacks-grid">{cards}</div>
</div>'''

    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Stack Guides", "/stacks/")])

    page = get_page_wrapper(
        f"SaaS Stack Guides ({CURRENT_YEAR})",
        f"Curated SaaS tool stacks by role and budget. From $0/mo founder stacks to $300/mo agency stacks. {len(STACKS)} guides.",
        "/stacks/",
        body,
        active_page="/stacks/",
        extra_head=bc_schema
    )
    write_page("stacks/index.html", page)


def build_about_page():
    """Generate the about page."""
    body = f'''<div class="about-page">
    <h1>About SultanOfSaaS</h1>

    <p>Every SaaS review site tells you the same thing: "it depends." Helpful? No. That is why SultanOfSaaS exists.</p>

    <p>The Sultan reviews SaaS tools the way a trusted advisor would: with opinions, scores, and clear recommendations. Every tool gets a score from 1 to 10. Every comparison declares a winner. Every category has a top pick.</p>

    <h2>Who is The Sultan?</h2>

    <p>The Sultan is an anonymous reviewer who has spent years helping SMBs and founders choose the right tools. No sponsor influence. No pay-for-placement. When The Sultan picks a winner, it is because the tool earned it.</p>

    <h2>How Tools Are Scored</h2>

    <p>Every tool is evaluated across four dimensions:</p>

    <ul style="color: var(--text-secondary); line-height: 2; padding-left: var(--space-6); margin-bottom: var(--space-4);">
        <li><strong>Ease of Use</strong> — How fast can a new user get productive?</li>
        <li><strong>Value</strong> — Is the pricing fair for what you get?</li>
        <li><strong>Features</strong> — Does it have the capabilities you need?</li>
        <li><strong>Support</strong> — Can you get help when something breaks?</li>
    </ul>

    <p>Scores are weighted toward what matters most for small businesses: value and ease of use. A tool that scores 9.5 on features but 5.0 on ease of use will lose to a simpler tool that delivers 80% of the functionality with none of the friction.</p>

    <h2>Affiliate Disclosure</h2>

    <p>Some links on this site are affiliate links. If you sign up through them, The Sultan earns a commission at no extra cost to you. This never influences reviews or scores. Tools that pay affiliate commissions do not get higher ratings.</p>
</div>'''

    bc_schema = get_breadcrumb_schema([("Home", "/"), ("About", "/about/")])

    page = get_page_wrapper(
        "About SultanOfSaaS",
        "The Sultan reviews SaaS tools with opinions, scores, and clear recommendations. No pay-for-placement. Every comparison declares a winner.",
        "/about/",
        body,
        active_page="/about/",
        extra_head=bc_schema
    )
    write_page("about/index.html", page)


def build_niche_pages():
    """Generate niche category pages at /best/{category}/{niche}/."""
    count = 0
    for niche_slug, niche in NICHES.items():
        for cat_slug in niche['applies_to']:
            cat = CATEGORIES[cat_slug]
            rankings = niche['rankings'].get(cat_slug, [])
            if not rankings:
                continue

            winner_slug = rankings[0]
            winner = TOOLS.get(winner_slug, {})
            why = niche['why_winners'].get(cat_slug, '')

            # Title and description
            title = niche['title_pattern'].format(category=cat['name'], year=CURRENT_YEAR)
            meta_desc = niche['meta_desc'].format(category=cat['name'], category_lower=cat['name'].lower(), year=CURRENT_YEAR)
            intro_text = niche['intro'].format(category=cat['name'], category_lower=cat['name'].lower())

            # Ranked tool cards
            tool_cards = ""
            for i, tool_slug in enumerate(rankings, 1):
                if tool_slug in TOOLS:
                    tool_cards += tool_card_html(tool_slug, show_category=False, rank=i)

            # Winner callout
            winner_callout = ""
            if winner and why:
                winner_callout = f'''<div class="niche-winner-callout">
    <h3>{DIAMONDS_TRIPLE} The Sultan's Pick for {niche["name"]}: {winner.get("name", "")}</h3>
    <p>{why}</p>
</div>'''

            # Niche nav — links to other niches for this category
            niche_nav = ""
            other_niches = []
            for ns, n in NICHES.items():
                if cat_slug in n['applies_to']:
                    active = ' active' if ns == niche_slug else ''
                    other_niches.append(f'<a href="/best/{cat_slug}/{ns}/" class="niche-nav-link{active}">{n["name"]}</a>')
            if len(other_niches) > 1:
                niche_nav = f'<div class="niche-nav">{"".join(other_niches)}</div>'

            # Breadcrumbs
            bc = breadcrumb_html([("Home", "/"), (cat['name'], f'/best/{cat_slug}/'), (niche['name'], "")])
            bc_schema = get_breadcrumb_schema([("Home", "/"), (cat['name'], f'/best/{cat_slug}/'), (niche['name'], f'/best/{cat_slug}/{niche_slug}/')])

            body = f'''<div class="category-page">
    {bc}
    <div class="category-header">
        <h1>{title}</h1>
        <p class="category-desc">{cat["description"]}</p>
    </div>
    {niche_nav}
    <div class="niche-intro">{intro_text}</div>
    {winner_callout}
    <div class="tool-grid">{tool_cards}</div>
    <div class="section" style="margin-top: var(--space-8)">
        <a href="/best/{cat_slug}/" class="comparison-link">
            <span class="comp-names">See all {cat["name"]} tools &rarr;</span>
        </a>
    </div>
</div>'''

            extra_head = bc_schema
            page = get_page_wrapper(
                title,
                meta_desc,
                f'/best/{cat_slug}/{niche_slug}/',
                body,
                active_page="/best/",
                extra_head=extra_head
            )
            write_page(f'best/{cat_slug}/{niche_slug}/index.html', page)
            count += 1
    return count


def build_industry_pages():
    """Generate industry pages at /for/{industry}/."""
    for slug, ind in INDUSTRIES.items():
        title = f"Best SaaS Tools for {ind['name']} ({CURRENT_YEAR})"
        meta_desc = f"The Sultan's recommended SaaS stack for {ind['name'].lower()}. {ind['description']}"

        # Picks grid
        picks_html = ""
        for cat_slug, pick in ind['picks'].items():
            cat = CATEGORIES.get(cat_slug, {})
            t = TOOLS.get(pick['tool'], {})
            if not t:
                continue
            score_color = verdict_color_style(t['score'])
            picks_html += f'''<a href="/tools/{pick["tool"]}/" class="industry-pick-card">
    <span class="industry-pick-category">{cat.get("name", "")}</span>
    <div class="industry-pick-info">
        <h3>{t["name"]}</h3>
        <p>{pick["why"]}</p>
        <span class="{get_price_tier_class(t["pricing_tier"])}" style="margin-top: 8px; display: inline-block;">{t["pricing_start"]}</span>
    </div>
    <div class="industry-pick-score" style="{score_color}">{t["score"]}</div>
</a>\n'''

        # Category links
        cat_links = ""
        for cat_slug in ind['picks']:
            cat = CATEGORIES.get(cat_slug, {})
            cat_links += f'<a href="/best/{cat_slug}/" class="comparison-link"><span class="comp-names">{cat.get("name", "")} &rarr;</span></a>\n'

        # Breadcrumbs
        bc = breadcrumb_html([("Home", "/"), ("Industries", "/for/"), (ind['name'], "")])
        bc_schema = get_breadcrumb_schema([("Home", "/"), ("Industries", "/for/"), (ind['name'], f'/for/{slug}/')])

        body = f'''<div class="industry-page">
    {bc}
    <div class="industry-header">
        <h1>Best SaaS Tools for {ind["name"]} ({CURRENT_YEAR})</h1>
        <p class="industry-intro">{ind["intro"]}</p>
    </div>
    <div class="section-header"><h2>The Sultan's Picks for {ind["name"]}</h2></div>
    <div class="industry-picks-grid">{picks_html}</div>
    <div class="section" style="margin-top: var(--space-8)">
        <div class="section-header"><h2>Explore by Category</h2></div>
        <div class="comparison-grid">{cat_links}</div>
    </div>
</div>'''

        extra_head = bc_schema
        page = get_page_wrapper(
            title,
            meta_desc,
            f'/for/{slug}/',
            body,
            extra_head=extra_head
        )
        write_page(f'for/{slug}/index.html', page)


def build_industries_index():
    """Generate /for/ index page listing all industries."""
    # Group by tier
    tier_groups = {1: [], 2: [], 3: []}
    for slug, ind in INDUSTRIES.items():
        tier_groups[ind['tier']].append((slug, ind))

    cards = ""
    tier_labels = {1: "Most Popular Industries", 2: "Growing Industries", 3: "Specialized Industries"}
    for tier in [1, 2, 3]:
        if tier_groups[tier]:
            cards += f'<h3 class="section-subhead" style="margin: var(--space-8) 0 var(--space-4); color: var(--text-tertiary); font-size: var(--text-sm); text-transform: uppercase; letter-spacing: 0.06em;">{tier_labels[tier]}</h3>\n'
            cards += '<div class="category-grid">\n'
            for slug, ind in tier_groups[tier]:
                pick_count = len(ind['picks'])
                cards += f'''<a href="/for/{slug}/" class="category-card">
    <h3>{ind["name"]}</h3>
    <p>{ind["description"][:120]}{"..." if len(ind["description"]) > 120 else ""}</p>
    <span class="tool-count">{pick_count} tool picks</span>
</a>\n'''
            cards += '</div>\n'

    body = f'''<div class="container">
    <div class="category-header">
        <h1>Best SaaS Tools by Industry ({CURRENT_YEAR})</h1>
        <p class="category-desc">The Sultan's recommended SaaS stack for {len(INDUSTRIES)} industries. Each page picks the best tool from every category for your specific business.</p>
    </div>
    {cards}
</div>'''

    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Industries", "/for/")])

    page = get_page_wrapper(
        f"Best SaaS Tools by Industry ({CURRENT_YEAR})",
        f"SaaS tool recommendations for {len(INDUSTRIES)} industries. CRM, email, SEO, PM, and help desk picks tailored to your business.",
        "/for/",
        body,
        extra_head=bc_schema
    )
    write_page("for/index.html", page)


def build_tools_index():
    """Generate /tools/ filterable index page."""
    # Team size mapping: which team sizes each tool fits
    # solo = 1 person, small = 2-10, mid = 11-50, enterprise = 50+
    TEAM_SIZES = {
        # CRM
        'hubspot': ['solo', 'small', 'mid'],
        'salesforce': ['mid', 'enterprise'],
        'pipedrive': ['small', 'mid'],
        'close': ['small', 'mid'],
        'freshsales': ['solo', 'small'],
        'zoho-crm': ['solo', 'small', 'mid'],
        'copper': ['small'],
        'monday-sales-crm': ['small', 'mid'],
        'nutshell': ['small'],
        'less-annoying-crm': ['solo', 'small'],
        # Project Management
        'asana': ['small', 'mid'],
        'monday': ['small', 'mid'],
        'clickup': ['solo', 'small', 'mid'],
        'notion': ['solo', 'small'],
        'trello': ['solo', 'small'],
        'basecamp': ['small', 'mid'],
        'linear': ['small', 'mid'],
        'wrike': ['mid', 'enterprise'],
        'teamwork': ['small', 'mid'],
        'smartsheet': ['mid', 'enterprise'],
        # Email Marketing
        'mailchimp': ['solo', 'small'],
        'convertkit': ['solo', 'small'],
        'activecampaign': ['small', 'mid'],
        'constant-contact': ['solo', 'small'],
        'brevo': ['solo', 'small'],
        'drip': ['small'],
        'mailerlite': ['solo', 'small'],
        'campaign-monitor': ['small', 'mid'],
        'klaviyo': ['small', 'mid'],
        'beehiiv': ['solo'],
        # SEO Tools
        'semrush': ['small', 'mid', 'enterprise'],
        'ahrefs': ['small', 'mid'],
        'moz': ['small', 'mid'],
        'se-ranking': ['solo', 'small'],
        'ubersuggest': ['solo', 'small'],
        'surfer-seo': ['solo', 'small'],
        'mangools': ['solo', 'small'],
        'spyfu': ['solo', 'small'],
        'serpstat': ['solo', 'small'],
        'screaming-frog': ['solo', 'small', 'mid'],
        # Help Desk
        'zendesk': ['mid', 'enterprise'],
        'freshdesk': ['solo', 'small', 'mid'],
        'intercom': ['small', 'mid'],
        'help-scout': ['small'],
        'hubspot-service': ['small', 'mid'],
        'zoho-desk': ['solo', 'small'],
        'liveagent': ['small', 'mid'],
        'happyfox': ['small', 'mid'],
        'kayako': ['small', 'mid'],
        'groove-helpdesk': ['solo', 'small'],
        # AI SDR
        '11x': ['mid', 'enterprise'],
        'artisan': ['small', 'mid'],
        'aisdr': ['solo', 'small'],
        'regie-ai': ['mid', 'enterprise'],
        'amplemarket': ['small', 'mid'],
        'lavender': ['solo', 'small'],
        'smartlead': ['solo', 'small', 'mid'],
        'salesrobot': ['solo', 'small'],
        'nooks': ['small', 'mid'],
        'outplay': ['small', 'mid'],
        # Sales Engagement
        'outreach': ['mid', 'enterprise'],
        'salesloft': ['mid', 'enterprise'],
        'apollo': ['solo', 'small', 'mid'],
        'instantly': ['solo', 'small'],
        'reply-io': ['small', 'mid'],
        'mixmax': ['solo', 'small'],
        'mailshake': ['solo', 'small'],
        'woodpecker': ['solo', 'small'],
        'lemlist': ['small', 'mid'],
        'yesware': ['solo', 'small'],
        # Conversation Intelligence
        'gong': ['mid', 'enterprise'],
        'chorus': ['mid', 'enterprise'],
        'clari': ['mid', 'enterprise'],
        'sybill': ['small', 'mid'],
        'fireflies': ['solo', 'small', 'mid'],
        'otter-ai': ['solo', 'small'],
        'avoma': ['small', 'mid'],
        'fathom': ['solo', 'small'],
        'jiminny': ['small', 'mid'],
        'modjo': ['mid', 'enterprise'],
        # Data Enrichment
        'zoominfo': ['mid', 'enterprise'],
        'clay': ['small', 'mid'],
        'clearbit': ['small', 'mid'],
        'lusha': ['solo', 'small'],
        'cognism': ['small', 'mid', 'enterprise'],
        'seamless-ai': ['solo', 'small'],
        'uplead': ['solo', 'small'],
        'rocketreach': ['solo', 'small'],
        'leadiq': ['small', 'mid'],
        'kaspr': ['solo', 'small'],
    }

    # Pre-compute which industries each tool appears in
    tool_industries = {slug: set() for slug in TOOLS}
    for ind_slug, ind in INDUSTRIES.items():
        for cat_slug, pick in ind['picks'].items():
            ts = pick['tool']
            if ts in tool_industries:
                tool_industries[ts].add(ind_slug)

    # Build tool cards with data attributes for filtering
    tool_cards = ""
    for slug, t in sorted(TOOLS.items(), key=lambda x: -x[1]['score']):
        teamsize = " ".join(TEAM_SIZES.get(slug, []))
        industries = " ".join(sorted(tool_industries.get(slug, set())))
        tool_cards += f'''<div class="tool-card-wrap" data-category="{t["category"]}" data-price="{t["pricing_tier"]}" data-score="{t["score"]}" data-name="{t["name"]}" data-teamsize="{teamsize}" data-industries="{industries}">
    {tool_card_html(slug, show_category=True)}
</div>
'''

    # Industry options (tier 1 first, then 2, then 3)
    industry_options = ""
    for ind_slug, ind in sorted(INDUSTRIES.items(), key=lambda x: (x[1]['tier'], x[1]['name'])):
        industry_options += f'<option value="{ind_slug}">{ind["name"]}</option>\n'

    # Filter JS
    filter_js = '''<script>
(function() {
    const cards = document.querySelectorAll('.tool-card-wrap');
    const catSelect = document.getElementById('filter-category');
    const pricePills = document.querySelectorAll('.filter-pill[data-price]');
    const sortSelect = document.getElementById('filter-sort');
    const teamsizeSelect = document.getElementById('filter-teamsize');
    const industrySelect = document.getElementById('filter-industry');
    const countEl = document.getElementById('tool-count');
    let activePrice = '';

    function applyFilters() {
        const cat = catSelect.value;
        const teamsize = teamsizeSelect.value;
        const industry = industrySelect.value;
        let visible = 0;
        const grid = document.querySelector('.tool-grid');
        const items = Array.from(cards);

        items.forEach(c => {
            const matchCat = !cat || c.dataset.category === cat;
            const matchPrice = !activePrice || c.dataset.price === activePrice;
            const matchTeamsize = !teamsize || (c.dataset.teamsize && c.dataset.teamsize.split(' ').includes(teamsize));
            const matchIndustry = !industry || (c.dataset.industries && c.dataset.industries.split(' ').includes(industry));
            const show = matchCat && matchPrice && matchTeamsize && matchIndustry;
            c.style.display = show ? '' : 'none';
            if (show) visible++;
        });

        const sort = sortSelect.value;
        items.sort((a, b) => {
            if (a.style.display === 'none' && b.style.display !== 'none') return 1;
            if (a.style.display !== 'none' && b.style.display === 'none') return -1;
            if (sort === 'score') return parseFloat(b.dataset.score) - parseFloat(a.dataset.score);
            if (sort === 'name') return a.dataset.name.localeCompare(b.dataset.name);
            if (sort === 'price') {
                const order = {free:0, budget:1, mid:2, premium:3, enterprise:4};
                return (order[a.dataset.price]||5) - (order[b.dataset.price]||5);
            }
            return 0;
        });
        items.forEach(c => grid.appendChild(c));
        countEl.textContent = visible + ' tools';
    }

    catSelect.addEventListener('change', applyFilters);
    sortSelect.addEventListener('change', applyFilters);
    teamsizeSelect.addEventListener('change', applyFilters);
    industrySelect.addEventListener('change', applyFilters);
    pricePills.forEach(pill => {
        pill.addEventListener('click', function() {
            if (activePrice === this.dataset.price) {
                activePrice = '';
                this.classList.remove('active');
            } else {
                pricePills.forEach(p => p.classList.remove('active'));
                activePrice = this.dataset.price;
                this.classList.add('active');
            }
            applyFilters();
        });
    });
})();
</script>'''

    body = f'''<div class="tools-index">
    <div class="category-header">
        <h1>All SaaS Tools ({CURRENT_YEAR})</h1>
        <p class="category-desc">{len(TOOLS)} tools reviewed, scored, and ranked by The Sultan.</p>
    </div>
    <div class="filter-bar">
        <div class="filter-group">
            <span class="filter-label">Category</span>
            <select id="filter-category" class="filter-select">
                <option value="">All</option>
                <option value="crm">CRM</option>
                <option value="project-management">Project Management</option>
                <option value="email-marketing">Email Marketing</option>
                <option value="seo-tools">SEO Tools</option>
                <option value="help-desk">Help Desk</option>
                <option value="ai-sdr">AI SDR</option>
                <option value="sales-engagement">Sales Engagement</option>
                <option value="conversation-intelligence">Conversation Intelligence</option>
                <option value="data-enrichment">Data Enrichment</option>
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">Price</span>
            <button class="filter-pill" data-price="free">Free</button>
            <button class="filter-pill" data-price="budget">Budget</button>
            <button class="filter-pill" data-price="mid">Mid</button>
            <button class="filter-pill" data-price="premium">Premium</button>
        </div>
        <div class="filter-group">
            <span class="filter-label">Team Size</span>
            <select id="filter-teamsize" class="filter-select">
                <option value="">All</option>
                <option value="solo">Solo (1)</option>
                <option value="small">Small Team (2-10)</option>
                <option value="mid">Mid-Market (11-50)</option>
                <option value="enterprise">Enterprise (50+)</option>
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">Industry</span>
            <select id="filter-industry" class="filter-select">
                <option value="">All</option>
                {industry_options}
            </select>
        </div>
        <div class="filter-group">
            <span class="filter-label">Sort</span>
            <select id="filter-sort" class="filter-select">
                <option value="score">Sultan's Score</option>
                <option value="price">Price: Low &rarr; High</option>
                <option value="name">Name: A &rarr; Z</option>
            </select>
        </div>
        <span id="tool-count" class="tool-count-display">{len(TOOLS)} tools</span>
    </div>
    <div class="tool-grid">{tool_cards}</div>
</div>
{filter_js}'''

    bc_schema = get_breadcrumb_schema([("Home", "/"), ("All Tools", "/tools/")])

    page = get_page_wrapper(
        f"All SaaS Tools Reviewed ({CURRENT_YEAR})",
        f"Browse all {len(TOOLS)} SaaS tools reviewed by The Sultan. Filter by category, price, company size, and industry.",
        "/tools/",
        body,
        extra_head=bc_schema
    )
    write_page("tools/index.html", page)


def build_category_index():
    """Generate /best/ index page listing all categories."""
    cards = ""
    for slug, cat in CATEGORIES.items():
        count = len(cat['tools'])
        cards += f'''<a href="/best/{slug}/" class="category-card">
    <h3>{cat["name"]}</h3>
    <p>{cat["description"][:140]}{"..." if len(cat["description"]) > 140 else ""}</p>
    <span class="tool-count">{count} tools reviewed</span>
</a>\n'''

    body = f'''<div class="container">
    <div class="category-header">
        <h1>All SaaS Categories ({CURRENT_YEAR})</h1>
        <p class="category-desc">{len(CATEGORIES)} categories of SaaS tools reviewed and ranked for founders and SMBs.</p>
    </div>
    <div class="category-grid">{cards}</div>
</div>'''

    bc_schema = get_breadcrumb_schema([("Home", "/"), ("Categories", "/best/")])

    page = get_page_wrapper(
        f"All SaaS Tool Categories ({CURRENT_YEAR})",
        f"Browse {len(CATEGORIES)} categories of SaaS software. Each category ranked, scored, and reviewed by The Sultan.",
        "/best/",
        body,
        active_page="/best/",
        extra_head=bc_schema
    )
    write_page("best/index.html", page)


def build_sitemap():
    """Generate sitemap.xml."""
    urls = ""
    for page_path in ALL_PAGES:
        # Convert file path to URL
        if page_path.endswith("index.html"):
            url_path = page_path.replace("index.html", "")
        else:
            url_path = page_path

        if not url_path.startswith("/"):
            url_path = "/" + url_path

        urls += f'''  <url>
    <loc>{SITE_URL}{url_path}</loc>
    <lastmod>{BUILD_DATE}</lastmod>
  </url>\n'''

    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>'''

    sitemap_path = os.path.join(OUTPUT_DIR, "sitemap.xml")
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"  sitemap.xml ({len(ALL_PAGES)} URLs)")


def build_robots():
    """Generate robots.txt."""
    robots = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
    robots_path = os.path.join(OUTPUT_DIR, "robots.txt")
    with open(robots_path, "w", encoding="utf-8") as f:
        f.write(robots)
    print("  robots.txt")


# =============================================================================
# MAIN BUILD
# =============================================================================

def main():
    print(f"\n{'='*60}")
    print(f"  SultanOfSaaS Build")
    print(f"  {BUILD_DATE}")
    print(f"{'='*60}\n")

    # Clean output
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # Copy assets
    src_assets = ASSETS_DIR
    dst_assets = os.path.join(OUTPUT_DIR, "assets")
    shutil.copytree(src_assets, dst_assets)
    print(f"  Copied assets/")

    # Build pages
    print(f"\n  Building pages...")
    print(f"  {len(TOOLS)} tools, {len(CATEGORIES)} categories\n")

    build_homepage()
    print(f"  Homepage")

    build_category_index()
    build_category_pages()
    print(f"  {len(CATEGORIES)} category pages + index")

    build_tool_pages()
    print(f"  {len(TOOLS)} tool review pages")

    build_comparison_pages()
    print(f"  {len(COMPARISONS)} comparison pages")

    build_alternatives_pages()
    print(f"  {len(ALTERNATIVES)} alternatives pages")

    pricing_count = sum(1 for t in TOOLS.values() if t['pricing_tiers'])
    build_pricing_pages()
    print(f"  {pricing_count} pricing pages")

    build_stacks_index()
    build_stack_pages()
    print(f"  {len(STACKS)} stack guides + index")

    build_about_page()
    print(f"  About page")

    niche_count = build_niche_pages()
    print(f"  {niche_count} niche pages")

    build_industries_index()
    build_industry_pages()
    print(f"  {len(INDUSTRIES)} industry pages + index")

    build_tools_index()
    print(f"  Tools index (filterable)")

    build_sitemap()
    build_robots()

    total = len(ALL_PAGES)
    print(f"\n{'='*60}")
    print(f"  BUILD COMPLETE: {total} pages generated")
    print(f"  Output: {OUTPUT_DIR}")
    print(f"  Preview: cd output && python3 -m http.server 8086")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
