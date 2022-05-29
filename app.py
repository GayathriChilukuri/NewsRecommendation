# importing libraries
import streamlit as st
import pickle
import math
import re
from collections import Counter

# loading the dataset using pickle
headlines_list_ini = pickle.load(open('headlines.pkl', 'rb'))

# dropping duplicates and resetting index
headlines_list = headlines_list_ini.drop_duplicates(subset='title', keep="first")
headlines_list = headlines_list.reset_index(drop=True)

# title and dropdown box
headlines_list_titles = headlines_list['title'].values
st.title('News Recommendation system')
selected_headline = st.selectbox('Select a news article to read', headlines_list_titles)


# function for finding the cosine similarity between vectors
def get_cosine(vector1, vector2):
    intersection = set(vector1.keys()) & set(vector2.keys())
    numerator = sum([vector1[x]*vector2[x] for x in intersection])
    sum1 = sum([vector1[x]*vector1[x] for x in list(vector1.keys())])
    sum2 = sum([vector2[x]*vector2[x] for x in list(vector2.keys())])
    denominator = math.sqrt(sum1)*math.sqrt(sum2)
    if not denominator:
        return 0.0
    else:
        return float(numerator)/denominator


# to convert text to vector
def text_to_vector(text):
    word = re.compile(r"\w+")
    words = word.findall(text)
    return Counter(words)


# function for recommending articles based on cosine similarity
def recommend(query):
    list1 = []
    for i in range(len(headlines_list['description'])):
        vector1 = text_to_vector(query)
        vector2 = text_to_vector(str(headlines_list['description'][i]))
        list1.append(get_cosine(vector1, vector2))
    headlines_list['score'] = list1

    # after sorting based on rank
    rslt_df = headlines_list.sort_values(by='score', ascending=False)

    # making a list of the result dataframe
    finalim = list(rslt_df['url_to_image'])
    finaldes = list(rslt_df['description'])
    finalurl = list(rslt_df['url'])

    # creating an empty list for recommended images,description and news url
    recommendations_images = []
    recommendations_news = []
    recommendations_descrip = []
    recommendations_url = []

    # adding the recommended articles,images, etc. into lists
    t = 0
    for k in rslt_df['title']:
        if t < 6 and k != query:
            recommendations_news.append(k)
            recommendations_images.append(finalim[t])
            recommendations_descrip.append(finaldes[t])
            recommendations_url.append(finalurl[t])
            t = t+1

    return recommendations_news, recommendations_images, recommendations_descrip, recommendations_url


if st.button('Recommend'):
    recomnews, recomimages, recomdescrip, recomurl = recommend(selected_headline)
    col1, col2 = st.columns(2)  # making beta columns
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)

    # displaying the corresponding image,news url and description of the recommended news
    with col1:
        st.image(recomimages[0], width=300, clamp=True)
        url = recomurl[0]
        with st.expander(recomnews[0]):
            st.write(recomdescrip[0])
            st.write(url)
    with col2:
        st.image(recomimages[1], width=300, clamp=True)
        url = recomurl[1]
        with st.expander(recomnews[1]):
            st.write(recomdescrip[1])
            st.write(url)
    with col3:
        st.image(recomimages[2], width=300, clamp=True)
        url = recomurl[2]
        with st.expander(recomnews[2]):
            st.write(recomdescrip[2])
            st.write(url)
    with col4:
        st.image(recomimages[3], width=300, clamp=True)
        url = recomurl[3]
        with st.expander(recomnews[3]):
            st.write(recomdescrip[3])
            st.write(url)
    with col5:
        st.image(recomimages[4], width=300, clamp=True)
        url = recomurl[4]
        with st.expander(recomnews[4]):
            st.write(recomdescrip[4])
            st.write(url)
    with col6:
        st.image(recomimages[5], width=300, clamp=True)
        url = recomurl[5]
        with st.expander(recomnews[5]):
            st.write(recomdescrip[5])
            st.write(url)