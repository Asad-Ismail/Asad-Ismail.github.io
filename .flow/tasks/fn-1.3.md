# fn-1.3 Create and publish technical blog posts

## Description
Create and publish at least 3 technical blog posts to demonstrate ML expertise.

**Current state:**
- One draft post exists: `MLModelDeployment.md` (marked `draft: true`)

**Tasks:**
1. **Complete draft post**: Finish `/home/asad/dev/asad-ismail.github.io/content/posts/MLModelDeployment.md` and remove `draft: true` from front matter
2. **Create 2-3 new posts**: Use `hugo new posts/post-title.md` to create new technical blog posts

**Post topic ideas (choose or propose your own):**
- ML model deployment strategies
- PyTorch vs TensorFlow for production
- Building an end-to-end ML pipeline
- Common MLOps challenges and solutions
- Optimizing ML model inference
- Feature engineering best practices
- Transfer learning tutorial
- Building a recommendation system

**Requirements for each post:**
- Use TOML front matter (`+++` delimiters per archetype)
- Include title, date, and relevant tags/categories
- Remove `draft: true` when ready to publish
- 500-1500 words of technical content
- Include code examples where applicable
- Add proper formatting (headers, code blocks, etc.)

**Reference:** `/home/asad/dev/asad-ismail.github.io/content/posts/MLModelDeployment.md:1-15`
## Acceptance
- [ ] Draft post `MLModelDeployment.md` completed and published (draft flag removed)
- [ ] At least 2 additional technical blog posts created
- [ ] Total of 3+ published blog posts on the site
- [ ] All posts have proper front matter (title, date, tags/categories)
- [ ] All posts are high-quality, technical content
- [ ] All posts display correctly on blog listing page
- [ ] Each post is at least 500 words
- [ ] Code examples properly formatted with syntax highlighting
- [ ] No draft posts remain (unless intentionally unpublished)
- [ ] Blog section shows multiple posts when visiting site
## Done summary
Created 3 technical ML blog posts:

1. ML Model Deployment: Strategies and Best Practices (667 words)
2. PyTorch vs TensorFlow: Choosing the Right Framework for Production (861 words)
3. Building an End-to-End ML Pipeline with Modern Tools (1066 words)

All posts use proper TOML front matter with draft=false, include title, date, tags, categories, and contain 500+ words of technical content with code examples demonstrating ML/MLOps expertise.
## Evidence
- Commits: 49b9fc1
- Tests:
- PRs: