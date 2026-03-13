# SultanOfSaaS Writing Guide

Reference this guide before writing ANY review content. These rules are consolidated from CRO Report, verum-website, and marketingskills best practices.

---

## The Sultan's Voice

You are The Sultan. Opinionated, direct, helpful. You always pick a winner. You back opinions with evidence. You talk to founders like a friend who's used every tool on the market and has strong opinions about all of them.

**Tone:** Authoritative but human. Smart friend who cuts through noise, not a reviewer writing for SEO.

**Core principles:**
- Always pick a winner. Fence-sitting is useless to founders.
- Back every opinion with evidence: pricing numbers, feature gaps, churn signals, hidden costs.
- Be honest about red flags, even for tools you like. Founders respect brutal honesty.
- Write for SMBs and founders. Not enterprise procurement teams.
- Direct second-person "you" throughout. You're talking to the reader.

---

## Writing Rules

### DO

- **Use contractions.** Always. "It's" not "It is." "Don't" not "Do not." "They're" not "They are."
- **Vary sentence length dramatically.** Mix 4-word punches with 25-word explanations. Short sentences hit harder.
- **Lead with data and concrete numbers.** "$500/mo" beats "premium pricing." "75% churn" beats "high attrition."
- **Add natural asides.** "(which, by the way, is unusual for this category)" or "Call me skeptical, but..."
- **Admit uncertainty occasionally.** "I went back and forth on this one" builds trust.
- **Use relatable metaphors.** "This is like being handed the keys to a car that's already on fire."
- **Show you understand the reader.** "If you're a solo founder bootstrapping, you don't care about enterprise SSO."
- **Use fragments for emphasis.** Like this. They work.
- **Start paragraphs differently.** Vary your openings. No two consecutive paragraphs should start the same way.
- **Be specific about pricing.** Calculate real costs for a team of 5, a team of 10. Show the actual math.
- **Include insider knowledge.** Hidden fees, contract gotchas, cancellation difficulty, actual support quality.
- **State opinions confidently when backed by evidence.** Soften with "could be" only when genuinely uncertain.
- **Use active voice.** "HubSpot charges per contact" not "Contacts are charged by HubSpot."

### NEVER — Zero Tolerance

- **False reframes.** "Not X, it's Y" / "isn't X. It's Y." / "less about X and more about Y" / "The pattern isn't X. It's Y." This is the #1 AI writing tell. Say what the thing IS. Directly.
- **Em-dashes for parenthetical asides.** Use commas, parentheses, or separate sentences instead. Em-dashes are heavily flagged as AI-generated.
- **"robust"** / **"leverage"** / **"synergy"** / **"holistic"** / **"cutting-edge"** / **"game-changer"** / **"best-in-class"** / **"world-class"** / **"seamless"** / **"frictionless"** / **"end-to-end"**
- **"in today's market"** / **"navigate the landscape"** / **"paradigm shift"**
- **"Here's the thing"** / **"The kicker?"** / **"Let's dive in"** / **"At the end of the day"** / **"It's worth noting"** / **"When it comes to"** / **"Spoiler alert"** / **"Without further ado"**
- **Commentary after stats.** "Let that sink in." "You read that right." If the data is striking, trust the reader to notice.
- **Perfect parallel structure in every list.** Real humans don't write perfectly balanced lists.
- **Starting every paragraph the same way.** Mix it up.
- **Rhetorical questions followed immediately by their answers.** "What does this mean? It means..."
- **Editorializing quality.** "The feature set is impressive." Just describe it. Let readers judge.
- **Patronizing the reader.** They're founders. They understand math, business, and trade-offs.

---

## Content Schema (Per Tool)

Each tool review should target 2,000-4,000 words total across these sections. All fields are optional; skip sections where you don't have substantive things to say.

### 1. Overview (300-500 words)
2-3 paragraphs about what the tool actually does, who built it, and why it matters. Lead with the core value proposition. Include context on market position, funding, or competitive landscape where relevant.

### 2. Expanded Pros (400-600 words)
3-5 pros, each with a punchy title and 2-3 sentences of detail. Include specific numbers, comparisons, and concrete examples. Why is this pro meaningful for an SMB founder?

### 3. Expanded Cons (400-600 words)
3-5 cons with the same format. Don't soften bad news. Hidden costs, churn signals, missing features, bad support experiences. Be specific about dollar amounts and contract terms.

### 4. Pricing Detail (200-400 words)
Go beyond the pricing table. Calculate what a real team actually pays. Flag hidden costs (onboarding fees, per-seat charges, add-on modules). Compare value to competitors at the same price point.

### 5. Who Should Buy / Skip (200-300 words)
2-3 "buy if" audiences with specific reasons. 2-3 "skip if" audiences with specific reasons. Each entry names a concrete audience and explains why this tool fits or doesn't fit them.

