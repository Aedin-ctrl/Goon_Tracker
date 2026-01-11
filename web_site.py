# web_site.py

from flask import Flask, render_template, request, session, jsonify
from web_site_data import FOODS, PEOPLE

app = Flask(__name__)
app.secret_key = "dev-secret-key-12345"  # you can make any random string

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            calories = float(request.form.get("calories", 0) or 0)
            protein = float(request.form.get("protein", 0) or 0)
        except ValueError:
            calories = 0
            protein = 0

        person = request.form.get("person", "Myself")

        if person not in session:
            session[person] = {"total_calories": 0, "total_protein": 0}

        session[person]["total_calories"] += calories
        session[person]["total_protein"] += protein
        session.modified = True

    selected_person = request.args.get("person", "Myself")
    totals = session.get(selected_person, {"total_calories": 0, "total_protein": 0})

    return render_template(
        "index.html",
        foods=FOODS,
        persons=PEOPLE,
        selected_person=selected_person,
        total_calories=round(totals["total_calories"], 1),
        total_protein=round(totals["total_protein"], 1)
    )


@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("q", "").lower().strip()
    if query == "":
        matches = [f["name"] for f in FOODS]  # show all foods if empty
    else:
        matches = [f["name"] for f in FOODS if query in f["name"].lower()]
    return jsonify(matches)


@app.route("/calculate", methods=["POST"])
def calculate():
    food_name = request.form.get("food", "").strip()
    portions = request.form.get("portions")
    weight = request.form.get("weight")

    food = next((f for f in FOODS if f["name"] == food_name), None)
    if not food:
        return jsonify({"error": "Food not found"}), 400

    try:
        if portions and portions != "custom":
            multiplier = float(portions)
            calories = food["calories_per_serving"] * multiplier
            protein = food["protein_per_serving"] * multiplier

        elif weight:
            weight_g = float(weight)
            calories = (food["calories_per_100g"] / 100) * weight_g
            protein = (food["protein_per_100g"] / 100) * weight_g

        else:
            return jsonify({"error": "Enter portions or weight"}), 400

    except ValueError:
        return jsonify({"error": "Invalid number"}), 400

    return jsonify({
        "calories": round(calories, 1),
        "protein": round(protein, 1),
        "serving_desc": food.get("serving_desc", "")
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
