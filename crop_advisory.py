"""
OptiCrop Agronomic Advisory & Knowledge Engine
Provides curated agronomic profiles, benchmark thresholds, and dynamic advisory generation for 22 crops.
"""

import json
import os

# Complete Agronomic Knowledge Profiles for all 22 crops
CROP_PROFILES = {
    "rice": {
        "display_name": "Rice (Oryza sativa)",
        "category": "Cereal Grain",
        "icon": "🌾",
        "season": "Kharif (June – November)",
        "growth_duration": "105 – 150 days",
        "water_need": "High (Flooded / Puddled fields)",
        "soil_type": "Clayey, Loamy, and Alluvial soils with good water retention",
        "summary": "Rice is a staple cereal requiring consistent moisture, warm humid climate, and fertile soils rich in organic matter.",
        "fertilizer_guide": "Apply N-P-K in split doses. Basal dose of P and K with 1/3 Nitrogen; top dress remaining Nitrogen at tillering and panicle initiation.",
        "pest_management": "Watch for Brown Planthopper (BPH) and Stem Borer. Use neem seed kernel extract (NSKE) or pheromone traps for pest monitoring.",
        "economic_outlook": "High national and international demand with established Minimum Support Price (MSP) and procurement channels."
    },
    "maize": {
        "display_name": "Maize / Corn (Zea mays)",
        "category": "Cereal Grain / Fodder",
        "icon": "🌽",
        "season": "Kharif & Rabi (All season adaptable)",
        "growth_duration": "90 – 110 days",
        "water_need": "Medium (Sensitive to waterlogging)",
        "soil_type": "Well-drained sandy loam to silt loam with high fertility",
        "summary": "Maize is the 'Queen of Cereals', having high genetic yield potential and vast industrial use in food, feed, and starch.",
        "fertilizer_guide": "Maize is a heavy feeder of Nitrogen. Apply balanced NPK with zinc sulfate at sowing to prevent white bud disorder.",
        "pest_management": "Monitor for Fall Armyworm (FAW). Intercropping with pulses and installing pheromone traps significantly reduces damage.",
        "economic_outlook": "Booming market demand for livestock feed, poultry industries, and corn syrup processing."
    },
    "chickpea": {
        "display_name": "Chickpea / Bengal Gram (Cicer arietinum)",
        "category": "Pulse / Legume",
        "icon": "🌱",
        "season": "Rabi (October – March)",
        "growth_duration": "90 – 120 days",
        "water_need": "Low (Drought-tolerant taproot system)",
        "soil_type": "Deep black soils, sandy loams with good internal drainage",
        "summary": "Chickpea is a major protein-rich cool-season pulse that enriches soil through atmospheric nitrogen fixation.",
        "fertilizer_guide": "Seed inoculation with Rhizobium culture is highly recommended. Low Nitrogen requirement; prioritize Phosphorus for root nodulation.",
        "pest_management": "Watch for Pod Borer (Helicoverpa armigera). Plant marigold border rows as trap crops and spray NPV or Bacillus thuringiensis.",
        "economic_outlook": "Steady domestic market demand as a primary source of vegetarian protein (besan, chana)."
    },
    "kidneybeans": {
        "display_name": "Kidney Beans / Rajma (Phaseolus vulgaris)",
        "category": "Pulse / Legume",
        "icon": "🫘",
        "season": "Rabi / Hill Kharif (Cool, mild climate)",
        "growth_duration": "100 – 130 days",
        "water_need": "Medium (Uniform soil moisture without stagnation)",
        "soil_type": "Light, friable loam rich in organic matter (pH 5.5 - 6.5)",
        "summary": "Unlike most other pulses, kidneybeans do not fix nitrogen efficiently and need adequate soil fertility and mild temperatures.",
        "fertilizer_guide": "Needs basal nitrogen application along with phosphorus and potash since natural nodulation is weaker.",
        "pest_management": "Protect from bean anthracnose and aphids. Use certified disease-free seeds and balanced organic compost.",
        "economic_outlook": "Premium cash value in retail markets and wholesale pulses trade."
    },
    "pigeonpeas": {
        "display_name": "Pigeonpea / Arhar / Tur (Cajanus cajan)",
        "category": "Pulse / Legume",
        "icon": "🫛",
        "season": "Kharif (June – January)",
        "growth_duration": "150 – 200 days (Long duration)",
        "water_need": "Low to Medium (Deep root system withstands dry spells)",
        "soil_type": "Deep well-drained loamy to black cotton soils",
        "summary": "Pigeonpeas are drought-hardy legumes ideal for intercropping with cotton, sorghum, or soybean, improving soil structure.",
        "fertilizer_guide": "Apply basal starter nitrogen and single super phosphate (SSP) for sulfur and phosphorus nutrition.",
        "pest_management": "Monitor for Maruca pod borer and wilt disease. Practice crop rotation and Trichoderma seed treatment.",
        "economic_outlook": "Essential staple pulse with high wholesale prices across major food grain mandis."
    },
    "mothbeans": {
        "display_name": "Moth Bean (Vigna aconitifolia)",
        "category": "Arid Pulse / Cover Crop",
        "icon": "🌾",
        "season": "Kharif (Monsoon)",
        "growth_duration": "65 – 80 days (Short duration)",
        "water_need": "Very Low (One of the most drought-hardy crops)",
        "soil_type": "Sandy, sandy-loam, and light desert soils",
        "summary": "Remarkable climate-resilient pulse grown in arid tracts; prevents soil erosion and fixes nitrogen in low-moisture zones.",
        "fertilizer_guide": "Requires minimal fertilizer. 10-15 kg N and 30-40 kg P2O5 per hectare is usually sufficient.",
        "pest_management": "Resistant to most pests; treat seeds against root rot in case of unseasonal heavy rainfall.",
        "economic_outlook": "High value for traditional snacks (Bikaneri Bhujia, namkeen), sprouts, and nutritious green fodder."
    },
    "mungbean": {
        "display_name": "Mung Bean / Green Gram (Vigna radiata)",
        "category": "Pulse / Legume",
        "icon": "🥣",
        "season": "Kharif, Rabi & Zaid (Triple season flexibility)",
        "growth_duration": "60 – 75 days (Very fast harvest)",
        "water_need": "Low to Moderate",
        "soil_type": "Well-drained fertile loam or alluvial soil",
        "summary": "Fast-growing short-duration pulse that fits into multi-cropping systems and restores depleted nitrogen in soils.",
        "fertilizer_guide": "Rhizobium and PSB seed treatment. Moderate starter dose of N and P; avoid excess nitrogen to prevent leafy lodging.",
        "pest_management": "Watch for Yellow Mosaic Virus (YMV) transmitted by whiteflies. Plant resistant cultivars and use yellow sticky cards.",
        "economic_outlook": "Quick cash flow for farmers between main cropping seasons; strong retail consumer demand."
    },
    "blackgram": {
        "display_name": "Black Gram / Urad (Vigna mungo)",
        "category": "Pulse / Legume",
        "icon": "🌱",
        "season": "Kharif & Late Rabi / Summer",
        "growth_duration": "70 – 90 days",
        "water_need": "Low to Medium",
        "soil_type": "Heavy black soils, loams with good water holding capacity",
        "summary": "Widely consumed Indian pulse with high protein and phosphoric acid content, crucial for fermenting traditional dishes.",
        "fertilizer_guide": "Basal application of DAP or SSP. Foliar spray of 2% DAP or urea at flowering boosts pod set.",
        "pest_management": "Whitefly management is crucial to curb Mungbean Yellow Mosaic Virus. Maintain clean field borders.",
        "economic_outlook": "Consistent high commercial value in urban food processing and hospitality industries."
    },
    "lentil": {
        "display_name": "Lentil / Masoor (Lens culinaris)",
        "category": "Pulse / Legume",
        "icon": "🥣",
        "season": "Rabi (Winter season)",
        "growth_duration": "100 – 120 days",
        "water_need": "Low (Grows well on residual soil moisture)",
        "soil_type": "Alluvial, clay loams, and light soils (pH 6.0 – 7.5)",
        "summary": "Cold-tolerant leguminous crop with high culinary significance, requiring minimal supplemental irrigation.",
        "fertilizer_guide": "Apply 20 kg N and 40 kg P2O5 / ha. Zinc application improves nodulation and overall yield.",
        "pest_management": "Watch for collar rot and rust in humid winter conditions. Ensure proper drainage.",
        "economic_outlook": "Strong export potential and dependable domestic culinary consumption."
    },
    "pomegranate": {
        "display_name": "Pomegranate (Punica granatum)",
        "category": "Horticultural Fruit Crop",
        "icon": "🍎",
        "season": "Perennial (Bahar treatment in Mrig/Hasta/Ambe)",
        "growth_duration": "Fruit matures 130 – 160 days after flowering",
        "water_need": "Low to Moderate (Drip irrigation ideal)",
        "soil_type": "Deep loamy or sandy loam soils with excellent drainage (pH 6.5 – 7.5)",
        "summary": "High-value semi-arid fruit with excellent drought tolerance, rich in antioxidants and suited for precision drip fertigation.",
        "fertilizer_guide": "Heavy requirement of organic farmyard manure, zinc, boron, and balanced potassium during fruit bulking.",
        "pest_management": "Manage Bacterial Blight (Telya) with copper bactericides. Monitor for fruit borer butterflies with pheromone traps.",
        "economic_outlook": "Very high export value to Middle East and Europe, high return per acre under modern orchard management."
    },
    "banana": {
        "display_name": "Banana (Musa acuminata)",
        "category": "Horticultural Fruit Crop",
        "icon": "🍌",
        "season": "Year-round planting in humid tropics / sub-tropics",
        "growth_duration": "11 – 13 months",
        "water_need": "Very High (Continuous moist soil required)",
        "soil_type": "Rich, deep alluvial or volcanic clay loam with organic mulch",
        "summary": "Fast-growing giant herbaceous perennial with heavy nutrient and water uptake, yielding high tonnage per hectare.",
        "fertilizer_guide": "Heavy Potassium and Nitrogen feeder. Apply fertilizers in split doses every 3-4 weeks through drip fertigation.",
        "pest_management": "Watch for Panama Wilt and Sigatoka Leaf Spot. Use tissue-culture disease-free suckers and sanitation.",
        "economic_outlook": "Continuous year-round harvest and dependable everyday cash income with strong retail turnover."
    },
    "mango": {
        "display_name": "Mango (Mangifera indica)",
        "category": "Horticultural Fruit Crop",
        "icon": "🥭",
        "season": "Flowering in winter (Dec–Feb), harvest in Summer (April–July)",
        "growth_duration": "Perennial orchard (Full bearing in 5-8 years)",
        "water_need": "Medium (Withhold water 2 months before flowering to induce bloom)",
        "soil_type": "Deep alluvial, red loamy, well-drained soils up to 2m depth",
        "summary": "The 'King of Fruits', well-adapted to tropical conditions with distinct dry periods for prolific flowering.",
        "fertilizer_guide": "Post-harvest application of organic manure, NPK, and micronutrient sprays (Zinc, Boron) before flower emergence.",
        "pest_management": "Mango hopper and powdery mildew during flowering. Timely prophylactic sulfur or neem sprays protect flower panicles.",
        "economic_outlook": "High domestic celebration season demand and lucrative international export avenues (Alphonso, Kesar, Dasheri)."
    },
    "grapes": {
        "display_name": "Grapes (Vitis vinifera)",
        "category": "Horticultural Fruit Crop",
        "icon": "🍇",
        "season": "Pruning cycle: Foundation (April) & Forward (October)",
        "growth_duration": "120 – 140 days post-October pruning",
        "water_need": "Medium (Precision drip with moisture stress during berry ripening)",
        "soil_type": "Well-drained sandy loam or gravelly soil; sensitive to salinity",
        "summary": "Commercial viticulture requires careful trellis training, rigorous canopy pruning, and balanced potassium for sugar content.",
        "fertilizer_guide": "Extremely high Potassium demand for berry sizing, cluster filling, and Brix development. Ample calcium prevents berry cracking.",
        "pest_management": "Downy mildew and powdery mildew in damp conditions; canopy aeration and systemic bio-fungicides are essential.",
        "economic_outlook": "Top-tier commercial fruit with domestic table consumption, raisin production, and wine processing industries."
    },
    "watermelon": {
        "display_name": "Watermelon (Citrullus lanatus)",
        "category": "Cucurbitaceous Fruit / Cash",
        "icon": "🍉",
        "season": "Zaid / Summer (January – June)",
        "growth_duration": "75 – 95 days",
        "water_need": "Medium (Drip irrigation with silver-black mulch recommended)",
        "soil_type": "Sandy riverbeds, fertile sandy loam with warm root zone",
        "summary": "Warm-season sun-loving fruit requiring high solar radiation, dry climate during ripening, and warm sandy soil.",
        "fertilizer_guide": "High initial Nitrogen for vine spread, shifted to high Potassium and Calcium during fruit development for sweet crisp rind.",
        "pest_management": "Protect seedlings from red pumpkin beetle and aphids. Use drip mulching and avoid overhead sprinkler wetting.",
        "economic_outlook": "Rapid 3-month investment turnaround with massive urban demand during hot summer months."
    },
    "muskmelon": {
        "display_name": "Muskmelon / Cantaloupe (Cucumis melo)",
        "category": "Cucurbitaceous Fruit / Cash",
        "icon": "🍈",
        "season": "Zaid / Summer (February – May)",
        "growth_duration": "70 – 85 days",
        "water_need": "Low to Moderate (Withhold water 7-10 days before harvest for sweetness)",
        "soil_type": "Light sandy loam, well-aerated with good organic matter",
        "summary": "Fast-maturing melon crop requiring hot dry sunny weather at ripening for optimal sweetness and aroma development.",
        "fertilizer_guide": "Balanced NPK basal with soluble potash and boron foliar spray during fruit setting to enhance sweetness.",
        "pest_management": "Watch for fruit fly; deploy methyl eugenol pheromone traps and cover developing melons if feasible.",
        "economic_outlook": "High profit margins for quality net-skinned and sweet varieties in modern supermarkets."
    },
    "apple": {
        "display_name": "Apple (Malus domestica)",
        "category": "Temperate Horticultural Fruit",
        "icon": "🍏",
        "season": "Temperate climate (Requires 800 - 1200 chilling hours < 7°C)",
        "growth_duration": "130 – 160 days from bloom to harvest",
        "water_need": "Medium to High (Consistent moisture throughout growing season)",
        "soil_type": "Deep well-drained loamy soil with rich humus (pH 5.5 – 6.5)",
        "summary": "Premier temperate fruit crop grown in high altitude hill zones with cold chilling winters and sunny summers.",
        "fertilizer_guide": "Requires substantial Potassium and Phosphorus for spur vigor, fruit firmness, and color coloration. Calcium sprays prevent bitter pit.",
        "pest_management": "Scab and woolly apple aphid control. Regular pruning for air circulation and copper-based sprays during dormant stage.",
        "economic_outlook": "High premium retail and cold storage asset with extensive shelf life and wholesale liquidity."
    },
    "orange": {
        "display_name": "Orange / Mandarin (Citrus reticulata)",
        "category": "Citrus Fruit Crop",
        "icon": "🍊",
        "season": "Ambe / Mrig Bahar (Harvest in Nov–Feb or March–May)",
        "growth_duration": "Fruit matures 210 – 240 days after bloom",
        "water_need": "Moderate (Requires strict water stress before flowering to trigger bloom)",
        "soil_type": "Deep well-drained medium black or alluvial soil without hardpan",
        "summary": "Major citrus fruit producing juicy refreshing segments; highly sensitive to poor drainage and waterlogged subsoil.",
        "fertilizer_guide": "Apply FYM along with nitrogen, zinc, iron, and boron. Micronutrient deficiency leads to chlorosis and fruit drop.",
        "pest_management": "Citrus psylla (vector of Greening disease) and Leaf miner. Timely spray of systemic insecticides or horticultural oils.",
        "economic_outlook": "High steady commercial demand for fresh juice markets, canning, and regional export."
    },
    "papaya": {
        "display_name": "Papaya (Carica papaya)",
        "category": "Tropical Fruit Crop",
        "icon": "🍈",
        "season": "Year-round planting in frost-free tropical zones",
        "growth_duration": "Starts fruiting in 9-10 months, productive for 2-3 years",
        "water_need": "Moderate (Very susceptible to root rot in waterlogged conditions)",
        "soil_type": "Rich sandy loam or alluvial soil with high drainage capacity",
        "summary": "Extremely fast-producing tropical fruit rich in papain and vitamin A; requires frost-free warm temperatures and gentle irrigation.",
        "fertilizer_guide": "Continuous feeder: small doses of N, P, K applied monthly along with organic manure and micronutrients.",
        "pest_management": "Papaya Ringspot Virus (PRSV) and Mealybugs. Vector control (aphids) and planting gynodioecious hybrids (e.g. Red Lady).",
        "economic_outlook": "High yield volume per unit area, regular weekly harvest revenue, and strong market liquidity."
    },
    "coconut": {
        "display_name": "Coconut (Cocos nucifera)",
        "category": "Coastal Plantation Crop",
        "icon": "🥥",
        "season": "Perennial (Continuous monthly spathe opening and harvest)",
        "growth_duration": "Begins yielding in 5-6 years; productive for 60+ years",
        "water_need": "High (Requires humid air and consistent underground water table)",
        "soil_type": "Coastal sandy soil, red sandy loam, and alluvial delta soils",
        "summary": "The 'Kalpavriksha' (Tree of Heaven), sustaining rural coastal economies with oil, tender water, coir, and timber.",
        "fertilizer_guide": "High Potassium and Sodium chloride (common salt) tolerance. Apply balanced NPK + magnesium sulfate annually around the palm basin.",
        "pest_management": "Rhinoceros beetle and Red Palm Weevil. Place pheromone traps and treat leaf axils with neem cake and sand mixture.",
        "economic_outlook": "Highly diversified income from tender water, copra, cold-pressed virgin oil, and coir industries."
    },
    "cotton": {
        "display_name": "Cotton (Gossypium hirsutum)",
        "category": "Commercial Fiber Crop",
        "icon": "☁️",
        "season": "Kharif (April/May to December/January)",
        "growth_duration": "150 – 180 days",
        "water_need": "Medium (Requires dry sunny weather during boll opening)",
        "soil_type": "Deep black cotton soils (regur) with moisture retentive clays",
        "summary": "'White Gold', the backbone of the global textile industry; requires warm days, sunny boll-bursting period, and rich soils.",
        "fertilizer_guide": "High Nitrogen feeder; split applications with potassium to prevent premature senescence and leaf reddening.",
        "pest_management": "Pink Bollworm (PBW) and sucking pests (jassids, thrips). Install PBW pheromone traps, refuge crops, and follow IPM.",
        "economic_outlook": "Tremendous cash crop value with extensive spinning mills, ginning hubs, and export demand."
    },
    "jute": {
        "display_name": "Jute (Corchorus olitorius)",
        "category": "Commercial Fiber Crop",
        "icon": "🌾",
        "season": "Early Kharif (March – August)",
        "growth_duration": "120 – 135 days",
        "water_need": "High (Prefers high humidity, warm monsoonal showers, water for retting)",
        "soil_type": "New alluvial soils along river floodplains (silt loam)",
        "summary": "'Golden Fiber', an eco-friendly biodegradable commercial fiber grown predominantly in fertile river delta basins.",
        "fertilizer_guide": "Responds well to basal Nitrogen and Potassium. Green manuring prior to sowing improves fiber strength and fineness.",
        "pest_management": "Jute semilooper and yellow mite. Intermittent spraying with bio-pesticides and maintaining ditch aeration.",
        "economic_outlook": "Surging international demand for eco-friendly packaging, geotextiles, and biodegradable shopping bags."
    },
    "coffee": {
        "display_name": "Coffee (Coffea arabica / canephora)",
        "category": "Hill Plantation Crop",
        "icon": "☕",
        "season": "Perennial (Blossom showers in March–April, harvest Nov–Feb)",
        "growth_duration": "Harvested annually from established bushes (3-4 years old)",
        "water_need": "Medium to High (High ambient humidity with shade canopy)",
        "soil_type": "Deep volcanic or humic forest loams rich in decaying leaf mold (pH 6.0 – 6.5)",
        "summary": "Shade-grown plantation crop cultivated on scenic tropical slopes; requires misty climates, tree canopies, and well-aerated acid soil.",
        "fertilizer_guide": "Apply NPK in split pre-monsoon and post-monsoon doses. Regular leaf litter mulching enriches microbial activity.",
        "pest_management": "Coffee Berry Borer and White Stem Borer. Maintain optimum shade density (two-tier canopy) and sanitation.",
        "economic_outlook": "Premium export commodity traded on global futures exchanges with dedicated specialty cafe markets."
    }
}

