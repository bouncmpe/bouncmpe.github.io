# Short News Feature Requirements

## Overview

The short news feature is designed to display brief, concise news items on the main page. These are distinct from the existing full "stories" and are meant for quick updates about defense news, visits, small achievements, and other brief announcements.

## 1. Content Requirements

### 1.1 Content Structure
- **Length**: One to two sentences per news item (approximately 20-50 words)
- **Format**: Markdown-formatted text to support:
  - **Bold text** for emphasis
  - *Italic text* for styling
  - [Links](URL) for references
  - No images required (text-only)
- **Bilingual Support**: Both English and Turkish versions required for each short news item

### 1.2 Content Types
Short news should be suitable for:
- PhD defense announcements
- Faculty/student visits
- Small awards and recognitions
- Conference participation
- Workshop announcements
- Brief research updates
- Collaboration announcements
- Minor departmental updates

### 1.3 Content Organization
- **Location**: Separate content type from full stories
  - Proposed: `content/shortnews/` directory
  - Alternative: Add `type: shortnews` frontmatter to distinguish from regular news
- **File Structure**: Each short news item in its own directory with bilingual files
  ```
  content/shortnews/YYYY-MM-DD-short-title/
    ├── index.en.md
    └── index.tr.md
  ```

## 2. Frontmatter Schema

### 2.1 Required Fields
```yaml
---
type: shortnews
date: YYYY-MM-DD
title: "Brief title (optional, for admin purposes)"
---
```

### 2.2 Optional Fields
```yaml
featured: false  # Not used for short news
thumbnail: ""    # Not used for short news
```

### 2.3 Content Body
- Markdown content immediately following frontmatter
- 1-2 sentences maximum
- Support for markdown inline formatting (bold, italic, links)

## 3. Display Requirements

### 3.1 Homepage Layout
- **Position**: On the main page, separate section from full stories newsroom
- **Visual Style**: Dense "wall of text" presentation
  - Compact spacing between items
  - List format or minimal card design
  - No images
  - Clear visual separation from full stories section
  
### 3.2 Proposed Layout Options

#### Option A: Sidebar Widget
- Display in the right sidebar (currently has eventbar)
- Titled section: "Recent Updates" or "Quick News"
- Scrollable if list is long
- Shows most recent 5-10 items

#### Option B: Full-Width Section
- Dedicated section above or below newsroom
- Multiple columns (2-3 columns on desktop, 1 on mobile)
- Compact list format
- Shows most recent 10-15 items

#### Option C: Integrated Timeline
- Single column timeline on left or right
- Chronological order (newest first)
- Date markers for each item
- Shows most recent 8-12 items

### 3.3 Individual Item Display
Each short news item should show:
- **Date**: Formatted as "Month Day, Year" or "DD.MM.YYYY"
- **Content**: Markdown-rendered text (1-2 sentences)
- **Optional**: Link to full story if exists (for items that have both short and full versions)

### 3.4 Typography and Styling
- **Font Size**: Slightly smaller than body text (e.g., 0.9rem)
- **Line Height**: Compact but readable (1.3-1.5)
- **Item Spacing**: Minimal vertical spacing (0.5-1rem between items)
- **Text Color**: Body text color or slightly muted
- **Date Styling**: Small, muted text
- **Links**: Standard link styling with hover effects

## 4. Sorting and Filtering

### 4.1 Default Order
- **Reverse chronological**: Most recent items first
- **Date-based**: Sorted by `date` field in frontmatter

### 4.2 Display Limits
- **Homepage**: Show N most recent items (configurable in params.yml)
  - Suggested default: 10 items
- **Archive Page**: Optional dedicated page showing all short news items

### 4.3 Pagination
- Homepage: No pagination (fixed number of items)
- Archive page (if implemented): Paginated with 30-50 items per page

## 5. Content Creation Workflow

### 5.1 GitHub Issue Template
- Create new issue template: `.github/ISSUE_TEMPLATE/shortnews.yml`
- Required fields:
  - Date (YYYY-MM-DD)
  - Content in English (1-2 sentences, markdown supported)
  - Content in Turkish (1-2 sentences, markdown supported)
