# 🚀 DEPLOY GUIDE — Like You're 5 Years Old

## What You Need (All FREE)
- A GitHub account (github.com)
- A Render account (render.com)
- A Supabase account (supabase.com)
- A Hugging Face account (huggingface.co)
- A NewsAPI key (newsapi.org) — optional but adds news+images

## Total time: ~30 minutes

---

## STEP 1: Fork This Repo (2 min)
1. Click the green "Fork" button on this GitHub repo
2. Now you have your own copy!

---

## STEP 2: Create Your Memory Vault (5 min)
1. Go to **supabase.com** → Sign Up → New Project
2. Name it `magic-alert-box`
3. Pick a strong database password → SAVE IT
4. Wait for project to initialize (~2 min)
5. Click **SQL Editor** in the left sidebar
6. Copy ALL the code from `supabase-setup/create_tables.sql`
7. Paste it in the SQL Editor → Click **Run**
8. Go to **Project Settings → API**
9. Copy these two values (you'll need them later):
   - `Project URL` (looks like https://xxxxx.supabase.co)
   - `anon public` key (long string starting with eyJ...)

---

## STEP 3: Deploy Your Brain (10 min)
1. Go to **render.com** → Sign Up with GitHub
2. Click **+ New → Blueprint**
3. Connect your forked `magic-alert-box` repo
4. Render detects `n8n-render/render.yaml` automatically
5. Click **Deploy Blueprint**
6. Wait 5-10 minutes for it to build
7. Once live, visit your n8n URL (shown in Render dashboard)
8. Set up your n8n admin account
9. Go to **Settings → Environment Variables** in n8n and add:
   - `SUPABASE_URL` = your Supabase Project URL
   - `SUPABASE_KEY` = your Supabase anon key
   - `NEWSAPI_KEY` = your NewsAPI key (from newsapi.org)
10. Go to **Workflows → Import** and import all 4 JSON files
    from the `n8n-workflows/` folder
11. **Activate** each workflow (toggle the switch!)

---

## STEP 4: Launch Your Website (10 min)
1. Go to **huggingface.co** → Sign Up
2. Click **Spaces → Create New Space**
3. Name it `magic-alert-box`
4. SDK: Choose **Docker**, then select **Streamlit** template
5. Upload ALL files from the `alert-website/` folder:
   - `README.md` (the one with YAML frontmatter)
   - `Dockerfile`
   - `requirements.txt`
   - `src/app.py`
6. Go to **Settings → Secrets** and add:
   - `SUPABASE_URL` = same value from Step 2
   - `SUPABASE_KEY` = same value from Step 2
7. Wait for build (~3-5 min)
8. YOUR SITE IS LIVE! 🎉

---

## STEP 5: Keep It Awake (5 min)
Option A (easiest): 
- Go to **uptimerobot.com** → Free account
- Add monitor for your Render n8n URL (every 5 min)
- Add monitor for your HuggingFace Space URL (every 5 min)

Option B (nerdy):
- Run `keepalive/keepalive.py` on your laptop

---

## 🎉 YOU'RE DONE!
Your multicloud crisis alert system is now:
- ☁️ Brain on Render (Cloud A)
- ☁️ Memory on Supabase (Cloud B)  
- ☁️ Face on Hugging Face (Cloud C)
- 📡 Scanning GDACS + USGS + ReliefWeb + NewsAPI
- 🗺️ Showing alerts on a world map
- 🖼️ Displaying images from news sources
- 🔴🟠🟢 Color-coded by severity

Share your HuggingFace URL with the world!
