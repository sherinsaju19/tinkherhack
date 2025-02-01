from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import random

# Initialize Flask app
app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'  # MySQL host (for localhost)
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'crocomom@18'  # Your MySQL password
app.config['MYSQL_DB'] = 'meal_planner'  # Database name

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    age = int(request.form['age'])
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    gender = request.form['gender']
    activity_level = request.form['activity_level']
    goal = request.form['goal']

    result = calculate_calories(age, weight, height, gender, activity_level, goal)

    # Get user restrictions
    restrictions = request.form['restrictions'].lower().split(',')

    # Get meal plan
    meal_plan = generate_meal_plan(restrictions, result)

    return render_template('meal_plan.html', meal_plan=meal_plan, restrictions=restrictions)

# Function to calculate calories (same as your original function)
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

# Function to generate meal plan (same as your original function, but with MySQL integration)
def generate_meal_plan(restrictions, result):
    # Fetch meals from the database based on restrictions
    cursor = mysql.connection.cursor()
    restrictions_placeholder = ', '.join(["%s"] * len(restrictions))
    query = f"SELECT * FROM meals WHERE LOWER(restrictions) LIKE {restrictions_placeholder}"
    
    cursor.execute(query, restrictions)
    meals = cursor.fetchall()

    # Sample selection and meal plan generation (simplified for now)
    meal_plan = {}
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        daily_meal = random.choice(meals)
        meal_plan[day] = daily_meal
    return meal_plan

if __name__ == '__main__':
    app.run(debug=True)
