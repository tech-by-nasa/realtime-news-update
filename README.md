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
