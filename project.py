import random
import pandas as pd

# Basic Data
# Course No: Course Type (1: Theory, 2: Lab)
courses = {1: 1, 2: 2, 3: 1, 4: 1}

# Section No: No of students
sections = {1: 119, 2: 54, 3: 59, 4: 110}

# Professor No: List of Course Nos that he can teach
professors = {
    1: [1, 2, 3],
    2: [3, 4, 1],
    3: [1, 4, 2],
    4: [2, 3, 4],
    5: [1, 2, 3, 4],
    6: [3, 4],
    7: [1, 2, 3],
    8: [1, 2, 3, 4],
    9: [2, 3, 4],
    10: [1, 3, 4],
}

# Timeslot No: Time
timeslots = {
    1: "8:30 - 9:50",
    2: "10:05 - 11:25",
    3: "11:40 - 1:00",
    4: "1:15 - 2:35",
    5: "2:50 - 4:10",
    6: "4:25 - 5:45"
}

# Room No: Capacity, Room Name (Same floor rooms like 4th floor has 401, 402, 3rd floor 301, 302 etc.)
rooms = {
    1: [60, 101],
    2: [120, 102],
    3: [60, 203],
    4: [120, 202],
    5: [60, 201],
    6: [120, 303],
    7: [60, 302],
    8: [120, 301]
}

# Names of the courses
course_names = {
    1: "Data Structures",
    2: "Algorithms",
    3: "Database Management",
    4: "Operating Systems"
}

# Names of the professors
professor_names = {
    1: "Sir Aadil",
    2: "Sir Saad Salman",
    3: "Sir Ejaz",
    4: "Sir Ali",
    5: "Sir Usman",
    6: "Sir Noman",
    7: "Sir Ahsan",
    8: "Sir Umar",
    9: "Sir Asad",
    10: "Sir Fahad"
}

# Names of the rooms
room_names = {
    1: "Room 101",
    2: "Room 102",
    3: "Room 203",
    4: "Room 202",
    5: "Room 201",
    6: "Room 303",
    7: "Room 302",
    8: "Room 301"
}

# Names of the sections
section_names = {
    1: "Section A",
    2: "Section B",
    3: "Section C",
    4: "Section D"
}


# Helper Functions
def get_total_classes():
    count_theory = 0
    count_lab = 0
    for course in courses:
        if courses[course] == 1:
            count_theory += 2
        else:
            count_lab += 1
    total_classes = count_theory * len(sections) + count_lab * len(sections)
    return total_classes

def get_min_classes_per_day():
    total_classes = get_total_classes()
    return total_classes // 5

# A function which gets the min bits needed to represent any dictionary
def get_min_bits(dictionary):
    return len(bin(max(dictionary.keys()))[2:])


# Genetic Algorithm Functions
def generate_chromosome():
    final = ""
    for i in range(5):
        chromosome = ""
        classes_per_day = get_min_classes_per_day()
        for _ in range(classes_per_day):
            course = random.choice(list(courses.keys()))
            section = random.choice(list(sections.keys()))
            professor = random.choice(list(professors.keys()))
            room = random.choice(list(rooms.keys()))
            timeslot = random.choice(list(timeslots.keys()))
            day = i + 1
            chromosome += format(course, f"0{get_min_bits(courses)}b")
            chromosome += format(section, f"0{get_min_bits(sections)}b")
            chromosome += format(professor, f"0{get_min_bits(professors)}b")
            chromosome += format(room, f"0{get_min_bits(rooms)}b")
            chromosome += format(timeslot, f"0{get_min_bits(timeslots)}b")
            chromosome += format(day, "03b")
        final += chromosome
    return final

