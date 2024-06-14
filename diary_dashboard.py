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

    # Plot Mood Graph
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    ax1.plot(df['date'], df['rating'], marker='o')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Rating')
    ax1.set_title('Ratings Over Time')
    ax1.tick_params(axis='x', rotation=45)

    # Plot Rating Frequency
    rating_counts = df['rating'].value_counts().sort_index()
    ax2.bar(rating_counts.index, rating_counts.values)
    ax2.set_xlabel('Rating')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Rating Frequency')

    st.pyplot(fig)

def main():
    #Header
    st.set_page_config(page_title="Diarydash")
    st.title('Diary Dashboard')
    st.write('Open Diarium App, click on export, select the time period to be displayed and for file format choose JSON, then upload the file here. At least one entry in the diary must have a rating.')

    #Analysis
    uploaded_file = st.file_uploader("Upload JSON", type=["json"])
    if uploaded_file is not None:
        diary_data = json.load(uploaded_file)
        mood_graph(diary_data)
    else: st.write('Please upload a JSON file to get started!')

    #Footer
    st.write('Made by Julian from the [Diarium Community](https://forum.diariumapp.com/)')

if __name__ == "__main__":
    main()
