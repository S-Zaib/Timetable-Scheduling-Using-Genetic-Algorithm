import random

# Basic Data
# Course No: Course Type (1: Theory, 2: Lab)
courses = {
    1 : 1,
    2 : 2,
    3 : 1,
    4 : 1,
    5 : 1,
    6 : 2,
    7 : 1,
    8 : 1,
    9 : 2,
    10 : 1}

# Section No: No of students
sections = {
    1 : 60,
    2 : 120,
    3 : 60,
    4 : 120,
    5 : 60}
# Professor No: List of Course Nos
professors = {
    1 : [1, 2],
    2 : [3, 4],
    3 : [5, 6],
    4 : [7, 8],
    5 : [9, 10],
    6 : [2, 3],
    7 : [4, 5],
    8 : [6, 7, 8],
    7 : [9, 10]}

# Timeslot No: Time
timeslots = {
    1 : "8:30 - 9:50",
    2 : "10:05 - 11:25",
    3 : "11:40 - 1:00",
    4 : "1:15 - 2:35",
    5 : "2:50 - 4:10",
    6 : "4:25 - 5:45",
}

# Room No: Capacity and Timeslots
rooms = {
    101 : [60, list(timeslots.keys())],
    201 : [60, list(timeslots.keys())],
    102 : [120, list(timeslots.keys())],
    202 : [120, list(timeslots.keys())],
    301 : [120, list(timeslots.keys())],
    302 : [120, list(timeslots.keys())],
    401 : [60, list(timeslots.keys())],
    402 : [60, list(timeslots.keys())],
    501 : [120, list(timeslots.keys())],
    502 : [120, list(timeslots.keys())],
    601 : [60, list(timeslots.keys())],
    602 : [60, list(timeslots.keys())],
    701 : [120, list(timeslots.keys())],
    702 : [120, list(timeslots.keys())],
    801 : [120, list(timeslots.keys())],
    802 : [120, list(timeslots.keys())],
    901 : [60, list(timeslots.keys())],
    902 : [60, list(timeslots.keys())],
    1001 : [120, list(timeslots.keys())]
}

def has_consecutive_timeslots(room):
    timeslots = sorted(room)
    for i in range(len(timeslots) - 1):
        if timeslots[i] + 1 == timeslots[i + 1]:
            return timeslots[i]
    return -1


# The chromosomes should be a whole timetable binary encoded with the following information:
# Course, Theory/Lab, Section, Section-Strength, Professor, First-lecture-day,
# First- lecture-timeslot, First-lecture-room, First-lecture-room-size, Second-
# lecture-day, Second-lecture-timeslot, Second-lecture-room, Second-lecture-
# room-size and so on depending on the number of lectures in a week.
def create_chromosome():
    chromosome = []
    for course in courses:
        # Select random count of 1 to number of sections for the course
        count = random.randint(1, len(sections))
        section_copy = sections.copy()
        for _ in range(count):
            # Select a random section
            section = random.choice(list(section_copy.keys()))
            # Get the section strength
            section_strength = section_copy[section]
            # Remove the section from the list to avoid repetition
            del section_copy[section]
            # Select a random professor that teaches the course
            possible_professors = [professor for professor, courses in professors.items() if course in courses]
            professor = random.choice(possible_professors)
            # Select a random room that can accommodate the section strength
            possible_rooms = [room for room, room_info in rooms.items() if room_info[0] >= section_strength]
            room = random.choice(possible_rooms)
            # Select a random timeslot for the lecture, select 1 if the course is theory and 2 if the course is lab
            # Add 1 timeslot and -1 for the second timeslot if course is theo
            timeslot = timeslot2 = -1
            max_tries = 10
            while rooms[room][1] == [] and max_tries > 0:
                    room = random.choice(possible_rooms)
                    max_tries -= 1
            if rooms[room][1] == []:
                print('No timeslots available')
                break
            if courses[course] == 1:
                timeslot = random.choice(list(rooms[room][1]))
                max_tries = 10
                while timeslot == -1 and max_tries > 0:
                    room = random.choice(possible_rooms)
                    timeslot = random.choice(rooms[room][1])
                    max_tries -= 1
                if timeslot != -1:
                    rooms[room][1].remove(timeslot)
                timeslot2 = -1
            else:
                # Check if the room has any consecutive timeslots available
                max_tries = 10
                timeslot = has_consecutive_timeslots(rooms[room][1])
                while timeslot == -1 and max_tries > 0:
                    print(rooms[room][1], timeslot)
                    room = random.choice(possible_rooms)
                    timeslot = has_consecutive_timeslots(rooms[room][1])
                    max_tries -= 1
                    if timeslot != -1:
                        rooms[room][1].remove(timeslot)                    
                if timeslot != -1 and courses[course] == 2:
                    timeslot2 = timeslot + 1
                    rooms[room][1].remove(timeslot2)

            if timeslot == -1 or timeslot2 == -1:
                print('No timeslots available')
                break
                            

            #     timeslot = random.choice(list(timeslots_copy.keys()))
            #     timeslot2 = -1
            # else:
            #     timeslot = random.choice(list(timeslots_copy.keys()))
            #     del timeslots_copy[timeslot]
            #     timeslot2 = random.choice(list(timeslots_copy.keys()))
            
            # Append the course no
            chromosome.append(course)
            # Append the course type
            chromosome.append(courses[course])
            # Append the section information
            chromosome.append(section)
            # Append the section strength
            chromosome.append(section_strength)
            # Append the professor 
            chromosome.append(professor)
            # Append the timeslot
            chromosome.append(timeslot)
            chromosome.append(timeslot2)
            # Append the room no and room size
            chromosome.append(room)
            chromosome.append(rooms[room][0])

    return chromosome
# In one chromosome, the first 5 elements are the course information and the rest are the lecture information
# Course, Theory/Lab, Section, Section-Strength, Professor, First-lecture-day,
# First- lecture-timeslot, First-lecture-room, First-lecture-room-size, Second-
# lecture-day, Second-lecture-timeslot, Second-lecture-room, Second-lecture-
# room-size and so on depending on the number of lectures in a week.

# Display timetable function
def display(chromosome):
    for i in range(0, len(chromosome), 9):
        course = chromosome[i]
        course_type = chromosome[i+1]
        section = chromosome[i+2]
        section_strength = chromosome[i+3]
        professor = chromosome[i+4]
        timeslot = chromosome[i+5]
        timeslot2 = chromosome[i+6]
        room = chromosome[i+7]
        room_size = chromosome[i+8]
        print(f"Course: {course}, Course Type: {course_type}, Section: {section}, Section Strength: {section_strength}, Professor: {professor}, Timeslot: {timeslots[timeslot]}" , end="")
        if timeslot2 != -1:
            print(f", {timeslots[timeslot2]}, Room: {room}, Room Size: {room_size}")
        else:
            print(f", Room: {room}, Room Size: {room_size}")

display(create_chromosome())



def create_population(population_size):
    population = []
    for i in range(population_size):
        population.append(create_chromosome())
    return population



        



