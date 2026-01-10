# Food database (could later be replaced by real API or DB)
FOODS = {
    "chicken breast": {"cal_per_gram": 1.65, "protein_per_gram": 0.31},
    "rice": {"cal_per_gram": 1.30, "protein_per_gram": 0.026},
    "egg": {"cal_per_gram": 1.55, "protein_per_gram": 0.13},
}

# Users / people being tracked
USERS = {
    "Aedin": {
        "daily_calories": 0,
        "daily_protein": 0,
        "entries": []
    },
    "Person2": {
        "daily_calories": 0,
        "daily_protein": 0,
        "entries": []
    }
}


def select_person(person_name):
    if person_name in USERS:
        return USERS[person_name]
    else:
        raise Error("Person not found")

def search_food(query):
    results = []
    for food_name in FOODS:
        if query.lower() in food_name.lower():
            results.append(food_name)
    return results

def calculate_nutrition(food_name, grams):
    food = FOODS[food_name]

    calories = food["cal_per_gram"] * grams
    protein = food["protein_per_gram"] * grams

    return calories, protein


def on_weight_change(food_name, grams):
    calories, protein = calculate_nutrition(food_name, grams)

    return {
        "calories": calories,
        "protein": protein
    }

def add_food_to_day(person_name, food_name, grams):
    calories, protein = calculate_nutrition(food_name, grams)

    USERS[person_name]["daily_calories"] += calories
    USERS[person_name]["daily_protein"] += protein

    USERS[person_name]["entries"].append({
        "food": food_name,
        "grams": grams,
        "calories": calories,
        "protein": protein,
        "timestamp": current_time()
    })

def get_daily_totals(person_name):
    return {
        "calories": USERS[person_name]["daily_calories"],
        "protein": USERS[person_name]["daily_protein"]
    }

LAST_RESET_DATE = today_date()

def check_daily_reset():
    global LAST_RESET_DATE

    now = current_datetime()

    if now.hour == 3 and now.minute >= 59:
        if LAST_RESET_DATE != today_date():
            reset_all_users()
            LAST_RESET_DATE = today_date()

def reset_all_users():
    for person in USERS:
        USERS[person]["daily_calories"] = 0
        USERS[person]["daily_protein"] = 0
        USERS[person]["entries"] = []


# Typical Request Flow
def handle_add_food_request():
    check_daily_reset()

    person = request.person
    food = request.food
    grams = request.grams

    add_food_to_day(person, food, grams)

    return get_daily_totals(person)

