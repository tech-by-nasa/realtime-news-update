"""
🚨 MAGIC ALERT BOX — Global Crisis & Disaster Dashboard
=========================================================
Real-time alerts from GDACS, USGS, ReliefWeb, and NewsAPI
displayed on an interactive map with images and severity colors.

Deployed on Hugging Face Spaces (FREE).
Reads from Supabase (FREE).
Fed by n8n workflows on Render (FREE).
"""

import os
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client

# ============================================================
# CONFIGURATION
# ============================================================
# Set these as Secrets in HuggingFace Space settings:
#   SUPABASE_URL = "https://xxxxx.supabase.co"
#   SUPABASE_KEY = "eyJhbGc..."
# ============================================================

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="🚨 Magic Alert Box",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS — Make it look like a real crisis dashboard
# ============================================================
st.markdown("""
<style>
    /* Dark theme override */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Severity badges */
    .severity-red {
        background: linear-gradient(135deg, #ff0000, #cc0000);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.8em;
        display: inline-block;
    }
    .severity-orange {
        background: linear-gradient(135deg, #ff8c00, #cc7000);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.8em;
        display: inline-block;
    }
    .severity-green {
        background: linear-gradient(135deg, #00cc44, #009933);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.8em;
        display: inline-block;
    }
    
    /* Alert cards */
    .alert-card {
        background: #1a1a2e;
        border-left: 4px solid #ff0000;
        padding: 16px;
        margin: 8px 0;
        border-radius: 8px;
    }
    .alert-card-orange {
        background: #1a1a2e;
        border-left: 4px solid #ff8c00;
        padding: 16px;
        margin: 8px 0;
        border-radius: 8px;
    }
    .alert-card-green {
        background: #1a1a2e;
        border-left: 4px solid #00cc44;
        padding: 16px;
        margin: 8px 0;
        border-radius: 8px;
    }
    
    /* Header pulse animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .live-dot {
        width: 10px;
        height: 10px;
        background: #ff0000;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 1.5s infinite;
        margin-right: 8px;
    }
    
    /* Scrolling ticker */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: #1a0000;
        padding: 8px 0;
        border-radius: 4px;
        margin-bottom: 16px;
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        animation: ticker 30s linear infinite;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE CONNECTION
# ============================================================
@st.cache_resource
def get_supabase_client() -> Client:
    """Create and cache the Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_alerts(
    limit: int = 50,
    severity_filter: str = "all",
    event_type_filter: str = "all",
    hours_back: int = 72
) -> list:
    """Fetch alerts from Supabase with optional filters."""
    client = get_supabase_client()
    if not client:
        return []
    
    try:
        query = client.table("alerts").select("*")
        
        # Time filter
        cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours_back)).isoformat()
        query = query.gte("created_at", cutoff)
        
        # Severity filter
        if severity_filter != "all":
            query = query.eq("severity", severity_filter)
        
        # Event type filter
        if event_type_filter != "all":
            query = query.eq("event_type", event_type_filter)
        
        # Order and limit
        query = query.order("created_at", desc=True).limit(limit)
        
        response = query.execute()
        return response.data if response.data else []
    
    except Exception as e:
        st.error(f"⚠️ Database connection error: {str(e)}")
        return []


def fetch_alert_stats() -> dict:
    """Get quick stats for the header."""
    client = get_supabase_client()
    if not client:
        return {"total": 0, "red": 0, "orange": 0, "green": 0}
    
    try:
        cutoff_24h = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
        
        response = client.table("alerts") \
            .select("severity") \
            .gte("created_at", cutoff_24h) \
            .execute()
        
        data = response.data or []
        return {
            "total": len(data),
            "red": sum(1 for d in data if d.get("severity") == "red"),
            "orange": sum(1 for d in data if d.get("severity") == "orange"),
            "green": sum(1 for d in data if d.get("severity") == "green"),
        }
    except Exception:
        return {"total": 0, "red": 0, "orange": 0, "green": 0}


