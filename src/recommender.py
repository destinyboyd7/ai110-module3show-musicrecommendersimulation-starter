"""
Music Recommender Implementation
"""

import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    mood_weights: Dict[str, float]  # Allow nuanced mood preferences
    energy_tolerance: float  # Range around target_energy

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommends songs based on the user's profile.
        """
        #Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Provides an explanation for why a song was recommended."""
        # Implement explanation logic
        return "Explanation placeholder"

#Genre-aware base profiles — each genre gets its own characteristic ranges
GENRE_PROFILES = {
    "rock": {
        "energy_range": (0.7, 1.0),
        "tempo_range": (110, 180),
        "danceability_min": 0.3,
        "valence_range": (0.3, 0.8),
        "mode_preference": "minor",
    },
    "lofi": {
        "energy_range": (0.1, 0.45),
        "tempo_range": (60, 100),
        "danceability_min": 0.2,
        "valence_range": (0.2, 0.55),
        "mode_preference": "minor",
    },
    "pop": {
        "energy_range": (0.5, 0.85),
        "tempo_range": (90, 140),
        "danceability_min": 0.5,
        "valence_range": (0.5, 0.9),
        "mode_preference": "major",
    },
    "hip-hop": {
        "energy_range": (0.4, 0.85),
        "tempo_range": (75, 130),
        "danceability_min": 0.6,
        "valence_range": (0.3, 0.75),
        "mode_preference": "minor",
    },
    "classical": {
        "energy_range": (0.1, 0.6),
        "tempo_range": (50, 130),
        "danceability_min": 0.1,
        "valence_range": (0.2, 0.7),
        "mode_preference": "major",
    },
    "edm": {
        "energy_range": (0.75, 1.0),
        "tempo_range": (120, 175),
        "danceability_min": 0.65,
        "valence_range": (0.4, 0.9),
        "mode_preference": "major",
    },
    # Fallback for unknown genres — wide ranges so nothing gets excluded
    "default": {
        "energy_range": (0.0, 1.0),
        "tempo_range": (50, 200),
        "danceability_min": 0.0,
        "valence_range": (0.0, 1.0),
        "mode_preference": None,
    },
}

def build_taste_profile(user_prefs: dict) -> dict:
    """
    Builds a dynamic taste profile based on user genre.
    Falls back to default if genre is not recognized.
    """
    genre = user_prefs.get("genre", "default").lower()
    base = GENRE_PROFILES.get(genre, GENRE_PROFILES["default"])

    return {
        "favorite_genre": genre,
        "favorite_mood": user_prefs.get("mood", "neutral"),
        "target_energy": user_prefs.get("energy", 0.5),
        **base,  # Spread in all genre-specific ranges
    }

def _linear_soft_range(value, lo, hi, pad):
    if lo <= value <= hi:
        return 1.0
    if value < lo:
        d = lo - value
    else:
        d = value - hi
    return max(0.0, 1.0 - d / pad)


