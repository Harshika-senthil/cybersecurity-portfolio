from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

# Load dataset
data = pd.read_csv("dataset.csv")

# Feature extraction
def extract_features(url):
    return [
        len(url),
        url.count('-'),
        url.count('.'),
        1 if "https" in url else 0,
        1 if any(word in url for word in ["login", "verify", "bank"]) else 0
    ]

# Train model
X = data['url'].apply(extract_features).tolist()
y = data['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
# Home page
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        url = request.form["url"]
        features = [extract_features(url)]
        prediction = model.predict(features)

        if prediction[0] == 1:
            result = "⚠️ Phishing Website!"
        else:
            result = "✅ Safe Website"

    return render_template("index.html", result=result, accuracy=round(accuracy*100, 2))

if __name__ == "__main__":
    app.run(debug=True)