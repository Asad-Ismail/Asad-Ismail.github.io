# fn-1.9 Fix Content page videos and Substack

## Description
Update content.md to match epic spec requirements.

## Changes Required

### 1. Replace YouTube videos
Current videos (incorrect):
- kCc8FmEb1nY
- c36lU1-4bG4
- aircAruvnKk

Required videos (from spec):
- IRnTpsDYQQQ
- WlyS8qYaABw
- rw7VUCCeNUA
- GjAJJnKN2CY
- ALJ9uDVYJ2s
- LLbJIzAMmCM

Need all 6 videos embedded, not just 3.

### 2. Fix Substack embed URL
- Current: https://asadismail.substack.com/embed
- Required: Update to use correct publication URL (https://substack.com/@asadismail2)
- Note: May need to verify actual embed URL format

### 3. Fix social links in Connect section
- Update all social links to match spec (same issues as contact page)

## Acceptance
- [ ] All 6 required YouTube videos embedded with correct IDs
- [ ] Substack embed displays correctly
- [ ] All social links in Connect section match spec
- [ ] No Twitter links present

## Done summary
# Fixed Content Page Videos and Substack

## What Changed
- Replaced all 3 incorrect YouTube videos with 6 correct video IDs from spec
- Added descriptive titles and descriptions for each video
- Updated Substack embed URL to correct publication
- Fixed all social links in Connect section
- Removed Twitter link
- Updated meta description

## Why
Content page had wrong YouTube video IDs and incorrect social links. Only 3 videos were embedded instead of 6 required by spec. Substack URL pointed to wrong publication.

## Verification
- All 6 required YouTube videos embedded with correct IDs
- Substack embed URL updated
- All social links match spec exactly
- Twitter link removed
## Evidence
- Commits: 3754a67
- Tests: YouTube video ID verification, Social link check
- PRs: