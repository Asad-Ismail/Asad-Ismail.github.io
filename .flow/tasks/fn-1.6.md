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
TBD

## Evidence
- Commits:
- Tests:
- PRs:
