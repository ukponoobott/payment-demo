import requests
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", items=items)


items = [
    {"name": "shoe", "price": 100000},
    {"name": "earphone", "price": 40000},
    {"name": "watch", "price": 500000}
]

ref = ""
url = "https://api.paystack.co/transaction/initialize"
access_token = "sk_test_8e81c920217c39de48c778ca688c97f23035f86a"


# Initialize the transaction using paystack API
@app.route("/payment", methods=["GET", 'POST'])
def pay():
    if request.method == "POST":
        price = int(request.form["price"])
        print(price)
        params = {}
        print(params)
        try:
            res = requests.post(url, data={"amount": price, "email": "legendsergio@gmail.com"}, headers={'Authorization': 'Bearer {}'.format(access_token)})
            print(res.json())
            # ref = res[3]["reference"]
            res_data = res.json()
            payment_url = res_data['data']['authorization_url']
            print(payment_url)
            # payment_url = res[3]['authorization_url']
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
    app.run()
