
#Q1
import queue
from datetime import datetime, timedelta

#the patient class
class Patient:
#'Initializing' the attributes of the objects
#"none because no appointment date and time have been set yet"
#'self' as a keyword to access variables, attributes and methods of a defined class which in this case is patient
    def __init__(self, name, age, appointment_date = None, appointment_time = None):
        self.name = name
        self.age = age
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time

#function for patient info
#insert the patients details into the string (name, age, date, time)
    def patient_info(self): return "{}, Age: {}, Appointment: {} {}".format(self.name, self.age, self.appointment_date, self.appointment_time)

#dictionary to hold queues for each date
appointment_schedule = {}

#dictionary to store the last appointment time for each date
last_appointment_time = {}

#this function calculates the next available appointment time for a given date
def get_next_appointment_time(date_str):
#use the global dictionary to track last appointment times for each date
    global last_appointment_time
#convert the date string from "D/M" format to a datetime object representing the date
    date = datetime.strptime(date_str, "%d/%m").date()
#check if the date is already in the last_appointment_time dictionary
    if date not in last_appointment_time:
#if the date is not present, start the first appointment of the day at 9:00 AM
        next_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=9)
    else:
#if the date is present, increment the last appointment time by 30 minutes
        last_appointment_time[date] += timedelta(minutes=30)
        next_time = last_appointment_time[date]
#update the last_appointment_time dictionary with the new appointment time
    last_appointment_time[date] = next_time
#return the next available appointment time as a string in "HH:MM" format
    return next_time.strftime("%H:%M")

#function to add a new patient to the appointment schedule
def add_patient(name, age, appointment_date):
#try to validate the date format
    try:
        datetime.strptime(appointment_date, "%d/%m")  # Check if the date string matches the "D/M" format
    except ValueError:
#if the date format is invalid, print an error message and exits the function
        print("Invalid date format. Please use the format D/M.")
        return

#automatically assigns the next available appointment time for the given date
    appointment_time = get_next_appointment_time(appointment_date)

#create a new Patient instance with the provided name, age, and calculated appointment time
    patient = Patient(name, age, appointment_date, appointment_time)

#check if there is already a queue for the given date in the appointment schedule
    if appointment_date not in appointment_schedule:
#if the date is new, initialize a new queue for that date
        appointment_schedule[appointment_date] = queue.Queue()

#adds the new patient to the queue for the specified date
    appointment_schedule[appointment_date].put(patient)

#prints a confirmation message with the patient's name, appointment date, and time
    print(f"Patient {name} has been added for {appointment_date} at {appointment_time}.")

#function to view the waitlist
def view_waitlist():
#print the header for the waitlist
    print("\nWaitlist for all appointments:")
#sort the dates in the appointment schedule in chronological order
    sorted_dates = sorted(appointment_schedule.keys(), key=lambda d: datetime.strptime(d, "%d/%m"))
#loop through each sorted date
    for date in sorted_dates:
        print(f"\nAppointments for {date}:")
#retrieves the queue of patients for the current date
        category_queue = appointment_schedule[date]
#convert the queue to a list to sort the patients by appointment time
        all_patients = list(category_queue.queue)
#sorts the patients by their appointment time in ascending order
        all_patients.sort(key=lambda patient: datetime.strptime(patient.appointment_time, "%H:%M"))
#loops through the sorted patients and print their information
        for idx, patient in enumerate(all_patients, 1):
            if idx == 1:
#prints the first patient's information without an arrow
                print(patient.patient_info(), end='')
            else:
#prints subsequent patients' information with an arrow showing the next
                print(" -> ", end='')
                print(f"{patient.name}_{date}_{patient.appointment_time}", end='')
        print()


def cli():
#menu to choose from
    while True:
        print()
        print("Welcome to the clinic, please select the action from the menu below.")
        print("1. Add a patient.")
        print("2. View waitlist.")
        print("3. Exit")

#input their choice
        choice = input("Enter your choice: ")

#allows the user to input their information and adds it to the attributes at the top
        if choice == "1":
            name = input("Enter patient's name: ")
            age = input("Enter patient's age: ")
            appointment_date = input("Enter preferred date (D/M): ")
            add_patient(name, age, appointment_date)

#calls the waitlist function
        elif choice == "2":
            view_waitlist()

#exits the program and breaks the loop
        elif choice == "3":
            print("Exiting the program.")
            break
#if something other than 1,2,3 is entered
        else:
            print("Invalid choice. Please try again.")

#10 patients, 3 of which had 3 appointments already
patients = [
    ("Ally Smith", 30, "31/5"),
    ("Ally Smith", 30, "1/6"),
    ("Ally Smith", 30, "2/6"),
    ("Bobby Johnson", 45, "29/5"),
    ("Bobby Johnson", 45, "30/5"),
    ("Bobby Johnson", 45, "1/6"),
    ("Caroline Lee", 30, "31/5"),
    ("Caroline Lee", 30, "2/6"),
    ("Caroline Lee", 30, "3/6"),
    ("David Willy", 25, "30/5"),
    ("Evelyn Davis", 25, "1/6"),
    ("Frankie Brown", 27, "30/5"),
    ("Gracie Clark", 31, "31/5"),
    ("Hank Lewis", 22, "31/5"),
    ("Ivy Walker", 23, "1/6"),
    ("Jack Hall", 27, "1/6"),
    ("Katy Allen", 28, "2/6"),
    ("Leonardo Young", 29, "3/6"),
    ("Mama Mia", 35, "3/6")
]

#iterates over each tuple in the patients list
for name, age, date in patients:
#unpack the tuple into name, age, and date variables
#calls the add_patient function with the unpacked values
    add_patient(name, age, date)

#starts the CLI function
cli()

#Q2
import queue
from datetime import datetime, timedelta

#patient class
class Patient:
#'Initializing' the attributes of the objects
#"none because no appointment time have been set yet"
#'self' as a keyword to access variables, attributes and methods of a defined class which in this case is patient
    def __init__(self, name, age, health_category, appointment_time=None):
        self.name = name
        self.age = age
        self.health_category = health_category
        self.appointment_time = appointment_time
#a method to retrieve formatted patient information in a single line
#patient details can be accessed via attributes in the placeholders
def patient_info(self): return "{}, Age: {}, Category: {}, Appointment Time: {}".format(self.name, self.age, self.health_category, self.appointment_time)

#dictionary to hold queues for each category
#allows for organization of patients waiting for appointments, with separate queues for different categories
appointment_schedule = {
    "General Consultation": queue.Queue(),
    "Obstetrics and Gynaecology": queue.Queue(),
    "Minor Surgery": queue.Queue()
}

#dictionary to store the last appointment time for each category
last_appointment_time = {
#"none" helps in determining the next available appointment time for each category when scheduling new appointments.
    "General Consultation": None,
    "Obstetrics and Gynaecology": None,
    "Minor Surgery": None
}

#mapping for category short forms to full names
#this dictionary provides a mapping between abbreviated category names (short forms) and their corresponding full names.
category_map = {
    "GC": "General Consultation",
    "OandG": "Obstetrics and Gynaecology",
    "MS": "Minor Surgery"
}

#function to determine the next available appointment time for a given health category
def get_next_appointment_time(health_category):
#for accessing the global variable to track the last appointment time for each category
    global last_appointment_time

    if not last_appointment_time[health_category]:
 #if there's no previous appointment for this category, start the first appointment of the day at 9:00 AM
        last_appointment_time[health_category] = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    else:
#if there's a previous appointment, schedule the next appointment one hour later
        last_appointment_time[health_category] += timedelta(hours=1)
#return the next available appointment time for the given health category in "HH:MM" format
    return last_appointment_time[health_category].strftime("%H:%M")

#function to add a new patient
def add_patient(name, age, health_category):
#automatically assign the next available appointment time
    appointment_time = get_next_appointment_time(health_category)
#create a new patient object with the provided details
    patient = Patient(name, age, health_category, appointment_time)

#check if the provided health category is valid and exists in the appointment schedule
#if so, add the patient to the corresponding queue for that category
    if health_category in appointment_schedule:
        appointment_schedule[health_category].put(patient)
#if not, this message is printed
    else:
        print("Invalid health category")

#function to view waitlist
def view_waitlist():
    print()
    print("Please select the category you want to view:")
    print("1. General Consultation")
    print("2. Obstetrics and Gynaecology")
    print("3. Minor Surgery")

#allows the user to enter the health category of the waitlist they want to view
    category_choice = input("Enter your choice: ")

    if category_choice == "1":
        category = "General Consultation"
    elif category_choice == "2":
        category = "Obstetrics and Gynaecology"
    elif category_choice == "3":
        category = "Minor Surgery"
    else:
        print("Invalid choice.")
        return

#P\print the waitlist for the selected category
    print(f"\nWaitlist for {category}:")
    if category in appointment_schedule:
#retrieve the queue of patients for the selected category
        category_queue = appointment_schedule[category]
#convert the queue to a list to allow sorting
        all_patients = list(category_queue.queue)
#sort the patients by their appointment time
        all_patients.sort(key=lambda patient: datetime.strptime(patient.appointment_time, "%H:%M"))
#print the patient information for each patient in the waitlist
        for patient in all_patients:
            print(patient.patient_info())
#if there are no patients, a message will be printed
    else:
        print("No appointments in", category_choice)

def call_patient(category):
#checks if the category is in the appointment schedule and if there are patients in the queue
    if category in appointment_schedule and not appointment_schedule[category].empty():
#retrieves and removes the patient from the queue for the specified category
        patient = appointment_schedule[category].get()
#prints a message indicating that the patient is being called
        print(f"Calling patient: {patient.patient_info()}")
    else:
#prints a message if there are no patients in the queue for the specified category
        print("No patients in the queue for this category.")


#menu of actions the user want to do
def cli():
    while True:
        print()
        print("Welcome to the clinic, please select the action from the menu below.")
        print("1. Add a patient.")
        print("2. View waitlist.")
        print("3. Call patient.")
        print("4. Exit")

