import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

def mood_graph(diary_data):
    # Parse the data
    entries = []
    for entry in diary_data:
        date = entry.get("date")
        rating = entry.get("rating")
        if rating is not None:
            entries.append({"date": date, "rating": rating})

    # Convert to DataFrame
    df = pd.DataFrame(entries)
    df['date'] = pd.to_datetime(df['date'])

    # Plot Mood Graph
    st.subheader('Mood Graph')
    fig, ax = plt.subplots()
    ax.plot(df['date'], df['rating'], marker='o')
    ax.set_xlabel('Date')
    ax.set_ylabel('Rating')
    ax.set_title('Ratings Over Time')
    st.pyplot(fig)

def main():
    st.set_page_config(page_title="Diarydash")
    st.title('Diary Dashboard')
    st.write('Open Diarium App, click on export, select the time period to be displayed and for file format choose JSON, then upload the file here.')
    uploaded_file = st.file_uploader("Upload JSON", type=["json"])
    if uploaded_file is not None:
        diary_data = json.load(uploaded_file)
        mood_graph(diary_data) # Display the mood graph
    else: st.write('Please upload a JSON file to get started!')
    st.write('Made by Julian from the [Diarium Community](https://forum.diariumapp.com/)')

if __name__ == "__main__":
    main()
