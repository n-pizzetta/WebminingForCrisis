import streamlit as st
import json
import re
import plotly.express as px
from textblob import TextBlob
from nltk.corpus import stopwords

def load_event_mapping():
    # Load stop words
    stop_words = set(stopwords.words("english"))
    event_mapping = {}
    with open("DATASET-20250325/database/Nodes/Event.json", "r", encoding="utf-8") as file:
        for line in file:
            try:
                event_json = json.loads(line)
                props = event_json['n']['properties']
                trecisid = props.get("trecisid", "")
                event_type = props.get("eventType", "")
                if trecisid and event_type:
                    event_mapping[trecisid] = event_type
            except:
                continue
    return event_mapping

def remove_urls(text):
    url_pattern = r'http[s]?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)

def load_tweets_with_sentiment():
    # Load stop words
    stop_words = set(stopwords.words("english"))
    tweets_with_sentiment = []
    event_mapping = load_event_mapping()
    
    with open("DATASET-20250325/database/Nodes/Tweet.json", "r", encoding="utf-8") as file:
        for line in file:
            try:
                tweet_json = json.loads(line)
                props = tweet_json['n']['properties']
                text = props.get("text", "")
                text = remove_urls(text)
                trecisid = props.get("topic", "")  # Assuming 'topic' holds the trecisid
                event_type = event_mapping.get(trecisid, "Unknown")
                
                if text:
                    words = re.findall(r'\b\w+\b', text.lower())
                    filtered_words = [word for word in words if word not in stop_words]
                    filtered_text = " ".join(filtered_words)
                    sentiment = TextBlob(filtered_text).sentiment.polarity
                    tweets_with_sentiment.append({"text": filtered_text, "eventType": event_type, "sentiment": sentiment})
            except:
                continue
    
    return tweets_with_sentiment

def show_page():
    st.title("📊 Sentiment Analysis Boxplots by Event")
    
    tweets_with_sentiment = load_tweets_with_sentiment()
    
    if not tweets_with_sentiment:
        st.error("No tweets loaded. Check the dataset path or structure.")
        return
    
    events = list(set(tweet["eventType"] for tweet in tweets_with_sentiment))
    selected_events = st.multiselect("Select events to display:", events, default=events[:5])
    
    filtered_data = [tweet for tweet in tweets_with_sentiment if tweet["eventType"] in selected_events]
    
    if not filtered_data:
        st.warning("No data available for the selected events.")
        return
    
    fig = px.box(
        filtered_data,
        x="eventType",
        y="sentiment",
        title="Sentiment Distribution per Event",
        labels={"eventType": "Event Type", "sentiment": "Sentiment Polarity"},
        color="eventType"
    )
    
    st.plotly_chart(fig, use_container_width=True)