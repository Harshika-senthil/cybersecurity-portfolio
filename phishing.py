import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("dataset.csv")

# Feature extraction function
def extract_features(url):
    return [
        len(url),                          # length of URL
        url.count('-'),                    # number of hyphens
        url.count('.'),                    # number of dots
        1 if "https" in url else 0,        # https or not
        1 if "login" in url or "verify" in url or "bank" in url else 0
    ]

# Apply feature extraction
X = data['url'].apply(extract_features).tolist()
y = data['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Test with user input
url = input("Enter URL to check: ")
features = [extract_features(url)]

prediction = model.predict(features)

if prediction[0] == 1:
    print("⚠️ This URL is likely PHISHING!")
else:
    print("✅ This URL is SAFE!") 