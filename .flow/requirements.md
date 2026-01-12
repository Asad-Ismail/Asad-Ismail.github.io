# Project Requirements: Senior ML Engineer Portfolio Website

## 1. Project Overview

**Title:** Senior Machine Learning Engineer Portfolio Website (GitHub Pages)

**Objective:** Create a world-class personal website that represents the author as a Senior/Staff-level ML Engineer, passes LLM-based evaluation with 10/10 acceptance score, and demonstrates real ML systems thinking competitive with engineers at OpenAI, DeepMind, Meta, Anthropic, Google Brain.

**Current Status:** Phase 1 Complete - Header/navigation integration and monochromatic design system implemented (8/10 rating).

---

## 2. Technical Architecture

### 2.1 Technology Stack
- **Static Site Generator:** Hugo 0.131.0
- **Hosting:** GitHub Pages (auto-deploy from `master` branch)
- **Theme:** `hugo-coder` (git submodule, extended via SCSS overrides)
- **Styling:** Custom SCSS with CSS design tokens
- **Fonts:**
  - Display: `JetBrains Mono` (headings, code-like elements)
  - Body: `IBM Plex Sans` (readable, professional)
  - Mono: `Fira Code` (code blocks)
- **Icons:** Font Awesome 6 (free tier)

### 2.2 Design Philosophy
**Core Principle:** Monochromatic minimal eye strain for developers

