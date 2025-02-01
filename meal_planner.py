import random

def calculate_calories(age, weight, height, gender, activity_level, goal):
    # BMR Calculation (Mifflin-St Jeor Equation)
    if gender.lower() == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Activity multipliers
    activity_factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9
    }

    # Calculate TDEE (Total Daily Energy Expenditure)
    tdee = bmr * activity_factors.get(activity_level.lower(), 1.2)

    # Adjust calories based on goal
    if goal.lower() == "maintain":
        calories = tdee
    elif goal.lower() == "lose":
        calories = tdee - 500  # ~0.5 kg/week loss
    elif goal.lower() == "gain":
        calories = tdee + 500  # ~0.5 kg/week gain
    else:
        return "Invalid goal! Choose 'maintain', 'lose', or 'gain'."
    return calories


def get_user_restrictions():
    """
    Prompts the user for their dietary restrictions.
    Input should be a comma-separated list (e.g., vegan, gluten free).
    Returns a set of restrictions in lower case with whitespace removed.
    """
    restrictions_input = input("Enter your dietary restrictions (comma-separated, e.g., vegan, gluten free, dairy free, nut free). If none, just press enter: ")
    restrictions = {r.strip().lower() for r in restrictions_input.split(",") if r.strip()}
    return restrictions


def filter_meals(meals, restrictions):
    """
    Filters a list of meal options based on whether they satisfy all of the given restrictions.
    Each meal in the list is a dictionary with 'name', 'restrictions', and 'calories' keys.
    """
    if not restrictions:
        return meals  # No restrictions, return all options.
    filtered = []
    for meal in meals:
        # Normalize the meal's restrictions to lowercase.
        meal_restrictions = {r.lower() for r in meal["restrictions"]}
        if restrictions.issubset(meal_restrictions):
            filtered.append(meal)
    return filtered


def select_meal(filtered_meals, meal_type, target_calories, tolerance=100):
    """
    Returns a randomly selected meal from a filtered list that is close to the target calories.
    If no meal is within the tolerance range, it returns a message indicating no options are available for that meal type.
    """
    # Filter the meals to only include those whose calories are within the tolerance range of the target calories.
    close_meals = [meal for meal in filtered_meals if abs(meal["calories"] - target_calories) <= tolerance]
    
    if close_meals:
        # Randomly select a meal from the close meals.
        selected = random.choice(close_meals)
        return selected["name"], selected["calories"]
    else:
        # If no meal is close enough, return a message indicating no options are available.
        return f"No available {meal_type} options that match the calorie requirement.", 0


