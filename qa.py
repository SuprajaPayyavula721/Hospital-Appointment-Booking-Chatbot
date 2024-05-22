import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Removing the stop words
stop_words = set(stopwords.words("english"))


def clean_text(text):
    tokens = word_tokenize(text)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return " ".join(filtered_tokens)


def answer_question(user_question, threshold=0.9):
    # Loading the dataset
    data = pd.read_csv("QA.csv")
    questions = data["Question"]
    answers = data["Answer"]

    # Remove stop words
    stop_words = set(stopwords.words("english"))

    
    clean_questions = []
    for question in questions:
        clean_questions.append(clean_text(question))

    # Calculating TF-IDF vectors for questions and answers
    tfidf_vectorizer = TfidfVectorizer()
    question_tfidf = tfidf_vectorizer.fit_transform(clean_questions)
    answer_tfidf = tfidf_vectorizer.transform(answers)

   
    clean_user_question = clean_text(user_question)

    # Calculating cosine similarity between user's question and questions in the dataset
    user_question_tfidf = tfidf_vectorizer.transform([clean_user_question])
    similarities = cosine_similarity(user_question_tfidf, question_tfidf)

    # Getting the index of the question with the highest similarity
    most_similar_index = similarities.argmax()

    # Getting the answer for the question with the highest similarity
    answer = answers[most_similar_index]

    # Checking if the similarity is above the threshold
    if similarities[0][most_similar_index] > threshold:
        # Return the answer if the similarity is above the threshold
        return answer
    else:
        # Return a message if the similarity is below the threshold
        return "No answer found"


# Ask user for a question
#user_question = "what is in the alpine mountain systems"

# Get the answer to the user's question
#answer = answer_question(user_question)

# Print the answer to the user
#print(answer)











'''import pandas as pd
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem.snowball import SnowballStemmer

# Loading the dataset
data = pd.read_csv('QA.csv')

# Extracting questions and answers
questions = data['Question'].tolist()
answers = data['Answer'].tolist()

# Initializing a stemmer
stemmer = SnowballStemmer('english')

# Preprocessing questions and answers
preprocessed_questions = []
preprocessed_answers = []

for question in questions:
    question_tokens = nltk.word_tokenize(question.lower())
    stemmed_question = [stemmer.stem(token) for token in question_tokens]
    preprocessed_questions.append(' '.join(stemmed_question))

for answer in answers:
    answer_tokens = nltk.word_tokenize(answer.lower())
    stemmed_answer = [stemmer.stem(token) for token in answer_tokens]
    preprocessed_answers.append(' '.join(stemmed_answer))

# Creating a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fitting the vectorizer to the preprocessed questions
tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_questions)

# threshold for similarity matching
threshold = 0.8


def find_matching_answer(prompt):
    # Preprocessing the user question
    preprocessed_user_question = stemmer.stem(prompt.lower())

    # Calculating cosine similarity between the user question and all questions
    user_question_vector = tfidf_vectorizer.transform([preprocessed_user_question])
    cosine_similarities = cosine_similarity(user_question_vector, tfidf_matrix)

    # Finding the index of the question with the highest cosine similarity
    highest_similarity_index = np.argmax(cosine_similarities)

    # Checking if the similarity is above the threshold
    if cosine_similarities[0, highest_similarity_index] >= threshold:
        return preprocessed_answers[highest_similarity_index]
    else:
        return "NOT FOUND"


user_question = "how big is bmc software in houston, tx"
response = find_matching_answer(user_question)
print(response)'''
