# Reposition GitHub Pages as ML Engineer Portfolio

## Overview

Transform the current GitHub Pages site from a placeholder personal website into a professional machine learning engineer portfolio. The site will showcase technical blog content, integrate embedded content from Substack and YouTube, and provide clear contact mechanisms for collaboration opportunities.

**Current State:**
- Hugo 0.131.0 with hugo-coder theme
- Generic placeholder content ("John Doe", placeholder job info)
- No contact functionality
- No external content integration
- Social links point to non-existent accounts
- One draft blog post (`MLModelDeployment.md`)

**Target State:**
- Professional ML engineer portfolio with authentic content
- Embedded YouTube videos and Substack content previews
- Working contact page with mailto: link
- Updated social links to real accounts
- Published technical blog posts
- SEO-optimized with proper metadata
- Automated deployment via GitHub Actions

## Scope

### In Scope
1. **Content Updates**
   - Replace all placeholder text with real information
   - Update About page with authentic experience and skills
   - Complete and publish draft ML Model Deployment blog post (needs work)
   - Create 2-3 new technical blog posts (topics decided during implementation)
   - Create dedicated Projects page showcasing ML work

2. **External Content Integration**
   - Create dedicated "Content" page for YouTube and Substack integration
   - Embed 6 YouTube videos from AIMLArchives channel
   - Add Substack newsletter signup form and latest posts preview
   - Aggregate external platform links on Content page

3. **Contact & Collaboration**
   - Create Contact page with mailto: link to asadismaeel@gmail.com
   - Add collaboration availability (consulting, open source, speaking)
   - No full-time roles (not looking for opportunities)

4. **Configuration & SEO**
   - Update all social media links with real URLs
   - Fix site description and metadata with portfolio-focused copy
   - Add structured data for SEO (Person schema)
   - Ensure RSS feeds work with no limit (all posts)
   - Setup GitHub Actions CI/CD for automated deployment

5. **Navigation Improvements**
   - Fix menu weight ordering: Home(1), Blog(2), Projects(3), About(4), Contact(5)
   - Add Content page to navigation

### Out of Scope
- Custom backend development (using mailto: for contact)
- Automated content synchronization from Substack/YouTube APIs
- Custom theme development (using existing hugo-coder theme)
- Commenting system integration
- Analytics setup
- Twitter/X social link (not needed)
- Image optimization beyond basic setup

## Approach

### Phase 1: Foundation (Config & Identity)
1. Update `hugo.toml` with:
   - Title: "Asad Ismail"
   - Tagline: "Senior ML Engineer | MLOps | Computer Vision | LLMs"
   - Description: "Portfolio and blog of a senior ML engineer specializing in MLOps, Computer Vision, and LLMs"
   - Keywords: "machine learning, mlops, computer vision, deep learning, llm, pytorch, tensorflow"
   - Social links with real URLs:
     - GitHub: https://github.com/Asad-Ismail
     - LinkedIn: https://www.linkedin.com/in/asadismaeel/
     - Substack: https://substack.com/@asadismail2
     - YouTube: https://www.youtube.com/@AIMLArchives
     - Email: asadismaeel@gmail.com
   - Avatar: Use Gravatar (comment out avatarURL, enable gravatar)
   - RSS: Set limit to -1 (all posts)
   - Color scheme: auto
   - Code highlighting: github-dark
   - Pagination: keep paginate=20
2. Fix menu weights:
   - Home: weight = 1
   - Blog: weight = 2
   - Projects: weight = 3
   - About: weight = 4
   - Contact: weight = 5
   - Content: weight = 6
3. Remove Twitter/X social link

### Phase 2: Content Creation
1. **About page** (`content/about.md`):
   - Rewrite with authentic experience:
     - 3 years building and optimizing CV models for edge devices
     - 5 years building end-to-end ML pipelines
     - Senior/Staff level experience
   - Highlight areas of expertise (CV, LLMs, agents, best practices)
   - Include technical skills (PyTorch, TensorFlow, etc.)
   - Include work experience and education
   - Keep it 300-500 words, first person, professional tone