# A function to convert the chromosome to a timetable
def chromosome_to_timetable(chrm):
    # Take into account the min classes per day
    timetable = {}
    classes = get_min_classes_per_day()
    # Get the total bits to iterate over the chromosome
    total_bits = (
        get_min_bits(courses)
        + get_min_bits(sections)
        + get_min_bits(professors)
        + get_min_bits(rooms)
        + get_min_bits(timeslots)
        + 3
    )
    for i in range(5):  # 5 days
        timetable[i + 1] = []
        # Get course count in the day
        class_count = get_min_classes_per_day()
        for j in range(class_count):
            start = i * classes * total_bits + j * total_bits
            end = start + total_bits
            course = int(chrm[start : start + get_min_bits(courses)], 2)
            section = int(
                chrm[
                    start
                    + get_min_bits(courses) : start
                    + get_min_bits(courses)
                    + get_min_bits(sections)
                ],
                2,
            )
            professor = int(
                chrm[
                    start
                    + get_min_bits(courses)
                    + get_min_bits(sections) : start
                    + get_min_bits(courses)
                    + get_min_bits(sections)
                    + get_min_bits(professors)
                ],
                2,
            )
            room = int(
                chrm[
                    start
                    + get_min_bits(courses)
                    + get_min_bits(sections)
                    + get_min_bits(professors) : start
                    + get_min_bits(courses)
                    + get_min_bits(sections)
                    + get_min_bits(professors)
                    + get_min_bits(rooms)
                ],
                2,
            )
            timeslot = int(
                chrm[
                    start
                    + get_min_bits(courses)
                    + get_min_bits(sections)
                    + get_min_bits(professors)
                    + get_min_bits(rooms) : start
                    + get_min_bits(courses)
                    + get_min_bits(sections)
                    + get_min_bits(professors)
                    + get_min_bits(rooms)
                    + get_min_bits(timeslots)
                ],
                2,
            )
            day = i + 1
            # print('T:',course, class_count, section, professor, room, timeslot, day)
            # Check if course is in the dictionary
            course_type = "N/A"
            if course in courses:
                course_type = "Theory" if courses[course] == 1 else "Lab"
            timetable[i + 1].append(
                {
                    "course": course,
                    "type": course_type,
                    "section": section,
                    "professor": professor,
                    "room": room,
                    "timeslot": timeslot,
                    "day": day,
                }
            )

    return timetable

# A function to create a population of chromosomes
def create_population(population_size):
    population = []
    for _ in range(population_size):
        population.append(generate_chromosome())
    return population

# A function to display the timetable
def display_timetable(timetable):
    for day in timetable:
        print(f"Day: {day}")
        for lecture in timetable[day]:
            print(
                f"Course: {course_names[lecture['course']]}",
                f"Type: {lecture['type']}",
                f"Section: {section_names[lecture['section']]}",
                f"Professor: {professor_names[lecture['professor']]}",
                f"Room: {room_names[lecture['room']]}",
                f"Timeslot: {timeslots[lecture['timeslot']]}",
            )
        print()


# A function to remove extra classes, failed attempt ;/
def remove_extra_classes(timetable):
    # Initialize a dictionary to keep track of the schedule for each course and section
    course_section_schedule = {}
    room_schedule = {}
    professor_schedule = {}

    # Fill up room and professor schedules
    for day in timetable:
        for lecture in timetable[day]:
            course = lecture["course"]
            section = lecture["section"]
            professor = lecture["professor"]
            room = lecture["room"]
            timeslot = lecture["timeslot"]


            # Update the room and professor schedules
            if room not in room_schedule:
                room_schedule[room] = [timeslot]
            else:
                room_schedule[room].append(timeslot)

            if professor not in professor_schedule:
                professor_schedule[professor] = [timeslot]
            else:
                professor_schedule[professor].append(timeslot)

    for day in range(1, 6):  # Assuming timetable days are numbered from 1 to 5
        # Initialize a list to keep track of the classes to remove or shift
        classes_to_remove_or_shift = []

        for lecture in timetable[day]:
            course = lecture["course"]
            section = lecture["section"]

            # Check if the course and section have two lectures on the same day
            if (course, section) in course_section_schedule and day in course_section_schedule[(course, section)]:
                # The course and section have two lectures on the same day, mark this class for removal or shifting
                classes_to_remove_or_shift.append(lecture)
            else:
                # The course and section do not have two lectures on the same day, add this day to the course and section schedule
                course_section_schedule.setdefault((course, section), []).append(day)

        # Remove or shift the marked classes
        for lecture in classes_to_remove_or_shift:
            timetable[day].remove(lecture)
            other_days = [d for d in course_section_schedule[(lecture["course"], lecture["section"])] if d != day]
            if other_days:
                # If there exists another class in the week with the same course and section, remove this class
                continue
            else:
                # If there doesn't exist another class in the week with the same course and section, shift this class 2 days ahead
                next_day = day + 2
                while next_day <= 5:  # Assuming timetable days are numbered from 1 to 5
                    # Check if the room and timeslot are free, the professor is free at that timeslot, and the room can accommodate the section
                    free_rooms = [room for room in rooms if rooms[room][0] >= sections[section] and (room not in room_schedule or next_day not in room_schedule[room])]
                    free_timeslots = [timeslot for timeslot in timeslots if (lecture["professor"] not in professor_schedule or next_day not in professor_schedule[lecture["professor"]]) and all(room not in room_schedule or next_day not in room_schedule[room] for room in free_rooms)]
                    if free_rooms and free_timeslots:
                        # Choose a room and timeslot that isn't occupied
                        lecture["room"] = random.choice(free_rooms)
                        lecture["timeslot"] = random.choice(free_timeslots)
                        timetable[next_day].append(lecture)
                        break
                    next_day += 1

    return timetable


