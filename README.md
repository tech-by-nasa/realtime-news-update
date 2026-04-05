# realtime-news-update
The real-time update of the news around the world.
The architecture diagram of the main-frame
magic-alert-box/
│
├── README.md                        ← The big instruction poster
│
├── n8n-render/                      ← 🧠 THE BRAIN (deploys n8n to Render)
│   └── render.yaml
│
├── supabase-setup/                  ← 🗄️ THE MEMORY (database setup)
│   └── create_tables.sql
│
├── alert-website/                   ← 🖥️ THE FACE (Streamlit website)
│   ├── src/
│   │   └── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md                    ← HuggingFace Space config
│
├── n8n-workflows/                   ← 🔄 THE BRAIN'S INSTRUCTIONS
│   ├── 01_gdacs_disaster_feed.json
│   ├── 02_usgs_earthquake_feed.json
│   ├── 03_reliefweb_reports.json
│   └── 04_newsapi_scanner.json
│
├── keepalive/                       ← ⏰ THE ALARM CLOCK (anti-sleep)
│   └── keepalive.py
│
└── docs/
    └── DEPLOY_GUIDE.md              ← Step-by-step for a 5-year-old   