2. **Blog posts**:
   - Complete `MLModelDeployment.md` draft (needs significant work)
   - Create 2-3 new technical blog posts
   - Topics: Deep learning, project tutorials, ML best practices, computer vision, LLMs, agents
   - Use TOML front matter (`+++`)
   - Remove `draft: true` when ready to publish
   - Target 500-1500 words per post
   - Include code examples with proper formatting

3. **Projects page** (`content/projects.md`):
   - Create dedicated Projects page in navigation
   - Showcase ML work (CV edge devices, ML pipelines)
   - Link to GitHub repos where applicable
   - Include brief descriptions and tech stack

### Phase 3: External Content Integration
1. **Create Content page** (`content/content.md`):
   - Add to navigation menu with weight = 6
   - Section for YouTube videos with embeds
   - Section for Substack content

2. **YouTube Integration**:
   - Embed 6 videos using Hugo shortcode: `{{< youtube "VIDEO_ID" >}}`
   - Video IDs to embed:
     - IRnTpsDYQQQ
     - WlyS8qYaABw
     - rw7VUCCeNUA
     - GjAJJnKN2CY
     - ALJ9uDVYJ2s
     - LLbJIzAMmCM
   - Display in video gallery format on Content page
   - Each embed should include video title/description

3. **Substack Integration**:
   - Embed newsletter signup form (iframe from Substack)
   - Embed latest posts preview section
   - Get embed code from: Substack > Settings > Growth features
   - Link to full Substack: https://substack.com/@asadismail2

### Phase 4: Contact & SEO
1. **Contact page** (`content/contact.md`):
   - Email: asadismaeel@gmail.com with mailto: link
   - Collaboration availability:
     - Consulting projects
     - Open source collaborations
     - Speaking engagements
   - NOT available for full-time roles
   - Include social media links (GitHub, LinkedIn, Substack, YouTube)
   - Brief intro: "Open to collaboration opportunities"
   - Add to navigation menu with weight = 5

2. **SEO Implementation**:
   - Create `/layouts/partials/seo.html` with Person schema:
     ```html
     <script type="application/ld+json">
     {
       "@context": "https://schema.org",
       "@type": "Person",
       "name": "Asad Ismail",
       "url": "https://Asad-Ismail.github.io/",
       "email": "asadismaeel@gmail.com",
       "jobTitle": "Senior Machine Learning Engineer",
       "description": "Senior ML Engineer specializing in MLOps, Computer Vision, and LLMs. 5 years building end-to-end ML pipelines, 3 years optimizing CV models for edge devices.",
       "sameAs": [
         "https://github.com/Asad-Ismail",
         "https://www.linkedin.com/in/asadismaeel/",
         "https://substack.com/@asadismail2",
         "https://www.youtube.com/@AIMLArchives"
       ]
     }
     </script>
     ```
   - Include partial in base template: `{{ partial "seo.html" . }}`
   - Add meta descriptions to key pages (About, Blog, Contact, Projects, Content)
   - Verify RSS feed at `/index.xml` includes all posts

3. **Robots.txt**:
   - Create `/static/robots.txt`:
     ```
     User-agent: *
     Allow: /
     Sitemap: https://Asad-Ismail.github.io/sitemap.xml
     ```

### Phase 5: CI/CD Setup
1. Create `.github/workflows/hugo.yaml` with:
   - Trigger on push to main branch
   - Install Hugo extended
   - Build site with minification
   - Deploy to GitHub Pages
   - Use Hugo's official GitHub Actions workflow

### Phase 6: Validation & Deploy
1. **Local Testing**:
   - Run `hugo server -D` to serve with drafts
   - Navigate to all pages: Home, About, Blog, Projects, Contact, Content
   - Test all navigation links
   - Click all social media links (verify correct profiles)
   - Click mailto: link (verify email client opens)
   - Test YouTube embeds load and play correctly
   - Test Substack embed displays correctly
   - Test responsive design using browser DevTools responsive mode
   - Test in Chromium browser

