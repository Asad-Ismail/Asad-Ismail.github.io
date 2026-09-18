# Asad Ismail — personal website

Live at https://asad-ismail.github.io/. Source belongs to the personal GitHub account **Asad-Ismail**, not `asadismail-prosus`.

## Build and verify

Use Hugo **0.131.0 extended**, matching the deployment workflow:

```sh
hugo --minify --destination /tmp/asad-site
python3 scripts/check_site.py /tmp/asad-site
hugo server
```

The check covers internal links, local assets, heading structure, structured data, article listings, project links, video links, and the persistent navigation. Browser QA should cover 320px, 390px, 768px, and 1280px widths, plus the existing long articles and videos page.

## Edit content

- `content/posts/`: original Markdown articles and short entries linking to Medium. External entries use `externalLink` and `publication`; the full article stays on Medium.
- `data/videos.json`: the six AIMLArchives videos, used for homepage previews and the `/content/` video gallery.
- `data/projects.json`: curated public personal repositories, used on the homepage and projects page.
- `content/about.md`: professional background verified against LinkedIn on 18 September 2026.
- `layouts/`: custom Hugo templates. Both `layouts/posts/list.html` and `layouts/posts/single.html` override the theme's section-specific templates.
- `assets/css/site.css`: the active stylesheet. The older theme SCSS is retained but is not loaded by the custom base layout.

The site uses a warm paper background, serif headings, rust links, and plain article and project lists. The homepage puts the five latest articles beside two video previews on desktop; all eight articles and six videos remain on their dedicated pages. Blog & writing, Videos, Projects, and About stay visible in the main navigation at every screen size. The user wants the clarity of George Hotz, Andrej Karpathy, and Lilian Weng’s sites with an original visual identity. Avoid marketing headlines, decorative artwork, badges, and repeated calls to action. No client-side JavaScript or font download is required. Video previews link to YouTube without loading embedded players.

## Sources

- LinkedIn: https://www.linkedin.com/in/asadismaeel/
- Prosus writing: https://medium.com/@asad.ismail.prosus
- Earlier personal writing: https://medium.com/@asadismaeel
- Personal projects: https://github.com/Asad-Ismail

Use published articles and public repositories for portfolio updates. Keep coauthor credit and publication attribution; do not publish private repositories or unpublished drafts.

## Deploy

Pushing source to `master` triggers `.github/workflows/hugo.yaml`. Actions builds into a clean runner temporary directory, runs the site check, and deploys the artifact to GitHub Pages. The repository also contains historical `public/` files and a legacy `gh-pages` branch; these are not the source to edit.

Before publishing, verify `gh api user --jq .login` returns `Asad-Ismail`. Browser login and GitHub CLI login are independent. Use the CLI credential helper for an HTTPS push if the SSH identity is uncertain.
