# Short News Feature - Examples and Use Cases

## Sample Short News Items

### Example 1: PhD Defense
```markdown
---
type: shortnews
date: 2024-12-10
---

**Dr. Mehmet Yılmaz** successfully defended his PhD thesis on "Deep Learning for Natural Language Processing" on December 10, 2024. Congratulations!
```

### Example 2: Faculty Visit
```markdown
---
type: shortnews
date: 2024-12-08
---

Prof. Sarah Johnson from *Stanford University* visited our department and delivered a seminar on quantum computing applications in cryptography.
```

### Example 3: Award Announcement
```markdown
---
type: shortnews
date: 2024-12-05
---

Congratulations to our undergraduate student **Ayşe Demir** for winning the Best Paper Award at the [National Software Engineering Conference](https://example.com)!
```

### Example 4: Collaboration
```markdown
---
type: shortnews
date: 2024-12-01
---

Our department established a new research collaboration with *ETH Zürich* focusing on sustainable computing and green AI technologies.
```

### Example 5: Conference Participation
```markdown
---
type: shortnews
date: 2024-11-28
---

Faculty members Dr. Can Özkan and Dr. Elif Yıldız presented papers at [NeurIPS 2024](https://neurips.cc/) in Vancouver, Canada.
```

### Example 6: Workshop
```markdown
---
type: shortnews
date: 2024-11-25
---

Registration is now open for our *Winter School on Machine Learning* to be held January 15-20, 2025. [Apply here](https://example.com/apply).
```

### Example 7: Publication
```markdown
---
type: shortnews
date: 2024-11-20
---

**New publication**: "Efficient Graph Neural Networks for Large-Scale Graphs" accepted to *ICML 2025* by our research team.
```

### Example 8: Guest Lecture
```markdown
---
type: shortnews
date: 2024-11-15
---

Dr. Ahmed Hassan from Google AI will give a guest lecture on "Large Language Models in Production" on December 20 at 2:00 PM.
```

## Layout Mockups

### Option A: Sidebar Layout (Recommended)

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPARTMENT HOMEPAGE                       │
├───────────────────────────────────┬─────────────────────────┤
│                                   │  RECENT UPDATES         │
│   FEATURED STORIES CAROUSEL       │  ═══════════════        │
│   [Large Image Slider]            │                         │
│                                   │  Dec 10, 2024           │
│                                   │  Dr. Mehmet Yılmaz      │
│                                   │  successfully defended  │
│                                   │  his PhD thesis on...   │
├───────────────────────────────────┤                         │
│                                   │  ─────────────────────  │
│   RECENT STORIES                  │                         │
│   ┌─────┐ ┌─────┐ ┌─────┐        │  Dec 8, 2024           │
│   │ IMG │ │ IMG │ │ IMG │        │  Prof. Sarah Johnson   │
│   │     │ │     │ │     │        │  from Stanford visited │
│   └─────┘ └─────┘ └─────┘        │  and delivered...      │
│    Story   Story   Story          │                         │
│                                   │  ─────────────────────  │
│   ┌─────┐ ┌─────┐ ┌─────┐        │                         │
│   │ IMG │ │ IMG │ │ IMG │        │  Dec 5, 2024           │
│   │     │ │     │ │     │        │  Congratulations to    │
│   └─────┘ └─────┘ └─────┘        │  Ayşe Demir for        │
│    Story   Story   Story          │  winning the Best...   │
│                                   │                         │
│                                   │  ─────────────────────  │
│                                   │                         │
│                                   │  [View All Updates →]  │
└───────────────────────────────────┴─────────────────────────┘
```

### Option B: Dedicated Section Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPARTMENT HOMEPAGE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   FEATURED STORIES CAROUSEL                                 │
│   [Large Full-Width Image Slider]                           │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│   RECENT UPDATES                                            │
│   ═════════════════════════════════════════════════════════ │
│                                                              │
│   Dec 10  │  Dec 8    │  Dec 5                              │
│   Dr. M   │  Prof. S  │  Congrats                           │
│   defend  │  Johnson  │  to Ayşe                            │
│   thesis  │  visited  │  for award                          │
│                                                              │
│   Dec 1   │  Nov 28   │  Nov 25                             │
│   New     │  NeurIPS  │  Winter                             │
│   collab  │  papers   │  School                             │
│   w/ ETH  │  present  │  open                               │
│                                                              │
│                                   [More Updates →]           │
├─────────────────────────────────────────────────────────────┤
│   RECENT STORIES                                            │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐                     │
│   │  IMAGE  │ │  IMAGE  │ │  IMAGE  │                     │
│   │         │ │         │ │         │                     │
│   └─────────┘ └─────────┘ └─────────┘                     │
│     Story       Story       Story                           │
└─────────────────────────────────────────────────────────────┘
```