2. **Build Verification**:
   - Clean build: `rm -rf public/ && hugo`
   - Verify output structure: `ls -la public/`, `ls -la public/index.xml`
   - Check for build errors
   - Verify RSS feed contains posts

3. **SEO Validation**:
   - Test structured data with: https://validator.schema.org/
   - Test Rich Results: https://search.google.com/test/rich-results
   - Verify robots.txt accessible
   - Check meta descriptions are present

4. **Performance Check**:
   - Target < 3 seconds Largest Contentful Paint
   - Test site load speed
   - Verify no blocking resources

5. **Final Checks**:
   - Verify no "John Doe" or placeholder text remains
   - Verify at least 3 blog posts published
   - Verify all embeds work
   - Verify mobile responsiveness
   - Verify RSS feed accessible

## Quick Commands

### Local Development
```bash
# Serve site locally with drafts
hugo server -D

# Build production site
hugo

# Clean build
rm -rf public/ && hugo

# Check for build errors
hugo server -D 2>&1 | grep -i "error"
```

### Content Creation
```bash
# Create new blog post
hugo new posts/my-new-post.md

# Create new page
hugo new contact.md
```

### Validation
```bash
# Test RSS feed
curl -I https://Asad-Ismail.github.io/index.xml

# Check robots.txt
curl -I https://Asad-Ismail.github.io/robots.txt

# Verify sitemap
curl -I https://Asad-Ismail.github.io/sitemap.xml
```

## Acceptance Criteria

### Must Have (P0)
- [ ] All placeholder "John Doe" text replaced with "Asad Ismail"
- [ ] All placeholder "johndoe" social links replaced with real URLs
- [ ] Contact page exists with mailto: link to asadismaeel@gmail.com
- [ ] Contact page mentions consulting, open source, speaking availability
- [ ] At least 3 published technical blog posts
- [ ] Social links configured: GitHub, LinkedIn, Substack, YouTube (no Twitter)
- [ ] Site tagline: "Senior ML Engineer | MLOps | Computer Vision | LLMs"
- [ ] Site description: "Portfolio and blog of a senior ML engineer specializing in MLOps, Computer Vision, and LLMs"
- [ ] Keywords: "machine learning, mlops, computer vision, deep learning, llm, pytorch, tensorflow"
- [ ] Menu items in correct order: Home(1), Blog(2), Projects(3), About(4), Contact(5), Content(6)
- [ ] 6 YouTube videos embedded on Content page
- [ ] Substack signup form embedded on Content page
- [ ] Substack latest posts preview on Content page
- [ ] RSS feed accessible at `/index.xml` with no limit (all posts)
- [ ] Site builds successfully with `hugo` command
- [ ] About page contains authentic experience (3y CV edge, 5y ML pipelines)
- [ ] Gravatar enabled for avatar
- [ ] GitHub Actions workflow created for deployment
- [ ] Robots.txt created allowing all crawlers

### Should Have (P1)
- [ ] Projects page created with ML work showcases
- [ ] Structured data (Person schema) implemented
- [ ] Meta descriptions added to all key pages
- [ ] Schema markup validates with https://validator.schema.org/
- [ ] Mobile responsive design verified via DevTools
- [ ] Site loads in < 3 seconds (LCP target)
- [ ] All YouTube videos play correctly
- [ ] Substack embed displays correctly

### Could Have (P2)
- [ ] Reading time displayed on blog posts
- [ ] Related posts section
- [ ] Social share buttons on blog posts
- [ ] Performance optimization beyond basic setup

## Key Decisions

### Configuration
- **Name**: Asad Ismail
- **Email**: asadismaeel@gmail.com
- **Tagline**: Senior ML Engineer | MLOps | Computer Vision | LLMs
- **Experience Level**: Senior/Staff (5 years ML pipelines, 3 years CV edge devices)
- **Avatar**: Gravatar (not custom image)
- **Code Theme**: github-dark (no change)
- **Color Scheme**: auto (no change)
- **RSS**: All posts (limit = -1)
- **Pagination**: 20 posts per page (no change)

