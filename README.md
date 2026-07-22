# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

My version is a content-based music recommender, which means it picks songs by looking at the songs own features instead of what other people listened to. Each song in my `songs.csv` has a genre, mood, and some number features like energy and acousticness. The user is just a taste profile that says what they are looking for (a favorite genre, a favorite mood, a target energy, and a target acousticness). To make a recommendation, my program gives every song a score between 0 and 1, and it cares about the "feel" of the song the most, so energy is worth the most at 0.5 for the weights and acousticness is next to energy at 0.3, while matching the mood (0.15) and the genre (0.05) are only small bonuses on top. After every song is scored it ranks them from highest to lowest and returns the top k, and it also gives a short reason for why each song got picked so you can actually see what matched.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

The song as well as the user's profile has a variety of different features, but the feature itself that we would be using in order to try and create a limited but functional song recommendation lists are the song's:
* acousticness
* energy
* genre
* mood
The only difference is that the user specifically has a name for their online username as well for our music recommender.
The recommender computes a score for each song by first seeing if the energy and acousticness matches the user's target energy and acoustic ness, if it does then the score will be significantly higher than those who do not, the genre and mood exist as a little bonus to add to the score since it does generally match the user's preference. If it was part of the recommender function, then it would have scored all the songs together using the above attributes and then sorts it by the score in descending order and returning the top k number of songs. These k number of songs is the songs we would recommend to the user.


---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```
(venv) PS C:\Users\jruan\OneDrive\Documents\AI110\ai110-module3show-musicrecommendersimulation-starter> pytest
================================================================================================================================================== test session starts ===================================================================================================================================================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\jruan\OneDrive\Documents\AI110\ai110-module3show-musicrecommendersimulation-starter
plugins: anyio-4.13.0
collected 15 items                                                                                                                                                                                                                                                                                                        

tests\test_recommender.py ...............                                                                                                                                                                                                                                                                           [100%]

=================================================================================================================================================== 15 passed in 0.47s ===================================================================================================================================================

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

User profile: name=PopFanJaz, genre=pop, mood=happy, energy=0.8
Recommendations:
  1. Sunrise City - Neon Echo (Score: 0.89)
  2. Rooftop Lights - Indigo Parade (Score: 0.89)
  3. Get Up Groove - The Funk Unit (Score: 0.86)
  4. Weekend Anthem - Voltline (Score: 0.85)
  5. Backroad Sunshine - Dusty Boots (Score: 0.84)

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.
Some significant limitations are those who are completely new to music or want to just figure out what songs they enjoy because the base/default input for them is 0.5. since they don't have a complete profile in the slightest, these types of profiles will gear toward songs that are mid to low energy since they have lower end acousticness or energy that matches these newer listeners. This specific recommender only looks at the energy and acousticness, it does not look at who the artist is, the lyrics behind the song, or whether or not it is trending in the current week.
Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Recommenders use the user's data to interpret what the user may like depending on the song's internal data as well. It uses the weights that it has assigned to it either by other engineers who have designed the system,the ones that it has gained from other users, or the song's trending data to influence whether or not to recommend this song to the users. This has a huge effect towards users because while it can recommend songs that align with certain users very well, other songs who may have been written by top artists or written very well may not get the recognition they may rightly deserve simply because the algorithm did not find it viable for that user specifically due to some factor pushing it down. This is where some biases start to show their effects. Similarly to the one that I have implemented where it boosts the songs that align with the users genre and mood, some songs who cater to the popular genres may be boosted in favor than other songs simply because they are more likely to match with those users than the ones who are catering to the much smaller genres in the music industry. This means that some lower quality songs may be artificially boosted due to them matching a user's or general public's profile significantly better than other probably better songs in the same genre. Some ways I could combat this if I had more time would be to try and incorporate some form of an average watch time for the song so that the better quality songs could shine much better than those who have a unusually higher skip rate, but then again it could introduce some other unknown side effects within the algorithm to the user. 