- **Inspiration:** GitHub dark mode, VS Code, Vercel, Stripe
- **Color Palette:** Single hue (#0d1117 base) with subtle variations
- **Typography:** Developer-friendly sizes (15px body - optimal like GitHub)
- **Visual Hierarchy:** Subtle borders, minimal backgrounds, clear spacing
- **No AI Slop:** No gradients, glows, animations for effect, generic aesthetics

### 2.3 File Structure

```
/home/asad/dev/asad-ismail.github.io/
├── assets/scss/
│   └── custom.scss          # Main stylesheet (design tokens, overrides)
├── content/
│   ├── posts/               # Blog posts (markdown)
│   ├── about.md             # About page
│   ├── projects.md          # Projects page
│   └── contact.md           # Contact page (with avatar)
├── layouts/
│   ├── partials/
│   │   └── home.html        # Custom homepage layout
│   └── _default/
│       └── list.html        # Blog listing with summaries
├── static/
│   └── img/                 # Images, favicon
├── themes/hugo-coder/       # Git submodule (base theme)
├── .flow/                   # Flow task management
├── hugo.toml                # Site configuration
└── CLAUDE.md                # Project documentation
```

---

## 3. Design System Specifications

### 3.1 Design Tokens (CSS Custom Properties)

Located in `assets/scss/custom.scss:9-68`

**Spacing (4px grid):**
```scss
--space-1: 0.25rem;   // 4px
--space-2: 0.5rem;    // 8px
--space-3: 0.75rem;   // 12px
--space-4: 1rem;      // 16px
--space-6: 1.5rem;    // 24px
--space-8: 2rem;      // 32px
--space-12: 3rem;     // 48px
```

**Typography (Developer-friendly sizes):**
```scss
--text-xs: 0.8125rem;   // 13px - small labels
--text-sm: 0.875rem;    // 14px - metadata, code
--text-base: 0.9375rem; // 15px - body text (optimal)
--text-md: 1rem;        // 16px - emphasis
--text-lg: 1.125rem;    // 18px - lead text
--text-xl: 1.25rem;     // 20px - H3
--text-2xl: 1.5rem;     // 24px - H2
--text-3xl: 2rem;       // 32px - H1
--text-4xl: 2.5rem;     // 40px - Hero
```

**Color Palette (Monochromatic Dark Mode):**
```scss
// Backgrounds
--bg-primary: #0d1117;      // Main background (GitHub dark)
--bg-secondary: #161b22;    // Cards, sections
--bg-tertiary: #21262d;     // Inputs, hover states

// Foreground
--fg-primary: #c9d1d9;      // Primary text
--fg-secondary: #8b949e;    // Secondary text
--fg-muted: #6e7681;        // Muted text

// Borders
--border-default: #30363d;  // Default borders
--border-subtle: #21262d;   // Subtle borders

// Single Accent ( sparing use)
--accent: #58a6ff;          // GitHub blue
--accent-dim: rgba(88, 166, 255, 0.15);
```

### 3.2 Navigation Design

**Current Implementation (assets/scss/custom.scss:236-381):**

- **Background:** Same as page body (`--bg-primary`) with `!important` to override theme
- **Border:** Very subtle `--border-subtle` bottom border for hierarchy
- **Position:** `position: sticky; top: 0; z-index: 100` for persistent access
- **Links:** White text with 0.9 opacity, hover shows `--bg-tertiary` background
- **Active State:** Opacity 1.0 with `--bg-tertiary` background
- **Responsive:** Mobile dropdown with card-like styling

**Design Rationale:** Seamless integration with content while maintaining clear navigation hierarchy. No floating elements, no harsh separations.

---

## 4. Page Requirements

### 4.1 Homepage (/)

**File:** `layouts/partials/home.html`

**Components:**
1. **Hero Section:**
   - Large heading: "Asad Ismail"
   - Tagline: "Senior ML Engineer | MLOps | Computer Vision | LLMs"
   - Subheading: "Building intelligent systems that bridge the gap between research and production"
   - CTA Buttons: "Read Blog", "View Projects", "Get in Touch"

2. **Recent Posts Section:**
   - Section title with styling: `┌─ Recent Posts`
   - Blog grid: 6 most recent posts
   - Card design with date, title, summary
   - Hover: Border color change to `--fg-muted`

**Content Strategy:** No avatar on homepage (moved to contact page). Focus on expertise and recent work.

### 4.2 Blog Listing (/posts/)

**File:** Uses `layouts/_default/list.html` override

**Requirements:**
- Grid layout: `repeat(auto-fill, minmax(360px, 1fr))`
- Each card shows: Date, title, summary
- Consistent with homepage blog cards
- Pagination if more than 20 posts

### 4.3 Individual Blog Post (/posts/slug/)

**File:** Theme default template

**Requirements:**
- Full markdown rendering
- Syntax highlighting (GitHub Dark style)
- Metadata: Date, reading time, tags
- Related posts section
- Back to blog link

### 4.4 Projects Page (/projects/)

**File:** `content/projects.md`

**Requirements:**
- Grid of project cards
- Each card: Title, description, tech stack badges, links
- Tech stack: Monospace font, small badges with `--bg-tertiary` background
- Live demo and GitHub repo links where applicable

### 4.5 About Page (/about/)

**File:** `content/about.md`

**Requirements:**
- Professional bio focusing on ML systems thinking
- Technical depth: Specific technologies, architectures, patterns
- NOT generic fluff - demonstrate expertise
- Sections: Background, Expertise, Philosophy, Contact CTA

### 4.6 Contact Page (/contact/)

**File:** `content/contact.md`

**Requirements:**
- Avatar: Gravatar image (160px circular)
- Contact methods: Email, social links
- Social icons: GitHub, LinkedIn, Email, Substack, YouTube
- Collaboration availability statement
- HTML structure: `<div class="contact-wrapper">` with avatar + info sections

---

## 5. Content Guidelines

### 5.1 Blog Post Requirements

**Front Matter (archetypes/default.md):**
```toml
+++
title = 'Post Title'
date = 2026-01-12
description = 'Brief summary for SEO and social sharing'
tags = ['tag1', 'tag2']
categories = ['category']
draft = false
+++
```

**Content Standards:**
- **Technical Depth:** Go beyond surface-level tutorials
- **Systems Thinking:** Discuss trade-offs, architecture, production considerations
- **Code Examples:** Real, production-like code (not toy examples)
- **Length:** 1500-3000 words typically
- **Structure:** Clear headings, code blocks, diagrams where helpful
- **Tone:** Professional, authoritative but approachable

**Topics to Cover:**
- MLOps pipeline design and implementation
- Model deployment strategies (serving, batching, monitoring)
- Computer Vision system architecture
- LLM application development (RAG, fine-tuning, evaluation)
- Performance optimization (latency, throughput, cost)
- Data engineering for ML (feature stores, data quality)
- ML infrastructure (Kubernetes, cloud platforms, CI/CD)

### 5.2 Projects Content

**Each Project Should Include:**
- **Problem Statement:** What real problem does this solve?
- **Technical Approach:** Architecture, key technologies, trade-offs
- **Challenges:** Difficult problems encountered and solutions
- **Results:** Metrics, learnings, impact
- **Links:** Live demo, GitHub repo, case study

### 5.3 About Page Content

**Sections:**
1. **Professional Summary:** 2-3 sentences establishing seniority
2. **Technical Expertise:** Bullet points of specific competencies
3. **Selected Experience:** Key roles with impact
4. **Philosophy:** Approach to ML engineering (systems-thinking, pragmatism)
5. **Publications/Talks:** If applicable
6. **Contact CTA:** Clear call-to-action

---

## 6. Evaluation Protocol

### 6.1 Automated Evaluation Loop (Ralph's Task)

For each iteration, the agent MUST:

1. **Start Hugo Server:**
   ```bash
   hugo server -D > /tmp/hugo-server.log 2>&1 &
   echo $! > /tmp/hugo.pid
   ```

2. **Open Chrome DevTools:**
   - Navigate to `http://127.0.0.1:1313/`

3. **Visit All Pages:**
   - Homepage (/)
   - Blog listing (/posts/)
   - At least 2 individual blog posts
   - Projects (/projects/)
   - About (/about/)
   - Contact (/contact/)

4. **Take Screenshots:**
   - Full viewport for each page
   - Save to `/tmp/screenshot-{page-name}.png`

5. **AI Image Analysis:**
   - Use `mcp__zai-mcp-server__ui_to_artifact` with `output_type: "description"`
   - Prompt for critique focusing on:
     - Visual polish (1-10)
     - Typography hierarchy (1-10)
     - Color consistency (1-10)
     - Layout quality (1-10)
     - Overall professional appearance (1-10)
   - Identify specific improvements needed

6. **Apply Improvements:**
   - Edit `assets/scss/custom.scss` for styling issues
   - Edit layout files for structure issues
   - Edit content files for content issues

7. **Repeat** until all pages score ≥ 9.5/10

### 6.2 Manual Quality Checklist

Before considering complete, verify:

**Visual Quality:**
- [ ] No default theme elements visible
- [ ] Consistent spacing (8px grid)
- [ ] Typography hierarchy is clear
- [ ] No visual clutter or amateur elements
- [ ] Dark mode is easy on eyes (not too dark, not too light)
- [ ] Navigation is clearly visible
- [ ] All interactive elements have hover states
- [ ] No broken layouts on any screen size

**Content Quality:**
- [ ] Homepage establishes expertise immediately
- [ ] Blog posts show technical depth
- [ ] Projects demonstrate real systems thinking
- [ ] About page is professional and specific
- [ ] Contact page is functional
- [ ] No placeholder content

**Technical Quality:**
- [ ] All links work
- [ ] Images load properly
- [ ] No console errors
- [ ] Page load time < 2s
- [ ] Mobile responsive (test at 375px width)
- [ ] SEO meta tags present

---

## 7. Development Workflow

### 7.1 Local Development

```bash
# Start development server
hugo server -D

# Create new blog post
hugo new posts/my-new-post.md

# Build for production
hugo --minify

# Test production build locally
hugo server --renderToDisk
```

### 7.2 Deployment

- **Automatic:** Push to `master` branch triggers GitHub Actions
- **Build command:** `hugo --minify`
- **Publish directory:** `./public`
- **Submodules included:** Yes (theme)

### 7.3 Making Changes

1. **Styling Changes:** Edit `assets/scss/custom.scss`
2. **Layout Changes:** Create/edit files in `layouts/`
3. **Content Changes:** Edit files in `content/`
4. **Configuration:** Edit `hugo.toml`
5. **Test:** Refresh browser (Ctrl+Shift+R for hard reload)
6. **Commit:** `git add && git commit -m "description"`
7. **Deploy:** `git push origin master`

### 7.4 Troubleshooting

**Changes not appearing:**
- Hugo may cache compiled assets: `touch assets/scss/custom.scss` to force rebuild
- Browser cache: Use Ctrl+Shift+R for hard reload
- Check `/tmp/hugo-server.log` for errors

**Layout not working:**
- Verify file path matches Hugo layout lookup rules
- Check `hugo.toml` has `unsafe = true` for Goldmark if using HTML
- Clear Hugo cache: `rm -rf resources/`

**Submodule issues:**
```bash
git submodule update --init --recursive
git submodule update --remote --merge
```

---

## 8. Target Audience Evaluation

The website should appeal to:

**Primary (Senior/Staff Level):**
- ML engineers at top companies (OpenAI, DeepMind, Meta, Anthropic, Google Brain)
- Staff/Principal engineers evaluating technical depth
- AI researchers looking for practical engineering insights
- Hiring managers for senior ML roles

**Secondary:**
- Technical founders building ML-powered products
- Applied research engineers transitioning to production
- Advanced ML practitioners seeking expertise

**Red Flags to Avoid:**
- Tutorial-style content ("Hello World" ML examples)
- Generic ML buzzwords without substance
- Over-promising without technical backing
- Amateur visual design
- Lack of systems thinking

**Green Flags to Demonstrate:**
- Real production experience
- Understanding of trade-offs
- Infrastructure and scaling knowledge
- Thoughtful architecture decisions
- Clear communication of complex topics

---

## 9. Success Criteria

### 9.1 Quantitative Metrics

- **AI Evaluation Score:** ≥ 9.5/10 on all pages
- **Page Load Time:** < 2 seconds (Lighthouse)
- **Mobile Responsive:** Pass all breakpoints (375px, 768px, 1024px, 1440px)
- **Accessibility:** WCAG AA compliant (contrast ratios, semantic HTML)
- **SEO:** Meta tags, sitemap, structured data

### 9.2 Qualitative Metrics

- **Immediate Credibility:** Visitor recognizes senior expertise within 5 seconds
- **Technical Depth:** Content demonstrates systems-level thinking
- **Visual Polish:** Design feels intentional and professional
- **Differentiation:** Clearly stands out from junior/engineer portfolios
- **Engagement:** Visitors want to connect or read more

### 9.3 Competitive Benchmark

The portfolio should be competitive with:
- Top ML engineers' personal sites
- Technical fellows' blogs (e.g., from Google, Meta)
- Principal engineers' public profiles
- Well-known ML practitioners' websites

---

## 10. Known Issues & Future Work

### 10.1 Current State (January 2026)

**Completed:**
- ✅ Monochromatic design system (GitHub-inspired)
- ✅ Header/navigation integration (8/10 rating)
- ✅ Homepage with hero + blog grid
- ✅ Contact page with avatar
- ✅ Typography sizing optimization
- ✅ Blog card hover states
- ✅ Responsive grid layouts

**In Progress:**
- 🔄 Header background color matching (minor difference remains)
- 🔄 Blog content creation (need more technical depth posts)

**Future Improvements:**
- Search functionality
- RSS feed optimization
- Syntax highlighting customization
- Project case studies
- Speaking engagements section
- Publications/papers section

### 10.2 Technical Debt

- Theme customization via SCSS overrides (not ideal, should fork theme for major changes)
- No automated testing for layout regressions
- Limited accessibility testing (should audit with axe-core)
- No performance monitoring (should add Core Web Vitals tracking)

---

## 11. Appendix

### 11.1 Key Commands Reference

```bash
# Development
hugo server -D                    # Start dev server with drafts
hugo new posts/title.md          # Create new post
hugo --minify                    # Production build

# Git
git add . && git commit -m "msg" # Commit changes
git push origin master           # Deploy to GitHub Pages

# Troubleshooting
touch assets/scss/custom.scss    # Force Hugo rebuild
rm -rf resources/                # Clear Hugo cache
```

### 11.2 File Locations

| Purpose | File Path |
|---------|-----------|
| Main styles | `assets/scss/custom.scss` |
| Homepage layout | `layouts/partials/home.html` |
| Blog listing | `layouts/_default/list.html` |
| Site config | `hugo.toml` |
| Contact page | `content/contact.md` |
| About page | `content/about.md` |
| Projects page | `content/projects.md` |
| Blog posts | `content/posts/*.md` |

### 11.3 Design Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01-11 | Monochromatic dark theme | User feedback: "background should be monochromatic for minimal eye strain" |
| 2026-01-11 | 15px body text | User feedback: "fonts look too big" - optimal for developers like GitHub |
| 2026-01-12 | Header integration | User request: "header seems very separate from rest of website" |
| 2026-01-12 | Remove avatar from homepage | User request: "nobody wants to see my face in first page" |
| 2026-01-12 | Blog grid on homepage | User request: "homepage we can have blogs directly" |

---

## 12. Ralph's Autonomous Loop Instructions

When Ralph processes this requirements file, it should:

1. **Read Current State:**
   - Read `CLAUDE.md` for project context
   - Read `assets/scss/custom.scss` for current design system
   - Read all page content files
   - Take screenshots of current state

2. **Evaluate Each Page:**
   - Use AI image analysis to rate each page
   - Compare against success criteria in Section 9
   - Identify gaps and improvement opportunities

3. **Prioritize Improvements:**
   - Fix visual issues (CSS) first
   - Fix content issues second
   - Fix technical issues third
   - Always aim for 10/10 on each change

4. **Apply Changes:**
   - Edit appropriate files (SCSS, layouts, content)
   - Test locally (force rebuild with `touch`)
   - Take new screenshots
   - Verify improvement

5. **Iterate:**
   - Continue until all pages score ≥ 9.5/10
   - Document changes in commit messages
   - Update this requirements file if scope changes

6. **Quality Gate:**
   - Before marking task complete, manually verify:
     - All pages load without errors
     - No visual regressions
     - Mobile responsive
     - Content is accurate and professional
     - Links work correctly

---

**Document Version:** 2.0
**Last Updated:** 2026-01-12
**Status:** Active - Ralph should process and iterate