### Social Media
- **GitHub**: https://github.com/Asad-Ismail
- **LinkedIn**: https://www.linkedin.com/in/asadismaeel/
- **Substack**: https://substack.com/@asadismail2
- **YouTube**: https://www.youtube.com/@AIMLArchives
- **Twitter/X**: None (excluded)

### Navigation Structure
1. Home (weight = 1)
2. Blog (weight = 2)
3. Projects (weight = 3) - dedicated page
4. About (weight = 4)
5. Contact (weight = 5)
6. Content (weight = 6) - NEW page for YouTube/Substack

### Content Strategy
- **Blog Topics**: Deep learning, project tutorials, ML best practices, CV, LLMs, agents
- **Blog Post Count**: 3 minimum (1 draft completed + 2-3 new)
- **Blog Topics**: Decide specific topics during implementation
- **YouTube**: 6 specific videos embedded on dedicated Content page
- **Substack**: Both signup form + latest posts preview on Content page

### Collaboration
- **Open to**: Consulting, Open source, Speaking
- **NOT open to**: Full-time roles

### Testing & Deployment
- **Mobile Testing**: Browser DevTools responsive mode only
- **Browser Testing**: Chromium only
- **Performance Target**: < 3 seconds LCP
- **Deployment**: GitHub Actions CI/CD (setup required)

## Edge Cases

### Missing Information
- **Mitigation**: All URLs and information gathered during interview, no placeholders needed
- **Fallback**: If any URL changes, update in hugo.toml

### Content Creation
- **Risk**: Writing 3 technical blog posts requires significant time
- **Mitigation**: Draft post needs work, 2-3 new posts with flexible topics
- **Fallback**: If time-constrained, publish 2 high-quality posts instead of 3

### External Platform Dependencies
- **Risk**: YouTube/Substack embeds depend on iframe support
- **Mitigation**: Tested specific video IDs, platforms have stable embed APIs
- **Fallback**: If embeds fail, provide direct links to videos/posts

### Avatar Image
- **Current**: my_pic.jpg in static/images may not exist
- **Decision**: Use Gravatar instead (configure in hugo.toml)
- **Fallback**: If Gravatar fails, comment out avatar entirely

### GitHub Actions
- **Risk**: Workflow may conflict with existing deployment
- **Mitigation**: Use Hugo's official GitHub Actions template
- **Fallback**: If CI/CD fails, manual deployment via `hugo` command works

## Risks & Dependencies

### User Input (COMPLETED)
All required information gathered:
- [x] Email: asadismaeel@gmail.com
- [x] Social URLs: GitHub, LinkedIn, Substack, YouTube
- [x] Experience: 3y CV edge, 5y ML pipelines, Senior/Staff level
- [x] YouTube video IDs: 6 specific videos
- [x] Substack URL: https://substack.com/@asadismail2
- [x] Collaboration types: Consulting, Open source, Speaking
- [x] Technical focus: MLOps, CV, LLMs, agents

### External Services
- **Substack**: Account active, publication URL confirmed
- **YouTube**: Channel active, videos public
- **GitHub Pages**: Repository configured for Pages
- **Gravatar**: Email asadismaeel@gmail.com must be registered

### Technical Risks
1. **Draft Post Quality**: MLModelDeployment.md needs significant work
   - **Mitigation**: Complete or replace with new content
2. **CI/CD Setup**: GitHub Actions may need workflow permissions
   - **Mitigation**: Configure Pages source to "GitHub Actions"
3. **Build Time**: Hugo build may timeout if site grows large
   - **Mitigation**: Currently small site, not a concern
4. **Theme Conflicts**: hugo-coder theme updates may break config
   - **Mitigation**: Theme is git submodule, pin to specific commit if issues arise

## Test Notes

