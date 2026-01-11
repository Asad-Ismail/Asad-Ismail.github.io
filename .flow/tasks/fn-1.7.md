# fn-1.7 Fix hugo.toml configuration

## Description
Fix all configuration issues in hugo.toml to match the epic spec requirements.

## Changes Required

### 1. Update params.info (tagline)
- Current: "Machine Learning Engineer | AI Researcher | Building intelligent systems with deep learning and PyTorch"
- Required: "Senior ML Engineer | MLOps | Computer Vision | LLMs"

### 2. Update params.description
- Current: "Asad Ismail's personal website - Machine Learning Engineer and AI researcher specializing in deep learning, computer vision, and natural language processing"
- Required: "Portfolio and blog of a senior machine learning engineer specializing in MLOps, Computer Vision, and LLMs"

### 3. Update params.keywords
- Current: "machine learning, ML engineer, AI, deep learning, PyTorch, TensorFlow, computer vision, NLP, neural networks"
- Required: "machine learning, mlops, computer vision, deep learning, llm, pytorch, tensorflow"

### 4. Remove Twitter social link
- Delete lines 84-87 (Twitter social link)

### 5. Fix social link URLs
- LinkedIn: Change from https://www.linkedin.com/in/asad-ismail/ to https://www.linkedin.com/in/asadismaeel/
- Substack: Change from https://asadismail.substack.com to https://substack.com/@asadismail2
- YouTube: Change from https://www.youtube.com/@AsadIsmailML to https://www.youtube.com/@AIMLArchives

### 6. Fix avatar configuration
- Comment out line 44: # avatarurl = "images/my_pic.jpg"
- Uncomment line 45: gravatar = "asadismaeel@gmail.com"

### 7. Fix menu weights
- Change Content from weight=5 to weight=6
- Change Contact from weight=6 to weight=5

## Acceptance
- [ ] Site tagline matches spec exactly
- [ ] Site description matches spec exactly
- [ ] Keywords match spec exactly
- [ ] Twitter/X social link removed
- [ ] All social URLs match spec exactly
- [ ] Gravatar enabled, local avatar commented out
- [ ] Menu order: Home(1), Blog(2), Projects(3), About(4), Contact(5), Content(6)

## Done summary
# Fixed hugo.toml Configuration

## What Changed
- Updated params.info (tagline) to match spec exactly
- Updated params.description to match spec exactly
- Updated params.keywords to match spec exactly
- Removed Twitter/X social link entirely
- Fixed all social link URLs to match spec
- Enabled Gravatar, commented out local avatar
- Fixed menu weights (Contact=5, Content=6)

## Why
Previous implementation didn't match the epic spec requirements exactly. Configuration values were incorrect, causing the site to display wrong information and link to incorrect social profiles.

## Verification
- All configuration values now match spec exactly
- Twitter link removed
- All social URLs point to correct profiles
- Gravatar enabled for avatar
- Menu order correct: Home(1), Blog(2), Projects(3), About(4), Contact(5), Content(6)
## Evidence
- Commits: cacb6d0
- Tests: Config file validation, Parameter verification
- PRs: