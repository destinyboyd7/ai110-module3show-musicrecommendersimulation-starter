# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

Model Name: Music Map

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

My recommender is designed to recommend songs to user that are similar to prefernces set in their profiles. I assigned name generes mood and energy to user prefernces.  My system is designed to match songs with the users profile prefernce and it shouldn't be used by someone trying to diverisfy their playlist. 

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

My model works by taking the features described in the user prferences and cross reference them with the songs in the dataseet to get the ranking. Genre, mood, energy, tempo, valence, danceability, and mode are features of each song used to rank theme. User preferences consisted on genre, mood, and energy. 

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

20 songs are currently included in the dataset. Lofi, pop, edm, hip-hop, and rock are all respresented. Happy, chill, intnse, relaxed, moody, hopeful, focused, and all some moods reprsented in the dataset. While the dataset has wide representation I think genres like rnd and alternative are missing. 

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

My system gives reasonable results for all user types however I think a larger data set would expand it's accuracy. It properly scores genre, energy, and mood this is because these are set in user profile the others points are also assinged in ranges. 

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

One weakness I discovered is that my recommender heavily prioritzes genre and mood. The scoring gives strong points to songs that are similar in these areas, the system may keep recommending the same type of music to the user instead of offering variety. This means the user can get stuck with the same styles. Also, my recommeneder has repeated generes and some genres like lofi and pop that may become over prioitized due to small dataset. 

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested 9 profiles set up in my main.py file. In my reccomendations I looked for genre to match becuase they was mostimportant to me when setting up my rcommender. Nothing surpirsed me but I was glad to see that even thought the generes were the same they didnt have the same highest recommendeed song it showed that other categories were being considered. 

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I would improve the following inmy recommender:
1. Include additional genres 
2. Add interest section to user profile to suggests song that the user may want to explore
3. Improve diversity of user profiles and dataset information

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

My biggest learning moment during this project was properly setting up the recommender and balancing out my alorigthmn recipe. Using AI for this tool helped me to understand the logic behind the recommender. I had to check AI when builiding my user preference profiles and when priting my top recommendation becuase often it would want to duplicate code that I had already added or suggest profiles with addition information then I wanted. It surprised me how simple it can feel to compare the songs with the user preferences for ranking. If I was to extend the project I would try to add features of users adding in their on preferences instead of hardcoded logic. 
