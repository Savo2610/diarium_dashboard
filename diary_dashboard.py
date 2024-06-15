import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

def mood_graph(diary_data):
    # Extract Mood Data (Rating)
    entries = []
    for entry in diary_data:
        date = entry.get("date")
        rating = entry.get("rating")
        if rating is not None:
            entries.append({"date": date, "rating": rating})

    # DataFrame
    df = pd.DataFrame(entries)
    df['date'] = pd.to_datetime(df['date'])

    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 20))
    # Plot Mood Graph
    ax1.plot(df['date'], df['rating'], marker='o')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Rating')
    ax1.set_title('Ratings Over Time')
    ax1.tick_params(axis='x', rotation=45)

    rating_counts = df['rating'].value_counts().sort_values(ascending=False)
    # Plot Pie Chart
    ax2.pie(rating_counts.values, labels=rating_counts.index, autopct='%1.1f%%')
    ax2.set_title('Rating Distribution')
   
    # Plot Rating Frequency
    rating_counts = df['rating'].value_counts().sort_index()
    ax3.bar(rating_counts.index, rating_counts.values)
    ax3.set_xlabel('Rating')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Rating Frequency')

    st.pyplot(fig)

def tracker_graph(diary_data, tracker, tracker_type):
    # Extract Tracker Data
    entries = []
    for entry in diary_data:
        date = entry.get("date")
        tracker_data = entry.get("tracker", [])
        for data in tracker_data:
            if data.startswith(tracker):
                value = data.split(": ")[1]
                entries.append({"date": date, "value": value})

    # DataFrame
    df = pd.DataFrame(entries)
    df['date'] = pd.to_datetime(df['date'])

    if tracker_type == "numerical":

        # Plot Tracker Graph
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        ax1.plot(df['date'], df['value'], marker='o')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Value')
        ax1.set_title(f'{tracker} Over Time')
        ax1.tick_params(axis='x', rotation=45)

        # Plot Value Frequency
        value_counts = df['value'].value_counts().sort_index()
        ax2.bar(value_counts.index, value_counts.values)
        ax2.set_xlabel('Value')
        ax2.set_ylabel('Frequency')
        ax2.set_title(f'{tracker} Frequency')


    if tracker_type == "text":

        # Plot Pie chart
        value_counts = df['value'].value_counts().sort_values(ascending=False)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        ax1.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
        ax1.set_title(f'{tracker} Distribution')

        # Plot Value Frequency
        ax2.bar(value_counts.index, value_counts.values)
        ax2.set_xlabel('Value')
        ax2.set_ylabel('Frequency')
        ax2.set_title(f'{tracker} Frequency')
        ax2.tick_params(axis='x', rotation=45)

    st.pyplot(fig)


def find_trackers(diary_data):
    trackers = {}
    for entry in diary_data:
        for tracker in entry.get('tracker', []):
            tracker_type, value = tracker.split(": ")
            if tracker_type not in trackers:
                if value.isdigit():
                    trackers[tracker_type] = "numerical"
                else:
                    trackers[tracker_type] = "text"

    return trackers


def main():
    #Header
    st.set_page_config(page_title="Diarydash")
    st.title('Diarium Dashboard')
    st.write('Open Diarium App, click on export, select the time period to be displayed and for file format choose JSON, then upload the file here. At least one entry in the diary must have a rating.')

    #Analysis
    uploaded_file = st.file_uploader("Upload JSON", type=["json"])
    if uploaded_file is not None:
        diary_data = json.load(uploaded_file)
        st.write('File uploaded successfully! Please choose the Tracker you want to analyse:')
        #User selection
        if st.checkbox('Analyse Ratings (Mood)'):
            mood_graph(diary_data)
        trackers = find_trackers(diary_data)
        selected_trackers = []
        for tracker in trackers:
            if st.checkbox(tracker):
                selected_trackers.append(tracker)
                tracker_graph(diary_data, tracker, trackers[tracker])     
    else: st.write('Please upload a JSON file to get started!')

    #Footer
    st.write('Made by Julian from the [Diarium Community](https://forum.diariumapp.com/). Check out the [source code](https://github.com/Savo2610/diarium_dashboard).')

if __name__ == "__main__":
    main()
