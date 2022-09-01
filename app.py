from flask import Flask, request
from TierCalculator import qualculate

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def adder_page():
    if request.method == "POST":
        address = request.form["address"]
        apiKey = request.form["apiKey"]
        if address is not None and apiKey is not None:
            result = qualculate(address, apiKey)
            return '''
                <html>
                    <body>
                        <p>The result is {result}</p>
                        <p><a href="/">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(result=result)
    return '''
        <html>
            <body>
                <p>Enter your information:</p>
                <form method="post" action=".">
                    <p><input name="address" /></p>
                    <p><input name="apiKey" /></p>
                    <p><input type="submit" value="Qualculate!" /></p>
                </form>
            </body>
        </html>
    '''


if __name__ == "__main__":
    app.run()