### Manual Testing Checklist
- [ ] Navigate to all pages (Home, About, Blog, Projects, Contact, Content)
- [ ] Verify menu items appear in correct order
- [ ] Click all social media links - verify correct profiles open
- [ ] Click mailto: link - verify email client opens with asadismaeel@gmail.com
- [ ] Test responsive layout via Chrome DevTools (mobile, tablet, desktop)
- [ ] Play all 6 YouTube videos - verify embeds work
- [ ] View Substack embed - verify signup form and posts display
- [ ] Check for any "John Doe" or placeholder text
- [ ] Verify RSS feed at /index.xml contains posts
- [ ] Verify robots.txt at /robots.txt allows all crawlers
- [ ] Validate structured data with https://validator.schema.org/
- [ ] Test Rich Results with https://search.google.com/test/rich-results
- [ ] Check site load performance (target < 3s LCP)
- [ ] Verify site builds: `hugo` command succeeds
- [ ] Check Gravatar loads correctly in header/homepage

### Build Verification
```bash
# Clean build
rm -rf public/
hugo

# Verify output structure
ls -la public/
ls -la public/index.xml
ls -la public/posts/
ls -la public/sitemap.xml

# Check for build errors
echo "Build exit code: $?"
```

### Browser Testing (Chromium)
- [ ] Chrome/Edge: All pages render correctly
- [ ] Responsive design: Mobile (375px), Tablet (768px), Desktop (1440px)
- [ ] YouTube embeds: Videos load and play
- [ ] Substack embed: Forms and content display
- [ ] Social links: All open in new tabs
- [ ] Navigation: Menu works on mobile (hamburger menu)

## References

### Hugo Documentation
- [Hugo Official Docs](https://gohugo.io/documentation/)
- [Hugo Quick Start](https://gohugo.io/getting-started/quick-start/)
- [Hugo YouTube Shortcode](https://gohugo.io/shortcodes/youtube/)
- [Hugo RSS Templates](https://gohugo.io/templates/rss/)

### GitHub Actions
- [Hugo GitHub Actions Workflow](https://github.com/marketplace/actions/hugo-deploy-github-pages)
- [GitHub Pages Deployment](https://gohugo.io/host-and-deploy/host-on-github-pages/)
- [Sample hugo.yaml workflow](https://gohugo.io/host-and-deploy/host-on-github-pages/)

### External Platform Integration
- [Substack Embed Documentation](https://support.substack.com/hc/en-us/articles/360041759232)
- [YouTube Embed Parameters](https://developers.google.com/youtube/player_parameters)
- [YouTube Video IDs Provided](IRnTpsDYQQQ, WlyS8qYaABw, rw7VUCCeNUA, GjAJJnKN2CY, ALJ9uDVYJ2s, LLbJIzAMmCM)

### SEO & Structured Data
- [Schema.org Person Type](https://schema.org/Person)
- [Google Structured Data Intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [Schema Markup Validator](https://validator.schema.org/)

### Best Practices
- [ML Portfolio Examples](https://karpathy.ai/), https://huyenchip.com/, https://jalammar.github.io/
- [Technical SEO Guide 2025](https://www.digitalfolks.co/blog/the-ultimate-guide-to-technical-seo-in-2025)
- [Hugo-coder Theme Documentation](https://github.com/luizdepra/hugo-coder)

### Existing Code Patterns
- Config: `/home/asad/dev/asad-ismail.github.io/hugo.toml:1-67`
- Theme: `/home/asad/dev/asad-ismail.github.io/themes/hugo-coder/`
- Content: `/home/asad/dev/asad-ismail.github.io/content/`
- Static: `/home/asad/dev/asad-ismail.github.io/static/`
- Draft Post: `/home/asad/dev/asad-ismail.github.io/content/posts/MLModelDeployment.md:1-15`

### Personal URLs
- **GitHub**: https://github.com/Asad-Ismail
- **LinkedIn**: https://www.linkedin.com/in/asadismaeel/
- **Substack**: https://substack.com/@asadismail2
- **YouTube**: https://www.youtube.com/@AIMLArchives
- **Email**: asadismaeel@gmail.com
