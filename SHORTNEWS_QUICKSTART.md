# Short News Feature - Quick Start Guide

## For Stakeholders

### Review Checklist

Read the documents in this order:

1. **START HERE**: `SHORTNEWS_SUMMARY.md` (5 min read)
   - Quick overview of the feature
   - See layout options with diagrams
   - Review key questions to answer

2. **THEN**: `SHORTNEWS_DECISION_MATRIX.md` (10 min read)
   - Detailed comparison of 3 layout options
   - Scoring matrix and recommendations
   - Vote sheet at the end

3. **OPTIONAL**: `SHORTNEWS_REQUIREMENTS.md` (20 min read)
   - Complete technical specification
   - All 16 requirement sections
   - For those wanting full details

4. **OPTIONAL**: `SHORTNEWS_EXAMPLES.md` (15 min read)
   - Practical examples and mockups
   - Code samples and templates
   - Migration strategy

### Decisions Needed

Please provide feedback on these questions (see SHORTNEWS_SUMMARY.md for full context):

#### 1. Layout Choice (Required)
- [ ] Option 1: Sidebar Widget (recommended)
- [ ] Option 2: Full-Width Section
- [ ] Option 3: Timeline Layout

#### 2. Display Count (Required)
- [ ] 5 items
- [ ] 10 items (recommended)
- [ ] 15 items
- [ ] Other: _____

#### 3. Archive Page (Required)
- [ ] Yes, with pagination
- [ ] No, homepage only

#### 4. Visual Styling (Optional)
- [ ] Distinct background/border
- [ ] Match existing styling
- [ ] Let designer decide

#### 5. Content Moderation (Required)
- [ ] Automatic (via GitHub Actions)
- [ ] Manual approval by: __________
- [ ] Mixed approach

#### 6. Update Frequency (Informational)
Expected: _____ items per month

#### 7. Retention Policy (Optional)
- [ ] Keep forever
- [ ] Archive after: _____ months

#### 8. Cross-posting (Optional)
- [ ] Create both short news + full story for major items
- [ ] Keep them separate

### How to Provide Feedback