# Heart of the project, the fitness function
def fitness(chromosome, debug=False):
    # Convert the chromosome to a timetable
    timetable = chromosome_to_timetable(chromosome)
    if debug:
        timetable = remove_extra_classes(timetable)
    # Initialize fitness to a high value
    fitness = 100

    # Initialize dictionaries to keep track of professor, room and section schedules
    professor_schedule = {}
    room_schedule = {}
    section_schedule = {}
    prof_floors = {}
    section_floors = {}

    for day in timetable:
        # Initialize dictionaries for the current day
        professor_schedule_day = {}
        room_schedule_day = {}
        section_schedule_day = {}
        course_section_room = {}
        professor_course_timeslots = {}

        for lecture in timetable[day]:
            course = lecture["course"]
            section = lecture["section"]
            professor = lecture["professor"]
            room = lecture["room"]
            timeslot = lecture["timeslot"]

            # Check if values are within the allowed range
            if (
                course not in courses
                or section not in sections
                or professor not in professors
                or room not in rooms
                or timeslot not in timeslots
            ):
                # Value is not in the allowed range, decrease fitness
                if debug:
                    print("Out of range values")
                fitness -= 100
                continue

            # Check if the room is free and big enough
            if room not in room_schedule_day:
                room_schedule_day[room] = {timeslot: section}
            elif timeslot not in room_schedule_day[room]:
                room_schedule_day[room][timeslot] = section
            else:
                # Room is already occupied at this timeslot, decrease fitness
                if debug:
                    print("Room is already occupied at this timeslot")
                fitness -= 1

            if sections[section] > rooms[room][0]:
                # Room is not big enough, decrease fitness
                if debug:
                    print("Room is not big enough")
                fitness -= 1

            # Check if the professor is free and can teach the course
            if professor not in professor_schedule_day:
                professor_schedule_day[professor] = {timeslot: course}
            elif timeslot not in professor_schedule_day[professor]:
                professor_schedule_day[professor][timeslot] = course
            else:
                # Professor is already teaching at this timeslot, decrease fitness
                if debug:
                    print("Professor is already teaching at this timeslot")
                fitness -= 1

            if course not in professors[professor]:
                # Professor can't teach this course, decrease fitness
                if debug:
                    print("Professor can't teach this course")
                fitness -= 1

            # Check if the section is free and has less than 5 courses
            if section not in section_schedule_day:
                section_schedule_day[section] = {timeslot: course}
            elif timeslot not in section_schedule_day[section]:
                section_schedule_day[section][timeslot] = course
            else:
                # Section already has a lecture at this timeslot, decrease fitness
                if debug:
                    print("Section already has a lecture at this timeslot")
                fitness -= 1

            if len(set(section_schedule_day[section].values())) > 5:
                # Section has more than 5 courses, decrease fitness
                if debug:
                    print("Section has more than 5 courses")
                fitness -= 1

            # Soft constraints
            # Check if theory courses are in the morning and lab courses are in the afternoon
            if course in courses and courses[course] == 1 and timeslot > 4:
                # Theory course is in the afternoon, decrease fitness
                if debug:
                    print("Theory course is in the afternoon")
                fitness -= 0.1
            elif course in courses and courses[course] == 2 and timeslot <= 4:
                # Lab course is in the morning, decrease fitness
                if debug:
                    print("Lab course is in the morning")
                fitness -= 0.1
            
            curr_floor = rooms[room][1] // 100 # Floors are in hundreds
            if professor not in prof_floors:
                prof_floors[professor] = curr_floor
            else:
                if prof_floors[professor] != curr_floor:
                    # Professor is teaching on a different floor, decrease fitness
                    if debug:
                        print("Professor is teaching on a different floor")
                    fitness -= 0.1
                prof_floors[professor] = curr_floor

            if section not in section_floors:
                section_floors[section] = curr_floor
            else:
                if section_floors[section] != curr_floor:
                    # Section is in a different floor, decrease fitness
                    if debug:
                        print("Section is in a different floor")
                    fitness -= 0.1
                section_floors[section] = curr_floor

            # Check if a class is held in the same classroom across the whole week
            if (course, section) in course_section_room and course_section_room[(course, section)] != room:
                # Class is not held in the same classroom across the whole week, decrease fitness
                if debug:
                    print("Class is not held in the same classroom across the whole week")
                fitness -= 0.1
            else:
                course_section_room[(course, section)] = room

            # Check if teachers prefer longer blocks of continuous teaching time
            if (professor, course) in professor_course_timeslots:
                if abs(professor_course_timeslots[(professor, course)] - timeslot) > 1:
                    # Professor has non-continuous teaching timeslots for the same course, decrease fitness
                    if debug:
                        print("Professor has non-continuous teaching timeslots for the same course")
                    fitness -= 0.1
            professor_course_timeslots[(professor, course)] = timeslot

        # Update the overall schedules with the schedules of the current day
        professor_schedule.update(professor_schedule_day)
        room_schedule.update(room_schedule_day)
        section_schedule.update(section_schedule_day)

    # Check for out of range values
    if fitness <= 0:
        return fitness

    # Check for each course if it has two lectures per week not on the same or adjacent days
    for section in section_schedule:
        course_days = {}
        for timeslot in section_schedule[section]:
            course = section_schedule[section][timeslot]
            day = (timeslot - 1) // len(timeslots) + 1
            if course not in course_days:
                course_days[course] = [day]
            else:
                course_days[course].append(day)

        for course in course_days:
            if (
                len(course_days[course]) != 2
                or abs(course_days[course][0] - course_days[course][1]) <= 1
            ):
                # Course doesn't have two lectures or they are on the same or adjacent days, decrease fitness
                if debug:
                    print(
                        "Course doesn't have two lectures or they are on the same or adjacent days"
                    )
                fitness -= 1

    # Check for each professor if they teach more than 3 courses
    for professor in professor_schedule:
        if len(set(professor_schedule[professor].values())) > 3:
            # Professor teaches more than 3 courses, decrease fitness
            if debug:
                print("Professor teaches more than 3 courses")
            fitness -= 1

    # Check if the lab course next timeslot is open with no classes for the same section
    for day in timetable:
        for lecture in timetable[day]:
            course = lecture["course"]
            section = lecture["section"]
            professor = lecture["professor"]
            room = lecture["room"]
            timeslot = lecture["timeslot"]
            if courses[course] == 2:
                next_timeslot = timeslot + 1
                if next_timeslot not in timeslots:
                    if debug:
                        print("Next timeslot is out of range")
                    fitness -= 1
                elif (
                    next_timeslot in room_schedule[room]
                    and next_timeslot in section_schedule[section]
                    and section_schedule[section][next_timeslot] != course
                ):
                    if debug:
                        print("Next timeslot is not open")
                    fitness -= 1

    return fitness