# Pre-computed dataset benchmarks (Mean, Min, Max) for each crop
BENCHMARKS = {
    "apple": {"N": {"mean": 20.8, "min": 0.0, "max": 40.0}, "P": {"mean": 134.2, "min": 120.0, "max": 145.0}, "K": {"mean": 199.9, "min": 195.0, "max": 205.0}, "temperature": {"mean": 22.6, "min": 21.0, "max": 24.0}, "humidity": {"mean": 92.3, "min": 90.0, "max": 95.0}, "ph": {"mean": 5.9, "min": 5.5, "max": 6.5}, "rainfall": {"mean": 112.7, "min": 100.1, "max": 125.0}},
    "banana": {"N": {"mean": 100.2, "min": 80.0, "max": 120.0}, "P": {"mean": 82.0, "min": 70.0, "max": 95.0}, "K": {"mean": 50.0, "min": 45.0, "max": 55.0}, "temperature": {"mean": 27.4, "min": 25.0, "max": 30.0}, "humidity": {"mean": 80.4, "min": 75.0, "max": 85.0}, "ph": {"mean": 6.0, "min": 5.5, "max": 6.5}, "rainfall": {"mean": 104.6, "min": 90.1, "max": 119.8}},
    "blackgram": {"N": {"mean": 40.0, "min": 20.0, "max": 60.0}, "P": {"mean": 67.5, "min": 55.0, "max": 80.0}, "K": {"mean": 19.2, "min": 15.0, "max": 25.0}, "temperature": {"mean": 30.0, "min": 25.0, "max": 35.0}, "humidity": {"mean": 65.1, "min": 60.0, "max": 70.0}, "ph": {"mean": 7.1, "min": 6.5, "max": 7.8}, "rainfall": {"mean": 67.9, "min": 60.4, "max": 74.9}},
    "chickpea": {"N": {"mean": 40.1, "min": 20.0, "max": 60.0}, "P": {"mean": 67.8, "min": 55.0, "max": 80.0}, "K": {"mean": 79.9, "min": 75.0, "max": 85.0}, "temperature": {"mean": 18.9, "min": 17.0, "max": 21.0}, "humidity": {"mean": 16.9, "min": 14.3, "max": 20.0}, "ph": {"mean": 7.3, "min": 6.0, "max": 8.8}, "rainfall": {"mean": 80.1, "min": 65.1, "max": 94.7}},
    "coconut": {"N": {"mean": 22.0, "min": 0.0, "max": 40.0}, "P": {"mean": 16.9, "min": 5.0, "max": 30.0}, "K": {"mean": 30.6, "min": 25.0, "max": 35.0}, "temperature": {"mean": 27.4, "min": 25.0, "max": 30.0}, "humidity": {"mean": 94.8, "min": 90.0, "max": 100.0}, "ph": {"mean": 6.0, "min": 5.5, "max": 6.5}, "rainfall": {"mean": 175.7, "min": 131.1, "max": 225.6}},
    "coffee": {"N": {"mean": 101.2, "min": 80.0, "max": 120.0}, "P": {"mean": 28.7, "min": 15.0, "max": 40.0}, "K": {"mean": 29.9, "min": 25.0, "max": 35.0}, "temperature": {"mean": 25.5, "min": 23.1, "max": 28.0}, "humidity": {"mean": 58.9, "min": 50.0, "max": 70.0}, "ph": {"mean": 6.8, "min": 6.0, "max": 7.5}, "rainfall": {"mean": 158.1, "min": 115.2, "max": 199.5}},
    "cotton": {"N": {"mean": 117.8, "min": 100.0, "max": 140.0}, "P": {"mean": 46.2, "min": 35.0, "max": 60.0}, "K": {"mean": 19.6, "min": 15.0, "max": 25.0}, "temperature": {"mean": 24.0, "min": 22.0, "max": 26.0}, "humidity": {"mean": 79.8, "min": 75.0, "max": 85.0}, "ph": {"mean": 6.9, "min": 6.0, "max": 8.0}, "rainfall": {"mean": 80.4, "min": 60.1, "max": 100.0}},
    "grapes": {"N": {"mean": 23.2, "min": 0.0, "max": 40.0}, "P": {"mean": 132.5, "min": 120.0, "max": 145.0}, "K": {"mean": 200.1, "min": 195.0, "max": 205.0}, "temperature": {"mean": 23.8, "min": 8.8, "max": 42.0}, "humidity": {"mean": 81.9, "min": 80.0, "max": 84.0}, "ph": {"mean": 6.0, "min": 5.5, "max": 6.5}, "rainfall": {"mean": 69.6, "min": 65.0, "max": 75.0}},
    "jute": {"N": {"mean": 78.4, "min": 60.0, "max": 100.0}, "P": {"mean": 46.9, "min": 35.0, "max": 60.0}, "K": {"mean": 40.0, "min": 35.0, "max": 45.0}, "temperature": {"mean": 25.0, "min": 23.1, "max": 27.0}, "humidity": {"mean": 79.6, "min": 70.9, "max": 90.0}, "ph": {"mean": 6.7, "min": 6.0, "max": 7.4}, "rainfall": {"mean": 174.8, "min": 150.1, "max": 199.8}},
    "kidneybeans": {"N": {"mean": 20.8, "min": 0.0, "max": 40.0}, "P": {"mean": 67.5, "min": 55.0, "max": 80.0}, "K": {"mean": 20.0, "min": 15.0, "max": 25.0}, "temperature": {"mean": 20.1, "min": 15.3, "max": 25.0}, "humidity": {"mean": 21.6, "min": 18.1, "max": 25.0}, "ph": {"mean": 5.7, "min": 5.5, "max": 6.0}, "rainfall": {"mean": 105.9, "min": 60.3, "max": 149.7}},
    "lentil": {"N": {"mean": 18.8, "min": 0.0, "max": 40.0}, "P": {"mean": 68.4, "min": 55.0, "max": 80.0}, "K": {"mean": 19.4, "min": 15.0, "max": 25.0}, "temperature": {"mean": 24.5, "min": 18.0, "max": 30.0}, "humidity": {"mean": 64.8, "min": 60.0, "max": 70.0}, "ph": {"mean": 6.9, "min": 6.0, "max": 7.8}, "rainfall": {"mean": 45.7, "min": 35.0, "max": 55.0}},
    "maize": {"N": {"mean": 77.8, "min": 60.0, "max": 100.0}, "P": {"mean": 48.4, "min": 35.0, "max": 60.0}, "K": {"mean": 19.8, "min": 15.0, "max": 25.0}, "temperature": {"mean": 22.4, "min": 18.0, "max": 26.5}, "humidity": {"mean": 65.1, "min": 55.3, "max": 75.0}, "ph": {"mean": 6.2, "min": 5.5, "max": 7.0}, "rainfall": {"mean": 84.8, "min": 60.7, "max": 109.8}},
    "mango": {"N": {"mean": 20.1, "min": 0.0, "max": 40.0}, "P": {"mean": 27.2, "min": 15.0, "max": 40.0}, "K": {"mean": 29.9, "min": 25.0, "max": 35.0}, "temperature": {"mean": 31.2, "min": 27.1, "max": 36.0}, "humidity": {"mean": 50.2, "min": 45.1, "max": 55.0}, "ph": {"mean": 5.8, "min": 4.5, "max": 7.0}, "rainfall": {"mean": 94.7, "min": 89.3, "max": 100.8}},
    "mothbeans": {"N": {"mean": 21.4, "min": 0.0, "max": 40.0}, "P": {"mean": 48.0, "min": 35.0, "max": 60.0}, "K": {"mean": 20.2, "min": 15.0, "max": 25.0}, "temperature": {"mean": 28.2, "min": 24.0, "max": 32.0}, "humidity": {"mean": 53.2, "min": 40.0, "max": 65.0}, "ph": {"mean": 6.8, "min": 3.5, "max": 9.9}, "rainfall": {"mean": 51.2, "min": 30.9, "max": 74.5}},
    "mungbean": {"N": {"mean": 21.0, "min": 0.0, "max": 40.0}, "P": {"mean": 47.3, "min": 35.0, "max": 60.0}, "K": {"mean": 19.9, "min": 15.0, "max": 25.0}, "temperature": {"mean": 28.5, "min": 27.0, "max": 30.0}, "humidity": {"mean": 85.5, "min": 80.0, "max": 90.0}, "ph": {"mean": 6.7, "min": 6.2, "max": 7.2}, "rainfall": {"mean": 48.4, "min": 36.0, "max": 59.9}},
    "muskmelon": {"N": {"mean": 100.3, "min": 80.0, "max": 120.0}, "P": {"mean": 17.7, "min": 5.0, "max": 30.0}, "K": {"mean": 50.1, "min": 45.0, "max": 55.0}, "temperature": {"mean": 28.7, "min": 27.0, "max": 30.0}, "humidity": {"mean": 92.3, "min": 90.0, "max": 95.0}, "ph": {"mean": 6.4, "min": 6.0, "max": 6.8}, "rainfall": {"mean": 24.7, "min": 20.2, "max": 29.9}},
    "orange": {"N": {"mean": 19.6, "min": 0.0, "max": 40.0}, "P": {"mean": 16.6, "min": 5.0, "max": 30.0}, "K": {"mean": 10.0, "min": 5.0, "max": 15.0}, "temperature": {"mean": 22.8, "min": 10.0, "max": 35.0}, "humidity": {"mean": 92.2, "min": 90.0, "max": 95.0}, "ph": {"mean": 7.0, "min": 6.0, "max": 8.0}, "rainfall": {"mean": 110.5, "min": 100.2, "max": 119.7}},
    "papaya": {"N": {"mean": 49.9, "min": 31.0, "max": 70.0}, "P": {"mean": 59.0, "min": 46.0, "max": 70.0}, "K": {"mean": 50.0, "min": 45.0, "max": 55.0}, "temperature": {"mean": 33.7, "min": 23.0, "max": 43.7}, "humidity": {"mean": 92.4, "min": 90.0, "max": 95.0}, "ph": {"mean": 6.7, "min": 6.5, "max": 7.0}, "rainfall": {"mean": 142.6, "min": 40.4, "max": 248.9}},
    "pigeonpeas": {"N": {"mean": 20.7, "min": 0.0, "max": 40.0}, "P": {"mean": 67.7, "min": 55.0, "max": 80.0}, "K": {"mean": 20.3, "min": 15.0, "max": 25.0}, "temperature": {"mean": 27.7, "min": 18.3, "max": 37.0}, "humidity": {"mean": 48.1, "min": 30.6, "max": 69.7}, "ph": {"mean": 5.8, "min": 4.5, "max": 7.4}, "rainfall": {"mean": 149.5, "min": 90.1, "max": 198.8}},
    "pomegranate": {"N": {"mean": 18.9, "min": 0.0, "max": 40.0}, "P": {"mean": 18.8, "min": 5.0, "max": 30.0}, "K": {"mean": 40.2, "min": 35.0, "max": 45.0}, "temperature": {"mean": 21.8, "min": 18.1, "max": 25.0}, "humidity": {"mean": 90.1, "min": 85.1, "max": 95.0}, "ph": {"mean": 6.4, "min": 5.6, "max": 7.2}, "rainfall": {"mean": 107.5, "min": 102.5, "max": 112.5}},
    "rice": {"N": {"mean": 79.9, "min": 60.0, "max": 100.0}, "P": {"mean": 47.6, "min": 35.0, "max": 60.0}, "K": {"mean": 39.9, "min": 35.0, "max": 45.0}, "temperature": {"mean": 23.7, "min": 20.0, "max": 27.0}, "humidity": {"mean": 82.3, "min": 80.1, "max": 85.0}, "ph": {"mean": 6.4, "min": 5.0, "max": 7.8}, "rainfall": {"mean": 236.2, "min": 182.5, "max": 298.6}},
    "watermelon": {"N": {"mean": 99.4, "min": 80.0, "max": 120.0}, "P": {"mean": 17.0, "min": 5.0, "max": 30.0}, "K": {"mean": 50.2, "min": 45.0, "max": 55.0}, "temperature": {"mean": 25.6, "min": 24.0, "max": 27.0}, "humidity": {"mean": 85.2, "min": 80.0, "max": 90.0}, "ph": {"mean": 6.5, "min": 6.0, "max": 7.0}, "rainfall": {"mean": 50.8, "min": 40.0, "max": 60.0}}
}

