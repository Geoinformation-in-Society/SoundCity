# Evidence-Based Livability Presets

## Research Summary

This document provides literature-backed justification for preset choices and indicator weightings in SoundCity.

---

## Key Literature Sources

### 1. WHO Environmental Burden of Disease (EBD)
The WHO quantifies health impacts using Disability-Adjusted Life Years (DALYs).

**Key findings for European context:**
| Environmental Factor | Health Impact Rank (Europe) | Key Health Outcomes |
|---------------------|----------------------------|---------------------|
| Air Pollution | **#1** (highest DALYs) | Cardiovascular disease, respiratory, lung cancer |
| Noise Pollution | **#2** | Cardiovascular disease, sleep disturbance, cognitive impairment |
| Lack of Green Space | **#3** | Reduced physical activity, mental health, heat exposure |

**Source:** WHO Regional Office for Europe, "Burden of Disease from Environmental Noise" (2011)

### 2. EIU Global Liveability Index
The Economist Intelligence Unit methodology uses these category weights:

| Category | Weight | Relevant Indicators |
|----------|--------|---------------------|
| Stability (Safety) | 25% | Crime, terrorism, civil unrest |
| Healthcare | 20% | Quality, availability of care |
| Culture & **Environment** | **25%** | Climate, humidity, green spaces |
| Education | 10% | Quality, availability |
| Infrastructure | 20% | Transport, energy, telecoms |

**Source:** EIU Global Liveability Index Methodology Report

### 3. European Environment Agency (EEA)
The EEA's Urban Quality of Life indicators emphasize:
- Air quality satisfaction varies widely across cities (major concern)
- Noise from traffic is second most reported environmental problem
- Green space accessibility correlates strongly with life satisfaction

**Source:** EEA Report "Ensuring quality of life in Europe's cities and towns" (2020)

---

## Proposed Evidence-Based Presets

Based on the literature, I recommend 4 presets with scientific justification:

### Preset 1: ⚖️ Balanced (Default)
**Rationale:** Equal weighting when no specific priority exists. Commonly used in multi-criteria indices as a neutral baseline.

| Indicator | Weight | Justification |
|-----------|--------|---------------|
| Air Quality | 25% | Equal distribution |
| Noise | 25% | Equal distribution |
| Green Coverage | 25% | Equal distribution |
| Urban Heat | 25% | Equal distribution |

**Literature:** AHP/entropy methods often start with equal weights before user adjustment (Saaty, 1980)

---

### Preset 2: 💚 Health-Focused
**Rationale:** Based on WHO Environmental Burden of Disease rankings for Europe.

| Indicator | Weight | Justification |
|-----------|--------|---------------|
| Air Quality | **40%** | #1 environmental health risk; 4.2M deaths/year globally (WHO, 2024) |
| Noise | **30%** | #2 in Europe for DALYs; cardiovascular and sleep impacts |
| Green Coverage | 20% | Mental health benefits, promotes physical activity |
| Urban Heat | 10% | Lower immediate mortality vs chronic exposures |

**Literature:**
- WHO Global Burden of Disease Study 2021
- EEA: "Noise is second only to air pollution in DALYs lost" (2021)
- Lancet Commission on Pollution and Health (2022)

---

### Preset 3: 🌿 Nature & Recreation
**Rationale:** Prioritizes access to green/blue infrastructure and natural cooling.

| Indicator | Weight | Justification |
|-----------|--------|---------------|
| Air Quality | 15% | Still important but not primary focus |
| Noise | 15% | Reduced emphasis on traffic noise |
| Green Coverage | **45%** | ~50% of EEA urban sustainability indicators relate to green space |
| Urban Heat | 25% | Green infrastructure provides cooling (0.5-6°C reduction) |

**Literature:**
- WHO Urban Green Spaces and Health report (2016)
- ISGlobal Barcelona: "Green spaces reduce mortality risk 4%" (Rojas-Rueda et al., 2019)
- Meta-analysis: Twohig-Bennett & Jones (2018) - Comprehensive green space health benefits

---

### Preset 4: 🌡️ Climate Resilience
**Rationale:** Focus on heat adaptation—critical for aging populations and climate change.

| Indicator | Weight | Justification |
|-----------|--------|---------------|
| Air Quality | 15% | Secondary to thermal stress |
| Noise | 10% | Least priority in climate context |
| Green Coverage | **35%** | Nature-based cooling (NBS) up to 6°C reduction |
| Urban Heat | **40%** | UHI can cause 26-45% higher mortality in vulnerable groups |

**Literature:**
- Lancet Countdown on Health and Climate Change (2023)
- Health Canada: "Urban heat islands can account for 50% of heat-related mortality" (2022)
- IPCC AR6: NBS for urban heat mitigation

---

## Alternative/Additional Presets to Consider

| Preset Name | Focus | Weights (A/N/G/H) | Source/Rationale |
|-------------|-------|-------------------|------------------|
| 🏃 Active Living | Exercise-friendly neighborhoods| 20/25/40/15 | WHO Physical Activity Guidelines |
| 👴 Senior-Friendly | Elderly population needs | 30/35/20/15 | Age-friendly cities (WHO, 2007) |
| 👶 Family with Children | Child development focus | 30/30/25/15 | UNICEF Child Friendly Cities |

---

## Implementation Recommendation

1. **Keep 4 presets** (matches current implementation)
2. **Rename presets** to be more descriptive:
   - `balanced` → "⚖️ Balanced"
   - `health` → "💚 Health (WHO)" 
   - `nature` → "🌿 Nature & Recreation"
   - `cooling` → "🌡️ Climate Resilience"

3. **Add tooltip citations** showing the source for each preset

4. **Updated weights based on research:**

```javascript
const presets = {
  balanced: { air: 25, noise: 25, greenCoverage: 25, urbanHeat: 25 },
  health: { air: 40, noise: 30, greenCoverage: 20, urbanHeat: 10 },
  nature: { air: 15, noise: 15, greenCoverage: 45, urbanHeat: 25 },
  climate: { air: 15, noise: 10, greenCoverage: 35, urbanHeat: 40 }
}
```

---

## References

1. WHO (2021). *Global burden of disease from air pollution*. Geneva: World Health Organization.
2. WHO Europe (2011). *Burden of disease from environmental noise*. Copenhagen.
3. EIU (2024). *Global Liveability Index Methodology*. The Economist Intelligence Unit.
4. EEA (2020). *Ensuring quality of life in Europe's cities and towns*. European Environment Agency.
5. Rojas-Rueda, D. et al. (2019). Green spaces and mortality: a systematic review. *Lancet Planetary Health*.
6. Twohig-Bennett, C., Jones, A. (2018). Health benefits of the great outdoors. *Environmental Research*, 166, 628-637.
7. Health Canada (2022). *Reducing Urban Heat Islands to Protect Health in Canada*.
8. IPCC (2022). *Climate Change 2022: Impacts, Adaptation and Vulnerability*. AR6 WGII.
