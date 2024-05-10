import random

# Basic Data
# Course No: Course Type (1: Theory, 2: Lab)
courses = {1: 1, 2: 2, 3: 1, 4: 1}

# Section No: No of students
sections = {1: 119, 2: 54, 3: 120, 4: 60}

# Professor No: List of Course Nos that he can teach
professors = {
    1: [1, 2],
    2: [3, 4],
    3: [1, 4],
    4: [2, 3],
    5: [1,2,3,4],
    6: [5,3,1],
    7: [2,4,5],
    8: [2,3,4],
    9: [4,5,3],
    10: [1,2,3,4,5]
}

# Timeslot No: Time
timeslots = {
    1: "8:30 - 9:50",

    2: "10:05 - 11:25",
    3: "11:40 - 1:00",
    4: "1:15 - 2:35",
    5: "2:50 - 4:10",
    6: "4:25 - 5:45",
}

# Room No: Capacity, Room Name (Same floor rooms like 4th floor has 401, 402, 3rd floor 301, 302 etc.)
rooms = {
    1: [60, 101],
    2: [120, 201],
    3: [60, 301],
    4: [120, 401],
    5: [60, 501],
    6: [120, 601]
}

def get_total_classes():
    count_theory = 0
    count_lab = 0
    for course in courses:
        if courses[course] == 1:
            count_theory += 2
        else:
            count_lab += 1
    total_classes = count_theory * 2 * len(sections) + count_lab * len(sections)
    return total_classes

def get_min_classes_per_day():
    total_classes = get_total_classes()
    return total_classes // 5

# Genetic Algorithm

# A function which gets the min bits needed to represent any dictionary
def get_min_bits(dictionary):
    return len(bin(max(dictionary.keys()))[2:])

def get_course_len_bits():
    return len(bin(len(courses))[2:])

def generate_chromosome():
    final = ""
    for i in range(5):
        chromosome = ""
        classes = get_min_classes_per_day()
        temp_courses = []
        courses_count = 0
        for course in courses:
            if courses[course] == 2:
                temp_courses.append(course)
                temp_courses.append(course)
            else:
                temp_courses.append(course)
        for _ in range(classes):
            if len(temp_courses) == 0:
                courses_count = 0
                continue
            else:
                courses_count += 1
            course = random.choice(temp_courses)
            temp_courses.remove(course)
            section = random.choice(list(sections.keys()))
            professor = random.choice(list(professors.keys()))
            room = random.choice(list(rooms.keys()))
            timeslot = random.choice(list(timeslots.keys()))
            day = i + 1
            # print('C:',course, courses_count, section, professor, room, timeslot, day)
            # use get_min_bits to get the min bits needed to represent any dictionary
            chromosome += format(course, f"0{get_min_bits(courses)}b")
            # chromosome += format(courses_count, f"0{get_course_len_bits()}b")
            chromosome += format(section, f"0{get_min_bits(sections)}b")
            chromosome += format(professor, f"0{get_min_bits(professors)}b")
            chromosome += format(room, f"0{get_min_bits(rooms)}b")
            chromosome += format(timeslot, f"0{get_min_bits(timeslots)}b")
            # 5 days so 3 bits
            chromosome += format(day, "03b")
        chromosome = format(courses_count, f"0{get_course_len_bits()}b") + chromosome
        final += chromosome
    return final

def chromosome_to_timetable(chrm):
    # Take into account the min classes per day
    timetable = {}
    classes = get_min_classes_per_day()
    # Get the total bits to iterate over the chromosome
    total_bits = get_min_bits(courses) + get_min_bits(sections) + get_min_bits(professors) + get_min_bits(rooms) + get_min_bits(timeslots) + 3
    for i in range(5): # 5 days
        timetable[i + 1] = []
        # Get course count in the day
        class_count = classes
        chrm = chrm[get_course_len_bits():]
        for j in range(class_count):
            start = (i * class_count + j) * total_bits
            end = start + total_bits
            gene = chrm[start:end]
            course = int(gene[:get_min_bits(courses)], 2)
            section = int(gene[get_min_bits(courses):get_min_bits(courses) + get_min_bits(sections)], 2)
            professor = int(gene[get_min_bits(courses) + get_min_bits(sections):get_min_bits(courses) + get_min_bits(sections) + get_min_bits(professors)], 2)
            room = int(gene[get_min_bits(courses) + get_min_bits(sections) + get_min_bits(professors):get_min_bits(courses) + get_min_bits(sections) + get_min_bits(professors) + get_min_bits(rooms)], 2)
            timeslot = int(gene[get_min_bits(courses) + get_min_bits(sections) + get_min_bits(professors) + get_min_bits(rooms):get_min_bits(courses) + get_min_bits(sections) + get_min_bits(professors) + get_min_bits(rooms) + get_min_bits(timeslots)], 2)
            day = int(gene[get_min_bits(courses) + get_min_bits(sections) + get_min_bits(professors) + get_min_bits(rooms) + get_min_bits(timeslots):], 2)
            # print('T:',course, class_count, section, professor, room, timeslot, day)
            # Check if course is in the dictionary
            course_type = 'N/A'
            if course in courses:
                course_type = "Theory" if courses[course] == 1 else "Lab"
            timetable[i + 1].append({
                "course": course,
                "type": course_type,
                "section": section,
                "professor": professor,
                "room": room,
                "timeslot": timeslot,
                "day": day,
            })
        
    return timetable



