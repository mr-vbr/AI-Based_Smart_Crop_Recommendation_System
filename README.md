# 🌾 AI-Based Smart Crop Recommendation System
### Using Real-Time Weather and Market Analysis

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4+-orange?style=for-the-badge&logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=for-the-badge&logo=streamlit)
![Accuracy](https://img.shields.io/badge/Accuracy-98.18%25-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)

---

## 📌 About the Project

An intelligent AI-powered decision support system designed to help
Indian farmers select the most suitable and profitable crops based
on their soil conditions, real-time weather data, and live market
prices. The system eliminates the guesswork in crop selection by
combining Machine Learning with agronomic domain knowledge and
real-time API integration.

---

## 🎯 Key Features

| Feature | Description |
|---|---|
| 🤖 ML Prediction | Random Forest Classifier with 98.18% accuracy |
| 🏆 Top 3 Crops | Gold / Silver / Bronze ranked recommendations |
| 🌤️ Live Weather | OpenWeather API + wttr.in scrape + city defaults |
| 💰 Market Prices | Live web scraping + MSP fallback database |
| 🌱 Fertilizer Advice | Dynamic NPK deficiency analysis per crop |
| 💧 Water Guidance | Rainfall-adjusted irrigation estimation |
| 💬 Smart Chatbot | 12+ agricultural query intents |
| 📊 Confidence Score | Normalized suitability scale per crop |

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.9+ |
| ML Algorithm | Random Forest Classifier (scikit-learn) |
| Web Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Web Scraping | BeautifulSoup4, Requests |
| Weather Data | OpenWeather API |
| Model Storage | Pickle |
| Version Control | Git & GitHub |

---

## 📊 Model Performance

| Metric | Value |
|---|---|
| Test Accuracy | **98.18%** |
| 5-Fold CV Accuracy | **97.9% ± 0.4%** |
| Precision (Weighted) | 0.982 |
| Recall (Weighted) | 0.982 |
| F1-Score (Weighted) | 0.982 |
| Algorithm | Random Forest |
| Number of Trees | 200 |
| Training Samples | 2,200 |
| Number of Crops | 22 |

---

## 🌾 22 Supported Crops

---

## ⚙️ Installation & Setup

### Step 1 — Clone the repository
```bash
git clone https://github.com/mr-vbr/AI-Based_Smart_Crop_Recommendation_System.git
cd AI-Based_Smart_Crop_Recommendation_System
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Train the model
```bash
python train_model.py
```

### Step 4 — Run the application
```bash
streamlit run app.py
```

### Step 5 — Open in browser

http://localhost:8501


---

## 🔑 OpenWeather API Key (Optional)

1. Go to [openweathermap.org](https://openweathermap.org)
2. Sign up for free account
3. Go to **My API Keys** → copy your key
4. Paste it in the **sidebar** of the running app

> ✅ Without API key — system automatically falls back
> to wttr.in scraping, then city default values.
> The app always works even without an API key.

---

## 📁 Project Structure

AI-Based_Smart_Crop_Recommendation_System/

│

├── app.py                 # Main Streamlit web application

├── train_model.py         # ML model training script

├── knowledge_base.py      # Crop knowledge & rules database

├── requirements.txt       # Python dependencies

├── crop_data.csv          # Training dataset (22 crops)

├── README.md              # Project documentation

├── .gitignore             # Git ignore rules

└── screenshots/           # Application screenshots

├── home.png

├── crop_cards.png

├── market.png

└── chatbot.png

---

## 🔬 System Architecture
┌─────────────────────────────────────┐

│         USER INPUT LAYER            │

│   N, P, K, pH, City/Location        │

└────────────────┬────────────────────┘

┌────────────────▼────────────────────┐

│      DATA INTEGRATION LAYER         │

│  OpenWeather API → wttr.in → Defaults│

└────────────────┬────────────────────┘

┌────────────────▼────────────────────┐

│       ML PROCESSING LAYER           │

│  Random Forest → predict_proba()    │

│  → Top 3 Crops + Confidence Scores  │

└────────────────┬────────────────────┘

┌────────────────▼────────────────────┐

│       INTELLIGENCE LAYER            │

│  Fertilizer + Water + Market + Chat │

└────────────────┬────────────────────

┌────────────────▼────────────────────┐

│     STREAMLIT OUTPUT LAYER          │

│  Premium UI + Chatbot Interface     │

└─────────────────────────────────────┘

---

## 👥 Team

| Name | Register Number | Role |
|---|---|---|
| Bharath V | 211423205047 | ML Model + Backend |
| Bharath S | 211423205046 | Data Pipeline + API |
| Arunkumar B | 211423205040 | UI + Integration |

**Institution :** Panimalar Engineering College  
**Department  :** Information Technology  
**Batch       :** 2023 – 2027  

---

## 📜 License

This project is licensed under the
**Apache License 2.0** — see the
[LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Pull requests are welcome. For major changes,
please open an issue first to discuss what
you would like to change.

---

## ⭐ Show Your Support

If this project helped you or you found it
interesting, please consider giving it a
**⭐ Star** on GitHub — it means a lot to us!

---

*Built with ❤️ for Indian Farmers*
