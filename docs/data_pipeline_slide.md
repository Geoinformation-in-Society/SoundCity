# Data Pipeline Slide Content

## Slide Title: **Data Sources & Processing Pipeline**

---

## Visual Layout Suggestion
Use a **flow diagram** with 4 parallel lanes (one per indicator), showing: **Source → Fetch → Process → Score**

---

## 1. 🔊 NOISE POLLUTION

| Aspect | Details |
|--------|---------|
| **Source** | Lärmkartierung NRW 2022 (EU Environmental Noise Directive) |
| **Fetched From** | Münster Open Data Portal (GeoJSON polygons) |
| **Data Format** | High-resolution dB contour polygons (day/night, street/industry) |
| **Storage** | Raw GeoJSON → `app/data/raw/noise_*.json` |
| **Processing** | Spatial intersection of district boundary with noise polygons |
| **Calculation** | Weighted average dB = Σ(area × dB level) / total_area |
| **Score Mapping** | <45dB→5, 45-50→4.5, 50-55→4, 55-60→3, 60-65→2, >65→1 |
| **Citation** | EU Directive 2002/49/EC; LANUV NRW [4] |

---

## 2. 💨 AIR QUALITY

| Aspect | Details |
|--------|---------|
| **Sources** | ① LUQS NRW (LANUV official stations) ② Sensor.Community (citizen science) |
| **Fetched From** | Live API endpoints (hourly updates) |
| **Data Format** | Point locations with PM₁₀, PM₂.₅, NO₂ readings (µg/m³) |
| **Storage** | JSON → `app/data/raw/air_sensors_global.json` |
| **Processing** | Filter sensors within Münster bbox → interpolate to district centroids |
| **Calculation** | Spatial averaging: mean PM values for sensors within district polygon |
| **Score Mapping** | Based on WHO Air Quality Guidelines: <20µg/m³→5, <35→4, <50→3, <75→2, >75→1 |
| **Fallback** | Distance-from-center heuristic when no sensors available |
| **Citation** | WHO AQG 2021; LANUV NRW [5,6,7] |

---

## 3. 🌿 GREEN COVERAGE (Combined Indicator)

| Aspect | Details |
|--------|---------|
| **Sources** | ① Grünflächen WFS (green spaces) ② Baumkataster WFS (tree registry) |
| **Fetched From** | Stadt Münster OGC Web Feature Service |
| **Data Format** | Polygons (parks, forests) + Points (individual trees) |
| **Storage** | GeoJSON → `app/data/raw/green_spaces.geojson`, `trees.geojson` |
| **Processing** | **Two-component fusion:** |
| | ① Green area coverage = intersection_area / district_area (0-1) |
| | ② Tree density = tree_count / max_expected (normalized 0-1) |
| **Calculation** | **Combined Score = 0.5 × green_coverage + 0.5 × tree_density** |
| **Score Mapping** | Scaled to 1-5: `1 + (combined × 4)` |
| **Citation** | WHO Urban Green Spaces & Health 2016 [8] |

---

## 4. 🌡️ URBAN HEAT (Multi-Factor UHI Model)

| Aspect | Details |
|--------|---------|
| **Approach** | **Proxy-based model** using literature-backed UHI correlates |
| **Data Sources** | |
| | ① **Green Coverage** (from Grünflächen + Baumkataster WFS) |
| | ② **Impervious Surface** proxy: derived from **Copernicus HRL Imperviousness** (10m resolution, 2021) OR approximated as `1 - green_coverage` |
| | ③ **District geometries** (for distance + area calculations) |
| **Available Official Sources** | |
| | • **Copernicus HRL Imperviousness Density** – 10m pan-European (land.copernicus.eu) |
| | • **ALKIS Building Footprints** – Stadt Münster WFS |
| | • **Versiegelungskarte Münster** – documented 51.18% avg imperviousness |
| **Current Implementation** | Uses green coverage as inverse proxy (simpler, real-time) |
| **Factors & Weights** | Based on UHI-LST correlation studies: |
| | ① **Green coverage (40%)** – evapotranspiration cooling |
| | ② **Distance from center (30%)** – urban core = higher UHI |
| | ③ **Impervious surface (20%)** – heat absorption/radiation |
| | ④ **District density (10%)** – smaller area = denser, hotter |
| **Grain** | District-level (same as other indicators) |
| **Score Mapping** | Scaled to 1-5 (higher = cooler/more resilient) |
| **Literature** | Yuan & Bauer (2007): ISA shows strong positive correlation with LST; Weng et al. (2004) |
| **Future Enhancement** | Integrate Stadtklimaanalyse WMS 2025 when available at district level |

---

## 5. 🗺️ NEIGHBOURHOOD BOUNDARIES

| Aspect | Details |
|--------|---------|
| **Source** | Stadt Münster Open Data (45 Stadtteile) |
| **Format** | GeoJSON Polygon features |
| **Storage** | `app/data/geojson/neighborhoods_boundaries.geojson` |
| **Used For** | Spatial aggregation unit for all indicator calculations |

---

## Data Flow Summary (for diagram)

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DATA SOURCES  │───→│     FETCH       │───→│    PROCESS      │───→│   LIVABILITY    │
│                 │    │                 │    │                 │    │     SCORE       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • LANUV NRW     │    │ HTTP requests   │    │ Spatial joins   │    │ Weighted avg    │
│ • Sensor.Comm   │    │ WFS GetFeature  │    │ Interpolation   │    │ of 4 indicators │
│ • Münster OGC   │    │ to GeoJSON      │    │ Score mapping   │    │ (user-defined   │
│ • Open Data     │    │ stored locally  │    │ Normalization   │    │  weights)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## Key Academic References

| Ref | Citation |
|-----|----------|
| [4] | EU Environmental Noise Directive 2002/49/EC |
| [5,6,7] | LANUV NRW Air Quality Monitoring Network; WHO Air Quality Guidelines 2021 |
| [8] | WHO (2016) Urban Green Spaces and Health – A Review of Evidence |
| [10] | Stadt Münster Stadtklimaanalyse 2025 |
| UHI | Yuan, F., & Bauer, M. E. (2007). Comparison of impervious surface area and NDVI. *Remote Sensing of Environment*, 104(4), 433-449 |
| UHI | Weng, Q., Lu, D., & Schubring, J. (2004). Estimation of land surface temperature–vegetation abundance relationship. *Remote Sensing of Environment*, 89(4), 467-483 |

---

## Concise One-Slide Version

### Data Pipeline

| Indicator | Source | Processing | Score Method |
|-----------|--------|------------|--------------|
| **Noise** | Lärmkartierung NRW 2022 | Spatial intersection with dB polygons | Weighted avg dB → 1-5 scale |
| **Air Quality** | LUQS NRW + Sensor.Community | Spatial interpolation of PM/NO₂ | WHO thresholds → 1-5 |
| **Green Coverage** | Grünflächen + Baumkataster WFS | 50% area coverage + 50% tree density | Combined → 1-5 |
| **Urban Heat** | Multi-factor UHI proxy | Green (40%) + Distance (30%) + Impervious (20%) + Density (10%) | Weighted sum → 1-5 |

**Storage:** GeoJSON files → Python processing → JSON API → Vue.js frontend

**Key Citations:** WHO AQG 2021; EU Noise Directive 2002/49/EC; Yuan & Bauer 2007 (ISA-UHI correlation)