# Standard Farm & Soil Presets for realistic quick-testing
PRESETS = [
    {
        "id": "rice_paddy",
        "name": "Indo-Gangetic Rice Paddy",
        "badge": "Monsoon Wetland",
        "description": "Fertile alluvial basin with high nitrogen, humid monsoon warmth, and heavy seasonal rainfall.",
        "values": {"N": 90, "P": 45, "K": 40, "temperature": 24.5, "humidity": 83, "ph": 6.5, "rainfall": 220}
    },
    {
        "id": "cotton_black",
        "name": "Deccan Black Soil Cotton Field",
        "badge": "Regur Clay Belt",
        "description": "Deep black soils with heavy nitrogen feeding, warm semi-arid conditions, and moderate showers.",
        "values": {"N": 120, "P": 48, "K": 20, "temperature": 25.0, "humidity": 78, "ph": 7.0, "rainfall": 82}
    },
    {
        "id": "apple_orchard",
        "name": "Himalayan Apple Orchard",
        "badge": "Temperate Hill",
        "description": "High altitude temperate loam rich in potassium and phosphorus with cool weather and mist.",
        "values": {"N": 22, "P": 132, "K": 198, "temperature": 22.0, "humidity": 92, "ph": 5.9, "rainfall": 110}
    },
    {
        "id": "coffee_plantation",
        "name": "Western Ghats Coffee Estate",
        "badge": "Tropical Highland",
        "description": "Highland forest loam rich in organic leaf litter, pleasant climate, and reliable pre-monsoon showers.",
        "values": {"N": 100, "P": 30, "K": 30, "temperature": 25.5, "humidity": 60, "ph": 6.7, "rainfall": 160}
    },
    {
        "id": "chickpea_pulse",
        "name": "Semi-Arid Pulse Field (Chickpea)",
        "badge": "Dryland Rabi",
        "description": "Dryland rabi pulse plot with lower atmospheric humidity, cool night temps, and balanced potassium.",
        "values": {"N": 40, "P": 65, "K": 80, "temperature": 19.0, "humidity": 18, "ph": 7.2, "rainfall": 78}
    },
    {
        "id": "watermelon_zaid",
        "name": "Riverbed Watermelon Patch",
        "badge": "Summer Zaid",
        "description": "Well-drained warm sandy loam with good nitrogen, sunny summer climate, and controlled watering.",
        "values": {"N": 100, "P": 18, "K": 50, "temperature": 26.5, "humidity": 85, "ph": 6.5, "rainfall": 50}
    }
]