def generate_meal_plan(user_restrictions, result):
    """
    Generates a weekly meal plan (breakfast, lunch, and dinner) based on the user's dietary restrictions and calorie target.
    """
    # Define expanded meal options with dietary tags and calorie counts.
    breakfasts = [
        {"name": "Oatmeal with fruits and nuts", "restrictions": ["vegan", "vegetarian", "dairy free", "gluten free"], "calories": 350},
        {"name": "Greek yogurt with granola and berries", "restrictions": ["gluten free", "nut free"], "calories": 300},
        {"name": "Spinach and banana smoothie", "restrictions": ["vegan", "vegetarian", "dairy free", "gluten free", "nut free"], "calories": 250},
        {"name": "Avocado toast with poached egg", "restrictions": ["gluten free"], "calories": 400},
        {"name": "Chia pudding with almond milk and mango", "restrictions": ["vegan", "vegetarian", "gluten free"], "calories": 320},
        {"name": "Quinoa porridge with berries and cinnamon", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free"], "calories": 360},
        {"name": "Scrambled tofu with spinach and tomatoes", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free", "nut free"], "calories": 300},
        {"name": "Whole grain toast with almond butter and banana", "restrictions": ["vegan", "vegetarian"], "calories": 380}
    ]
    
    lunches = [
        {"name": "Grilled chicken salad with mixed greens", "restrictions": ["gluten free", "nut free"], "calories": 450},
        {"name": "Quinoa bowl with roasted vegetables", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free", "nut free"], "calories": 500},
        {"name": "Turkey wrap with lettuce, tomato, and hummus", "restrictions": ["nut free"], "calories": 480},
        {"name": "Lentil soup with a side of whole-grain bread", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free", "nut free"], "calories": 400},
        {"name": "Vegetable stir-fry with tofu and brown rice", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free", "nut free"], "calories": 520},
        {"name": "Chickpea and spinach curry with brown rice", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free", "nut free"], "calories": 530},
        {"name": "Roasted vegetable and hummus wrap", "restrictions": ["vegan", "vegetarian", "nut free"], "calories": 470},
        {"name": "Grilled shrimp salad with avocado", "restrictions": ["gluten free", "nut free"], "calories": 440}
    ]
    
    dinners = [
        {"name": "Baked salmon with steamed broccoli and quinoa", "restrictions": ["gluten free", "nut free", "dairy free"], "calories": 550},
        {"name": "Grilled tofu with brown rice and mixed vegetables", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free", "nut free"], "calories": 500},
        {"name": "Vegetable curry with chickpeas served over rice", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free", "nut free"], "calories": 530},
        {"name": "Zucchini noodles with marinara sauce and a side salad", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free", "nut free"], "calories": 480},
        {"name": "Stuffed bell peppers with quinoa and black beans", "restrictions": ["vegan", "vegetarian", "gluten free", "dairy free", "nut free"], "calories": 510},
        {"name": "Baked cod with sweet potato mash and green beans", "restrictions": ["gluten free", "nut free", "dairy free"], "calories": 540},
        {"name": "Eggplant Parmesan with a side salad", "restrictions": ["vegetarian", "nut free"], "calories": 560},
        {"name": "Spaghetti squash with pesto and cherry tomatoes", "restrictions": ["vegan", "vegetarian", "gluten free", "nut free"], "calories": 490}
    ]
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    meal_plan = {}
    
    for day in days:
        day_plan = {}
        daily_calories = 0
        
        # Filter meal options for each category based on user restrictions.
        available_breakfasts = filter_meals(breakfasts, user_restrictions)
        available_lunches = filter_meals(lunches, user_restrictions)
        available_dinners = filter_meals(dinners, user_restrictions)
        
        # Randomly select a meal (or use a fallback message if none available), considering the calorie requirement.
        b_name, b_cal = select_meal(available_breakfasts, "breakfast", result)
        l_name, l_cal = select_meal(available_lunches, "lunch", result)
        d_name, d_cal = select_meal(available_dinners, "dinner", result)
        
        day_plan["Breakfast"] = b_name
        day_plan["Lunch"] = l_name
        day_plan["Dinner"] = d_name
        daily_calories += b_cal + l_cal + d_cal

        day_plan["Total Calories"] = daily_calories
        meal_plan[day] = day_plan
    
    return meal_plan


def print_meal_plan(plan, restrictions):
    """
    Prints the meal plan in a readable format, including the dietary restrictions and daily calorie totals.
    """
    restrictions_str = ", ".join(restrictions) if restrictions else "None"
    print("\nWeekly Healthy Meal Plan")
    print(f"Dietary Restrictions: {restrictions_str}")
    print("=" * 50)
    for day, meals in plan.items():
        print(f"\n{day}:")
        for meal_type, meal in meals.items():
            print(f"  {meal_type}: {meal}")


# Example Usage
age = int(input("Enter your age: "))
weight = float(input("Enter your weight (kg): "))
height = float(input("Enter your height (cm): "))
gender = input("Enter your gender (male/female): ")
activity_level = input("Enter your activity level (sedentary, light, moderate, active, very active): ")
goal = input("Enter your goal (maintain, lose, gain): ")

result = calculate_calories(age, weight, height, gender, activity_level, goal)
print("Your required calories is", result)


user_restrictions = get_user_restrictions()
meal_plan = generate_meal_plan(user_restrictions, result)

print_meal_plan(meal_plan, user_restrictions)