- Optional fields:
  - Title (for administrative purposes)
  - Link to related full story (if applicable)

### 5.2 Automated PR Creation
- Use existing issue-to-pr workflow
- Create markdown files in appropriate directory structure
- Follow same pattern as existing news items

### 5.3 Manual Creation
- Content editors can manually create files in `content/shortnews/`
- Follow established naming convention: `YYYY-MM-DD-descriptive-slug/`
- Include both `index.en.md` and `index.tr.md`

## 6. Configuration Parameters

### 6.1 Site Parameters (config/_default/params.yml)
```yaml
shortnews:
  enabled: true          # Enable/disable short news section
  limit: 10             # Number of items to show on homepage
  layout: sidebar       # Layout option: 'sidebar', 'section', 'timeline'
  title_en: "Recent Updates"
  title_tr: "Son Gelişmeler"
  show_dates: true      # Show dates with each item
  date_format: "Jan 2, 2006"  # Hugo date format string
```

### 6.2 Internationalization (i18n/)
Add to `i18n/en.yaml`:
```yaml
recent-updates:
  other: "recent updates"

short-news:
  other: "short news"

more-updates:
  other: "more updates"
```

Add to `i18n/tr.yaml`:
```yaml
recent-updates:
  other: "son gelişmeler"

short-news:
  other: "kısa haberler"

more-updates:
  other: "daha fazla"
```

## 7. Implementation Components

### 7.1 Hugo Templates
New partial templates needed:
- `layouts/partials/bouncmpe/shortnews.html` - Main short news section
- `layouts/partials/bouncmpe/shortnews-item.html` - Individual item display

### 7.2 Homepage Integration
Modify `layouts/index.html`:
- Add short news section based on configuration
- Position according to selected layout option
- Ensure responsive design

### 7.3 Archive Page (Optional)
- Create `layouts/_default/shortnews.html` for archive list
- Create `content/shortnews/_index.en.md` and `_index.tr.md`
- List all short news items with pagination

## 8. Differentiation from Full Stories

### 8.1 Full Stories (Existing)
- **Length**: 2-3 paragraphs (200-500 words)
- **Image**: Required cover photo
- **Display**: Card layout with thumbnail
- **Featured**: Can be featured in carousel
- **Content**: Detailed information with context

### 8.2 Short News (New)
- **Length**: 1-2 sentences (20-50 words)
- **Image**: Not required (text-only)
- **Display**: Compact list/timeline format
- **Featured**: Not applicable
- **Content**: Brief announcements, minimal context

### 8.3 Relationship
- Items can exist as both short news and full story
- Short news can link to corresponding full story
- Full stories continue to be the primary content type
- Short news complements, not replaces, full stories

## 9. Accessibility Requirements

### 9.1 Semantic HTML
- Use appropriate semantic elements (`<article>`, `<time>`, `<section>`)
- Proper heading hierarchy
- ARIA labels where appropriate

### 9.2 Responsive Design
- Mobile-first approach
- Readable on all screen sizes
- Appropriate breakpoints for layout changes
- Touch-friendly spacing on mobile devices

### 9.3 Keyboard Navigation
- All interactive elements keyboard accessible
- Logical tab order
- Visible focus indicators

## 10. Performance Considerations

### 10.1 Build Time
- Short news items are markdown files processed during Hugo build
- No additional build time overhead expected
- Efficient querying using Hugo's taxonomy and filtering

### 10.2 Page Load
- Text-only content (no images)
- Minimal CSS/JS requirements
- Lazy loading not necessary (small content size)

### 10.3 Scalability
- Hugo handles large numbers of content files efficiently
- Consider archiving very old items (1+ years) if needed
- Pagination on archive page for large collections

## 11. Content Guidelines

### 11.1 Writing Style
- **Concise**: Get to the point immediately
- **Active Voice**: Use active voice for clarity
- **Clear**: Avoid jargon unless necessary
- **Complete**: Each item should be self-contained
- **Professional**: Maintain academic/professional tone

### 11.2 Examples

