# fn-1.4 Integrate YouTube and Substack content

## Description
Integrate embedded YouTube videos and Substack content into the website.

**YouTube Integration:**
1. Choose 2-3 YouTube videos to embed (tutorials, talks, etc.)
2. Create a new page or section to showcase videos
3. Use Hugo's built-in YouTube shortcode: `{{< youtube "VIDEO_ID" >}}`
4. Example: `{{< youtube "dQw4w9WgXcQ" >}}` for video ID `dQw4w9WgXcQ`

**Substack Integration:**
1. Get your Substack publication URL
2. Choose integration approach:
   - **Option A**: Embed newsletter signup form (iframe from Substack)
   - **Option B**: Embed latest post preview
   - **Option C**: Create a "Content" page with links to Substack + embedded videos

**Implementation:**
- Create `/home/asad/dev/asad-ismail.github.io/content/content.md` page
- Add embedded YouTube videos using shortcode
- Add Substack embed iframe (get code from Substack > Settings > Growth features)
- Add this page to navigation menu in hugo.toml

**Alternative: Add to homepage**
- If you prefer, add embeds directly to homepage content
- Or create a dedicated "Videos" or "Content" section

**References:**
- YouTube shortcode: https://gohugo.io/shortcodes/youtube/
- Substack embed docs: https://support.substack.com/hc/en-us/articles/360041759232
## Acceptance
- [ ] At least 2 YouTube videos embedded on site
- [ ] YouTube videos load and play correctly
- [ ] Substack content integrated (signup form OR post embed)
- [ ] Substack embed displays correctly on page
- [ ] New "Content" or "Media" page created (or added to homepage)
- [ ] Page added to navigation menu with proper weight
- [ ] All embeds are responsive on mobile
- [ ] No iframe loading errors
- [ ] Page layout looks professional
- [ ] Links to external platforms (Substack, YouTube channel) work correctly
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
