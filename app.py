from flask import Flask, url_for, render_template


app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template("welcome.html")

@app.route('/predict')
def predict():
	return render_template("predict.html")