def generate_crop_advisory(crop_name, user_inputs):
    """
    Compares the user's soil & environmental inputs against the benchmarks for the predicted crop,
    generating targeted agronomic feedback and fertilizer recommendations.
    """
    crop_name = crop_name.lower().strip()
    profile = CROP_PROFILES.get(crop_name, {
        "display_name": crop_name.title(),
        "category": "Agricultural Crop",
        "icon": "🌱",
        "season": "Standard Agricultural Season",
        "growth_duration": "90 – 120 days",
        "water_need": "Moderate",
        "soil_type": "Well-drained fertile loam",
        "summary": "Suitable for cultivation based on current soil and climate profile.",
        "fertilizer_guide": "Apply balanced N-P-K according to regional agricultural extension recommendations.",
        "pest_management": "Follow standard Integrated Pest Management (IPM) practices.",
        "economic_outlook": "Dependable market crop with regular wholesale liquidity."
    })
    
    benchmark = BENCHMARKS.get(crop_name, {})
    
    analysis = []
    
    # Nitrogen Analysis
    user_n = user_inputs.get("N", 0)
    if "N" in benchmark:
        b = benchmark["N"]
        if user_n < b["min"]:
            analysis.append({
                "param": "Nitrogen (N)",
                "status": "Low",
                "badge_class": "status-warning",
                "message": f"Your soil Nitrogen ({user_n:.1f} kg/ha) is below optimal ({b['min']:.0f} - {b['max']:.0f} kg/ha). Apply urea (46% N) in split doses or well-rotted farmyard manure (FYM) before sowing."
            })
        elif user_n > b["max"]:
            analysis.append({
                "param": "Nitrogen (N)",
                "status": "High",
                "badge_class": "status-warning",
                "message": f"Nitrogen is on the higher side ({user_n:.1f} kg/ha). Excess N can cause excessive vegetative growth and lodging. Restrict synthetic nitrogen applications."
            })
        else:
            analysis.append({
                "param": "Nitrogen (N)",
                "status": "Optimal",
                "badge_class": "status-success",
                "message": f"Soil Nitrogen is well-aligned ({user_n:.1f} kg/ha) with {profile['display_name']}'s baseline requirements."
            })
            
    # Phosphorus Analysis
    user_p = user_inputs.get("P", 0)
    if "P" in benchmark:
        b = benchmark["P"]
        if user_p < b["min"]:
            analysis.append({
                "param": "Phosphorus (P)",
                "status": "Low",
                "badge_class": "status-warning",
                "message": f"Phosphorus is deficient ({user_p:.1f} kg/ha vs ideal {b['min']:.0f}-{b['max']:.0f} kg/ha). Incorporate Single Super Phosphate (SSP) or DAP into the root zone during land preparation."
            })
        elif user_p > b["max"]:
            analysis.append({
                "param": "Phosphorus (P)",
                "status": "High",
                "badge_class": "status-info",
                "message": f"Phosphorus reserve ({user_p:.1f} kg/ha) is abundant. No supplemental phosphate is needed for this cycle."
            })
        else:
            analysis.append({
                "param": "Phosphorus (P)",
                "status": "Optimal",
                "badge_class": "status-success",
                "message": f"Phosphorus level is ideal for robust root establishment and energy transfer."
            })
            
    # Potassium Analysis
    user_k = user_inputs.get("K", 0)
    if "K" in benchmark:
        b = benchmark["K"]
        if user_k < b["min"]:
            analysis.append({
                "param": "Potassium (K)",
                "status": "Low",
                "badge_class": "status-warning",
                "message": f"Potassium is low ({user_k:.1f} kg/ha vs benchmark {b['min']:.0f}-{b['max']:.0f} kg/ha). Apply Muriate of Potash (MOP) to boost disease resistance and crop yield quality."
            })
        elif user_k > b["max"]:
            analysis.append({
                "param": "Potassium (K)",
                "status": "High",
                "badge_class": "status-info",
                "message": f"Potassium is well-supplied ({user_k:.1f} kg/ha). Retain current potash management."
            })
        else:
            analysis.append({
                "param": "Potassium (K)",
                "status": "Optimal",
                "badge_class": "status-success",
                "message": f"Potassium level is optimal for stem rigidity and drought adaptation."
            })
            
    # pH Analysis
    user_ph = user_inputs.get("ph", 7.0)
    if user_ph < 5.8:
        analysis.append({
            "param": "Soil pH",
            "status": "Acidic",
            "badge_class": "status-danger",
            "message": f"Soil pH ({user_ph:.2f}) is moderately acidic. Consider broadcast application of agricultural lime (calcium carbonate) or dolomite to sweeten the soil."
        })
    elif user_ph > 7.6:
        analysis.append({
            "param": "Soil pH",
            "status": "Alkaline",
            "badge_class": "status-warning",
            "message": f"Soil pH ({user_ph:.2f}) is moderately alkaline. Apply gypsum, composted green manure, or elemental sulfur to improve nutrient availability."
        })
    else:
        analysis.append({
            "param": "Soil pH",
            "status": "Neutral / Balanced",
            "badge_class": "status-success",
            "message": f"Soil pH ({user_ph:.2f}) is in the sweet spot for microbiological activity and nutrient bioavailability."
        })
        
    # Rainfall & Irrigation Analysis
    user_rain = user_inputs.get("rainfall", 100)
    if "rainfall" in benchmark:
        b = benchmark["rainfall"]
        if user_rain < b["min"] * 0.8:
            analysis.append({
                "param": "Rainfall / Water",
                "status": "Deficit",
                "badge_class": "status-warning",
                "message": f"Recorded rainfall ({user_rain:.1f} mm) is less than typical requirement ({b['mean']:.0f} mm). Plan for supplemental drip, sprinkler, or canal irrigation cycles."
            })
        elif user_rain > b["max"] * 1.2:
            analysis.append({
                "param": "Rainfall / Water",
                "status": "Excess",
                "badge_class": "status-warning",
                "message": f"High rainfall recorded ({user_rain:.1f} mm). Ensure raised beds or ridge-and-furrow drainage to avoid water stagnation."
            })
        else:
            analysis.append({
                "param": "Rainfall / Water",
                "status": "Sufficient",
                "badge_class": "status-success",
                "message": f"Rainfall pattern ({user_rain:.1f} mm) provides adequate moisture for cultivation."
            })
            
    return {
        "profile": profile,
        "benchmark": benchmark,
        "soil_analysis": analysis
    }