# ============================================================
# DEMO DATA (When Supabase isn't connected yet)
# ============================================================
def get_demo_alerts() -> list:
    """Return demo alerts so the website looks alive even without DB."""
    return [
        {
            "id": 1,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "title": "🌍 M6.2 Earthquake — Southern Peru",
            "summary": "A magnitude 6.2 earthquake struck 45km SSE of Arica. "
                       "Tsunami warning NOT issued. Depth: 35km.",
            "source": "USGS",
            "source_url": "https://earthquake.usgs.gov",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Seismogram.svg/1200px-Seismogram.svg.png",
            "severity": "orange",
            "event_type": "earthquake",
            "latitude": -18.47,
            "longitude": -70.31,
            "country": "Peru"
        },
        {
            "id": 2,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
            "title": "🌊 Tropical Cyclone Alert — Bay of Bengal",
            "summary": "Cyclone forming with sustained winds of 85 km/h. "
                       "Expected landfall in 48 hours. Evacuations advised.",
            "source": "GDACS",
            "source_url": "https://www.gdacs.org",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Tropical_cyclone_drawing.svg/800px-Tropical_cyclone_drawing.svg.png",
            "severity": "red",
            "event_type": "cyclone",
            "latitude": 15.5,
            "longitude": 88.3,
            "country": "India"
        },
        {
            "id": 3,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat(),
            "title": "🏥 Humanitarian Update — Eastern DRC",
            "summary": "Armed conflict displaces 50,000 people in North Kivu. "
                       "Aid agencies mobilizing emergency response.",
            "source": "ReliefWeb",
            "source_url": "https://reliefweb.int",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Flag_of_the_Red_Cross.svg/800px-Flag_of_the_Red_Cross.svg.png",
            "severity": "red",
            "event_type": "war",
            "latitude": -1.68,
            "longitude": 29.22,
            "country": "DR Congo"
        },
        {
            "id": 4,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=8)).isoformat(),
            "title": "🌋 Volcanic Activity — Mount Etna, Italy",
            "summary": "Strombolian activity observed at summit craters. "
                       "Aviation color code raised to ORANGE.",
            "source": "GDACS",
            "source_url": "https://www.gdacs.org",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Etna_eruption_seen_from_the_International_Space_Station.jpg/1280px-Etna_eruption_seen_from_the_International_Space_Station.jpg",
            "severity": "orange",
            "event_type": "volcano",
            "latitude": 37.75,
            "longitude": 14.99,
            "country": "Italy"
        },
        {
            "id": 5,
            "created_at": (datetime.now(timezone.utc) - timedelta(hours=12)).isoformat(),
            "title": "🌊 Flash Flood Warning — Dhaka, Bangladesh",
            "summary": "Heavy monsoon rainfall causes flooding in low-lying areas. "
                       "Water levels 2m above normal.",
            "source": "GDACS",
            "source_url": "https://www.gdacs.org",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Flooding_in_a_street.jpg/1280px-Flooding_in_a_street.jpg",
            "severity": "red",
            "event_type": "flood",
            "latitude": 23.81,
            "longitude": 90.41,
            "country": "Bangladesh"
        }
    ]


# ============================================================
# RENDER FUNCTIONS
# ============================================================
def severity_badge(severity: str) -> str:
    """Return HTML for a colored severity badge."""
    colors = {
        "red": "severity-red",
        "orange": "severity-orange", 
        "green": "severity-green"
    }
    labels = {
        "red": "🔴 CRITICAL",
        "orange": "🟠 WARNING",
        "green": "🟢 ADVISORY"
    }
    css_class = colors.get(severity, "severity-green")
    label = labels.get(severity, "🟢 INFO")
    return f'<span class="{css_class}">{label}</span>'


def event_icon(event_type: str) -> str:
    """Return an emoji for event type."""
    icons = {
        "earthquake": "🌍",
        "flood": "🌊",
        "cyclone": "🌀",
        "volcano": "🌋",
        "war": "⚔️",
        "news": "📰",
        "wildfire": "🔥",
        "tsunami": "🌊",
    }
    return icons.get(event_type, "📡")


def time_ago(iso_string: str) -> str:
    """Convert ISO timestamp to human-readable 'X hours ago'."""
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = now - dt
        
        if diff.total_seconds() < 60:
            return "just now"
        elif diff.total_seconds() < 3600:
            mins = int(diff.total_seconds() / 60)
            return f"{mins}m ago"
        elif diff.total_seconds() < 86400:
            hours = int(diff.total_seconds() / 3600)
            return f"{hours}h ago"
        else:
            days = int(diff.total_seconds() / 86400)
            return f"{days}d ago"
    except Exception:
        return "recently"


def render_alert_card(alert: dict):
    """Render a single alert as a styled card."""
    severity = alert.get("severity", "green")
    card_class = {
        "red": "alert-card",
        "orange": "alert-card-orange",
        "green": "alert-card-green"
    }.get(severity, "alert-card-green")
    
    icon = event_icon(alert.get("event_type", "news"))
    badge = severity_badge(severity)
    ago = time_ago(alert.get("created_at", ""))
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(
            f"""<div class="{card_class}">
                {badge} &nbsp; <small>{ago} · {alert.get('source', 'Unknown')} · {icon} {alert.get('event_type', 'news').upper()}</small>
                <h3 style="margin:8px 0 4px 0; color:#ffffff;">{alert.get('title', 'No title')}</h3>
                <p style="color:#cccccc; margin:0;">{alert.get('summary', '')}</p>
                {f'<p style="color:#888;"><small>📍 {alert.get("country", "Unknown location")}</small></p>' if alert.get("country") else ''}
                {f'<a href="{alert["source_url"]}" target="_blank" style="color:#4da6ff;">🔗 Read full report →</a>' if alert.get("source_url") else ''}
            </div>""",
            unsafe_allow_html=True
        )
    
    with col2:
        img_url = alert.get("image_url")
        if img_url:
            try:
                st.image(img_url, use_container_width=True)
            except Exception:
                st.markdown("🖼️ *Image unavailable*")