#input to let the user choose
        choice = input("Enter your choice: ")

        if choice == "1":
#the user to enter their name, age, and health category
            name = input("Enter patient's name: ")
            age = input("Enter patient's age: ")
            health_category_short = input("Enter health category (GC (General Consultation), OandG (Obstetrics and Gynaecology), MS (Minor Surgery)): ")
#convert the short form of health category to full name
            health_category = category_map.get(health_category_short)
#print a message indicating that the patient has been added successfully
            print("Patient", name, "added successfully in", health_category, "queue.")
#check if the health category is valid, if not, inform the user and continue the loop
            if not health_category:
                print("Invalid health category")
                continue
#add the patient to the appointment schedule
            add_patient(name, age, health_category)

#calls the waitlist function
        elif choice == "2":
            view_waitlist()

        elif choice == "3":
            print()
            print("Please select the category you want to call a patient from:")
            print("1. General Consultation")
            print("2. Obstetrics and Gynaecology")
            print("3. Minor Surgery")
            print()

#lets the patient choose the health category of the patient they want to call
            category_choice = input("Enter your choice: ")

            if category_choice == "1":
                category = "General Consultation"
            elif category_choice == "2":
                category = "Obstetrics and Gynaecology"
            elif category_choice == "3":
                category = "Minor Surgery"
            else:
                print("Invalid choice.")
                continue

            call_patient(category)
#exits the function and breaks the loop
        elif choice == "4":
            print("Exiting the program.")
            break
#result of an input other than 1,2,3,4
        else:
            print("Invalid choice. Please try again.")

#a list of 13 patients
patients = [
    ("Joey Lee", 30, "General Consulation"),
    ("Annie Fong", 25, "Obstetrics and Gynaecology"),
    ("Vinny Lay", 40, "Minor Surgery"),
    ("Vicky Lam", 35, "General Consulation"),
    ("Timmy Turner", 29, "Obstetrics and Gynaecology"),
    ("Tommy Lee", 50, "Minor Surgery"),
    ("Sammy Tong", 45, "General Consultation"),
    ("Anthony Tan", 33, "Obstetrics and Gynaecology"),
    ("Kenny Rogers", 38, "Minor Surgery"),
    ("Bobby Brown", 28, "General Consultation"),
    ("Celine Kang", 31, "Obstetrics and Gynaecology"),
    ("Joyce Wong", 42, "Minor Surgery"),
    ("Edward Ong", 27, "General Consultation")
]

for name, age, category_short in patients:
#get the full name of the health category using category_map
    category = category_map.get(category_short)
#add the patient to category they chose to the appointment schedule
    add_patient(name, age, category)

#starts function the CLI
cli()

#Q3
import networkx as nx
import matplotlib.pyplot as plt

#create graph 1: Company Hierarchy Network with nodes A to G
graph1 = nx.Graph()
nodes_graph1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
edges_graph1 = [('A', 'B'), ('A', 'D'), ('B', 'C'),
                ('C', 'E'), ('D', 'E'), ('D', 'G'),
                ('E', 'G')]
graph1.add_nodes_from(nodes_graph1)
graph1.add_edges_from(edges_graph1)

#create graph 2: Bus Routes Network with nodes A to G
graph2 = nx.Graph()
nodes_graph2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
edges_graph2 = [('A', 'C'), ('A', 'D'), ('B', 'E'), ('C', 'F'),
                ('C', 'G'), ('D', 'E'), ('E', 'G'), ('F', 'G')]
graph2.add_nodes_from(nodes_graph2)
graph2.add_edges_from(edges_graph2)

#graph 1

#degree centrality
degree_centralities_graph1 = nx.degree_centrality(graph1)
print()
print("Graph 1:")
print("Degree Centrality:")
for node, centrality in degree_centralities_graph1.items():
    print(f"{node}: {centrality}")

#connectivity
is_connected_graph1 = nx.is_connected(graph1)
print("Is Connected:", is_connected_graph1)

#is tree
is_tree_graph1 = nx.is_tree(graph1)
print("Is Tree:", is_tree_graph1)

#graph 2

#degree centrality
degree_centralities_graph2 = nx.degree_centrality(graph2)
print()
print("Graph 2:")
print("Degree Centrality:")
for node, centrality in degree_centralities_graph2.items():
    print(f"{node}: {centrality}")

#connectivity
is_connected_graph2 = nx.is_connected(graph2)
print("Is Connected:", is_connected_graph2)

#is tree
is_tree_graph2 = nx.is_tree(graph2)
print("Is Tree:", is_tree_graph2)

#graph 1
plt.figure()
nx.draw(graph1, with_labels=True, font_weight='bold', node_color='lightblue', node_size=500)
plt.title('Graph 1: Company Hierarchy Network')
plt.show()

#graph 2
plt.figure()
nx.draw(graph2, with_labels=True, font_weight='bold', node_color='lightpink', node_size=500)
plt.title('Graph 2: Transportation Network for Bus Routes')
plt.show()