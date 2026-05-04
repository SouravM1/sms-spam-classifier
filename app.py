import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# 🔥 FIX (VERY IMPORTANT)
nltk.download('stopwords')

# Initialize
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Text preprocessing
def transform_text(text):
    text = text.lower()
    words = text.split()

    # Remove non-alphanumeric
    words = [word for word in words if word.isalnum()]

    # Remove stopwords & punctuation
    words = [word for word in words if word not in stop_words and word not in string.punctuation]

    # Stemming
    words = [ps.stem(word) for word in words]

    return " ".join(words)

# Load model and vectorizer
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# UI
st.title("📩 SMS Spam Detector")

input_sms = st.text_area("Enter the message")

if st.button("Predict"):
    if input_sms.strip() == "":
        st.warning("Please enter a message")
    else:
        transformed_sms = transform_text(input_sms)
        vector_input = tfidf.transform([transformed_sms])
        result = model.predict(vector_input)[0]

        if result == 1:
            st.error("🚨 Spam")
        else:
            st.success("✅ Not Spam")