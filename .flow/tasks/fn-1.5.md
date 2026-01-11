# fn-1.5 Create Contact page and implement SEO

## Description
Create a Contact page and implement SEO improvements including structured data.

**Contact Page:**
1. Create `/home/asad/dev/asad-ismail.github.io/content/contact.md`
2. Include:
   - Brief introduction ("I'm open to collaboration opportunities")
   - Email address with mailto: link: `<a href="mailto:your@email.com">your@email.com</a>`
   - Links to social media profiles (GitHub, LinkedIn, Substack, YouTube)
   - Optional: What types of collaborations you're interested in
3. Use YAML front matter and add to navigation menu in hugo.toml

**SEO Improvements:**
1. **Structured Data (Person Schema):**
   - Create `/home/asad/dev/asad-ismail.github.io/layouts/partials/seo.html` (if it doesn't exist)
   - Add JSON-LD Person schema with your information:
     ```html
     <script type="application/ld+json">
     {
       "@context": "https://schema.org",
       "@type": "Person",
       "name": "Asad Ismail",
       "url": "https://Asad-Ismail.github.io/",
       "jobTitle": "Machine Learning Engineer",
       "sameAs": [
         "https://github.com/Asad-Ismail",
         "https://linkedin.com/in/yourprofile"
       ]
     }
     </script>
     ```
   - Include this partial in base template: `{{ partial "seo.html" . }}`

2. **Meta Descriptions:**
   - Add meta description to key pages (About, Blog, Contact)
   - Example in front matter: `description: "Senior ML engineer specializing in..."`

3. **Verify RSS feed:**
   - Confirm RSS is enabled in hugo.toml outputs section
   - Test feed is accessible

**References:**
- Schema.org Person: https://schema.org/Person
- Hugo RSS: https://gohugo.io/templates/rss/
## Acceptance
- [ ] Contact page created at `/content/contact.md`
- [ ] Contact page has working mailto: link with real email
- [ ] Contact page includes collaboration availability info
- [ ] Contact page added to navigation menu
- [ ] Structured data (Person schema) implemented
- [ ] SEO partial included in base template
- [ ] RSS feed is accessible at `/index.xml`
- [ ] Meta descriptions added to key pages
- [ ] Schema markup validates with https://validator.schema.org/
- [ ] Contact page displays correctly
- [ ] All social media links on contact page work
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
