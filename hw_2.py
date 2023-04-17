import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import glob, nltk, os, re
from nltk.corpus import stopwords 
from nltk import FreqDist
st.set_option('deprecation.showPyplotGlobalUse', False)
nltk.download('stopwords')


st.markdown('''
# Analyzing Shakespeare Texts
''')

# Create a dictionary (not a list)
books = {" ":" ","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice":"data/merchant.txt","Romeo and Juliet":"data/romeo.txt"}

# Sidebar
st.sidebar.header('Word Cloud Settings')
max_word = st.sidebar.slider("Max Words", min_value=10, max_value=200, value=100, step=10)
max_font_size = st.sidebar.slider("Max Font Size", min_value=20, max_value=200, value=100, step=10)
width = st.sidebar.slider("Image Width", min_value=500, max_value=2000, value=800, step=100)
random_state = st.sidebar.slider("Random State", min_value=0, max_value=1000, value=42, step=10)
remove_stop_words = st.sidebar.checkbox("Remove Stop Words?", value=True)
st.sidebar.header('Word Count Settings')

st.sidebar.header('Bar Chart Settings')
min_count = st.sidebar.slider("Minimum Word Count", min_value=5, max_value=100, value=10, step=5)


## Select text files
image = st.selectbox("Choose a text file", books.keys())

## Get the value
image = books.get(image)

if image != " ":
    stop_words = []
    raw_text = open(image,"r").read().lower()
    raw_text = raw_text.translate(str.maketrans('', '', string.punctuation))
    nltk_stop_words = stopwords.words('english')

    if remove_stop_words:
        stop_words = set(nltk_stop_words)
        stop_words.update(['us', 'one', 'though','will', 'said', 'now', 'well', 'man', 'may',
        'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
        'put', 'seem', 'asked', 'made', 'half', 'much',
        'certainly', 'might', 'came','thou'])
        # These are all lowercase

    tokens = nltk.word_tokenize(raw_text)


wc = WordCloud(background_color='white', stopwords = stopwords)


tab1, tab2, tab3 = st.tabs(['Word Cloud', 'Bar Chart', 'View Text'])

with tab1:
    wc = WordCloud(background_color='white', stopwords=stop_words,max_words=max_word,max_font_size=max_font_size,random_state=random_state, width = width)    
    wc.generate(' '.join(tokens))
    plt.figure(figsize=(12,8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    st.pyplot() 


    
with tab2:
    st.header('Most Popular Words')
    st.subheader('Top Words')
    freq_dist = FreqDist(tokens)
    word_count_df = pd.DataFrame(list(freq_dist.items()), columns=["Word","Frequency"])
    
    # Filter out stop words
    if remove_stop_words:
        word_count_df = word_count_df[~word_count_df["Word"].isin(stop_words)]
    
    # Filter out words with frequency below minimum count
    word_count_df = word_count_df[word_count_df["Frequency"] >= min_count]
    
    # Sort by frequency
    word_count_df = word_count_df.sort_values("Frequency", ascending=False)
    
    # Plot bar chart
    bars = alt.Chart(word_count_df).mark_bar().encode(
        x=alt.X("Frequency", sort="-y"),
        y=alt.Y("Word"),
        tooltip=["Word","Frequency"]
    ).properties(width=width)
    
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-5
    ).encode(
        text="Frequency"
    )
    
    st.altair_chart((bars + text).configure_mark(color='steelblue'), use_container_width=True)
    


with tab3:
    if image != " ":
        raw_text = open(image,"r").read().lower()
        st.write(raw_text)
