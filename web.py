from flask import Flask, request, render_template
import numpy as np
import animation

app = Flask(__name__, static_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def visual():
	time = request.form.get("time", type=float)
	massOne = request.form.get("massOne", type=float)
	velOne = np.array([request.form.get("velOneX", type=float), request.form.get("velOneY", type=float)])
	posOne = np.array([request.form.get("posOneX", type=float), request.form.get("posOneY", type=float)])
	massTwo = request.form.get("massTwo", type=float)
	velTwo = np.array([request.form.get("velTwoX", type=float), request.form.get("velTwoY", type=float)])
	posTwo = np.array([request.form.get("posTwoX", type=float), request.form.get("posTwoY", type=float)])

	fileName = animation.generate(2, np.array([massOne, massTwo]), np.array([velOne, velTwo]), np.array([posOne, posTwo]), time)

	return render_template('visual.html', currentPath=fileName)
