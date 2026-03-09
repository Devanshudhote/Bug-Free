import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import joblib
import os

print("🚀 Starting Model Training for TruthShield AI...")

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_CSV = os.path.join(BASE_DIR, "kaggle_fake_train.csv")
TEST_CSV = os.path.join(BASE_DIR, "kaggle_fake_test.csv")

if not os.path.exists(TRAIN_CSV):
    print(f"❌ Error: {TRAIN_CSV} not found!")
    exit(1)

# 1. Load Data
print("\n📊 Loading datasets...")
df_train = pd.read_csv(TRAIN_CSV)

print(f"Original train shape: {df_train.shape}")

# 2. Preprocessing
print("🧹 Preprocessing data...")
# Combine title and text for better context, fill NaNs with empty strings
df_train['title'] = df_train['title'].fillna('')
df_train['text'] = df_train['text'].fillna('')
df_train['content'] = df_train['title'] + " " + df_train['text']

# The Kaggle dataset can have empty contents, let's filter out completely empty ones
df_train = df_train[df_train['content'].str.strip() != '']
print(f"Cleaned train shape: {df_train.shape}")

X = df_train['content']
y = df_train['label'] # 1 is FAKE, 0 is REAL

# Split into train and validation sets (80/20)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 3. Vectorization (TF-IDF)
print("\n🔤 Vectorizing text (TF-IDF)...")
vectorizer = TfidfVectorizer(max_features=50000, lowercase=True, stop_words='english', ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)

# 4. Model Training
print("🧠 Training Logistic Regression model...")
model = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
model.fit(X_train_vec, y_train)

# 5. Evaluation
print("\n📈 Evaluating on Validation Set...")
y_pred = model.predict(X_val_vec)
acc = accuracy_score(y_val, y_pred)
print(f"Validation Accuracy: {acc:.4f}")
print("Classification Report:")
print(classification_report(y_val, y_pred, target_names=["REAL (0)", "FAKE (1)"]))

# 6. Save Artifacts
print("\n💾 Saving model & vectorizer to disk...")
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")
VEC_PATH = os.path.join(BASE_DIR, "vectorizer.joblib")

joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VEC_PATH)

print(f"✅ Saved to: \n - {MODEL_PATH}\n - {VEC_PATH}")
print("\n🎉 Training Complete!")
