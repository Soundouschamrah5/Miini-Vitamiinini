
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from processing import get_product

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/", methods=["GET", "POST"])
def adder_page():
    result = ""
    if request.method == "POST":
        name = request.form["fname"]
        gender = request.form["gender"] == "male"
        age = None
        try:
            deficiency = request.form["deficiency"] is not None and request.form["deficiency"] == "on"
        except:
            deficiency = False
        try:
            age = float(request.form["age"])
            product = get_product(age, gender, deficiency)
            result = f'<h4>{name}, the best vitamin option for you is {product["Name"]} in {product["Market"]} for the price of {product["Price"]} euros. <br> It is {product["Type"]} type with {product["Capsules"]} capsules and IU index of {product["IU"]}.</h4>'
        except:
            result = 'The age is incorrect!'
    return '''
        <html>
        <head>
            <title>Vitamins</title>
            <link rel="stylesheet" link href="/static/styles.css">
        </head>
        <body style="margin:20;padding:0">
            <form method="post" action=".">
                <h1>What vitamin should I take?</h1>

                    <fieldset>
                        <legend>Name:</legend>
                        <input type="text" id="fname" name="fname" value="Name"><br>
                    </fieldset>

                    <fieldset>
                        <legend>I am genetically a:</legend>

                        <div>
                        <input type="radio" id="male" name="gender" value="male"
                                checked>
                        <label for="male">Male</label>
                        </div>

                        <div>
                        <input type="radio" id="female" name="gender" value="female">
                        <label for="female">Female</label>
                        </div>
                    </fieldset>

                    <fieldset>
                        <legend>Age:</legend>
                        <input type="text" id="age" name="age" value="18"><br>
                    </fieldset>

                    <fieldset>
                        <legend>Deficiency:</legend>

                        <div>
                        <input type="checkbox" id="deficiency" name="deficiency">
                        <label for="deficiency">I have a vitamin deficiency</label>
                        </div>
                    </fieldset>
<br>
                    <button id = "show_output" class = "btn btn-primary" type = "submit">Look for the best vitamin option</button>
                </form>
                {result}
            </body>
        </html>
    '''.format(result=result)

