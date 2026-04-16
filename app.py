import streamlit as st
import time
from model import MusicRecommender

# Page config
st.set_page_config(page_title="Music Recommender 🎵", page_icon="🎧", layout="wide")

# Load model
@st.cache_resource
def load_model():
    return MusicRecommender("spotifydataset.csv")

model = load_model()

# ✅ SAFE song list (after cleaning in model)
songs_list = model.df['track_name'].values

# 🎨 Custom UI
st.markdown("""
<style>

/* 🔥 Full background image */
.stApp {
    background: url("https://images.unsplash.com/photo-1511379938547-c1f69419868d") no-repeat center center fixed;
    background-size: cover;
    backdrop-filter: blur(6px);
}

/* Overlay for readability */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(15, 23, 42, 0.85);  /* dark overlay */
    z-index: -1;
}

/* 🔥 Gradient Title */
.title {
    text-align: center;
    font-size: 65px;
    font-weight: bold;
    background: linear-gradient(90deg, #6d28d9, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Cards */
.song-card {
    background: rgba(30, 41, 59, 0.85);
    padding: 15px;
    margin: 10px 0;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #7c3aed, #6366f1);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎛️ Controls")
top_n = st.sidebar.slider("Number of Songs", 3, 10, 5)
st.sidebar.markdown("---")
st.sidebar.info("🎵 Built by Rohini Bhite")

# Title
st.markdown('<div class="title">🎵 Music Recommender</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover songs based on your vibe 💜</div>', unsafe_allow_html=True)

# Dropdown
selected_song = st.selectbox("🎧 Select a song", songs_list)

# Button
if st.button("✨ Recommend Songs"):

    with st.spinner("Finding best songs for you... 🎶"):
        time.sleep(1.5)
        recommendations = model.recommend(selected_song)

    st.success("Here are your recommendations 🎉")

    for i, song in enumerate(recommendations[:top_n], 1):
        st.markdown(f"""
        <div class="song-card">
            <h4>🎵 {i}. {song}</h4>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<hr><center>Made with 💜 using Streamlit</center>", unsafe_allow_html=True)