def create_population(population_size):
    population = []
    for _ in range(population_size):
        population.append(generate_chromosome())
    return population

def display_timetable(timetable):
    for day in timetable:
        print(f"Day: {day}")
        for lecture in timetable[day]:
            print(
                f"Course: {lecture['course']}, Type: {lecture['type']}\t Section: {lecture['section']}, Professor: {lecture['professor']}, Room: {lecture['room']}, Timeslot: {lecture['timeslot']}"
            )

def fitness(chromosome):
    # Convert the chromosome to a timetable
    timetable = chromosome_to_timetable(chromosome)

    # Initialize a high fitness score
    fitness_score = 100

    
    # Check each constraint and subtract a penalty for each violation
    for day in timetable:
        # Initialize dictionaries to keep track of professor and section schedules
        professor_schedule = {}
        section_schedule = {}

        # Initialize dictionary to count no. of courses each professor teaches
        professor_courses = {}

        # Initialize dictionary to count no. of courses each section has
        section_courses = {}

        # Initialize dictionary to track the schedule for each course
        course_schedule = {}

        # Initialize dictionary to track the schedule for each lab
        lab_schedule = {}

        # Initialize dictionary to track the schedule for each room
        room_schedule = {}

        for lecture in timetable[day]:
            course = lecture['course']
            section = lecture['section']
            professor = lecture['professor']
            room = lecture['room']
            timeslot = lecture['timeslot']

            # Check if values are within the allowed range
            if course not in courses or section not in sections or professor not in professors or room not in rooms or timeslot not in timeslots:
                return -1000

            # Check if the room is big enough for the section
            if sections[section] > rooms[room][0]:
                fitness_score -= 1

            # Check if the professor is teaching another class at the same time
            if professor in professor_schedule and timeslot in professor_schedule[professor]:
                fitness_score -= 1
            else:
                professor_schedule.setdefault(professor, []).append(timeslot)

            # Check if the section has another class at the same time
            if section in section_schedule and timeslot in section_schedule[section]:
                fitness_score -= 1
            else:
                section_schedule.setdefault(section, []).append(timeslot)

            # Update the number of courses each professor teaches
            professor_courses[professor] = professor_courses.get(professor, 0) + 1

            # Check if the professor is teaching more than 3 courses
            if professor_courses[professor] > 3:
                fitness_score -= 1

            # Update the number of courses each section has
            section_courses[section] = section_courses.get(section, 0) + 1

            # Check if the section has more than 5 courses in a semester
            if section_courses[section] > 5:
                fitness_score -= 1

            # Update the room schedule
            room_schedule.setdefault(room, []).append(timeslot)

            # Check if the room is being used by another class or not
            if room in room_schedule and timeslot in room_schedule[room]:
                fitness_score -= 1

            # Check if each course has two lectures per week not on the same or adjacent days
            if courses[course] == 1:
                if course in course_schedule and (day in course_schedule[course] or day-1 in course_schedule[course] or day+1 in course_schedule[course]):
                    fitness_score -= 1
                else:
                    course_schedule.setdefault(course, []).append(day)

            # Check if the next timeslot is the same lab
            if courses[course] == 2:
                if course in lab_schedule and timeslot - 1 in lab_schedule[course]:
                    fitness_score -= 1
                else:
                    lab_schedule.setdefault(course, []).append(timeslot)

    return fitness_score

def crossover(chromosome1, chromosome2):
    crossovered_chromosome = ""
    for gene1, gene2 in zip(chromosome1, chromosome2):
        if random.random() < 0.5:
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
    # Choose two random chromosomes from the population
    tournament_size = 5
    tournament = random.sample(list(enumerate(fitness_values)), tournament_size)

    # Return the index of the chromosome with the highest fitness
    return max(tournament, key=lambda x: x[1])[0]


def mutation(chromosome, mutation_rate):
    mutated_chromosome = ""
    for gene in chromosome:
        if random.random() < mutation_rate:
            # Flip the bit
            mutated_chromosome += "0" if gene == "1" else "1"
        else:
            mutated_chromosome += gene
    return mutated_chromosome

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
        for _ in range(population_size - 1, 2):
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
    if max(fitness_values) > max_fitness:
        max_fitness = max(fitness_values)
    # Convert the best chromosome to a timetable
    timetable = chromosome_to_timetable(best_chromosome)

    return timetable, max_fitness

# print("---------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------")
# chrom = generate_chromosome()
# print(chrom)
# timetable = chromosome_to_timetable(chrom)
# display_timetable(timetable)
# print("---------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------")
# print("---------------------------------------------------------------------------------------")

# Run the genetic algorithm
population_size = 1000
generations = 1000
mutation_rate = 0.01
timetable, fitness_score = genetic_algorithm(population_size, generations, mutation_rate)

# Display the final timetable
display_timetable(timetable)
print("Fitness Score:", fitness_score)