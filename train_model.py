# ============================================================
#  train_model.py  —  Train & save the Random Forest model
#  Fixes: class imbalance, overfitting, cross-validation
#  Run ONCE: python train_model.py
# ============================================================

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report
import pickle

# ── Load dataset ─────────────────────────────────────────────
print("=" * 55)
print("  SMART CROP RECOMMENDATION — MODEL TRAINING")
print("=" * 55)

df = pd.read_csv("crop_data.csv")
df.columns = df.columns.str.strip().str.lower()
df["label"] = df["label"].str.strip().str.lower()

print(f"\nDataset shape : {df.shape}")
print(f"Unique crops  : {df['label'].nunique()}")
print(f"\nClass distribution:\n{df['label'].value_counts().to_string()}")

counts    = df["label"].value_counts()
imbalance = counts.max() / counts.min()
print(f"\nImbalance ratio: {imbalance:.2f}x")
if imbalance > 2:
    print("WARNING: Imbalance detected — using class_weight='balanced'")

# ── Features & target ────────────────────────────────────────
FEATURES = ["n", "p", "k", "temperature", "humidity", "ph", "rainfall"]
X = df[FEATURES]
y = df["label"]

# ── Train / test split ────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"\nTraining: {len(X_train)} | Testing: {len(X_test)}")

# ── Train Random Forest (with all fixes applied) ──────────────
print("\nTraining Random Forest...")
model = RandomForestClassifier(
    n_estimators=200,        # more trees = more stable predictions
    max_depth=15,            # prevents overfitting
    min_samples_split=4,     # prevents overfitting
    min_samples_leaf=2,      # prevents overfitting
    max_features="sqrt",     # standard for classification
    class_weight="balanced", # FIXES muskmelon / imbalance bias
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────
y_pred = model.predict(X_test)
acc    = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy : {acc * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ── Cross-validation ──────────────────────────────────────────
cv     = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring="accuracy", n_jobs=-1)
print(f"5-Fold CV Accuracy: {scores.mean()*100:.2f}% ± {scores.std()*100:.2f}%")

# ── Feature importance ────────────────────────────────────────
print("\nFeature importances:")
for feat, imp in sorted(zip(FEATURES, model.feature_importances_), key=lambda x: -x[1]):
    print(f"  {feat:<14} {'█' * int(imp*50)}  {imp:.4f}")

# ── Sanity check ─────────────────────────────────────────────
print("\nSanity check predictions:")
samples = [
    {"n":90,  "p":42,  "k":43,  "temperature":21, "humidity":82, "ph":6.5, "rainfall":203},
    {"n":20,  "p":130, "k":200, "temperature":16, "humidity":58, "ph":5.5, "rainfall":58},
    {"n":60,  "p":55,  "k":44,  "temperature":27, "humidity":65, "ph":7.0, "rainfall":85},
]
for s in samples:
    row   = pd.DataFrame([s])
    pred  = model.predict(row)[0]
    proba = model.predict_proba(row)[0]
    top3  = [(model.classes_[i], round(proba[i]*100,1))
             for i in proba.argsort()[-3:][::-1]]
    print(f"  N={s['n']} P={s['p']} K={s['k']} pH={s['ph']} => {pred} | Top3: {top3}")

# ── Save ──────────────────────────────────────────────────────
with open("model.pkl", "wb") as f:
    pickle.dump({
        "model":    model,
        "features": FEATURES,
        "classes":  list(model.classes_),
        "accuracy": round(acc * 100, 2),
        "cv_mean":  round(scores.mean() * 100, 2),
    }, f)

print(f"\nmodel.pkl saved! Classes: {list(model.classes_)}")
print("Run: streamlit run app.py")
print("=" * 55)
