import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=9f6365d94d2339efc888f3c27b2c5a8b&language=en-US'.format(
            movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


sim = pickle.load(open('sim.pkl', 'rb'))
movies_list = pickle.load(open('mov_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = sim[movie_index]
    moives_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    rec = []
    rec_post = []
    for i in moives_list:
        rec.append(movies.iloc[i[0]].title)
        movie_id = movies.iloc[i[0]].id
        rec_post.append(fetch_poster(movie_id))
    return rec, rec_post


st.title('Movie recommended System')

option = st.selectbox(
    'Enter the movies names',
    movies['title'].values)

if st.button('recommend'):
    rec, rec_post = recommend(option)

    for i in range(5):
        st.subheader(rec[i])
        st.image(rec_post[i])
