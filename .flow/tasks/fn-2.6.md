# fn-2.6 Transform blog posts into card design

## Description
TBD

## Acceptance
- [ ] TBD

## Done summary
# Blog Post Card Design Implementation

## What Changed
- Enhanced blog post list with minimal card design
- Added padding (1.5rem/24px) and border-radius (8px) to post cards
- Implemented hover effects: translateY(-2px) with subtle box-shadow
- Added transparent border that becomes visible on hover
- Improved title styling (1.125rem, weight 600) with hover color change
- Enhanced date display (1rem, secondary color) with proper spacing
- Removed duplicate list styles for code cleanliness

## Why
- Transform blog listing from plain list to modern card-based layout
- Improve visual hierarchy and readability
- Add interactive feedback for better UX
- Maintain minimalist aesthetic consistent with site design

## Verification
- Built site successfully with `hugo` command
- No errors or warnings during build
- CSS compiled without issues
- Custom SCSS changes applied correctly

## Follow-ups
- Test in browser to verify hover effects work as expected
- Consider adding subtle tag/category badges if needed later
## Evidence
- Commits: 10e260059e2498abc3df227cff112c92a7a1eea2
- Tests: hugo build successful - no errors or warnings
- PRs: