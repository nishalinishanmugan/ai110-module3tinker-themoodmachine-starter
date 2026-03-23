# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
Describe whether you used the rule based model, the ML model, or both.  
Example: “I used the rule based model only” or “I compared both models.”

I compared both the rule based model and the ML model. 

**Intended purpose:**  
What is this model trying to do?  
Example: classify short text messages as moods like positive, negative, neutral, or mixed.

The purpose of this model is to classify short text into mood categories such as positivie, negative. neutral, or mixed. 

**How it works (brief):**  
For the rule based version, describe the scoring rules you created.  
For the ML version, describe how training works at a high level (no math needed).

The rule-based model uses a list of positive and negative words to create a score for each message. If there are more positive words, the score increases. If there are more negative words, then the score decreases. Whichever final score value dominates, then that determines the final classification of the text. The ML model is trained based on specific examples in the dataset. And the training helps predicts the mood of the text. 


## 2. Data

**Dataset description:**  
Summarize how many posts are in `SAMPLE_POSTS` and how you added new ones.

The SAMPLE_POSTS have 14 in total. The original data set had 6. And I added 8 more examples to add more positive, negative, mixed, and neutral words. I also included everyday language, emois, and statements with mixed emotions. 

**Labeling process:**  
Explain how you chose labels for your new examples.  
Mention any posts that were hard to label or could have multiple valid labels.

Each post was labeled as positive, netagive, neutral, or mixed depending on the emotional tone of the sentence. I thought about the overall meaning of the text instead of invidiual words. For example, "Feeling tired but kind of hopeful" is mixed. And "I feel cold and I have a cough, but I'm okay" is also mixed. Because they have both positive and negative words. 

**Important characteristics of your dataset:**  
Examples you might include:  

- Contains slang or emojis  
- Includes sarcasm  
- Some posts express mixed feelings  
- Contains short or ambiguous messages

I have informal language, emojis, mixed emotional statements, sarcasm, and short vague messages. 

**Possible issues with the dataset:**  
Think about imbalance, ambiguity, or missing kinds of language.

The dataset is small because it only has 14 examples. Some of the statements are vaugue, so there would be more than one label. This is fine could be postiive, but it also could be mixed. It's hard for the AI model to identify sarcasm based on how small the dataset is. Some emojis and emotional words are missing, so those are more likely to be mislabled. 

## 3. How the Rule Based Model Works (if used)
**Your scoring rules:**  
Describe the modeling choices you made.  
Examples:  

- How positive and negative words affect score  
- Negation rules you added  
- Weighted words  
- Emoji handling  
- Threshold decisions for labels

In the preprocessing stage, it converts text from lowercase, removed punctuation, and it splits the sentence into words. For each positive, the score increases by 1. For each negative word, the score decreases by -1. Positive emojis can increase the score. And negative emojis can decrease the score. The model also checks if the meaning is flipped like "not happy". That would be classified as negative. If the text only has positive words, then it is labeled as positive. If the text only have negative words, then it is labeled as negative. If it has both positive and negative words, then it is mixed. If there are no positive or negative words, then it is neutral. 

**Strengths of this approach:**  
Where does it behave predictably or reasonably well?

It performs well when asked clear emotional words such as "love", "terrible", or "excited. It performs better if it is words that are in the dataset. If the text is emotional and direct instead of being vaugue, then that performs better. 

**Weaknesses of this approach:**  
Where does it fail?  
Examples: sarcasm, subtlety, mixed moods, unfamiliar slang.

The model can't label sarcasm. That's a big limitation such as "I love getting stuck in traffic". It can't understand deep text. It will probably ignore unfamilar slang or expressions. And subtle emotions can be ignored if it is not in the dataset. 

## 4. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
Example: “Bag of words using CountVectorizer.”

The model uses bag of words using CountVectorizer. This converts each text into a vector based on the frequency of specific emotional words. 

**Training data:**  
State that the model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.

The model was trained using the labeled examples in SAMPLE_POSTS and TRUE_LABELS from dataset.py.

**Training behavior:**  
Did you observe changes in accuracy when you added more examples or changed labels?

When I added more examples, this made the model more accurate because it had more emamples of positive and negative words as well as emojis and expressions that it could learn from. 

**Strengths and weaknesses:**  
Strengths might include learning patterns automatically.  
Weaknesses might include overfitting to the training data or picking up spurious cues.

It can learn patterns from lableled examples. It can perform better than the rule-based model for sarcasm. It is more likely to overfit a small dataset. It is learning based on statistical patterns only. It is more sensitive to small changes in the training data. 

## 5. Evaluation

**How you evaluated the model:**  
Both versions can be evaluated on the labeled posts in `dataset.py`.  
Describe what accuracy you observed.

Both models were evaluated by comparing predicted labels to the human labels in dataset.py. The ML model was more accurate with a 1.00 accuracy. But the rule-based model was more at 0.86 accuracy because it incorrectly labeled "This is fine" and "I absolutely love getting stuck in traffic". But the first statement is vague and the second is sarcasm, so this is just a limitation.

**Examples of correct predictions:**  
Provide 2 or 3 examples and explain why they were correct.

“Today was a terrible day” was labeled as negative. Both models correctly identified the word “terrible” as a negative emotion.
“Kinda nervous about that presentation but also excited for tomorrow” was labeled as mixed. The models recognized both positive and negative emotions such as nervous being negative and excited being positive. 
“I have to file my taxes 💀” was labled as negative. The emoji and wording showed negative emotion for both models. 

**Examples of incorrect predictions:**  
Provide 2 or 3 examples and explain why the model made a mistake.  
If you used both models, show how their failures differed.

The rule-based model failed for “This is fine”. It was predicted positive, but it was true neutral. But the ML model predicted this as neutral correctly. The rule-based model interpreted “fine” as a positive word and not with a neutral tone.The rule-based model failed for “I absolutely love getting stuck in traffic” . It predicted positive, but it was true negative. The model focused on the “love” and failed to detect sarcasm.But the ML model predicted this as negative correctly.
Before I fixed the mixed emotion. The rule-based ML model incorrectly labled this statement: “Feeling tired but kind of hopeful”. It classified it as negative, but the mixed logic helped it get classified as mixed. 

## 6. Limitations

Describe the most important limitations.  
Examples:  

- The dataset is small  
- The model does not generalize to longer posts  
- It cannot detect sarcasm reliably  
- It depends heavily on the words you chose or labeled

The dataset is small because there are only 14 examples. If the messages are more complex, then both models are more likely to predict incorrecly. The rule-based model can't predict sarcasm or messages that are subtle. The ML model is more likely to overfit.Both models depend on diversity of labeled data.

## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications.  
Examples: 

- Misclassifying a message expressing distress  
- Misinterpreting mood for certain language communities  
- Privacy considerations if analyzing personal messages

I can misclassify messages that express distress, which would be misleading. Mood can be interpreted differently across cultures and different langugage communities, which can lead to bias. There could be some privacy concerns with analysing personal intimate text. There could be incorrect decisions if this was used for mental health monitoring, which would be determinal. 

## 8. Ideas for Improvement

List ways to improve either model.  
Possible directions:  

- Add more labeled data  
- Use TF IDF instead of CountVectorizer  
- Add better preprocessing for emojis or slang  
- Use a small neural network or transformer model  
- Improve the rule based scoring method  
- Add a real test set instead of training accuracy only

The preprocessing could be improved to handle more emojis and slang. It can be improved to add weighted emotional words instead of just rule-based scoring. It can be improved by using a more advance model like neutral networks. Better sarcasm detection can improve the classification. The dataset has to be expanded to include more examples. 

Bias and Scope

This model is optimized for english speakers annd casual tone. It also includes some common slang and emojis. The model may misinterpret non-english text, cultural expressions from specific communities, formal writing, and sarcas,. 

Rule-Based vs Machine Learning Comparison

The ML model is senstive to labels. Changing a few lables changes the predictions. And if the sarcasm was labeled differently, it would behave differently. The rule-based model is sensitive to word list design and score rules. If these aspects are improved and expanded, then the rule-based model would improve. 
