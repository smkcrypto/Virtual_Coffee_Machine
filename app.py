from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

menu = {
    "latte": {"ingredients": {"water": 200, "milk": 150, "coffee": 24}, "cost": 150},
    "espresso": {"ingredients": {"water": 50, "coffee": 18}, "cost": 100},
    "cappuccino": {"ingredients": {"water": 250, "milk": 100, "coffee": 24}, "cost": 200},
}

resources = {"water": 500, "milk": 200, "coffee": 100}
profit = 0

@app.route('/')
def index():
    return render_template('index.html', menu=menu, resources=resources, profit=profit)

@app.route('/order', methods=['POST'])
def order():
    global profit
    coffee_type = request.form.get('coffee_type')
    if coffee_type in menu:
        coffee = menu[coffee_type]
        if check_resources(coffee['ingredients']):
            payment = process_coins()
            if is_payment_successful(payment, coffee['cost']):
                make_coffee(coffee_type, coffee['ingredients'])
                flash(f"Your {coffee_type} is being prepared!")
            else:
                flash("Not enough money. Money refunded.")
        else:
            flash("Not enough resources.")
    else:
        flash("Invalid coffee type.")
    return redirect(url_for('index'))

def check_resources(order_ingredients):
    for item, amount in order_ingredients.items():
        if resources.get(item, 0) < amount:
            return False
    return True

def process_coins():
    print("Please insert coins.")
    coins_five = int(request.form.get("coins_five", 0))
    coins_ten = int(request.form.get("coins_ten", 0))
    coins_twenty = int(request.form.get("coins_twenty", 0))
    return coins_five * 5 + coins_ten * 10 + coins_twenty * 20

def is_payment_successful(money_received, coffee_cost):
    global profit
    if money_received >= coffee_cost:
        profit += coffee_cost
        change = money_received - coffee_cost
        flash(f"Here is your Rs{change} in change.")
        return True
    return False

def make_coffee(coffee_name, coffee_ingredients):
    global resources
    for item, amount in coffee_ingredients.items():
        resources[item] -= amount

if __name__ == "__main__":
    app.run(debug=True)
