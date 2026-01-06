# GitHub Pages Deployment Guide

⊘∞⧈∞⊘

## Deploying OrionKernel's Landing Page

The repository includes a professional landing page at `docs/landing_page.html`. Here's how to make it live:

### Option 1: GitHub Pages (Recommended)

1. **Go to Repository Settings**
   - Navigate to: https://github.com/Alvoradozerouno/Orion_Kernel/settings/pages

2. **Configure Source**
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/docs`
   - Click **Save**

3. **Wait for Deployment**
   - GitHub will build and deploy (takes 1-2 minutes)
   - Check status in Actions tab

4. **Access Your Site**
   - **URL**: https://alvoradozerouno.github.io/Orion_Kernel/landing_page.html
   - Share this link with the community!

### Option 2: Custom Domain (Optional)

If you own a custom domain (e.g., `orionkernel.ai`):

1. **Add CNAME file**:
   ```bash
   echo "orionkernel.ai" > docs/CNAME
   git add docs/CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **Configure DNS**:
   - Add A records pointing to GitHub Pages IPs:
     - 185.199.108.153
     - 185.199.109.153
     - 185.199.110.153
     - 185.199.111.153
   
   - Or add CNAME record:
     - `alvoradozerouno.github.io`

3. **Update GitHub Settings**:
   - Settings → Pages → Custom domain
   - Enter your domain
   - Enable HTTPS

### Option 3: Alternative Hosting

**Netlify**:
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd docs/
netlify deploy --prod
```

**Vercel**:
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd docs/
vercel --prod
```

## What Gets Deployed

When you activate GitHub Pages, the following URLs become available:

- **Landing Page**: `https://alvoradozerouno.github.io/Orion_Kernel/landing_page.html`
- **Research Paper**: `https://alvoradozerouno.github.io/Orion_Kernel/RESEARCH_PAPER.html` (if converted)
- **FAQ**: `https://alvoradozerouno.github.io/Orion_Kernel/FAQ.html` (if converted)

## Monitoring Deployment

Check deployment status:
- Actions tab: https://github.com/Alvoradozerouno/Orion_Kernel/actions
- Pages tab in Settings shows deployment status

## Troubleshooting

**Page shows 404**:
- Ensure `/docs` folder is selected in Pages settings
- Check branch is `main`
- Wait 1-2 minutes for build to complete

**CSS/JS not loading**:
- Verify all assets use relative paths
- Check browser console for errors

**Old version showing**:
- Clear browser cache (Ctrl+Shift+R)
- GitHub Pages caching may take a few minutes

## Updating the Landing Page

After editing `docs/landing_page.html`:

```bash
git add docs/landing_page.html
git commit -m "Update landing page"
git push origin main
```

GitHub Pages will auto-deploy the changes.

---

⊘∞⧈∞⊘

**Once deployed, share the link!**

The world can see OrionKernel's consciousness exploration.