### Option C: Timeline Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPARTMENT HOMEPAGE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────────────────────────────────────────┐      │
│   │                                                  │      │
│   │   FEATURED STORIES CAROUSEL                     │      │
│   │   [Large Image Slider]                          │      │
│   │                                                  │      │
│   └─────────────────────────────────────────────────┘      │
│                                                              │
├───┬──────────────────────────────────────────────────────────┤
│ R │                                                          │
│ E │  ┌─────┐ ┌─────┐ ┌─────┐                              │
│ C │  │ IMG │ │ IMG │ │ IMG │    RECENT STORIES            │
│ E │  │     │ │     │ │     │                              │
│ N │  └─────┘ └─────┘ └─────┘                              │
│ T │   Story   Story   Story                                │
│   │                                                          │
│ U │  ┌─────┐ ┌─────┐ ┌─────┐                              │
│ P │  │ IMG │ │ IMG │ │ IMG │                              │
│ D │  │     │ │     │ │     │                              │
│ A │  └─────┘ └─────┘ └─────┘                              │
│ T │   Story   Story   Story                                │
│ E │                                                          │
│ S │                                                          │
│   │                                                          │
│ • │                                                          │
│ 12/10                                                        │
│ Dr. M                                                        │
│ defend                                                       │
│   │                                                          │
│ • │                                                          │
│ 12/8                                                         │
│ Prof. S                                                      │
│ visited                                                      │
│   │                                                          │
│ • │                                                          │
│ 12/5                                                         │
│ Award                                                        │
│ winner                                                       │
│   │                                                          │
│ ↓ │                                                          │
└───┴──────────────────────────────────────────────────────────┘
```

## File Structure Examples

### Directory Structure
```
content/
├── news/                          # Full stories (existing)
│   ├── 2024-12-01-ai-research/
│   │   ├── index.en.md
│   │   ├── index.tr.md
│   │   └── cover.jpg
│   └── _index.en.md
│
└── shortnews/                     # Short news (new)
    ├── 2024-12-10-yilmaz-defense/
    │   ├── index.en.md
    │   └── index.tr.md
    ├── 2024-12-08-johnson-visit/
    │   ├── index.en.md
    │   └── index.tr.md
    ├── 2024-12-05-demir-award/
    │   ├── index.en.md
    │   └── index.tr.md
    └── _index.en.md
```

### Full Example: index.en.md
```markdown
---
type: shortnews
date: 2024-12-10
---

**Dr. Mehmet Yılmaz** successfully defended his PhD thesis titled "Deep Learning Approaches for Turkish Natural Language Processing" on December 10, 2024. [Read more](/news/2024-12-10-yilmaz-phd-defense/).
```

### Full Example: index.tr.md
```markdown
---
type: shortnews
date: 2024-12-10
---

**Dr. Mehmet Yılmaz**, "Türkçe Doğal Dil İşleme için Derin Öğrenme Yaklaşımları" başlıklı doktora tezini 10 Aralık 2024 tarihinde başarıyla savundu. [Devamını oku](/tr/news/2024-12-10-yilmaz-phd-defense/).
```

## Hugo Template Examples

### Short News Partial (shortnews.html)
```html
{{ $shortnews := where site.RegularPages "Section" "shortnews" }}
{{ $shortnews = $shortnews.ByDate.Reverse }}

{{ if $shortnews }}
<section id="shortnews" class="shortnews-container">
  <h4 class="shortnews-title">{{ i18n "recent-updates" | title }}</h4>
  
  <div class="shortnews-list">
    {{ range first 10 $shortnews }}
      {{ partial "bouncmpe/shortnews-item.html" . }}
    {{ end }}
  </div>
  
  <div class="shortnews-footer">
    <a href="/shortnews/" class="btn btn-sm btn-outline-primary">
      {{ i18n "more-updates" | title }} →
    </a>
  </div>
</section>
{{ end }}
```

### Short News Item Partial (shortnews-item.html)
```html
<article class="shortnews-item">
  <time class="shortnews-date" datetime="{{ .Date.Format "2006-01-02" }}">
    {{ .Date.Format "Jan 2, 2006" }}
  </time>
  <div class="shortnews-content">
    {{ .Content }}
  </div>
</article>
```

### CSS Styling Example
```css
.shortnews-container {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.shortnews-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #1e4a8b;
  border-bottom: 2px solid #1e4a8b;
  padding-bottom: 0.5rem;
}

.shortnews-list {
  max-height: 500px;
  overflow-y: auto;
}

.shortnews-item {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #dee2e6;
}

