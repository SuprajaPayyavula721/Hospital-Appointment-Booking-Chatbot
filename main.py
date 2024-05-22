import random
import datetime
import pandas as pd
import warnings
import re
import nltk
from qa import answer_question
from nltk.stem import WordNetLemmatizer
#nltk.download('wordnet')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from book import book_appointment
import json

#warnings.filterwarnings("ignore")

class Chatbot:
    
    def __init__(self, name, intents):
        flag = True
        print(f"Chatbot: Hi, This is Medi Assist. How may I assist you today?")
        self.name = name
        self.intents = intents
        self.context = {'name': None}
        self.database = None

    def discoverability(self):
        phrases = ["help", "what can you do"]
        return {"intent": "help", "phrases": phrases, "responses": ["You can ask me about the following:\n- Book an appointment\n- Healthcare facilities\n- Scheduling the appointment"]}
    
    def change_username(self, prompt):
        if "change my name to" in prompt.lower() or "can you change my name" in prompt.lower():
            self.context['name'] = prompt.split("change my name to", 1)[1].strip() if "change my name to" in prompt.lower() else prompt.split("can you change my name", 1)[1].strip()
            return f"Sure, I'll call you {self.context['name']}!"
        else:
            return None
         
    def username(self, prompt):
        if "my name is" in prompt.lower() or "call me" in prompt.lower():
            self.context['name'] = prompt.split("my name is", 1)[1].strip() if "my name is" in prompt.lower() else prompt.split("call me", 1)[1].strip()
            return f"Nice to meet you, {self.context['name']}!"
        else:
             return None

    def user_name(self, prompt):
        if "what is my name" in prompt.lower():
            if self.context['name']:
                return f"Your name is {self.context['name']}."
            else:
                return "I don't know your name yet. Could you please tell me?"
        else:
            return None
        
    def generate_response(self, prompt):
        
        name_response = self.username(prompt)
        if name_response:
            return name_response

        user_name_response = self.user_name(prompt)
        if user_name_response:
            return user_name_response
        
        change_name_response = self.change_username(prompt)
        if change_name_response:
            return change_name_response
        
        
        
        for phrase in self.discoverability()['phrases']:
            if prompt.lower().startswith(phrase.lower()):
                return random.choice(self.discoverability()['responses'])
        
        response = None
        for intent in self.intents:
            for phrase in intent['phrases']:
                if prompt.lower().startswith(phrase.lower()):
                    response = random.choice(intent['responses'])
                    break
       


        
        self.context['last_prompt'] = prompt
        self.context['last_response'] = response

        return response



chatbot = Chatbot("Doc", [
       {
        "intent": "greeting",
        "phrases": ["hello", "hi", "hey","hey there", "heyy",
                      "hi there",
                        "hello there",
            ],
        "responses": [  "Hello there! What is your name?",
                        "Hi! Can I have your name please?",
                        "Hey!! May I know your name please?",
                        "Hello! What is your name?",
                        "Hi there! How may I call you?",
                        "Hey!! Can I have your name please?"
],
    },
     {
                  "intent": "CourtesyGreeting",
                  "phrases": [
                        "How are you?",
                        "How are you doing?",
                        "Hope you are doing well?",
                        "Hello hope you are doing well?"
                  ],
                  "responses": [
                        " I am great, how are you? ",
                        "I am great thanks! How are you? ",
                        "I am good thank you, how are you? ",
                        " I am great, how are you? ",
                        " how are you? I am great thanks! ",
                        "I am good thank you, how are you? ",
                        "good thank you, how are you? "
                  ]
            },
        {"intent": "CourtesyGreetingResponse",
         "phrases": [
             "Am great",
             "Am fine",
             "Am good"],
         "responses": ["Nice to hear that!"]},
        {
                  "intent": "NameQuery",
                  "phrases": [
                        "What is your name?",
                        "What could I call you?",
                        "What can I call you?",
                        "Who are you?",
                        "Tell me your name?"
                  ],
                  "responses": [
                        "You can call me MediAssist",
                        "Call me MediAssist",
                        "I am MediAssist"
                  ]
            },
        {
                  "intent": "Thanks",
                  "phrases": [
                        "OK thank you",
                        "OK thanks",
                        "OK",
                        "Thanks",
                        "Thank you",
                        "That's helpful"
                        "good, thanks",
                        "ok",
                        "fine thank you",
                        "great thanks",
                        "ok, thanks",
                        "Great thanks!"
                  ],
                  "responses": [
                        "No problem! Is there anything else I can help with?",
                        "Happy to help!",
                        "Any time!",
                        "My pleasure"
                  ]
            },
        {
				"intent": "NotFineResponses",
                  "phrases": [
                        "not fine.",
                        "not great",
                        "no"
                        "sad",
                        "unhappy",
                        "unwell",
                        "depressed"
                  ],
                  "responses": [
                        "Sad to hear that! How can I help you?",
                        "Sorry to hear that! Is there anything I can do to help?",
                        "Anything I can do to help?"
                  ]
				
			},
        
        
        
    {
        "intent": "ask_time",
        "phrases": ["what time is it?", "what's the time?"],
        "responses": [f"The current day of the week is {datetime.datetime.now().strftime('%A')}. The current time is {datetime.datetime.now().strftime('%H:%M:%S')}."],
    },
    {
        "intent": "navigate",
        "phrases": ["Can you help with the directions to hospital",
            "Can you guide me through the directions to the hospital",
"I'm looking for assistance in finding my way to the hospital.",
"Could you provide me with directions to the hospital entrance",
"I'm a bit lost; can you help me navigate to the hospital",
"Where is the hospital located",
"can you  help me navigate the hospital premises",
"I need to find directions to the hospital.",
"What's the best route to the hospital",
"I'm unfamiliar with the directions, can you assist me in finding hospital"],
        "responses": ["Sure, I can help with that! Hospital is next to medical campus, University of Nottingham, Nottinghamshire.",
"Hospital is located next to medical campus, University of Nottingham, Nottinghamshire.",
"Hospital is situated next to medical campus, University of Nottingham, Nottinghamshire."],
    },
    {
        "intent": "healthcare",
        "phrases": ["Could you please provide information on the healthcare facilities",
"I'm interested in the range of medical services your hospital provides. Could you share details about your healthcare facilities",
"Can you give me an overview of the healthcare services available at your hospital, including any specialized facilities",
"I'd like to know more about the facilities at your hospital. What medical services are available for patients",
"Could you provide a list of healthcare facilities within your hospital, such as emergency services, surgical facilities, and specialized care units",
"I'm looking for information on the healthcare facilities at your hospital. Can you share details about the services you offer",
"What types of medical facilities can patients access at your hospital I'm interested in understanding the range of services available.",
"If someone were seeking medical care at your hospital, what healthcare facilities would they have access to",
"I'm curious about the healthcare facilities provided by your hospital. Could you provide an overview of the medical services available",
"Can you tell me more about the healthcare infrastructure at your hospital, including any specialized departments or facilities"],
        "responses": ["Emergency Services,Surgical Facilities,Intensive Care Units,Maternity Wards,Pediatric Care,Diagnostic Imaging,Laboratory Services,Pharmacy,Specialized Clinics (e.g., Cardiology, Oncology)"],
    },
    {
        "intent": "diet_recommendation",
        "phrases": ["Can you recommend a diet plan",
"I'm aiming to lose weight; what dietary changes do you suggest",
"What are some effective strategies for weight loss through diet",
"I want to adopt a healthier lifestyle and lose weight. Where should I start",
"Are there specific foods that can help with weight loss",
"Can you provide tips on maintaining a calorie deficit for weight loss",
"I'm looking for dietary advice to support my weight loss journey. Any recommendations",
"What role does nutrition play in achieving weight loss goals",
"Do you have any suggestions for healthy snacks that aid in weight loss",
"I've set a goal to lose weight. How can I modify my diet to achieve this"],
        "responses": ["Include a variety of colorful fruits and vegetables",
"Choose whole grains like brown rice quinoa and oats",
"Incorporate lean protein sources such as chicken fish tofu beans and legumes",
"Include healthy fats from avocados nuts seeds and olive oil",
"Opt for low-fat or fat-free dairy products or fortified alternatives",
"Stay hydrated with plenty of water; limit sugary drinks and excessive caffeine",
"Limit added sugars found in snacks candies and sweetened beverages",
"Be mindful of sodium intake; choose low-sodium options and avoid excessive salt",
"Control portion sizes to avoid overeating; use smaller plates",
"Plan meals ahead for a balanced and varied diet"],
    },
        {
        "intent": "health",
        "phrases": ["What exercises can I incorporate into my routine for better health?",
"I'm interested in improving my mental health. Any recommendations?",
"Can you suggest ways to stay healthy lifestyle",
"How does stress impact health, and what can I do to manage it effectively?",
"Are there specific foods that can boost energy and vitality?",
"I want to establish a bedtime routine for better sleep. Any tips?",
"Can you recommend mindfulness techniques for overall well-being?",
"What role does hydration play in maintaining good health?",
"I'm looking for healthy snacks. Any nutritious and tasty options?",
"How important is social connection for overall health, and how can I foster it?",
"Can you share tips on maintaining a healthy work-life balance?",
"What are the benefits of regular health check-ups, and how often should I schedule them?",
"I've heard about superfoods. Which ones are particularly beneficial for health?",
"What are the potential health risks of sitting for extended periods, and how can I counteract them?",
"I want to improve my posture. Any exercises or tips for better alignment?"],
        "responses": ["To enhance your overall health, focus on a balanced diet, regular exercise, sufficient sleep, and stress management.It's also important to stay hydrated and avoid harmful habits like smoking."],
    },
        {
        "intent": "health",
        "phrases": ["What exercises can I incorporate into my routine for better health?",
"I'm interested in improving my mental health. Any recommendations?",
"Can you suggest ways to stay motivated for a healthy lifestyle?",
"How does stress impact health, and what can I do to manage it effectively?",
"Are there specific foods that can boost energy and vitality?",
"I want to establish a bedtime routine for better sleep. Any tips?",
"Can you recommend mindfulness techniques for overall well-being?",
"What role does hydration play in maintaining good health?",
"I'm looking for healthy snacks. Any nutritious and tasty options?",
"How important is social connection for overall health, and how can I foster it?",
"Can you share tips on maintaining a healthy work-life balance?",
"What are the benefits of regular health check-ups, and how often should I schedule them?",
"I've heard about superfoods. Which ones are particularly beneficial for health?",
"What are the potential health risks of sitting for extended periods, and how can I counteract them?",
"I want to improve my posture. Any exercises or tips for better alignment?"],
        "responses": ["To enhance your overall health, focus on a balanced diet, regular exercise, sufficient sleep, and stress management.It's also important to stay hydrated and avoid harmful habits like smoking."],
    }

],)


while True:
    # Prompt the user for input.
    prompt = input("User: ")
    # Checking if the user wants to exit.
    if "bye" in prompt.lower() or "good bye" in prompt.lower():
        print("chatbot: Bye! Have a nice day!")
        break

    # Generate a response to the prompt.
    if (prompt != 'bye'):
        
        response = chatbot.generate_response(prompt)
        if response != None:
            print("chatbot:", response)
            continue

        response=answer_question(prompt)
        if response != "No answer found":
            print("Chatbot:", response)
            continue
        
        response = ["i would like to book an appointment", "can you help me with appointment booking", "book"]
        if prompt.lower() in response:
            book_appointment()
        else:
            print("Chatbot: Sorry! I couldn't understand you, Please try again.")
            
           
