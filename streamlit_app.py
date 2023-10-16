import streamlit as st
import matplotlib.pyplot as plt
import librosa
import librosa.display
import pandas as pd
import numpy as np

# Load audio file
file = st.file_uploader("Upload an audio file", type=["mp3"])
if file is not None:
    data, sr = librosa.load(file)

    # Display waveform
    fig, ax = plt.subplots(figsize=(14, 5))
    librosa.display.waveshow(data, sr=sr, ax=ax)
    st.pyplot(fig)

    # Annotate audio
    start = st.number_input("Start time")
    end = st.number_input("End time")
    annotation = st.text_input("Annotation")
    if st.button("Submit"):
        new_annotation = pd.DataFrame({'Start': [start], 'End': [end], 'Annotation': [annotation]})
        annotations = pd.concat([annotations, new_annotation], ignore_index=True)

        # Display annotations
        st.write(annotations)

    # Export annotations
    if st.button("Export annotations"):
        annotations.to_csv('annotations.csv', index=False)
        st.success("Annotations exported successfully!")
