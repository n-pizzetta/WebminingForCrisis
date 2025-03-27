import streamlit as st
import json
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

def load_event_mapping():
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

# Function to remove URLs from the tweet text
def remove_urls(text):
    # Regex pattern to remove URLs
    url_pattern = r'http[s]?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)

def load_tweets_by_event():

    nltk.download('stopwords')
    
    tweets_by_event = {}
    event_mapping = load_event_mapping()
    stop_words = set(stopwords.words('english'))
    stop_words.update(["http", "https", "t"])  # Add 'http' and 'https' to stop words
    
    with open("DATASET-20250325/database/Nodes/Tweet.json", "r", encoding="utf-8") as file:
        for line in file:
            try:
                tweet_json = json.loads(line)
                props = tweet_json['n']['properties']
                text = props.get("text", "")
                
                text = remove_urls(text)
                
                text = " ".join([word for word in text.split() if word.lower() not in stop_words])
                
                trecisid = props.get("topic", "")  # Assuming 'topic' holds the trecisid
                event_type = event_mapping.get(trecisid, "Unknown")
                
                if text:
                    if event_type not in tweets_by_event:
                        tweets_by_event[event_type] = []
                    tweets_by_event[event_type].append(text)
            except:
                continue
    
    return tweets_by_event

def generate_wordcloud(texts):
    text_combined = " ".join(texts)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_combined)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

def show_page():
    st.title("☁️ Event-Based Word Clouds")
    
    tweets_by_event = load_tweets_by_event()
    
    if not tweets_by_event:
        st.error("No tweets loaded. Check the dataset path or structure.")
        return
    
    events = list(tweets_by_event.keys())
    selected_event = st.selectbox("Select an event to display its word cloud:", events)
    
    if selected_event and selected_event in tweets_by_event:
        st.subheader(f"Word Cloud for {selected_event}:")
        generate_wordcloud(tweets_by_event[selected_event])
    else:
        st.warning("No data available for the selected event.")
