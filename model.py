import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MusicRecommender:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.prepare_data()

    def prepare_data(self):
        # ✅ Clean column names (IMPORTANT FIX)
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace(" ", "_")

        print("Columns in dataset:", self.df.columns)

        # ✅ Check required columns
        if 'track_name' not in self.df.columns or 'artist_name' not in self.df.columns:
            raise Exception("Dataset must contain 'track_name' and 'artist_name' columns")

        # Keep only required columns
        self.df = self.df[['track_name', 'artist_name']].dropna()

        # Create combined feature
        self.df['combined'] = self.df['track_name'] + " " + self.df['artist_name']

        # Convert text to vectors
        cv = CountVectorizer(stop_words='english')
        self.matrix = cv.fit_transform(self.df['combined'])

        # Compute similarity
        self.similarity = cosine_similarity(self.matrix)

    def recommend(self, song):
        song = song.lower()

        if song not in self.df['track_name'].str.lower().values:
            return ["Song not found"]

        idx = self.df[self.df['track_name'].str.lower() == song].index[0]

        distances = list(enumerate(self.similarity[idx]))
        songs = sorted(distances, key=lambda x: x[1], reverse=True)[1:11]

        recommendations = []
        for i in songs:
            recommendations.append(self.df.iloc[i[0]].track_name)

        return recommendations