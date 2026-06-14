# ============================================================
#  knowledge_base.py  —  All 22 crops fully filled
# ============================================================

CROP_INFO = {
    "rice":        {"water":"High",   "duration":"3-4 months",     "fertilizers":["Urea (N)","SSP (P)","Potash (K)"],           "season":"Kharif",        "icon":"🍚"},
    "maize":       {"water":"Medium", "duration":"3-4 months",     "fertilizers":["Urea (N)","DAP (P+N)","Zinc Sulfate"],       "season":"Kharif / Rabi", "icon":"🌽"},
    "chickpea":    {"water":"Low",    "duration":"3-4 months",     "fertilizers":["DAP (P+N)","MOP (K)","Zinc Sulfate"],        "season":"Rabi",          "icon":"🫘"},
    "kidneybeans": {"water":"Medium", "duration":"3-4 months",     "fertilizers":["Rhizobium (bio)","SSP (P)","MOP (K)"],       "season":"Kharif",        "icon":"🫘"},
    "pigeonpeas":  {"water":"Low",    "duration":"5-6 months",     "fertilizers":["Rhizobium (bio)","SSP (P)","MOP (K)"],       "season":"Kharif",        "icon":"🫘"},
    "mothbeans":   {"water":"Low",    "duration":"2-3 months",     "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Kharif",        "icon":"🫘"},
    "mungbean":    {"water":"Low",    "duration":"2-3 months",     "fertilizers":["Rhizobium (bio)","SSP (P)","MOP (K)"],       "season":"Kharif / Zaid", "icon":"🫘"},
    "blackgram":   {"water":"Low",    "duration":"3-4 months",     "fertilizers":["Rhizobium (bio)","DAP (P+N)","MOP (K)"],     "season":"Kharif",        "icon":"🫘"},
    "lentil":      {"water":"Low",    "duration":"4-5 months",     "fertilizers":["DAP (P+N)","MOP (K)","Sulfur"],              "season":"Rabi",          "icon":"🫘"},
    "pomegranate": {"water":"Low",    "duration":"5-7 months",     "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Perennial",     "icon":"🍎"},
    "banana":      {"water":"High",   "duration":"10-12 months",   "fertilizers":["Urea (N)","MOP (K)","Magnesium Sulfate"],    "season":"Perennial",     "icon":"🍌"},
    "mango":       {"water":"Medium", "duration":"3-5 months",     "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Perennial",     "icon":"🥭"},
    "grapes":      {"water":"Medium", "duration":"4-6 months",     "fertilizers":["Urea (N)","SSP (P)","Potash"],               "season":"Perennial",     "icon":"🍇"},
    "watermelon":  {"water":"Medium", "duration":"2-3 months",     "fertilizers":["Urea (N)","DAP (P+N)","MOP (K)"],            "season":"Zaid / Summer", "icon":"🍉"},
    "muskmelon":   {"water":"Medium", "duration":"2-3 months",     "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Zaid / Summer", "icon":"🍈"},
    "apple":       {"water":"Medium", "duration":"4-6 months",     "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Perennial",     "icon":"🍏"},
    "orange":      {"water":"Medium", "duration":"7-8 months",     "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Perennial",     "icon":"🍊"},
    "papaya":      {"water":"Medium", "duration":"9-11 months",    "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Perennial",     "icon":"🍈"},
    "coconut":     {"water":"High",   "duration":"12 months+",     "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Perennial",     "icon":"🥥"},
    "cotton":      {"water":"High",   "duration":"5-6 months",     "fertilizers":["CAN (N)","SSP (P)","MOP (K)"],               "season":"Kharif",        "icon":"🌿"},
    "jute":        {"water":"High",   "duration":"4-5 months",     "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Kharif",        "icon":"🌿"},
    "coffee":      {"water":"High",   "duration":"9-11 months",    "fertilizers":["Urea (N)","SSP (P)","MOP (K)"],              "season":"Perennial",     "icon":"☕"},
}