# ============================================================
# MAIN APP
# ============================================================
def main():
    # ── HEADER ──
    st.markdown(
        """<h1 style="text-align:center; color:#ff4444;">
            <span class="live-dot"></span> 
            🚨 MAGIC ALERT BOX
        </h1>
        <p style="text-align:center; color:#888888; font-size:1.1em;">
            Real-Time Global Crisis & Disaster Dashboard<br>
            <small>Powered by GDACS · USGS · ReliefWeb · NewsAPI · n8n · Supabase</small>
        </p>
        <hr style="border-color:#333;">""",
        unsafe_allow_html=True
    )
    
    # ── CONNECTION STATUS ──
    client = get_supabase_client()
    using_demo = client is None
    
    if using_demo:
        st.warning(
            "⚠️ **DEMO MODE** — Supabase not connected. "
            "Showing sample alerts. Add SUPABASE_URL and SUPABASE_KEY "
            "to your Space Secrets to see real data!"
        )
    
    # ── STATS BAR ──
    if not using_demo:
        stats = fetch_alert_stats()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📊 Alerts (24h)", stats["total"])
        c2.metric("🔴 Critical", stats["red"])
        c3.metric("🟠 Warning", stats["orange"])
        c4.metric("🟢 Advisory", stats["green"])
        st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
    
    # ── SIDEBAR FILTERS ──
    with st.sidebar:
        st.markdown("## 🎛️ Filters")
        
        severity_filter = st.selectbox(
            "Severity Level",
            ["all", "red", "orange", "green"],
            format_func=lambda x: {
                "all": "🌐 All Severities",
                "red": "🔴 Critical Only",
                "orange": "🟠 Warnings Only",
                "green": "🟢 Advisories Only"
            }[x]
        )
        
        event_type_filter = st.selectbox(
            "Event Type",
            ["all", "earthquake", "flood", "cyclone", 
             "volcano", "war", "wildfire", "news"],
            format_func=lambda x: f"{event_icon(x)} {x.capitalize()}" if x != "all" else "🌐 All Types"
        )
        
        hours_back = st.slider(
            "Time Window (hours)", 
            min_value=6, 
            max_value=168, 
            value=72, 
            step=6
        )
        
        limit = st.slider(
            "Max Alerts", 
            min_value=10, 
            max_value=100, 
            value=50, 
            step=10
        )
        
        st.markdown("---")
        st.markdown("## 📡 Data Sources")
        st.markdown("""
        - [GDACS](https://www.gdacs.org) — UN Disasters
        - [USGS](https://earthquake.usgs.gov) — Earthquakes
        - [ReliefWeb](https://reliefweb.int) — Humanitarian
        - [NewsAPI](https://newsapi.org) — Breaking News
        """)
        
        st.markdown("---")
        st.markdown(
            "#### 🔄 Auto-refresh\n"
            "Page refreshes data on each interaction.\n"
            "Use the button below for manual refresh."
        )
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.cache_resource.clear()
            st.rerun()
    
    # ── FETCH ALERTS ──
    if using_demo:
        alerts = get_demo_alerts()
    else:
        alerts = fetch_alerts(
            limit=limit,
            severity_filter=severity_filter,
            event_type_filter=event_type_filter,
            hours_back=hours_back
        )
    
    # ── MAP VIEW ──
    st.markdown("### 🗺️ Alert Map")
    map_data = [
        a for a in alerts 
        if a.get("latitude") and a.get("longitude")
    ]
    
    if map_data:
        import pydeck as pdk
        
        df = pd.DataFrame(map_data)
        df["lat"] = df["latitude"].astype(float)
        df["lon"] = df["longitude"].astype(float)
        
        # Color by severity
        def sev_color(s):
            if s == "red":
                return [255, 0, 0, 180]
            elif s == "orange":
                return [255, 140, 0, 180]
            return [0, 200, 70, 180]
        
        df["color"] = df["severity"].apply(sev_color)
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["lon", "lat"],
            get_color="color",
            get_radius=80000,
            pickable=True,
            auto_highlight=True,
        )
        
        view_state = pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=1.5,
            pitch=0
        )
        
        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "{title}\n{severity} · {source}"},
            map_style="mapbox://styles/mapbox/dark-v10"
        )
        
        st.pydeck_chart(deck)
    else:
        st.info("No geo-located alerts to display on map.")
    
    st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
    
    # ── ALERT FEED ──
    st.markdown(f"### 📋 Alert Feed ({len(alerts)} alerts)")
    
    if not alerts:
        st.info("No alerts found. Check your filters or wait for n8n to fetch data.")
    else:
        for alert in alerts:
            render_alert_card(alert)
            st.markdown("")  # spacing
    
    # ── FOOTER ──
    st.markdown(
        """<hr style='border-color:#333;'>
        <p style="text-align:center; color:#555; font-size:0.85em;">
            🚨 Magic Alert Box v1.0 · 
            Open Source · MIT License · 
            <a href="https://github.com/YOUR-USERNAME/magic-alert-box" 
               style="color:#4da6ff;">GitHub</a><br>
            Built with ❤️ using n8n + Supabase + Streamlit + HuggingFace<br>
            <small>Images shown are thumbnails linking back to original sources. 
            We do not store or redistribute copyrighted media.</small>
        </p>""",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
