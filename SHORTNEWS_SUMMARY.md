# Short News Feature - Summary for Stakeholders

## Quick Overview

**Purpose**: Add a lightweight "short news" feature to display brief, 1-2 sentence updates on the homepage for quick announcements like PhD defenses, visits, awards, and minor achievements.

**Status**: Requirements brainstorming phase - seeking stakeholder input before implementation.

## Key Points

### What is Short News?
- **Brief announcements**: 1-2 sentences per item
- **Markdown formatted**: Support for bold, italic, and links
- **Text-only**: No images required (unlike full stories)
- **Dense display**: Stacked as a "wall of text" on the homepage
- **Bilingual**: English and Turkish versions

### Why Short News?
- **Current state**: Full stories require 2-3 paragraphs and cover photos
- **Gap**: Need a lighter way to announce smaller updates quickly
- **Use cases**: 
  - PhD defenses
  - Faculty/student visits
  - Small awards
  - Conference participation
  - Workshop announcements
  - Brief research updates

### How is it Different from Full Stories?

| Aspect | Full Stories (Current) | Short News (New) |
|--------|----------------------|------------------|
| Length | 2-3 paragraphs (200-500 words) | 1-2 sentences (20-50 words) |
| Image | Required cover photo | Not required (text-only) |
| Display | Card layout with thumbnail | Compact list format |
| Featured | Can be in carousel | Not applicable |
| Purpose | Detailed announcements | Quick updates |

## Display Layout Options

We propose **three layout options** for stakeholder consideration:

### Option 1: Sidebar Widget (Recommended)
```
┌──────────────────────┬─────────────┐
│ Featured Stories     │ Recent      │
│ [Carousel]           │ Updates     │
│                      │ ────────    │
│ Recent Stories       │ • Dec 10    │
│ [Cards with images]  │   PhD def.. │
│                      │             │
│                      │ • Dec 8     │
│                      │   Visit...  │
└──────────────────────┴─────────────┘
```
**Pros**: Doesn't disrupt existing layout, always visible, easy to scan
**Cons**: Limited space, may need scrolling for many items

### Option 2: Full-Width Section
```
┌────────────────────────────────────┐
│ Featured Stories [Carousel]        │
├────────────────────────────────────┤
│ Recent Updates (Multi-column)      │
│ Dec 10 │ Dec 8  │ Dec 5            │
│ PhD    │ Visit  │ Award            │
├────────────────────────────────────┤
│ Recent Stories [Cards]             │
└────────────────────────────────────┘
```
**Pros**: More space, better visibility, clearer separation
**Cons**: Pushes other content down, requires more vertical space

### Option 3: Timeline Layout
```
┌──┬─────────────────────────────────┐
│R │ Featured Stories [Carousel]     │
│E │                                 │
│C │ Recent Stories [Cards]          │
│E │                                 │
│N │                                 │
│T │                                 │
│  │                                 │
│• │                                 │
│12│                                 │
└──┴─────────────────────────────────┘
```
**Pros**: Space-efficient, chronologically clear, distinctive
**Cons**: Unconventional, may not fit mobile well

## Example Short News Items

```markdown
**Dr. Mehmet Yılmaz** successfully defended his PhD thesis 
on "Deep Learning for NLP" on December 10, 2024. Congratulations!
```

```markdown
Prof. Sarah Johnson from *Stanford University* visited our 
department and delivered a seminar on quantum computing.
```

```markdown
Congratulations to **Ayşe Demir** for winning the Best Paper 
Award at the [National Software Conference](https://example.com)!
```

## Implementation Overview

### Content Structure
```
content/shortnews/
├── 2024-12-10-yilmaz-defense/
│   ├── index.en.md
│   └── index.tr.md
└── 2024-12-08-johnson-visit/
    ├── index.en.md
    └── index.tr.md
```

### Frontmatter
```yaml
---
type: shortnews
date: 2024-12-10
---

Content goes here (1-2 sentences with markdown formatting).
```