MARKET_PRICE = {
    "rice":        "₹2,183/qtl",
    "maize":       "₹1,962/qtl",
    "chickpea":    "₹5,440/qtl",
    "kidneybeans": "₹4,500/qtl",
    "pigeonpeas":  "₹7,000/qtl",
    "mothbeans":   "₹4,600/qtl",
    "mungbean":    "₹8,558/qtl",
    "blackgram":   "₹6,950/qtl",
    "lentil":      "₹6,425/qtl",
    "pomegranate": "₹8,000/qtl",
    "banana":      "₹1,500/qtl",
    "mango":       "₹3,000/qtl",
    "grapes":      "₹5,000/qtl",
    "watermelon":  "₹800/qtl",
    "muskmelon":   "₹1,200/qtl",
    "apple":       "₹10,000/qtl",
    "orange":      "₹3,500/qtl",
    "papaya":      "₹1,500/qtl",
    "coconut":     "₹2,000/qtl",
    "cotton":      "₹6,380/qtl",
    "jute":        "₹4,750/qtl",
    "coffee":      "₹19,200/qtl",
}

OPTIMAL_NPK = {
    "rice":        {"N":(80,120),  "P":(40,60),  "K":(40,60)},
    "maize":       {"N":(80,100),  "P":(40,60),  "K":(40,60)},
    "chickpea":    {"N":(20,40),   "P":(60,80),  "K":(40,60)},
    "kidneybeans": {"N":(20,40),   "P":(60,80),  "K":(20,40)},
    "pigeonpeas":  {"N":(20,40),   "P":(60,80),  "K":(20,40)},
    "mothbeans":   {"N":(20,40),   "P":(40,60),  "K":(20,40)},
    "mungbean":    {"N":(20,40),   "P":(40,60),  "K":(20,40)},
    "blackgram":   {"N":(20,40),   "P":(40,60),  "K":(20,40)},
    "lentil":      {"N":(20,40),   "P":(40,60),  "K":(20,40)},
    "pomegranate": {"N":(20,40),   "P":(10,30),  "K":(40,60)},
    "banana":      {"N":(100,140), "P":(75,100), "K":(50,70)},
    "mango":       {"N":(20,40),   "P":(10,20),  "K":(30,50)},
    "grapes":      {"N":(20,40),   "P":(10,30),  "K":(20,40)},
    "watermelon":  {"N":(100,120), "P":(50,70),  "K":(50,70)},
    "muskmelon":   {"N":(100,120), "P":(50,70),  "K":(50,70)},
    "apple":       {"N":(20,40),   "P":(120,140),"K":(200,220)},
    "orange":      {"N":(20,40),   "P":(10,30),  "K":(20,40)},
    "papaya":      {"N":(50,80),   "P":(50,70),  "K":(50,70)},
    "coconut":     {"N":(20,40),   "P":(10,30),  "K":(50,70)},
    "cotton":      {"N":(115,140), "P":(45,65),  "K":(70,90)},
    "jute":        {"N":(80,100),  "P":(40,60),  "K":(40,60)},
    "coffee":      {"N":(20,40),   "P":(30,50),  "K":(30,50)},
}


def get_fertilizer_advice(N, P, K, crop=None):
    advice = []
    if crop and crop in OPTIMAL_NPK:
        opt = OPTIMAL_NPK[crop]
        n_lo, n_hi = opt["N"]
        p_lo, p_hi = opt["P"]
        k_lo, k_hi = opt["K"]
        if N < n_lo:
            advice.append(f"Urea — Nitrogen low ({N} vs optimal {n_lo}-{n_hi} kg/ha)")
        elif N > n_hi:
            advice.append(f"Reduce N inputs — Nitrogen excess ({N} vs optimal {n_lo}-{n_hi} kg/ha)")
        if P < p_lo:
            advice.append(f"DAP / SSP — Phosphorus low ({P} vs optimal {p_lo}-{p_hi} kg/ha)")
        elif P > p_hi:
            advice.append(f"Skip P fertilizer — Phosphorus sufficient")
        if K < k_lo:
            advice.append(f"MOP / Potash — Potassium low ({K} vs optimal {k_lo}-{k_hi} kg/ha)")
        elif K > k_hi:
            advice.append(f"Reduce K inputs — Potassium excess")
    else:
        if N < 50: advice.append("Urea — Nitrogen is low")
        if P < 30: advice.append("DAP — Phosphorus is low")
        if K < 30: advice.append("MOP — Potassium is low")

    if not advice:
        advice.append("NPK is optimal — use compost / FYM to maintain soil health")
    return advice


def get_water_need(crop, rainfall_mm):
    base = CROP_INFO.get(crop, {}).get("water", "Medium")
    if rainfall_mm > 150 and base == "High":
        return "Medium (rain sufficient)"
    if rainfall_mm > 100 and base == "Medium":
        return "Low (rain sufficient)"
    if rainfall_mm < 40  and base == "Low":
        return "Medium (irrigation needed)"
    return base