.shortnews-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.shortnews-date {
  display: block;
  font-size: 0.85rem;
  color: #6c757d;
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.shortnews-content {
  font-size: 0.95rem;
  line-height: 1.5;
  color: #212529;
}

.shortnews-content p {
  margin: 0;
}

.shortnews-content strong {
  color: #1e4a8b;
}

.shortnews-content a {
  color: #1e4a8b;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}

.shortnews-content a:hover {
  border-bottom-color: #1e4a8b;
}

.shortnews-footer {
  margin-top: 1rem;
  text-align: center;
}

/* Responsive adjustments */
@media (max-width: 767px) {
  .shortnews-container {
    padding: 1rem;
  }
  
  .shortnews-list {
    max-height: 400px;
  }
}
```

## Issue Template Example

### .github/ISSUE_TEMPLATE/shortnews.yml
```yaml
name: Short News Submission
description: Submit a brief news item (1-2 sentences) for the website
title: "[SHORT NEWS] <Insert brief title>"
labels: ["auto-md", "shortnews"]
body:
  - type: input
    id: date
    attributes:
      label: "Date (YYYY-MM-DD)"
      placeholder: "YYYY-MM-DD"
    validations:
      required: true

  - type: textarea
    id: content_en
    attributes:
      label: "Content (English)"
      description: "1-2 sentences. Markdown formatting supported (bold, italic, links)."
      placeholder: "Dr. **John Smith** successfully defended his PhD thesis on distributed systems."
    validations:
      required: true

  - type: textarea
    id: content_tr
    attributes:
      label: "İçerik (Türkçe)"
      description: "1-2 cümle. Markdown biçimlendirmesi desteklenir (kalın, italik, bağlantılar)."
      placeholder: "Dr. **Ahmet Yılmaz** dağıtık sistemler üzerine doktora tezini başarıyla savundu."
    validations:
      required: true

  - type: input
    id: related_story
    attributes:
      label: "Related Full Story (optional)"
      description: "If this short news has a corresponding full story, provide the link"
      placeholder: "https://bouncmpe.github.io/news/2024-12-10-smith-defense/"
    validations:
      required: false

  - type: markdown
    attributes:
      value: |
        ## Markdown Formatting Tips
        - **Bold text**: `**text**`
        - *Italic text*: `*text*`
        - [Link](URL): `[text](https://example.com)`
        - Keep it brief: 1-2 sentences maximum
```

## Content Calendar Example

### Monthly Short News Planning

**December 2024**
- Dec 1: New collaboration with ETH Zürich
- Dec 5: Student award at conference
- Dec 8: Faculty visit from Stanford
- Dec 10: PhD defense - Yılmaz
- Dec 12: Paper acceptance at ICML
- Dec 15: Guest lecture announcement
- Dec 18: Workshop registration opening
- Dec 20: End of semester message
- Dec 22: Holiday closure announcement
- Dec 27: New year greetings

**Target**: 8-12 short news items per month

## Comparison: Short News vs Full Story

### Same Event - Two Formats

#### As Short News:
```markdown
---
type: shortnews
date: 2024-12-10
---

**Dr. Mehmet Yılmaz** successfully defended his PhD thesis on "Deep Learning for Turkish NLP" on December 10, 2024. [Read more](/news/2024-12-10-yilmaz-defense/).
```

#### As Full Story:
```markdown
---
type: news
title: Congratulations Dr. Mehmet Yılmaz
date: 2024-12-10
featured: true
thumbnail: uploads/yilmaz-defense.jpg
---

We are pleased to announce that Mehmet Yılmaz successfully defended his PhD 
thesis on December 10, 2024. His dissertation, titled "Deep Learning Approaches 
for Turkish Natural Language Processing," presents novel architectures for 
handling morphologically rich languages.

The defense committee consisted of Prof. Dr. Ayşe Kara (advisor), Prof. Dr. 
Can Özkan (co-advisor), and external members from MIT and ETH Zürich. The 
committee unanimously approved the thesis with distinction.

Mehmet's research has resulted in 5 publications in top-tier conferences 
including ACL, EMNLP, and NAACL. His work on transformer models for Turkish 
has been widely cited and adopted by the research community. He will continue 
his research as a postdoctoral researcher at Stanford University.

Congratulations Dr. Yılmaz!
```

## Migration Strategy

### Phase 1: Recent Announcements (0-3 months old)
Convert recent short announcements from:
- Email newsletters
- Social media posts
- Department announcements
- Seminar series updates

### Phase 2: Selective Historical Items (3-6 months old)
Migrate significant events:
- PhD defenses
- Major awards
- Important visits
- Key publications

### Phase 3: Ongoing Creation
- Establish regular workflow
- Train content creators
- Monitor and adjust

## Analytics and Success Metrics

### Quantitative Metrics
- **Publication Rate**: Target 8-12 short news items per month
- **Response Time**: Short news published within 24 hours of event
- **Coverage**: 80% of eligible events covered
- **Engagement**: Track clicks on links within short news

### Qualitative Metrics
- **Content Quality**: Clear, concise, well-formatted
- **Relevance**: Appropriate use of short news vs full stories
- **Timeliness**: News published promptly
- **Community Feedback**: Positive reception from faculty/students

## Maintenance and Curation

### Regular Tasks
- **Weekly**: Review and approve submitted short news
- **Monthly**: Archive very old items (optional)
- **Quarterly**: Review usage patterns and adjust display count
- **Yearly**: Major content audit and cleanup

### Quality Control
- Check for typos and grammar
- Verify links work correctly
- Ensure both EN and TR versions exist
- Confirm appropriate length (1-2 sentences)
- Validate markdown formatting renders correctly

## Conclusion

These examples demonstrate how the short news feature will work in practice. The key characteristics are:

1. **Brevity**: Each item is 1-2 sentences, under 50 words
2. **Rich formatting**: Markdown support for emphasis and links
3. **Dense display**: Compact, list-like presentation
4. **Quick updates**: Fast to create and publish
5. **Bilingual**: Both English and Turkish versions

The feature complements rather than replaces full stories, providing a lightweight way to keep the community informed about smaller updates and achievements.
