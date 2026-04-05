-- ============================================================
-- create_tables.sql — Run this in Supabase SQL Editor
-- ============================================================
-- HOW TO USE:
-- 1. Go to supabase.com → Create Free Project
-- 2. Click "SQL Editor" (left sidebar)
-- 3. Paste this ENTIRE file
-- 4. Click "Run"
-- 5. Your memory vault is ready!
-- ============================================================

-- Main alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id              BIGSERIAL PRIMARY KEY,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    
    -- What happened?
    title           TEXT NOT NULL,
    summary         TEXT,
    
    -- Where did we learn about it?
    source          TEXT NOT NULL DEFAULT 'unknown',
    source_url      TEXT,
    
    -- Show me a picture!
    image_url       TEXT,
    
    -- How scary is it? (green / orange / red)
    severity        TEXT DEFAULT 'green',
    
    -- What type? (earthquake / flood / war / cyclone / volcano / news)
    event_type      TEXT DEFAULT 'news',
    
    -- Where on Earth?
    latitude        DOUBLE PRECISION,
    longitude       DOUBLE PRECISION,
    country         TEXT,
    
    -- Is this a duplicate? (unique constraint helper)
    source_id       TEXT,
    
    -- Was this alert sent to users?
    notified        BOOLEAN DEFAULT FALSE,
    
    -- Prevent exact duplicates
    UNIQUE(source, source_id)
);

-- Index for fast "latest alerts" queries
CREATE INDEX IF NOT EXISTS idx_alerts_created_at 
    ON alerts (created_at DESC);

-- Index for filtering by severity
CREATE INDEX IF NOT EXISTS idx_alerts_severity 
    ON alerts (severity);

-- Index for filtering by event type
CREATE INDEX IF NOT EXISTS idx_alerts_event_type 
    ON alerts (event_type);

-- Enable Row Level Security (Supabase best practice)
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

-- Allow anyone to READ alerts (public dashboard)
CREATE POLICY "Allow public read access" 
    ON alerts FOR SELECT 
    USING (true);

-- Only authenticated service role can INSERT
CREATE POLICY "Allow service role insert" 
    ON alerts FOR INSERT 
    WITH CHECK (true);

-- Only authenticated service role can UPDATE
CREATE POLICY "Allow service role update" 
    ON alerts FOR UPDATE 
    USING (true);

-- ============================================================
-- OPTIONAL: A "sources" reference table
-- ============================================================
CREATE TABLE IF NOT EXISTS sources (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    api_url     TEXT,
    description TEXT,
    is_active   BOOLEAN DEFAULT TRUE
);

INSERT INTO sources (name, api_url, description) VALUES
    ('GDACS', 'https://www.gdacs.org/gdacsapi', 'UN/EU Global Disaster Alert System'),
    ('USGS', 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php', 'US Geological Survey Earthquakes'),
    ('ReliefWeb', 'https://api.reliefweb.int/v1', 'UN OCHA Humanitarian Reports'),
    ('NewsAPI', 'https://newsapi.org/v2', 'Breaking News Aggregator')
ON CONFLICT (name) DO NOTHING;

-- ============================================================
-- DONE! Your vault is ready. 
-- Now copy your Supabase URL and anon key from:
--   Project Settings → API → Project URL
--   Project Settings → API → anon/public key
-- ============================================================
