# fn-1.1 Update site configuration and metadata

## Description
Update hugo.toml configuration file to replace all placeholder content with real information and fix site metadata.

**Changes needed:**
1. Keep `baseURL` as `https://Asad-Ismail.github.io/` (no custom domain)
2. Update `title` if needed (currently "Asad Ismail")
3. Update `params.author` to "Asad Ismail"
4. Update `params.info` tagline to something more descriptive than "Machine learning developer"
5. Update `params.description` from "John Doe's personal website" to ML-focused description
6. Update `params.keywords` from generic "blog,developer,personal" to ML-specific keywords
7. Update all `params.social` links with real URLs:
   - `github`: Replace `https://github.com/johndoe` with your GitHub
   - `linkedin`: Replace `https://www.linkedin.com/johndoe` with your LinkedIn
   - `twitter`: Update or remove if not used
   - `email`: Update `your.email@example.com` to real email
8. Fix menu weights in `[[menu.main]]` section:
   - Home: weight = 1
   - Blog: weight = 2
   - Projects: weight = 3
   - About: weight = 4
9. Add social links for Substack and YouTube (use FontAwesome icons: `fa-substack` for Substack, `fa-youtube` for YouTube)

**Reference file:** `/home/asad/dev/asad-ismail.github.io/hugo.toml:1-67`
## Acceptance
- [ ] Site title updated with "Asad Ismail"
- [ ] Description changed from "John Doe's personal website"
- [ ] All placeholder social links (johndoe) replaced with real Asad Ismail URLs
- [ ] Email address updated from placeholder to real email
- [ ] Menu weights fixed (no conflicts, proper ordering: Home=1, Blog=2, Projects=3, About=4)
- [ ] Author info tagline updated to be more descriptive (ML-focused)
- [ ] Keywords updated to ML-focused terms (e.g., "machine learning, ML engineer, AI, deep learning, PyTorch, TensorFlow")
- [ ] Substack social link added with FontAwesome icon
- [ ] YouTube social link added with FontAwesome icon
- [ ] Site builds successfully with `hugo` command
- [ ] No "John Doe" or "johndoe" text remains in config
- [ ] baseURL remains `https://Asad-Ismail.github.io/`
## Done summary
TBD

## Evidence
- Commits:
- Tests:
- PRs:
