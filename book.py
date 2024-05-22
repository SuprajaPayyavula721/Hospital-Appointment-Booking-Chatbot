import json
import random
import re
import csv


def appointment_data(appointment_details):
    with open('appointments.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            appointment_details['day'],
            appointment_details['slot'],
            appointment_details['doctor'],
            appointment_details['patient_age'],
            appointment_details['patient_phone'],
            appointment_details['patient_email'],
            appointment_details['patient_health_issue'],
            appointment_details['booking_id'],
            appointment_details['user_feedback']
        ])
        
        
def random_id():
    random_id = random.randint(1, 50)
    return random_id

def book_appointment():
    # Loading the available slots data from the JSON file
    data = json.load(open('available_slots.json'))
    
#Available weeks
    print("Chatbot: Sure, I will search my database for available days. Please wait.")
    print("Chatbot: Available days")
    for week in data['availableslots']:
        print(week['week'].lower())
        
    
    print("Note: We are not available on weekends")
#Preferred week from the user
    while True:
        print("Chatbot: Enter the preferred week ")
        preferred_week = input("User: ")
        preferred_week = preferred_week.lower()


        if preferred_week not in [week['week'].lower() for week in data['availableslots']]:
          print("Chatbot: Invalid week. Please try again.")
          continue

    # Finding the data with the matching week which user has provided
        index = [week['week'].lower() == preferred_week for week in data['availableslots']].index(True)
        slot_list = data['availableslots'][index]['slots']

    # Printing all the available slots for the preferred week
        print("Chatbot: Available slots for " + preferred_week + ":")
        for slot in slot_list:
            print(slot)

    #Asking preferred slot from the user
        while True:
            print("Chatbot: Enter the preferred slot ")
            preferred_slot = input("User: ")
            preferred_slot = preferred_slot.lower()
            slot_list = [slot.lower() for slot in slot_list]

        # Checking if the input is valid and belongs to the selected week
            if preferred_slot not in slot_list:
                print("Chatbot: Invalid slot. Please enter a valid slot.")
                continue
        
        # Finding the index of the matching slot
            slot_index = slot_list.index(preferred_slot)
        
        # Getting the list of available doctors for the selected slot
            doctor_list = data['availableslots'][index]['doctors']

    # Printing all the available doctors for the selected slot
            print("Chatbot: Available doctors for " + preferred_slot + ":")
            for doctor in doctor_list:
                print(doctor)

    # Getting the preffered doctor from the user
            while True:
                print("Chatbot: Enter the preferred doctor")
                preferred_doctor = input("User: ")
                preferred_doctor = preferred_doctor.lower()
                doctor_list = [doctor.lower() for doctor in doctor_list]
            
            # Checking if the input is valid and belongs to the selected slot
                if preferred_doctor not in doctor_list:
                    print("Chatbot: Invalid doctor. Please enter a valid doctor.")
                    continue

    # Printing a confirmation message
                print("Chatbot: Schedule booked for " + preferred_week + " at " + preferred_slot + " with " + preferred_doctor)
                break
            break

        break

    # Collecting user information
    age_regex = "^[0-9]{1,3}$"
    phone_regex = "^(?:\d{10}|\w+@\w+\.\w{2,3})$"
    email_regex = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+(?:\.[a-zA-Z0-9-]+)*$"
    print("Chatbot: Please enter patient name")
    patient_name = input("User: ")
    print("Chatbot: Please enter your age")
    user_age = input("User: ")
    while not re.match(age_regex, user_age):
        print("Chatbot: Invalid age. Please enter a valid age ")
        user_age = input("User: ")
    
    print("Chatbot: Please enter your phone number")
    user_phone = input("User: ")
    while not re.match(phone_regex, user_phone):
        print("Chatbot: Invalid phone number. Please enter a valid phone number")
        user_phone = input("User: ")

    print("Chatbot: Please enter your email address")
    user_email = input("User: ")
    while not re.match(email_regex, user_email):
        print("Chatbot: Invalid email address. Please enter a valid email address")
        user_email = input("User: ")

    print("Chatbot: Please enter your health issue")
    user_problem = input("User: ")
    

    # Storing appointment details
    appointment_details = {
        "day": preferred_week,
        "slot": preferred_slot,
        "doctor": preferred_doctor,
        "patient_age": user_age,
        "patient_phone": user_phone,
        "patient_email": user_email,
        "patient_health_issue": user_problem,
        "patient_name": patient_name
    }
    # Confirming appointment details and booking
    print("Chatbot: Patient appointment details:")
    print("day:"+preferred_week+ "\n slot:"+preferred_slot+ "\n doctor:"+preferred_doctor+ "\n patient_age:"+user_age+ "\n patient_contact:"+user_phone+ "\n patient_email:"+user_email+"\n patient_health_issue:"+user_problem+"\n patient_name:"+patient_name) 

    print("Chatbot: I'll make the appointment for you now. Is that okay? (yes/no)")
    confirmation = input("User: ")

    # Generating a unique booking ID if the user confirms
    if confirmation.lower() == "yes":
        booking_id = random_id()

        # Adding the booking ID to the appointment details
        appointment_details['booking_id'] = booking_id
        # Informing the user that booking is successfull
        print("Chatbot: Your appointment is successfully booked. Booking ID:", booking_id)
    else:
        # Informing the user of appointment cancellation
        print("Chatbot: Appointment canceled.")
    
    feedback_prompt = "Chatbot: Would you like to provide feedback on your appointment booking experience? (yes/no): "
    feedback = input(feedback_prompt)

    #feedback based on user's response
    if feedback.lower() == "yes":
        print("Chatbot: Please provide your feedback")
        feedback = input("User: ")
        appointment_details['user_feedback'] = feedback
        appointment_data(appointment_details)
        print("Chatbot: Thank you for your feedback. We appreciate it!")
    else:
        print("Chatbot: No problem! I appreciate your honesty.")