**Good Examples:**
- "Dr. Ayşe Yılmaz successfully defended her PhD thesis on distributed systems."
- "Professor John Smith from MIT visited our department and gave a talk on quantum computing."
- "**Congratulations** to our students who won the [ACM Programming Contest](https://acm.org)!"
- "New collaboration established with *Technical University of Munich* for AI research."

**Bad Examples:**
- "Great news! We're so excited to announce..." (too informal, too long)
- "Defense tomorrow" (too brief, lacks context)
- Long paragraph with multiple topics (should be multiple short news items)

### 11.3 Markdown Usage
- **Bold**: For names, key terms, emphasis on achievements
- *Italic*: For institution names, publication titles
- [Links]: For external references, related pages
- No complex formatting (tables, images, code blocks)

## 12. Success Metrics

### 12.1 Content Metrics
- Number of short news items published per month
- Ratio of short news to full stories
- Coverage of different content types (defenses, visits, awards)

### 12.2 Engagement Metrics (if analytics available)
- Click-through rate on links in short news
- Time spent on homepage
- Scroll depth to short news section

### 12.3 Editorial Metrics
- Time to publish short news vs full stories
- Number of contributors
- Update frequency

## 13. Future Enhancements (Out of Scope for v1)

### 13.1 Potential Features
- RSS feed for short news only
- Email notifications for new short news
- Search/filter by content type (defense, visit, award, etc.)
- Tags or categories for short news
- Archive by year/month
- "Pin" important short news items
- Social media integration
- Export to JSON/API for external consumption

### 13.2 Advanced Display Options
- Animated transitions for new items
- Compact/expanded view toggle
- Integration with calendar/events
- Related news clustering
- Multi-language switching without page reload

## 14. Migration and Rollout

### 14.1 Initial Content
- Migrate recent announcements (last 3 months) from other sources
- Create 10-15 sample short news items for launch
- Ensure both English and Turkish content ready

### 14.2 Rollout Plan
1. Implement core feature (templates, content structure)
2. Create issue template for easy submission
3. Populate with initial content
4. Test on staging/preview
5. Deploy to production
6. Monitor and gather feedback
7. Iterate based on usage patterns

### 14.3 Documentation
- Update CONTRIBUTING.md with short news guidelines
- Create example short news items
- Document issue template usage
- Update README with new feature information

## 15. Open Questions for Stakeholders

### 15.1 Design Questions
1. **Layout preference**: Sidebar widget, full-width section, or timeline? (see Section 3.2)
2. **Number of items**: How many short news items to show on homepage? (suggested: 10)
3. **Archive page**: Do we need a dedicated archive page for all short news?
4. **Styling**: Should short news have a distinct background color or border?

### 15.2 Content Questions
1. **Moderation**: Who approves short news submissions?
2. **Frequency**: Expected number of short news items per week/month?
3. **Retention**: How long should short news items remain visible? (archive after N months?)
4. **Cross-posting**: Should some full stories also appear as short news?

### 15.3 Technical Questions
1. **Analytics**: Do we need specific tracking for short news engagement?
2. **SEO**: Should short news items have individual pages or only appear in the list?
3. **API**: Do we need to expose short news via API for external consumption?
4. **Notifications**: Should there be any notification system for new short news?

## 16. Dependencies

### 16.1 Technical Dependencies
- Hugo static site generator (already in use)
- Bootstrap framework (already in use)
- GitHub Actions workflow (already in use)
- No new external dependencies required

### 16.2 Content Dependencies
- Bilingual content team (English and Turkish)
- Content approval workflow
- Style guide adherence

### 16.3 Design Dependencies
- Consistent with existing design system
- Responsive layout compatible with current templates
- Accessibility standards compliance

## Conclusion

This requirements document provides a comprehensive foundation for implementing the short news feature. The key differentiators from full stories are:
- **Brevity**: 1-2 sentences vs 2-3 paragraphs
- **No images**: Text-only vs required cover photo
- **Density**: Compact wall-of-text display vs spacious card layout
- **Purpose**: Quick updates vs detailed announcements

The implementation should be minimal, maintainable, and consistent with the existing Hugo-based architecture of the website.