def score_song(song: dict, profile: dict):
    """
    Scores a song against the user's taste profile and provides a breakdown of the score.
    """
    reasons: List[str] = []

    # Genre (0 or 2.0)
    if song.get("genre", "").lower() == profile["favorite_genre"]:
        genre_points = 2.0
        reasons.append(f"Genre matches '{profile['favorite_genre']}' (+2.0)")
    else:
        genre_points = 0.0
        reasons.append(f"Genre '{song.get('genre', '?')}' does not match '{profile['favorite_genre']}' (+0.0)")


    if song.get("mood", "").lower() == profile["favorite_mood"]:
        mood_points = 1.0
        reasons.append(f"Mood matches '{profile['favorite_mood']}' (+1.0)")
    else:
        mood_points = 0.0
        reasons.append(f"Mood '{song.get('mood', '?')}' does not match '{profile['favorite_mood']}' (+0.0)")
    #mood_points = 0.0
    #reasons.append("Mood check disabled (+0.0)")

    # Energy (0.0 – 2.0)
    song_energy = float(song.get("energy", 0.5))
    target_energy = float(profile.get("target_energy", 0.5))
    energy_points = 2.0 * max(0.0, 1.0 - abs(song_energy - target_energy) / 0.6)
    reasons.append(f"Energy {song_energy:.2f} vs target {target_energy:.2f} (+{energy_points:.2f})")

    # Tempo (0.0 – 0.5)
    tempo = float(song.get("tempo_bpm", song.get("tempo", 100)))
    t_lo, t_hi = profile["tempo_range"]
    tempo_points = 0.5 * _linear_soft_range(tempo, t_lo, t_hi, pad=10.0)
    if t_lo <= tempo <= t_hi:
        reasons.append(f"Tempo {tempo:.0f} BPM is in preferred range {t_lo}–{t_hi} (+{tempo_points:.2f})")
    else:
        reasons.append(f"Tempo {tempo:.0f} BPM is outside preferred range {t_lo}–{t_hi} (+{tempo_points:.2f})")

    # Valence (0.0 – 0.5)
    valence = float(song.get("valence", 0.5))
    v_lo, v_hi = profile["valence_range"]
    valence_points = 0.5 * _linear_soft_range(valence, v_lo, v_hi, pad=0.10)
    if v_lo <= valence <= v_hi:
        reasons.append(f"Valence {valence:.2f} is in preferred range {v_lo}–{v_hi} (+{valence_points:.2f})")
    else:
        reasons.append(f"Valence {valence:.2f} is outside preferred range {v_lo}–{v_hi} (+{valence_points:.2f})")

    # Danceability (0.0 – 0.5)
    dance = float(song.get("danceability", 0.5))
    d_min = float(profile.get("danceability_min", 0.0))
    if dance >= d_min:
        dance_points = 0.5
        reasons.append(f"Danceability {dance:.2f} meets minimum {d_min:.2f} (+0.50)")
    else:
        dance_points = 0.5 * max(0.0, 1.0 - (d_min - dance) / 0.20)
        reasons.append(f"Danceability {dance:.2f} is below minimum {d_min:.2f} (+{dance_points:.2f})")

    # Mode (0.0, 0.25, or 0.5)
    pref_mode = profile.get("mode_preference")
    song_mode = song.get("mode")
    if pref_mode is None:
        mode_points = 0.25
        reasons.append("No mode preference set (+0.25)")
    elif str(song_mode).lower() == str(pref_mode).lower():
        mode_points = 0.5
        reasons.append(f"Mode '{song_mode}' matches preference '{pref_mode}' (+0.50)")
    else:
        mode_points = 0.0
        reasons.append(f"Mode '{song_mode}' does not match preference '{pref_mode}' (+0.00)")

    total = genre_points + mood_points + energy_points + tempo_points + valence_points + dance_points + mode_points
    breakdown = {
        "genre": genre_points,
        "mood": mood_points,
        "energy": energy_points,
        "tempo": tempo_points,
        "valence": valence_points,
        "danceability": dance_points,
        "mode": mode_points,
        "total": total,
    }
    return total, breakdown, reasons

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    with open(csv_path, mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    print(f"Loaded songs: {len(songs)}")
    return songs

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    profile = build_taste_profile(user_prefs)
    scored = []

    for song in songs:
        score, breakdown, reasons = score_song(song, profile)
        if score >= 2.2:
            scored.append((song, score, breakdown, reasons))

    if len(scored) < k:
        for song in songs:
            score, breakdown, reasons = score_song(song, profile)
            if score >= 1.8:
                scored.append((song, score, breakdown, reasons))

    # Deduplicate if second pass re-added same song
    seen = set()
    uniq = []
    for s in scored:
        key = (s[0].get("title"), s[0].get("artist"))
        if key not in seen:
            seen.add(key)
            uniq.append(s)

    uniq.sort(key=lambda x: x[1], reverse=True)

    return [
        (
            song,
            score,
            " | ".join(reasons)
        )
        for song, score, _breakdown, reasons in uniq[:k]
    ]
