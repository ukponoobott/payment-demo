import requests
from flask import Flask, redirect, render_template, request
from transaction import tranaction

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", items=items)


items = [
    {"name": "shoe", "price": 100},
    {"name": "earphone", "price": 40.00},
    {"name": "watch", "price": 500}
]

ref = ""


# Initialize the transaction using paystack API
@app.route("/payment", methods=["GET", 'POST'])
def pay():
    if request.method == "POST":
        price = float(request.form["price"])
        try:
            init = tranaction.initialize(email="legendsergio@gmail.com", amount=price, metadata="")
            ref = init[3]["reference"]
            payment_url = init[3]['authorization_url']
            return redirect(payment_url)
        except Exception as err:
            print(err)
        return "Error processing payment"
        


# Verify transaction status
@app.route('/verify')
def verify():
    reference = ref
    response = transaction.verify(reference)
    if response[3]["status"] == "success":
        status = "paid" 
    elif response[3]["status"] == "failed":
        status = "unpaid" 
    return render_template("payment.html", status=status)


if __name__ == "__main__":
    app.run(port=5000)