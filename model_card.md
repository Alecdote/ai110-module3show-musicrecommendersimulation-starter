# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MoodSynker 1** — I called it this because my recommender mostly cares about the "feel" of a song (its energy and how acoustic it is) and tries to sync a song to the mood/vibe the user is looking for, more than the genre label.

---

## 2. Intended Use  

This recommender is supposed to find songs that match the kind of vibe a listener is in the mood for, instead of just matching a genre, it generates a short ranked list (the top k songs) with a little reason attached to each one so you can see why it got picked. It assumes the user already knows roughly what they want and can describe it as a taste profile (a favorite genre, a favorite mood, a target energy, and a target acousticness), and it also assumes that the number features are the most honest signal of what a song actually feels like. Though outside of it being a test-case, it is definitely not mean't to be used for a real-world application but more so figuring out how a small recommender like spotify, youtube, or apple music works.

---

## 3. How the Model Works  

Every song in my catalog has a genre, a mood, an energy number, and an acousticness number, and the user profile has a target for each of those same things. To score a song the model basically checks how close the song's energy and acousticness are to what the user asked for, and the closer they are the higher the score. Energy matters the most (it is worth 0.5 of the score) and acousticness is second (0.3), while matching the mood (0.15) and the genre (0.05) only add small bonuses on top. So a perfect song can reach a score of 1.0 and a total opposite lands at 0.0. The biggest change I made from the starter was turning acousticness from a true/false switch into a target number between 0 and 1, that way "kind of acoustic" is a real option instead of just yes or no, and it gets scored by closeness the same way energy does.

---

## 4. Data  

The catalog is a CSV with 45 songs. I expanded it a lot from the original 10 because most genres only had one song, so the recommender had nothing to actually pick between. Now there are around 30 genres (pop, lofi, rock, hip hop, r&b, edm, jazz, classical, folk, metal, k-pop, and a bunch more) and a wide range of moods like happy, chill, intense, moody, calm, and melancholy. I also made sure to add several songs with energy under 0.30 so that a low energy listener actually has variety instead of getting stuck with the same few chill songs. Parts of musical taste that are still missing are things like the year a song came out, the language or lyrics, and anything about the artist, so the dataset only really captures the "sound" of a song and not its meaning or culture.

---

## 5. Strengths  

The system works best for a listener who has a clear vibe in mind, like someone who wants high energy non-acoustic gym music or someone who wants low energy acoustic study music, because those requests line up cleanly with the energy and acousticness numbers. It seems to correctly capture the idea that two songs in different genres can still "feel" the same, for example a high energy pop song and a high energy rock song end up near each other, which matches how I actually listen. When I tested a pop/happy/high energy profile the top picks were upbeat pop and funk songs, which is exactly what I expected, so the scoring lined up with my intuition.

---

## 6. Limitations and Bias 

The model only looks at energy and acousticness for the real scoring, so it ignores who the artist is, the lyrics, the language, and whether a song is trending right now. A big fairness issue is with brand new listeners: if someone does not fill out a full profile the defaults land around 0.5, which quietly pushes them toward mid-to-low energy songs instead of giving them a fair spread, so the "average" user gets a biased starting point. It can also overfit to one preference, since energy is worth half the whole score a song with the perfect energy can beat a song that matches everything else. And because genre is only worth 0.05, genres that are underrepresented do not really get a fair shot anyway, the feel of the song basically overrides the label.

---

## 7. Evaluation  

I mostly checked the model with the pytest tests and by running different user profiles by hand to see if the top songs made sense. I ran 15 automated tests and they all passed, and they check things like a perfect match scoring 1.0, a total mismatch scoring 0.0, the genre bonus being small, and the username never changing the score. For the by-hand part I tested profiles like a pop/happy/high energy fan and a low energy acoustic listener and looked at whether the top 5 actually matched the vibe I asked for. What surprised me was how often songs from totally different genres showed up next to each other in the results, which made it really clear that my model is ranking by feel and not by genre.

---

## 8. Future Work  

I would like to group similar genres together (like treating "pop" and "indie pop" as related) so the genre bonus is not so all-or-nothing. Another improvement would be adding some diversity to the top results so it does not return five songs that all feel identical, and giving a better default for new users instead of just 0.5 so they are not biased toward low energy. Longer term it would be cool to explain recommendations in more natural language and to handle more complex tastes, like a user who likes two very different vibes at once.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Honestly I was a bit surprised to learn how surprisingly adaptable the hybrid style model works when done in an actual production setting. Being able to see what the user likes before actually comparing them to song data makes a lot of sense to see how the user not only listens to the songs but behaves when interacting with them makes me appreciate them slightly more because they get more accurate the longer you use them. While implementing this small recommender though, I did not take any of that into account and while it was still a bit of a pain to set it up, it still made me appreciate all the work that goes into these systems.