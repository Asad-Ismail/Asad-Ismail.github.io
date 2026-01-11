# fn-1.10 Create missing site items

## Description
Create items that are missing from the implementation.

## Items to Create

### 1. Projects page (content/projects.md)
Create dedicated Projects page showcasing ML work:
- CV edge devices work
- ML pipeline projects
- Link to GitHub repos
- Include brief descriptions and tech stack
- Add to navigation menu (already exists with weight=3)

### 2. robots.txt
Create /static/robots.txt with:
```
User-agent: *
Allow: /
Sitemap: https://Asad-Ismail.github.io/sitemap.xml
```

### 3. GitHub Actions workflow
Create .github/workflows/hugo.yaml with:
- Trigger on push to main branch
- Install Hugo extended
- Build site with minification
- Deploy to GitHub Pages
- Use Hugo's official GitHub Actions workflow template

## Acceptance
- [ ] Projects page created with ML work showcases
- [ ] robots.txt created in static/ directory
- [ ] GitHub Actions workflow created
- [ ] Projects page accessible at /projects/
- [ ] robots.txt accessible at /robots.txt
- [ ] Workflow file is valid YAML

## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