**Option A**: Comment on the GitHub issue
- Go to the issue: [Add Short News](https://github.com/bouncmpe/bouncmpe.github.io/issues/XXX)
- Add your feedback as a comment
- Tag relevant people: @gokceuludogan @Cydonia01 @uskudarli

**Option B**: Fill out the vote sheet
- See `SHORTNEWS_DECISION_MATRIX.md` bottom section
- Print or copy the vote sheet
- Fill it out and share with the team

**Option C**: Schedule a meeting
- Discuss together as a group
- Make decisions collaboratively
- Document decisions in the issue

---

## For Developers

### Implementation Checklist

Once stakeholder decisions are made, follow this checklist to implement:

#### Phase 1: Setup (Day 1)

**1. Create Content Directory**
```bash
mkdir -p content/shortnews
touch content/shortnews/_index.en.md
touch content/shortnews/_index.tr.md
```

**2. Add Index Files**

`content/shortnews/_index.en.md`:
```yaml
---
title: Recent Updates
---
```

`content/shortnews/_index.tr.md`:
```yaml
---
title: Son Gelişmeler
---
```

**3. Update Configuration**

Add to `config/_default/params.yml`:
```yaml
shortnews:
  enabled: true
  limit: 10                    # Adjust based on stakeholder decision
  layout: sidebar              # or 'section' or 'timeline'
  title_en: "Recent Updates"
  title_tr: "Son Gelişmeler"
  show_dates: true
  date_format: "Jan 2, 2006"
```

**4. Add i18n Translations**

Add to `i18n/en.yaml`:
```yaml
recent-updates:
  other: "recent updates"

short-news:
  other: "short news"

more-updates:
  other: "more updates"

view-all-updates:
  other: "view all updates"
```

Add to `i18n/tr.yaml`:
```yaml
recent-updates:
  other: "son gelişmeler"

short-news:
  other: "kısa haberler"

more-updates:
  other: "daha fazla"

view-all-updates:
  other: "tüm güncellemeleri gör"
```

#### Phase 2: Templates (Day 2-3)

**5. Create Main Partial**

`layouts/partials/bouncmpe/shortnews.html`:
```html
{{ $shortnews := where site.RegularPages "Section" "shortnews" }}
{{ $shortnews = $shortnews.ByDate.Reverse }}
{{ $limit := site.Params.shortnews.limit | default 10 }}

{{ if $shortnews }}
<section id="shortnews" class="card rounded-4 p-3 mb-4">
  <h5 class="mb-3 pb-2 border-bottom">
    {{ i18n "recent-updates" | title }}
  </h5>
  
  <div class="shortnews-list">
    {{ range first $limit $shortnews }}
      {{ partial "bouncmpe/shortnews-item.html" . }}
    {{ end }}
  </div>
  
  {{ if gt (len $shortnews) $limit }}
  <div class="text-center mt-3">
    <a href="/shortnews/" class="btn btn-sm btn-outline-primary">
      {{ i18n "view-all-updates" }} →
    </a>
  </div>
  {{ end }}
</section>
{{ end }}
```

**6. Create Item Partial**

`layouts/partials/bouncmpe/shortnews-item.html`:
```html
<article class="shortnews-item mb-3 pb-3 border-bottom">
  {{ if site.Params.shortnews.show_dates }}
  <time class="d-block text-muted small mb-1" datetime="{{ .Date.Format "2006-01-02" }}">
    {{ .Date.Format (site.Params.shortnews.date_format | default "Jan 2, 2006") }}
  </time>
  {{ end }}
  
  <div class="shortnews-content">
    {{ .Content }}
  </div>
</article>
```

**7. Update Homepage**

Modify `layouts/index.html` to include short news.

For **Sidebar Layout** (Option 1), add to the right column:
```html
<div class="col-xl-4 order-xl-5 my-3 text-center">
    {{ if site.Params.eventbar.enabled }}
        {{ partial "bouncmpe/eventbar.html" . }}
    {{ end }}
    
    <!-- Add short news here -->
    {{ if site.Params.shortnews.enabled }}
        {{ partial "bouncmpe/shortnews.html" . }}
    {{ end }}
</div>
```

For **Section Layout** (Option 2), add between carousel and stories:
```html
{{ if site.Params.shortnews.enabled }}
    {{ partial "bouncmpe/shortnews.html" . }}
{{ end }}
```

For **Timeline Layout** (Option 3), add a new column:
```html
<div class="row">
    <div class="col-lg-2">
        {{ if site.Params.shortnews.enabled }}
            {{ partial "bouncmpe/shortnews.html" . }}
        {{ end }}
    </div>
    <div class="col-lg-10">
        <!-- Existing content -->
    </div>
</div>
```

**8. Add CSS Styling**

Create `assets/scss/components/_shortnews.scss` (or add to existing CSS):
```css
#shortnews {
  background-color: #f8f9fa;
  
  h5 {
    color: #1e4a8b;
    font-weight: 600;
  }
}

.shortnews-list {
  max-height: 500px;
  overflow-y: auto;
  overflow-x: hidden;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
    
    &:hover {
      background: #555;
    }
  }
}

.shortnews-item {
  &:last-child {
    border-bottom: none !important;
    margin-bottom: 0 !important;
    padding-bottom: 0 !important;
  }
  
  time {
    font-size: 0.85rem;
    font-weight: 500;
  }
  
  .shortnews-content {
    font-size: 0.95rem;
    line-height: 1.5;
    
    p {
      margin: 0;
    }
    
    strong {
      color: #1e4a8b;
      font-weight: 600;
    }
    
    a {
      color: #1e4a8b;
      text-decoration: none;
      border-bottom: 1px solid transparent;
      transition: border-color 0.2s;
      
      &:hover {
        border-bottom-color: #1e4a8b;
      }
    }
  }
}

@media (max-width: 767px) {
  .shortnews-list {
    max-height: 400px;
  }
}
```

#### Phase 3: Issue Template (Day 3)

**9. Create Issue Template**

`.github/ISSUE_TEMPLATE/shortnews.yml`:
```yaml
name: Short News Submission
description: Submit a brief news item (1-2 sentences) for the website
title: "[SHORT NEWS] <Insert brief title>"
labels: ["auto-md", "shortnews"]
body:
  - type: markdown
    attributes:
      value: |
        ## Short News Submission
        Submit brief news items (1-2 sentences) for quick announcements.
        
        **Examples:**
        - PhD defenses
        - Faculty visits
        - Awards and achievements
        - Conference participation
        - Workshop announcements

  - type: input
    id: date
    attributes:
      label: "Date (YYYY-MM-DD)"
      description: "Date of the news event"
      placeholder: "2024-12-10"
    validations:
      required: true

  - type: textarea
    id: content_en
    attributes:
      label: "Content (English)"
      description: "1-2 sentences maximum. Markdown formatting supported: **bold**, *italic*, [links](URL)"
      placeholder: |
        **Dr. John Smith** successfully defended his PhD thesis on "Deep Learning for Natural Language Processing" on December 10, 2024. Congratulations!
    validations:
      required: true

  - type: textarea
    id: content_tr
    attributes:
      label: "İçerik (Türkçe)"
      description: "Maksimum 1-2 cümle. Markdown biçimlendirmesi desteklenir: **kalın**, *italik*, [bağlantılar](URL)"
      placeholder: |
        **Dr. Ahmet Yılmaz**, "Doğal Dil İşleme için Derin Öğrenme" konulu doktora tezini 10 Aralık 2024 tarihinde başarıyla savundu. Tebrikler!
    validations:
      required: true

  - type: input
    id: related_story
    attributes:
      label: "Related Full Story (Optional)"
      description: "If this has a corresponding full story, provide the URL or path"
      placeholder: "/news/2024-12-10-smith-defense/"
    validations:
      required: false

  - type: markdown
    attributes:
      value: |
        ---
        ### Formatting Tips
        - **Bold**: Use for names, achievements (`**Dr. Name**`)
        - *Italic*: Use for institutions, titles (`*Stanford University*`)
        - [Links]: Use for references (`[Conference Name](https://url.com)`)
        - Keep it brief: 1-2 sentences maximum!
```

**10. Update Issue-to-PR Workflow**

Modify `.github/workflows/issue-to-pr.yml` to handle shortnews issues.

Add a new section to handle the shortnews label (follow existing pattern for news).

#### Phase 4: Testing (Day 4)

**11. Create Sample Content**

Create 3-5 sample short news items for testing:

```bash
mkdir -p content/shortnews/2024-12-10-test-defense
mkdir -p content/shortnews/2024-12-08-test-visit
mkdir -p content/shortnews/2024-12-05-test-award
```

Each with `index.en.md` and `index.tr.md` following the format in SHORTNEWS_EXAMPLES.md.

**12. Local Testing**

```bash
# Install Hugo if not already installed
# See .devcontainer/Dockerfile for Hugo version

# Start development server
hugo server --disableFastRender

# Open http://localhost:1313
# Check:
# - Short news appears in chosen layout
# - Responsive design works (test mobile)
# - Links work correctly
# - Markdown renders properly
# - Both EN and TR versions work
```

**13. Accessibility Testing**

- Keyboard navigation works
- Screen reader compatible
- Proper semantic HTML
- Sufficient color contrast
- Touch targets adequate on mobile

**14. Cross-browser Testing**

- Chrome/Edge
- Firefox
- Safari
- Mobile browsers (iOS Safari, Android Chrome)

#### Phase 5: Content Migration (Day 5)

**15. Migrate Initial Content**

Create 10-15 short news items from recent announcements:
- Recent PhD defenses
- Recent awards
- Recent visits
- Recent publications
- Recent events

**16. Documentation Updates**

Update these files:
- `CONTRIBUTING.md` - Add section on short news
- `README.md` - Mention short news feature
- Create content guidelines document if needed

#### Phase 6: Deployment (Day 6-7)

**17. Pre-deployment Checklist**

- [ ] All templates created and tested
- [ ] CSS styling complete and responsive
- [ ] Configuration settings finalized
- [ ] i18n translations added
- [ ] Issue template created
- [ ] Workflow updated (if needed)
- [ ] Sample content created
- [ ] Documentation updated
- [ ] Accessibility validated
- [ ] Cross-browser tested
- [ ] Stakeholder approval received

**18. Deploy to Production**

```bash
# Commit all changes
git add .
git commit -m "Add short news feature"

# Push to main branch
git push origin main

# GitHub Actions will automatically deploy
# Monitor: https://github.com/bouncmpe/bouncmpe.github.io/actions
```

**19. Post-deployment**

- Verify on live site: https://bouncmpe.github.io
- Test issue template by creating a test short news item
- Monitor for any errors or issues
- Gather initial feedback

#### Phase 7: Launch & Monitor (Week 2)

**20. Announce Feature**

- Email department members
- Post on social media
- Add to newsletter
- Update training materials

**21. Monitor Usage**

- Track number of submissions
- Monitor issue template usage
- Gather user feedback
- Check for any bugs or issues

**22. Iterate**

- Adjust display count if needed
- Fine-tune styling based on feedback
- Update guidelines based on usage
- Add any missing features

---

## Troubleshooting

### Short news not appearing

**Check:**
1. Is `shortnews.enabled: true` in `params.yml`?
2. Do short news files exist in `content/shortnews/`?
3. Is the partial included in `layouts/index.html`?
4. Are the frontmatter fields correct (`type: shortnews`)?

### Styling looks broken

**Check:**
1. Is CSS file included in build?
2. Are Bootstrap classes available?
3. Browser caching issue? (Hard refresh: Ctrl+Shift+R)
4. Check browser console for CSS errors

### Markdown not rendering

**Check:**
1. Hugo version supports markdown in content
2. Content is in `.Content` not `.RawContent`
3. Goldmark markdown settings in `config/_default/markup.yml`

### Mobile layout issues

**Check:**
1. Viewport meta tag in head
2. Responsive breakpoints in CSS
3. Bootstrap grid classes correct
4. Test on actual device, not just browser devtools

### Issue template not working

**Check:**
1. YAML syntax is valid
2. File is in correct location: `.github/ISSUE_TEMPLATE/`
3. Labels exist in repository
4. Workflow has correct permissions

---

## Quick Reference

### File Locations

```
Repository Root
├── content/shortnews/              # Content files
│   ├── _index.en.md
│   ├── _index.tr.md
│   └── YYYY-MM-DD-slug/
│       ├── index.en.md
│       └── index.tr.md
├── layouts/
│   ├── index.html                  # Homepage (modify)
│   └── partials/bouncmpe/
│       ├── shortnews.html          # Main partial (create)
│       └── shortnews-item.html     # Item partial (create)
├── config/_default/
│   ├── params.yml                  # Configuration (modify)
│   └── markup.yml                  # Markdown settings
├── i18n/
│   ├── en.yaml                     # Translations (modify)
│   └── tr.yaml                     # Translations (modify)
├── assets/scss/
│   └── components/
│       └── _shortnews.scss         # Styling (create)
└── .github/ISSUE_TEMPLATE/
    └── shortnews.yml               # Issue template (create)
```

### Key Commands

```bash
# Start development server
hugo server --disableFastRender

# Build for production
hugo --minify

# Check Hugo version
hugo version

# Validate content
hugo list all

# Run locally with draft content
hugo server -D
```

### Support & Help

- **Documentation**: See full requirements in `SHORTNEWS_REQUIREMENTS.md`
- **Examples**: See `SHORTNEWS_EXAMPLES.md` for code samples
- **Issues**: Create GitHub issue for bugs or questions
- **Contact**: @doganulus for implementation questions

---

**Document Version**: 1.0
**Last Updated**: December 12, 2024
