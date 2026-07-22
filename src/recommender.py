import pandas as pd
from typing import List, Dict, Tuple, Optional
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
    name: str  # the user's name or online tag, for telling profiles apart
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_acousticness: float  # 0.0 = fully electronic, 1.0 = fully acoustic


# --- Scoring weights (tunable in one place) --------------------------------
# The two continuous "feel" features carry most of the weight. Mood is a
# medium categorical bonus, and genre is intentionally the SMALLEST bonus so
# it only breaks ties between songs that already fit the user's feel.
weight_of_energy = 0.5
weight_of_acoustics = 0.3
mood_bonus = 0.15
genre_bonus = 0.05


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def score(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """
        Score one song against the user's profile.

        Returns (score, reasons) where `reasons` is a human-readable list
        describing which components contributed, so explanations come for free.
        """
        score = 0.0
        reasons: List[str] = []

        # Continuous features: reward closeness to the user's TARGET, not the
        # raw maximum. 1 - |difference| is 1.0 for a perfect match, 0.0 far off.
        energy_fit = 1.0 - abs(song.energy - user.target_energy)
        score += weight_of_energy * energy_fit
        if energy_fit == 1.0:
            reasons.append(f"Nice the score matches perfectly with the user as it has the matching {song.energy}")
        else:
            reasons.append(f"The energy fit was {energy_fit:.2f} due to the song's energy slightly or majorly differing from the user's energy")
        acoustic_fit = 1.0 - abs(song.acousticness - user.target_acousticness)
        score += weight_of_acoustics * acoustic_fit
        if acoustic_fit == 1.0:
            reasons.append(f"Nice! the acousticness fits very nicely for this user as it scored a perfect {acoustic_fit}")
        else:
            reasons.append(f"The acousticness fit was {acoustic_fit:.2f} due to the song's acousticness slightly or majorly differing from the user's target of {user.target_acousticness}")

        # Categorical bonuses: added only on an exact match.
        if song.mood == user.favorite_mood:
            score += mood_bonus
            reasons.append(f"This song was given a slight score bonus of {mood_bonus} due to it matching the user's mood of {user.favorite_mood}")

        if song.genre == user.favorite_genre:
            score += genre_bonus
            reasons.append(f"This song was given a slight score bonus of {genre_bonus} due to it matching the user's genre of {user.favorite_genre}")

        return score, reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # Score every song, then sort by score (highest first) and keep top k.
        scored = [(self.score(user, song)[0], song) for song in self.songs]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self.score(user, song)
        return f"Score {score:.2f} — " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    # read_csv infers types per column: id -> int, the numeric feature
    # columns -> float, and text columns (title/artist/genre/mood) -> str.
    df = pd.read_csv(csv_path)
    # to_dict("records") turns each row into a {column: value} dict, giving
    # the List[Dict] the rest of the functional path expects.
    return df.to_dict(orient="records")

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # Reuse the same scoring logic as the OOP path: convert the plain dicts
    # into the dataclasses Recommender.score expects, then delegate.
    song_obj = Song(**song)
    user = UserProfile(
        name=user_prefs.get("name", "anonymous"),
        favorite_genre=user_prefs.get("genre", ""),
        favorite_mood=user_prefs.get("mood", ""),
        target_energy=user_prefs.get("energy", 0.5),
        # main.py's example profile has no acousticness, so default to a
        # neutral 0.5 (biases toward neither acoustic nor electronic).
        target_acousticness=user_prefs.get("acousticness", 0.5),
    )
    return Recommender.score(user, song_obj)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Score each song, then sort by score (highest first) and keep the top k.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
