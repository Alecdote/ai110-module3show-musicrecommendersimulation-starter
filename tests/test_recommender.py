import os

from src.recommender import *

DATA_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


def make_song(**overrides) -> dict:
    """A song dict with sensible defaults; override any field per test."""
    base = dict(
        id=1, title="t", artist="a", genre="pop", mood="happy",
        energy=0.5, tempo_bpm=100, valence=0.5,
        danceability=0.5, acousticness=0.5,
    )
    base.update(overrides)
    return base

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        name="TestListener",
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_acousticness=0.2,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        name="TestListener",
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_acousticness=0.2,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- Functional path: load_songs -------------------------------------------

def test_load_songs_reads_all_rows_with_numeric_types():
    songs = load_songs(DATA_CSV)
    assert len(songs) > 0
    first = songs[0]
    # Text stays str; feature columns are converted to numbers.
    assert isinstance(first["title"], str)
    assert isinstance(first["energy"], float)
    assert isinstance(first["acousticness"], float)


# --- Functional path: score_song -------------------------------------------

def test_score_song_adds_genre_bonus_on_match():
    # Two identical songs except genre; the matching one should score
    # exactly genre_bonus higher.
    base = dict(
        id=1, title="t", artist="a", mood="chill",
        energy=0.5, tempo_bpm=100, valence=0.5,
        danceability=0.5, acousticness=0.5,
    )
    prefs = {"name": "GenreTester", "genre": "rock", "energy": 0.5, "acousticness": 0.5}

    match_score, _ = score_song(prefs, {**base, "genre": "rock"})
    miss_score, _ = score_song(prefs, {**base, "genre": "pop"})

    assert round(match_score - miss_score, 6) == genre_bonus


def test_genre_is_only_a_small_bonus_feel_dominates():
    # A song with a perfect energy/acoustic fit but the WRONG genre should
    # still beat a wrong-feel song that happens to match the genre.
    prefs = {"name": "FeelFirstFan", "genre": "rock", "energy": 0.8, "acousticness": 0.2}
    good_feel_wrong_genre = dict(
        id=1, title="fit", artist="a", genre="pop", mood="x",
        energy=0.8, tempo_bpm=120, valence=0.5,
        danceability=0.5, acousticness=0.2,
    )
    bad_feel_right_genre = dict(
        id=2, title="genre", artist="a", genre="rock", mood="x",
        energy=0.0, tempo_bpm=60, valence=0.5,
        danceability=0.5, acousticness=1.0,
    )
    high, _ = score_song(prefs, good_feel_wrong_genre)
    low, _ = score_song(prefs, bad_feel_right_genre)
    assert high > low


# --- Functional path: recommend_songs --------------------------------------

def test_recommend_songs_returns_k_sorted_descending():
    songs = load_songs(DATA_CSV)
    prefs = {"name": "TopKTester", "genre": "pop", "mood": "happy", "energy": 0.8}
    results = recommend_songs(prefs, songs, k=3)

    assert len(results) == 3
    scores = [score for _song, score, _explanation in results]
    assert scores == sorted(scores, reverse=True)
    # Each result carries a non-empty explanation string.
    assert all(isinstance(expl, str) and expl for _s, _sc, expl in results)


# --- Edge cases: scoring boundaries ----------------------------------------

def test_perfect_match_scores_the_maximum():
    # Every component maxed out: energy(0.5) + acoustic(0.3) + mood(0.15)
    # + genre(0.05) == 1.0.
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2}
    song = make_song(genre="pop", mood="happy", energy=0.8, acousticness=0.2)
    score, _ = score_song(prefs, song)
    assert round(score, 6) == 1.0


def test_complete_mismatch_scores_zero():
    # Opposite feel on both continuous features and no categorical matches
    # bottoms the score out at 0.0.
    prefs = {"genre": "rock", "mood": "intense", "energy": 1.0, "acousticness": 0.0}
    song = make_song(genre="pop", mood="happy", energy=0.0, acousticness=1.0)
    score, _ = score_song(prefs, song)
    assert round(score, 6) == 0.0


def test_name_does_not_affect_score():
    # The name/tag is identity only; it must never change the numeric score.
    song = make_song()
    with_name = {"name": "DJTest", "genre": "pop", "energy": 0.5, "acousticness": 0.5}
    without_name = {"genre": "pop", "energy": 0.5, "acousticness": 0.5}
    assert score_song(with_name, song)[0] == score_song(without_name, song)[0]


def test_missing_acousticness_defaults_to_neutral_half():
    # Omitting acousticness should behave exactly like passing 0.5.
    song = make_song(acousticness=0.7)
    omitted = {"genre": "pop", "energy": 0.5}
    explicit = {"genre": "pop", "energy": 0.5, "acousticness": 0.5}
    assert score_song(omitted, song)[0] == score_song(explicit, song)[0]


def test_mood_bonus_applies_only_on_match():
    prefs = {"mood": "happy", "energy": 0.5, "acousticness": 0.5}
    match = score_song(prefs, make_song(mood="happy"))[0]
    miss = score_song(prefs, make_song(mood="sad"))[0]
    assert round(match - miss, 6) == mood_bonus


def test_unknown_genre_never_earns_the_genre_bonus():
    # A genre no song has: the genre reason should never appear.
    prefs = {"genre": "polka", "energy": 0.5, "acousticness": 0.5}
    _score, reasons = score_song(prefs, make_song(genre="pop"))
    assert not any("genre" in reason.lower() for reason in reasons)


# --- Edge cases: recommend_songs boundaries --------------------------------

def test_recommend_songs_k_larger_than_catalog_returns_all():
    songs = load_songs(DATA_CSV)
    prefs = {"name": "Big K", "genre": "pop", "energy": 0.5}
    results = recommend_songs(prefs, songs, k=1000)
    assert len(results) == len(songs)


def test_recommend_songs_k_zero_returns_empty():
    songs = load_songs(DATA_CSV)
    prefs = {"name": "Zero K", "genre": "pop", "energy": 0.5}
    assert recommend_songs(prefs, songs, k=0) == []


def test_recommend_on_empty_catalog_returns_empty():
    user = UserProfile(
        name="EmptyCatalog",
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_acousticness=0.2,
    )
    assert Recommender([]).recommend(user, k=5) == []
