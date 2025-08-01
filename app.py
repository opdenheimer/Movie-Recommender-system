import streamlit as st
import pickle 
import pandas as pd
import requests
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMDA4MzZiYTNkNWNmZmM3MzUyZGVjOWJlNGY4N2I5ZCIsIm5iZiI6MTc1MzUyNjE2Mi44ODUsInN1YiI6IjY4ODRhZjkyZGZmMDA4MWRhYzcyZTkyNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.SGj7d7hMuK-szhAGbAK91-6fDPX6fzRaKtTQ3DyTkws"
        }
        response = requests.get(url, headers=headers, timeout=5)  # Added timeout
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        st.error(f"Connection error: {str(e)}")
    except Exception as e:
        st.error(f"Error fetching poster: {str(e)}")
    return "https://via.placeholder.com/500x750?text=No+Poster+Available"  # Fallback image

def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_posters
    
   
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')
selected_movie_name= st.selectbox('Search For Movie',movies['title'].values)
if st.button('Recommend'):
    names,posters= recommend(selected_movie_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.header(names[idx])
            st.image(posters[idx])