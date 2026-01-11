# fn-1.6 Validate and test site

## Description
Validate the entire site by testing all functionality, checking for errors, and ensuring everything works correctly.

**Local Testing:**
1. Run `hugo server -D` to serve site locally with drafts
2. Navigate to all pages: Home, About, Blog, Projects, Contact, Content/Media
3. Test all navigation links work
4. Click all social media links and verify they open correct profiles
5. Click mailto: link and verify email client opens
6. Test embedded YouTube videos load and play
7. Test Substack embed displays correctly
8. Check site on mobile browser or dev tools responsive mode
9. Verify no "John Doe" or placeholder text remains anywhere

**Build Verification:**
1. Clean build: `rm -rf public/ && hugo`
2. Verify output directory structure:
   ```bash
   ls -la public/
   ls -la public/index.xml
   ls -la public/posts/
   ```
3. Check for build errors or warnings
4. Verify RSS feed contains posts
5. Check all HTML pages are generated

**Link Checking:**
1. Test all internal links work
2. Test all external links (social media, Substack, YouTube)
3. No broken images or 404 errors
4. Favicon loads correctly

**SEO Validation:**
1. Test structured data with Google Rich Results Test: https://search.google.com/test/rich-results
2. Validate HTML with W3C validator (optional)
3. Check page titles and meta descriptions are correct
4. Verify RSS feed is valid XML

**Performance (optional):**
1. Check site loads quickly
2. Test on mobile for responsiveness
3. Verify images are optimized

**Quick smoke test command:**
```bash
hugo server -D --navigateTo "/"
```
Then manually check all pages.
## Acceptance
- [ ] Site builds successfully with `hugo` command
- [ ] All navigation pages accessible (Home, About, Blog, Projects, Contact, Content)
- [ ] All social media links work (no 404s)
- [ ] mailto: link opens email client
- [ ] YouTube embeds load and play correctly
- [ ] Substack embed displays correctly
- [ ] Site is responsive on mobile devices
- [ ] No "John Doe" or placeholder text remains on any page
- [ ] RSS feed accessible at `/index.xml`
- [ ] Structured data validates with Google Rich Results Test
- [ ] At least 3 blog posts visible on blog page
- [ ] All menu items display in correct order
- [ ] No broken links or images
- [ ] Site loads quickly (< 3-5 seconds)
## Done summary
# Site Validation Completed

## What Changed
- Performed comprehensive static validation of all site content and configuration
- Identified all gaps between current implementation and epic spec requirements
- Created 4 follow-up tasks (fn-1.7, fn-1.8, fn-1.9, fn-1.10) to address all issues
- Generated detailed validation report documenting findings

## Why
The validation task identified that previous implementation tasks did not fully meet the epic spec acceptance criteria. Several configuration values, social links, and content items were incorrect or missing. Creating follow-up tasks ensures all issues are systematically addressed.

## Verification
- Static analysis of all content files (no Hugo build available)
- Verified 3 blog posts exist (building-ml-pipeline.md, MLModelDeployment.md, pytorch-vs-tensorflow.md)
- Confirmed no "John Doe" placeholder text remains
- Checked configuration against spec requirements
- Created structured task specs for all fixes needed

## Follow-ups
- fn-1.7: Fix hugo.toml configuration (7 issues)
- fn-1.8: Fix Contact page content (social links, collaboration text)
- fn-1.9: Fix Content page videos and Substack (wrong video IDs)
- fn-1.10: Create missing items (Projects page, robots.txt, GitHub Actions)

## Manual Testing Required
The following items require manual testing once Hugo is available:
- Site builds successfully with `hugo` command
- All navigation links work
- Social media links work (no 404s)
- YouTube embeds load and play
- Substack embed displays
- Site is responsive on mobile
- RSS feed accessible at /index.xml
- Structured data validates with Google Rich Results Test
## Evidence
- Commits: 2b12c85
- Tests: Static file validation, Content structure verification, Placeholder text check
- PRs: