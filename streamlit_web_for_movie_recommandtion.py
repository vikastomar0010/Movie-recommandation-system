import streamlit as st
import pickle


# Load pickle files
@st.cache_resource
def load_data():
    with open('movie_list.pkl', 'rb') as file:
        movies = pickle.load(file)
    with open('similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)
    return movies, similarity


movies, similarity = load_data()


# Recommendation function
def recommend_movies(title, num_recommendations=5):
    if title.lower() in movies['title'].str.lower().values:
        idx = movies[movies['title'].str.lower() == title.lower()].index[0]
        sim_scores = list(enumerate(similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]

        recommendations = [(movies.iloc[i[0]]['title']) for i in sim_scores]
        return recommendations
    else:
        return None


# Streamlit UI
st.title("🎥 Movie Recommender System")
st.markdown("""
Welcome to the Movie Recommender System!  
Type the name of a movie, and we’ll recommend similar ones for you.  
---
""")

# Input movie title
movie_title = st.text_input("Enter a movie title:", "")

# Display recommendations
if st.button("Recommend"):
    if movie_title.strip():
        recommendations = recommend_movies(movie_title)
        if recommendations:
            st.subheader(f"Movies similar to **{movie_title}**:")
            for idx, title in enumerate(recommendations, start=1):
                st.write(f"**{idx}. {title}**")
        else:
            st.error("Movie not found! Please try a different title.")
    else:
        st.warning("Please enter a movie title to get recommendations.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Vikash Tomar")