### Configuration
```yaml
shortnews:
  enabled: true
  limit: 10              # Number shown on homepage
  layout: sidebar        # or 'section' or 'timeline'
  title_en: "Recent Updates"
  title_tr: "Son Gelişmeler"
```

## Questions for Stakeholders

### 1. Layout Preference
**Which layout option do you prefer?**
- [ ] Option 1: Sidebar Widget (recommended)
- [ ] Option 2: Full-Width Section
- [ ] Option 3: Timeline Layout
- [ ] Other suggestion: _______________

### 2. Display Count
**How many short news items should appear on the homepage?**
- [ ] 5 items
- [ ] 10 items (recommended)
- [ ] 15 items
- [ ] Other: _____

### 3. Archive Page
**Should there be a dedicated archive page showing all historical short news?**
- [ ] Yes, with pagination
- [ ] No, only show on homepage
- [ ] Undecided

### 4. Styling
**Should short news have a distinct visual treatment?**
- [ ] Background color/border to distinguish from other content
- [ ] Same styling as rest of page
- [ ] Undecided

### 5. Content Moderation
**Who will approve short news submissions?**
- [ ] Automatic approval (via GitHub Actions)
- [ ] Manual approval by: _______________
- [ ] Mix of automatic for trusted contributors, manual for others

### 6. Update Frequency
**How often do you expect to publish short news items?**
- [ ] Daily
- [ ] 2-3 times per week (8-12 per month)
- [ ] Weekly
- [ ] As needed

### 7. Content Retention
**How long should short news remain visible?**
- [ ] Forever (no archiving)
- [ ] Archive after 3 months
- [ ] Archive after 6 months
- [ ] Archive after 1 year

### 8. Cross-posting
**Should some full stories also appear as short news?**
- [ ] Yes, create both formats for major announcements
- [ ] No, they are mutually exclusive
- [ ] Case by case

## Content Guidelines Summary

### Good Examples ✅
- Brief and complete (1-2 sentences)
- Uses markdown for emphasis (**bold**, *italic*)
- Includes relevant links
- Professional tone
- Self-contained information

### Bad Examples ❌
- Too long (more than 2 sentences)
- Too brief (lacks context: "Defense tomorrow")
- Too informal ("Great news! We're so excited...")
- Multiple topics in one item (should be separate items)
- Complex formatting (tables, images, code blocks)

## Next Steps

1. **Review** these requirements documents:
   - `SHORTNEWS_REQUIREMENTS.md` - Full specification (16 sections)
   - `SHORTNEWS_EXAMPLES.md` - Examples and mockups
   - `SHORTNEWS_SUMMARY.md` - This document

2. **Discuss** with stakeholders:
   - @gokceuludogan @Cydonia01 @uskudarli

3. **Decide** on:
   - Preferred layout option
   - Display settings (count, styling)
   - Content moderation workflow
   - Timeline for implementation

4. **Implement** after approval:
   - Hugo templates and partials
   - Content structure
   - Issue template for submissions
   - Initial content migration
   - Testing and deployment

## Timeline Estimate

**Phase 1**: Requirements & Design (Current)
- Brainstorm requirements ✅
- Review with stakeholders (pending)
- Finalize decisions (pending)

**Phase 2**: Implementation (1-2 weeks)
- Create templates and layouts
- Set up content structure
- Create issue template
- Test on staging

**Phase 3**: Content & Launch (1 week)
- Migrate initial content (10-15 items)
- Documentation updates
- Deploy to production
- Monitor and gather feedback

**Total**: 2-3 weeks from approval to launch

## Additional Resources

- Full requirements: `SHORTNEWS_REQUIREMENTS.md`
- Examples and mockups: `SHORTNEWS_EXAMPLES.md`
- Issue discussion: [Link to GitHub issue]

## Contact

For questions or feedback on these requirements, please comment on the GitHub issue or contact:
- @doganulus (Project lead)
- @gokceuludogan @Cydonia01 @uskudarli (Stakeholders)

---

**Last Updated**: December 12, 2024
**Status**: Awaiting stakeholder review and feedback
