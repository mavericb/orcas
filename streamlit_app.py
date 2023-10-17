import matplotlib.pyplot as plt
import librosa.display
import pandas as pd
import datetime
from pymongo import MongoClient
import streamlit as st

print(st.secrets.values())

if 'file' not in st.session_state:
    st.session_state['file'] = None
if 'annotations' not in st.session_state:
    st.session_state['annotations'] = pd.DataFrame(columns=['Start', 'End', 'Annotation'])
if 'annotation_list' not in st.session_state:
    st.session_state['annotation_list'] = []

# Initialize MongoDB client (replace 'mongodb_uri' with your MongoDB URI)
client = MongoClient(st.secrets["mongodb_uri"])
db = client[st.secrets["database"]]  # replace 'your_database' with your database name
collection = db[st.secrets["collection"]]  # replace 'annotations' with your collection name

# Load audio file
file = st.file_uploader("Upload an audio file of orcas talking", type=["mp3"])
if file is not None:
    st.session_state['file'] = file

if st.session_state['file'] is not None:
    data, sr = librosa.load(st.session_state['file'])

    # Play audio
    st.audio(st.session_state['file'])

    # Annotate audio
    start = st.slider("Start time Annotation", min_value=0, max_value=int(len(data)/sr))
    end = st.slider("End time Annotation", min_value=start, max_value=int(len(data)/sr))
    annotation = st.text_input("Annotation")
    if st.button("Submit"):
        new_annotation = pd.DataFrame({'Start': [start], 'End': [end], 'Annotation': [annotation]})
        st.session_state['annotations'] = pd.concat([st.session_state['annotations'], new_annotation], ignore_index=True)
        st.session_state['annotation_list'].append((start, end, annotation))  # Add new annotation to the list

        # Save annotation to MongoDB
        collection.insert_one({'Start': start, 'End': end, 'Annotation': annotation})

    # Display waveform and add all annotations to the plot
    fig, ax = plt.subplots(figsize=(14, 5))
    librosa.display.waveshow(data, sr=sr, ax=ax)
    for ann in st.session_state['annotation_list']:
        ax.annotate(ann[2], ((ann[0] + ann[1]) / 2, 0), bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))  # Adjust the position as needed
        ax.fill_betweenx([-1, 1], ann[0], ann[1], color='red', alpha=0.3)  # Color the annotated part

    # Redraw the plot to keep the old annotations
    st.pyplot(fig)

    # Display annotations
    st.write(st.session_state['annotations'])
