"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os

from recommender import load_songs, recommend_songs

# data/ sits next to src/, one level up from this file. Resolving the path
# relative to __file__ means main.py works no matter where it's launched from.
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


def main() -> None:
    songs = load_songs(CSV_PATH)

    # Sanity check: confirm every song loaded before we start recommending.
    print(f"\nLoaded {len(songs)} songs:")
    for song in songs:
        print(f"  [{song['id']}] {song['title']} - {song['artist']} ({song['genre']})")

    # A few example profiles, including some edge cases, to show how the
    # scoring reacts to different (and sometimes incomplete) preferences.
    # Each profile carries a "name" (the user's online tag) so they're easy
    # to tell apart in the output.
    profiles = [
        # Starter example: pop / happy / high energy.
        {"name": "PopFanJaz", "genre": "pop", "mood": "happy", "energy": 0.8},

        # Matching acousticness: a quiet, acoustic lofi profile. energy 0.35
        # and acousticness 0.86 line up exactly with tracks like "Library Rain".
        {
            "name": "LoFiLuna",
            "genre": "lofi", "mood": "chill",
            "energy": 0.35, "acousticness": 0.86,
        },

        # Edge case: extreme high-energy, fully-electronic rock.
        {
            "name": "RiffRaiderX",
            "genre": "rock", "mood": "intense",
            "energy": 1.0, "acousticness": 0.0,
        },

        # Edge case: a genre no song has, so the genre bonus never applies.
        {"name": "PolkaPioneer", "genre": "polka", "mood": "happy", "energy": 0.5},

        # Edge case: a partial profile (energy only) — genre/mood/acousticness
        # fall back to their defaults instead of crashing.
        {"name": "MinimalMax", "energy": 0.5},
    ]

    for user_prefs in profiles:
        # Compact "key=value" description of the profile, e.g.
        # "name=PopFanJaz, genre=pop, mood=happy, energy=0.8".
        details = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
        print(f"\nUser profile: {details}")
        print("Recommendations:")

        recommendations = recommend_songs(user_prefs, songs, k=5)
        for rank, (song, score, _explanation) in enumerate(recommendations, start=1):
            print(f"  {rank}. {song['title']} - {song['artist']} (Score: {score:.2f})")


if __name__ == "__main__":
    main()
