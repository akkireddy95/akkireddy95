# Setup guide — 5 steps, under 5 minutes

## Step 1 — Upload these files to your profile repository

Open https://github.com/akkireddy95/akkireddy95 and upload every file keeping the folder structure:

    README.md                                     → repo root
    generate_readme.py                            → repo root
    .github/workflows/update-profile-readme.yml  → create folders if missing
    SETUP.md                                      → repo root (delete after setup)

Tip: use GitHub's built-in file upload (drag & drop works) or git clone + push.

---

## Step 2 — Allow the workflow to write to the repo

1. Open the repository → Settings → Actions → General
2. Under "Workflow permissions" select → Read and write permissions
3. Save

---

## Step 3 — Add your feed URLs (optional but recommended)

1. Repository → Settings → Secrets and variables → Actions → Variables tab
2. Click "New repository variable" and add:

   Name: BLOG_FEED_URL
   Value: your blog RSS or Atom feed URL
   Example (Jekyll / GitHub Pages): https://akkireddy1.github.io/feed.xml

   Name: VLOG_FEED_URL
   Value: your YouTube Atom feed URL
   Format: https://www.youtube.com/feeds/videos.xml?channel_id=YOUR_CHANNEL_ID
   Find channel ID: YouTube → Your Channel → About → Share → Copy channel ID

If you skip this step the script still works — it will show recent GitHub repos only.

---

## Step 4 — Run the workflow now

1. Actions tab → "Update profile README" → Run workflow → Run workflow
2. Wait ~30 seconds then visit https://github.com/akkireddy95

---

## Step 5 — Pin the right repositories

On your profile page click "Customize your pins" and select:
  1. aws-analytics-platform-terraform
  2. akkireddy95.github.io
  3. DevOps-guide
  4. akkireddy95
  5. Online-Banking-system

---

## What happens automatically from now on

Every day at 04:17 UTC GitHub Actions will:
  - Pull latest blog posts and vlog entries from your feeds
  - Pull your 5 most recently updated non-fork repositories
  - Rebuild the "Current output" section in README.md
  - Commit and push only if something changed

Your profile stays live with zero manual effort.
