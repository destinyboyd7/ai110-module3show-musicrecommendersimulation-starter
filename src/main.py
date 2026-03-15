"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from textwrap import fill
from recommender import load_songs, recommend_songs, build_taste_profile


USER_PREFERENCE_PROFILES = [
    {"name": "Lofi Focus", "genre": "lofi", "mood": "chill", "energy": 0.2},
    {"name": "Pop Boost", "genre": "pop", "mood": "happy", "energy": 0.75},
    {"name": "Rock Drive", "genre": "rock", "mood": "intense", "energy": 0.9},
    {"name": "Conflict Pop Sad Sprint", "genre": "pop","mood": "sad", "energy": 0.9},
    {"name": "Lofi Adrenaline", "genre": "lofi", "mood": "intense", "energy": 0.95},
    {"name": "Out Of Range Energy High", "genre": "edm", "mood": "energetic", "energy": 2.0,},
    {"name": "Mood Weights Ignored","genre": "pop", "mood": "happy", "energy": 0.75},
    {"name": "Hip Hop Label Variant", "genre": "hip hop", "mood": "confident", "energy": 0.8,},
    {"name": "Unknown Genre", "genre": "rock", "mood": "calm", "energy": 0.3,}
]


def main() -> None:
    """
    Main function to run the music recommender simulation.
    """

    songs = load_songs("data/songs.csv")

    for user_prefs in USER_PREFERENCE_PROFILES:
        taste_profile = build_taste_profile(user_prefs)

        print(f"\n=== Profile: {user_prefs['name']} ===")
        print(f"Built taste profile for genre: '{taste_profile['favorite_genre']}'")
        print(f"  Energy range   : {taste_profile['energy_range']}")
        print(f"  Tempo range    : {taste_profile['tempo_range']}")
        print(f"  Valence range  : {taste_profile['valence_range']}")
        print(f"  Mode preference: {taste_profile['mode_preference']}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop Recommendations:\n")
        for idx, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            print(f"{idx}. {song['title']}")
            print(f"   Score     : {score:.2f}")
            print(f"   Reasons   : {fill(explanation, width=60)}")
            print("-" * 60)


if __name__ == "__main__":
    main()
