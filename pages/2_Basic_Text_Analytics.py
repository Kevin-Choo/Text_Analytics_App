import streamlit as st

# for syllable counting
import textstat

# create containers for the basic analytics section section
syllable = st.container()
analytics_data = st.container()


st.title("Basic Text Analytics Section (Under Construction)")
		
word_count = st.sidebar.checkbox("Word Count")
sent_count = st.sidebar.checkbox("Sentence Count")