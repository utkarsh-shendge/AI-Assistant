import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import os

# Load dataset
data = pd.read_csv("intents.csv")

X = data["text"]
y = data["intent"]

# Convert text to numbers
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train Naive Bayes model
model = MultinomialNB()
model.fit(X_vec, y)

# Save model
os.makedirs("model", exist_ok=True)
pickle.dump(model, open("model/intent_model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

print("✅ ML model trained and saved successfully")