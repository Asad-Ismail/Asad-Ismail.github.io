# fn-2.2 Implement improved typography hierarchy

## Description
Establish clear typography hierarchy using the Inter font loaded in fn-2.1. Define font sizes, weights, and line heights for different elements (name, title, body, navigation).

## Acceptance
- [ ] Name text styled at 2.5rem (40px), weight 700
- [ ] Title/tagline styled at 1.5rem (24px), weight 400
- [ ] Body text at 1rem (16px), weight 400
- [ ] Navigation links at 1rem (16px), weight 500
- [ ] Line heights: 1.6 for body, 1.25 for headings
- [ ] Heading hierarchy defined: H1 (2.5rem), H2 (1.75rem), H3 (1.5rem)
- [ ] Inter font family applied site-wide
- [ ] Typography consistent across all pages

## Done summary
# Typography Hierarchy Implementation

## What Changed
- Updated heading sizes to match spec: H2 (1.75rem), H3 (1.5rem)
- Added separate `--text-title` variable (1.5rem) for homepage tagline
- Fixed `.home .info` to use the new title variable instead of H2 size

## Why
- Previous heading sizes (H2: 1.5rem, H3: 1.25rem) didn't match specification
- Homepage tagline needed 1.5rem but H2 needed 1.75rem - required separate variables
- Proper typography hierarchy improves visual hierarchy and readability

## Verification
- Reviewed custom.scss to confirm all font sizes match acceptance criteria
- Verified Name: 2.5rem weight 700, Title: 1.5rem weight 400
- Verified Body: 1rem weight 400, Navigation: 1rem weight 500
- Confirmed line heights: 1.6 for body, 1.25 for headings
- Confirmed heading hierarchy: H1 (2.5rem), H2 (1.75rem), H3 (1.5rem)
- Inter font already loaded and applied site-wide from fn-2.1

## Follow-ups
- None
## Evidence
- Commits: e7c5a0b5ee4a2e81a6dc4087314bcc45cdd29d0e
- Tests:
- PRs: