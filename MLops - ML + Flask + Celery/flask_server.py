#Install Flask
"""
pip install flask
"""
from flask import Flask, request, jsonify
import tasks

"""
Create a Flask App, app gets exposed when you run this file.
"""

app = Flask(__name__)

"""
'/home' - it is a route of our app. Through this route, we can implement the functions we need, based on our requirement, here it is returning string "Welcome to Home".
A route can be different types like GET, POST, PUT, DELETE etc.  By default, its GET request. '/home' is dummy get request to check if everything is working fine with flask.
"""
@app.route("/home")
def home():
	return "Welcome to Home"


"""
For Inference, We will need an route which accepts a POST request.
Because POST request takes in parameters from user unlike GET, which just sits around & show same results. 
Like an Login Page of a website.
"""
@app.route('/predict', methods=["POST"])
def predict():
	if request.method == 'POST':

		file = request.files['file']
		img_bytes = file.read()
		class_name = tasks.run_inference.delay(image=img_bytes)
		
		return "passed"

"""
This conditional statement is executed when this script is executed. Since Flask is a server, when you execute this file, it will run port 8000.
"""
if __name__ =='__main__':
	app.run(host='0.0.0.0',port=8000, debug=True)


