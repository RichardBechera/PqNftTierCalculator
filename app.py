from flask import Flask, request, render_template
from TierCalculator import qualculate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def adder_page():
    if request.method == 'POST':
        address = request.form["address"]
        apiKey = request.form["apiKey"]
        if address is not None and apiKey is not None:
            result = qualculate(address, apiKey)
            return render_template('result.html', name=result)
    return render_template('form.html')


if __name__ == "__main__":
    app.run(port=8080)
