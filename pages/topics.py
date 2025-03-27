import streamlit as st
import json
import textwrap
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from gensim.models import Word2Vec
from sentence_transformers import SentenceTransformer
import plotly.express as px
import plotly.graph_objects as go
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

def load_tweets_with_event():
    # Load stop words
    stop_words = set(stopwords.words("english"))
    tweets_with_event = []
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
                    tweets_with_event.append({"text": filtered_text, "eventType": event_type})
            except:
                continue
    
    return tweets_with_event

def get_top_k_idf_clusters(texts, k=50, cluster_n=5):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    idf_scores = vectorizer.idf_

    top_indices = idf_scores.argsort()[-k:][::-1]
    top_words = [feature_names[i] for i in top_indices]
    clusters = [top_words[i::cluster_n] for i in range(cluster_n)]
    return clusters

def plot_word_embeddings(texts):
    tokenized = [re.findall(r'\b\w+\b', text.lower()) for text in texts]
    model = Word2Vec(sentences=tokenized, vector_size=50, window=5, min_count=2, workers=4)

    vocab = list(model.wv.key_to_index)
    vectors = [model.wv[word] for word in vocab]
    reduced = PCA(n_components=2).fit_transform(vectors)

    fig = px.scatter(
        x=reduced[:, 0],
        y=reduced[:, 1],
        hover_name=vocab,  # Show word only on hover
        title="Word Embeddings"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_tweet_embeddings(tweets_with_event, num_tweets):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Randomly sample tweets instead of taking the first num_tweets
    sampled_tweets = random.sample(tweets_with_event, min(num_tweets, len(tweets_with_event)))
    texts = [tweet["text"] for tweet in sampled_tweets]
    event_types = [tweet["eventType"] for tweet in sampled_tweets]
    
    embeddings = model.encode(texts)
    reduced = TSNE(n_components=2, perplexity=30, random_state=42).fit_transform(embeddings)

    # Truncate long tweets for cleaner hover tooltips
    truncated_texts = [textwrap.shorten(t, width=80, placeholder="...") for t in texts]
    
    fig = px.scatter(
        x=reduced[:, 0],
        y=reduced[:, 1],
        color=event_types,  # Color points by event type
        hover_name=truncated_texts,
        title="Tweet Embeddings (Semantic Map)",
        labels={"color": "Event Type"}
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_page():
    st.title("🧠 Tweet Topics and Semantic Maps")

    method = st.radio("Choose method for topic analysis:",
                      ["Top-k IDF word clusters", "Word embeddings", "Tweet embeddings"])

    tweets_with_event = load_tweets_with_event()
    texts = [tweet["text"] for tweet in tweets_with_event]  # Extract only texts for processing

    if method == "Top-k IDF word clusters":
        k = st.slider("Number of top words (k):", 10, 100, 50)
        n_clusters = st.slider("Number of clusters:", 2, 10, 5)
        clusters = get_top_k_idf_clusters(texts, k=k, cluster_n=n_clusters)
        for i, cluster in enumerate(clusters):
            st.markdown(f"**Cluster {i+1}**: {', '.join(cluster)}")

    elif method == "Word embeddings":
        info_placeholder = st.empty()
        info_placeholder.info("Generating and visualizing word embeddings (this might take a few seconds)...")
        plot_word_embeddings(texts)
        info_placeholder.empty()

    elif method == "Tweet embeddings":
        num_tweets = st.slider("Number of tweets to display:", 100, 2000, 500, step=50)
        info_placeholder = st.empty()
        info_placeholder.info("Encoding and reducing tweet vectors (this might take a bit)...")
        plot_tweet_embeddings(tweets_with_event, num_tweets)
        info_placeholder.empty()