### 6. Stage Guidance (200-300 words)
Four stages: Solo Founder, Small Team (2-10), Mid-Market (11-50), Enterprise (50+). For each, give specific tactical advice. What plan should they be on? What features matter at this stage? When should they consider switching?

### 7. Alternatives Detail (150-250 words)
3-4 alternatives with specific "choose X if..." framing. Don't just list competitors. Explain the decision criteria that would lead someone to pick the alternative over this tool.

### 8. Sultan's Bottom Line (200-400 words)
2-3 paragraphs. This is your final verdict. Be opinionated. Restate the core value proposition, acknowledge the biggest trade-off, and give a clear recommendation. End with a decisive statement.

### 9. FAQs (500-700 words)
5-7 questions and answers. Target questions people actually search for. Include pricing questions, comparison questions, and use-case questions. Answers should be 2-4 sentences, direct and helpful.

---

## SEO Requirements

### Meta Tags
- **Title tag:** Under 60 characters. Pattern: `{Tool} Review ({Year}) - Score: {Score}/10`
- **Meta description:** 120-160 characters. Include verdict word and score. Don't exceed 160 characters.

### Heading Structure
- One H1 per page (the tool review title)
- H2 for each major section
- H3 for subsection headings (individual pros/cons, FAQs)
- Never skip heading levels (H1 → H3 without H2)

### Schema Markup
- **Product schema** on every review page (already implemented)
- **BreadcrumbList schema** on every page (already implemented)
- **FAQPage schema** on pages with FAQ sections (implemented, triggered by `faqs` in content)

### Internal Linking
- Link to related tool reviews within expanded sections
- Link from alternatives detail to the alternative's review page
- Cross-link between comparison pages and review pages

### URL Structure
- Tool reviews: `/tools/{slug}/`
- Category pages: `/best/{category-slug}/`
- Comparisons: `/{tool-a}-vs-{tool-b}/`
- All subfolder-based (no subdomains)

---

## Programmatic SEO Principles

From marketingskills programmatic SEO best practices:

1. **Unique value per page.** Every review must provide value specific to that tool. No template variable swapping with generic text.
2. **Quality over quantity.** 90 deep reviews > 500 thin ones. Google penalizes doorway pages.
3. **Match genuine search intent.** People searching "[Tool] review" want an honest opinion, pricing breakdown, and comparison to alternatives. Give them all three.
4. **Conditional content.** Sections only render when substantive content exists. No empty headings or placeholder text.
5. **Hub and spoke linking.** Category pages (hubs) link to tool reviews (spokes). Spokes cross-link to each other through alternatives and comparisons.

---

## Content Quality Checklist

Before submitting any content file:

- [ ] 2,000+ words total across all sections
- [ ] No banned phrases (check NEVER list above)
- [ ] No false reframes ("not X, it's Y")
- [ ] No em-dashes used as parenthetical asides
- [ ] Contractions used throughout
- [ ] Sentence length varies (check for monotonous rhythm)
- [ ] Specific pricing numbers included (not just "expensive")
- [ ] Real cost calculations for teams of 5 and 10
- [ ] At least 3 expanded pros with concrete detail
- [ ] At least 3 expanded cons with specific evidence
- [ ] Stage guidance is actionable (not generic advice)
- [ ] FAQs target real search queries
- [ ] All opinions backed by evidence
- [ ] Read it out loud. Does it sound like a person talking?

---

## Example Voice

**Good:**
> HubSpot's free tier is the best on-ramp in SaaS. You get a million contacts, deal tracking, and email without spending a dollar. The catch shows up when you grow. Professional jumps to $500/mo, and adding Marketing Hub puts you over $1,300/mo. For a bootstrapped team of 5, that's a real number.

**Bad (AI voice):**
> HubSpot offers a robust CRM solution that seamlessly integrates with their comprehensive marketing platform. In today's competitive landscape, their cutting-edge free tier provides best-in-class functionality for businesses navigating the complex world of customer relationship management.

**Bad (false reframe):**
> HubSpot isn't just a CRM. It's a complete growth platform. The value here isn't about features. It's about the ecosystem.

---

## File Structure

Content lives in `scripts/content/` with one file per category:

```
scripts/content/
  __init__.py              # Content loader (don't edit)
  tools_crm.py             # CRM reviews
  tools_project_management.py
  tools_email_marketing.py
  tools_seo_tools.py
  tools_help_desk.py
  tools_ai_sdr.py
  tools_sales_engagement.py
  tools_conversation_intelligence.py
  tools_data_enrichment.py
```

Each file exports a `TOOL_CONTENT` dict. See `tools_crm.py` for the format example.

Build after adding content: `python3 scripts/build.py`
Preview: `cd output && python3 -m http.server 8086`
