# 🚨 Magic Alert Box — Real-Time Global Crisis & Disaster Alert System

A **free**, **multicloud**, real-time alert system that monitors earthquakes,
floods, wars, and humanitarian crises — then shows them on a live website
with images, severity colors, and source links.

## Architecture (3 Free Cloud Services = Multicloud)
- **Brain**: n8n workflow engine on [Render.com](https://render.com) (Cloud A)
- **Memory**: PostgreSQL database on [Supabase.com](https://supabase.com) (Cloud B)  
- **Face**: Streamlit dashboard on [Hugging Face Spaces](https://huggingface.co/spaces) (Cloud C)

## Data Sources (All Free, All Ethical)
| Source | What It Watches | Update Speed |
|--------|----------------|--------------|
| GDACS (UN/EU) | Earthquakes, floods, cyclones, volcanoes | ~6 min |
| USGS GeoJSON | Earthquakes worldwide | ~1 min |
| ReliefWeb API | War zones, humanitarian crises | ~30 min |
| NewsAPI.org | Breaking news + images | ~5 min |

## Quick Start
See `docs/DEPLOY_GUIDE.md` for the complete 5-year-old-friendly walkthrough.

## License
MIT — Use it. Save lives. Share it.


    ┌─────────────────────────────────────────────────────────────────┐
    │                    🌍 THE INTERNET                              │
    │                                                                 │
    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
    │  │  GDACS   │ │  USGS    │ │ ReliefWeb│ │    NewsAPI       │   │
    │  │  (UN/EU) │ │(US Govt) │ │ (UN OCHA)│ │  (News+Images)   │   │
    │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └───────┬──────────┘   │
    │       │             │            │               │              │
    │       └──────┬──────┴─────┬──────┘               │              │
    │              │            │                       │              │
    │              ▼            ▼                       ▼              │
    │  ┌──────────────────────────────────────────────────────────┐   │
    │  │  🧠 n8n BRAIN — render.com (Cloud A)                    │   │
    │  │                                                          │   │
    │  │  Workflow 01: GDACS disasters every 10 min               │   │
    │  │  Workflow 02: USGS earthquakes every 5 min               │   │
    │  │  Workflow 03: ReliefWeb reports every 30 min             │   │
    │  │  Workflow 04: NewsAPI crisis news every 15 min           │   │
    │  │                                                          │   │
    │  │  Each workflow: Fetch → Parse → Deduplicate → Write      │   │
    │  └──────────────────────┬───────────────────────────────────┘   │
    │                         │                                       │
    │                         │ HTTPS POST (insert alert)             │
    │                         ▼                                       │
    │  ┌──────────────────────────────────────────────────────────┐   │
    │  │  🗄️ SUPABASE MEMORY — supabase.com (Cloud B)            │   │
    │  │                                                          │   │
    │  │  PostgreSQL: "alerts" table                              │   │
    │  │  ┌─────────────────────────────────────────────────┐     │   │
    │  │  │ id │ title │ summary │ severity │ image_url │...│     │   │
    │  │  │ 1  │ M6.2  │ Peru... │ orange   │ https://..│   │     │   │
    │  │  │ 2  │ Cycl  │ India.. │ red      │ https://..│   │     │   │
    │  │  └─────────────────────────────────────────────────┘     │   │
    │  │  + Row Level Security + Indexes + Deduplication          │   │
    │  └──────────────────────┬───────────────────────────────────┘   │
    │                         │                                       │
    │                         │ HTTPS GET (read latest alerts)        │
    │                         ▼                                       │
    │  ┌──────────────────────────────────────────────────────────┐   │
    │  │  🖥️ STREAMLIT FACE — huggingface.co/spaces (Cloud C)    │   │
    │  │                                                          │   │
    │  │  ┌────────────────────────────────────┐                  │   │
    │  │  │  🚨 MAGIC ALERT BOX               │                  │   │
    │  │  │  ┌─────────────────────────────┐   │                  │   │
    │  │  │  │     🗺️ WORLD MAP            │   │                  │   │
    │  │  │  │     (pydeck / scatterplot)   │   │                  │   │
    │  │  │  │  🔴 Peru  🔴 India  🟠 Italy│   │                  │   │
    │  │  │  └─────────────────────────────┘   │                  │   │
    │  │  │                                    │                  │   │
    │  │  │  🔴 CRITICAL: Cyclone Bay Bengal   │                  │   │
    │  │  │  [image] 2h ago · GDACS            │                  │   │
    │  │  │  🟠 WARNING: M6.2 Earthquake Peru  │                  │   │
    │  │  │  [image] 5h ago · USGS             │                  │   │
    │  │  │  🟢 ADVISORY: Relief Update DRC    │                  │   │
    │  │  │  12h ago · ReliefWeb               │                  │   │
    │  │  └────────────────────────────────────┘                  │   │
    │  └──────────────────────────────────────────────────────────┘   │
    │                                                                 │
    │  ⏰ KEEPALIVE: UptimeRobot pings both services every 5 min     │
    └─────────────────────────────────────────────────────────────────┘