# Uniform crossover
def crossover(chromosome1, chromosome2, crossover_rate=0.5):
    crossovered_chromosome = ""
    for gene1, gene2 in zip(chromosome1, chromosome2):
        if random.random() < crossover_rate:
            if gene1 != gene2:
                if gene1 == "1":
                    crossovered_chromosome += "0"
                else:
                    crossovered_chromosome += "1"
            else:
                if gene1 == "1":
                    crossovered_chromosome += "1"
                else:
                    crossovered_chromosome += "0"
        else:
            if gene1 == "1":
                crossovered_chromosome += "1"
            else:
                crossovered_chromosome += "0"

    return crossovered_chromosome


# tournament selection
def selection(fitness_values):
    # tournament selection
    tournament_size = 5
    tournament = random.sample(range(len(fitness_values)), tournament_size)
    best_chromosome = tournament[0]
    for chromosome in tournament:
        if fitness_values[chromosome] > fitness_values[best_chromosome]:
            best_chromosome = chromosome
    return best_chromosome

# Mutation
def mutation(chromosome, mutation_rate):
    mutated_chromosome = ""
    for gene in chromosome:
        if random.random() < mutation_rate:
            # Flip the bit
            mutated_chromosome += "0" if gene == "1" else "1"
        else:
            mutated_chromosome += gene
    return mutated_chromosome

