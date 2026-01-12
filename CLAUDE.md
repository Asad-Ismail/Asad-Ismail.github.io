# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Hugo Development
```bash
# Build the site (production)
hugo --minify

# Run local development server (includes drafts)
hugo server -D

# Run local server (published content only)
hugo server

# Create new content using archetype
hugo new posts/my-new-post.md
```

### Git and Deployment
- The site is automatically deployed to GitHub Pages when pushing to the `master` branch
- Hugo version 0.131.0 is used in CI
- Submodules are included in deployment (the `hugo-coder` theme)

## Project Architecture

This is a **Hugo static site** for a personal portfolio/blog. The architecture follows Hugo's standard conventions with custom styling layered on top of the `hugo-coder` theme.

### Directory Structure
```
.
├── content/           # Markdown content pages
│   ├── posts/        # Blog posts (markdown files)
│   ├── about.md      # About page
│   ├── projects.md   # Projects page
│   └── contact.md    # Contact page
├── layouts/          # Custom layout overrides (partials only)
│   └── partials/     # Custom template partials
│       ├── custom-head.html  # Injected into <head>
│       └── seo.html          # SEO metadata
├── assets/scss/      # Custom SCSS styles
│   └── custom.scss   # Design tokens and theme overrides
├── static/           # Static assets (images, favicon, robots.txt)
├── archetypes/       # Content templates (front matter defaults)
├── hugo.toml         # Site configuration
├── themes/hugo-coder/ # Git submodule - base theme
└── .flow/            # Flow task management (epics, tasks)
```

### Theme Customization Strategy

The site uses the **hugo-coder** theme as a base but heavily customizes the visual appearance through SCSS overrides. Key principle: **extend, don't modify** the theme files.

1. **Design Tokens** (`assets/scss/custom.scss:4-39`): CSS custom properties define spacing (8px grid), typography scale, and color schemes for light/dark modes
2. **SCSS Overrides**: The `customSCSS` parameter in `hugo.toml` loads `assets/scss/custom.scss` after the theme styles
3. **Layout Partials**: Custom templates in `layouts/partials/` override theme partials automatically

### Styling Architecture

The custom SCSS is organized into sections:
1. **Design Tokens** - CSS variables for spacing, typography, colors
2. **Overrides** - Font family, body styles, typography hierarchy
3. **Navigation Redesign** - Hover states, active indicators, mobile menu
4. **Blog Post Cards** - Card-based layout with hover effects
5. **Spacing & Layout** - Consistent spacing system using 8px grid
6. **Color Overrides** - Dark mode enforcement, accent colors
7. **Visual Polish** - Transitions, animations, accessibility

### Color Scheme
- **Accent**: Cyan (`#22d3ee`)
- **Light mode**: Off-white backgrounds (`#fafafa`), dark text
- **Dark mode**: Soft black (`#121212`), off-white text
- Uses CSS custom properties with `[data-theme="dark"]` selector

### Flow Task Management

The `.flow/` directory contains epic and task definitions managed by flow-next:
- `.flow/epics/*.json` - Epic definitions
- `.flow/tasks/*.json` - Individual task specifications
- `.flow/config.json` - Flow configuration
- `.flow/meta.json` - Schema version and epic counter

When working on tasks tracked in Flow, update the corresponding JSON files and mark tasks as completed.

## Configuration

### Site Settings (`hugo.toml`)
- **Base URL**: `https://Asad-Ismail.github.io/`
- **Theme**: `hugo-coder` (submodule)
- **Navigation**: Home, Blog, Projects, About, Contact, Content
- **Social Links**: GitHub, LinkedIn, Email, Substack, YouTube
- **Features**: Font Awesome icons, Twemoji support, auto color scheme with toggle

### Content Front Matter
Blog posts use front matter defined in `archetypes/default.md`:
```toml
+++
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
date = {{ .Date }}
draft = true
+++
```

## Development Notes

- **Font**: Inter (loaded via Google Fonts)
- **Icons**: Font Awesome 6 (free tier)
- **Syntax Highlighting**: GitHub Dark style
- **Deployment**: GitHub Pages via Actions workflow
- **Footer**: Hidden via CSS (`footer { display: none; }`)

### Spacing System
All spacing uses an 8px grid defined in CSS custom properties:
- `--space-1`: 4px, `--space-2`: 8px, `--space-4`: 16px, etc.
- Use these variables for consistent spacing throughout custom styles

### When Modifying Styles
1. Add new styles to `assets/scss/custom.scss`
2. Use CSS custom properties for colors and spacing
3. Include both light and dark mode variants
4. Test with both theme toggles
5. Maintain the 8px grid for spacing
