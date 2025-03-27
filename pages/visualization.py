import streamlit as st
import json
import re
from collections import Counter
from datetime import datetime
import plotly.graph_objects as go
from nltk.corpus import stopwords

def remove_urls(text):
    url_pattern = r'http[s]?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)

def import_data_per_day():
    stop_words = set(stopwords.words("english"))
    
    tweets_per_day = Counter()
    words_per_day = Counter()

    with open("DATASET-20250325/database/Nodes/Tweet.json", "r", encoding="utf-8") as file:
        for line in file:
            try:
                tweet_json = json.loads(line)
                props = tweet_json['n']['properties']

                created_at = props.get("created_at")
                if created_at:
                    date = datetime.strptime(created_at, "%Y-%m-%dT%H:%MZ").date()
                    tweets_per_day[date] += 1

                    text = props.get("text", "")
                    text = remove_urls(text)

                    words = re.findall(r'\b\w+\b', text.lower())
                    filtered_words = [word for word in words if word not in stop_words]
                    words_per_day[date] += len(filtered_words)
            except Exception as e:
                print("Erreur sur une ligne :", e)
                continue

    return words_per_day, tweets_per_day

def filter_data(data_dict, start_date, end_date):
    return {
        date: count
        for date, count in sorted(data_dict.items())
        if start_date <= date <= end_date
    }

def plot_timeseries(dates, values, title, y_label, color):
    fig = go.Figure(data=go.Scatter(
        x=dates,
        y=values,
        mode='markers',
        line=dict(color=color)
    ))
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=y_label,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)
    
def show_page():
    st.title("📊 Tweet Analysis Dashboard")

    option = st.selectbox(
        "Choose what to visualize:",
        ("Select...", "Tweets per date", "Words per date", "Both")
    )

    if option != "Select...":
        words_per_day, tweets_per_day = import_data_per_day()
        all_dates = sorted(set(words_per_day) | set(tweets_per_day))
        min_date, max_date = min(all_dates), max(all_dates)

        try:
            start_date, end_date = st.date_input(
                "Select date range:",
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )

            if not start_date or not end_date:
                st.info("ℹ️ Please select both a start and end date to visualize data.")
                return

            if start_date > end_date:
                st.warning("⚠️ Start date must be before end date.")
                return

        except Exception as e:
            st.info("ℹ️ Please select a valid date range.")
            return

        if option in ("Tweets per date", "Both"):
            filtered_tweets = filter_data(tweets_per_day, start_date, end_date)
            plot_timeseries(
                list(filtered_tweets.keys()),
                list(filtered_tweets.values()),
                title="📅 Tweets per Day",
                y_label="Tweet Count",
                color="royalblue"
            )

        if option in ("Words per date", "Both"):
            filtered_words = filter_data(words_per_day, start_date, end_date)
            plot_timeseries(
                list(filtered_words.keys()),
                list(filtered_words.values()),
                title="📝 Words per Day",
                y_label="Word Count",
                color="seagreen"
            )