# Genetic Algorithm
def genetic_algorithm(population_size, generations, mutation_rate):
    # Create an initial population of random chromosomes
    population = create_population(population_size)
    max_fitness = -1000
    for _ in range(generations):
        # Calculate the fitness of each chromosome in the population
        fitness_values = [fitness(chromosome) for chromosome in population]

        # Create a new population
        new_population = []

        # Keep the best chromosome from the previous generation
        best_chromosome = population[fitness_values.index(max(fitness_values))]
        new_population.append(best_chromosome)

        # Create the rest of the new population
        for _ in range(population_size - 1):
            # Select two parents using tournament selection
            parent1 = population[selection(fitness_values)]
            parent2 = population[selection(fitness_values)]

            # Create a child chromosome using crossover
            child = crossover(parent1, parent2)

            # Mutate the child chromosome
            child = mutation(child, mutation_rate)

            # Add the child to the new population
            new_population.append(child)

        # Replace the old population with the new population
        population = new_population

    # Calculate the fitness of the final population
    fitness_values = [fitness(chromosome) for chromosome in population]

    # Find the best chromosome in the final population
    best_chromosome = population[fitness_values.index(max(fitness_values))]
    # Convert the best chromosome to a timetable
    timetable = chromosome_to_timetable(best_chromosome)
    timetable = remove_extra_classes(timetable)
    # Debug
    max_fitness = fitness(best_chromosome, debug=True)

    return timetable, max_fitness

# Run the genetic algorithm
population_size = 50
generations = 100

mutation_rate = 0.01
timetable, fitness_score = genetic_algorithm(
    population_size, generations, mutation_rate
)

# Display the final timetable
display_timetable(timetable)
# Get the fitness score
print("Fitness Score:", fitness_score)

# Create a DataFrame and an Excel writer
df = pd.DataFrame()
writer = pd.ExcelWriter('timetable.xlsx')

# Swap the keys with the names
for day in timetable:
    for lecture in timetable[day]:
        lecture["course"] = course_names[lecture["course"]]
        lecture["professor"] = professor_names[lecture["professor"]]
        lecture["room"] = room_names[lecture["room"]]
        lecture["section"] = section_names[lecture["section"]]
        lecture["timeslot"] = timeslots[lecture["timeslot"]]

# Create a separate sheet for each day
for day in timetable:
    df_day = pd.DataFrame(timetable[day])
    # Rename the columns
    df_day.columns = [
        "Course",
        "Type",
        "Section",
        "Professor",
        "Room",
        "Timeslot",
        "Day",
    ]
    # Write the DataFrame to the Excel file
    df_day.to_excel(writer, sheet_name=f"Day {day}", index=False)

# Save the Excel file
writer.close()