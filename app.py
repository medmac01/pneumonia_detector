from crypt import methods
from distutils import file_util
from fileinput import filename

from nis import cat
from flask import Flask, url_for, render_template, flash, request, redirect
from forms import uploadScanForm
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "f3d2e1a3218a034b3d3ff21c"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOAD_FOLDER = os.getcwd() + '/database/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/' , methods=["GET","POST"])
def welcome():
	form = uploadScanForm()
	if form.is_submitted():
		uploaded_file = request.files[form.uploadedFile.name]
		if uploaded_file.filename != '':
			uploaded_file.save(os.path.join(UPLOAD_FOLDER,uploaded_file.filename))
			flash("File uploaded successfully!",category="success")
		# file = request.files['file']
			return redirect(url_for("process",file=uploaded_file.filename))

	return render_template("welcome.html", form=form)


@app.route('/process')
def process():
	file = request.args.get("file")
	model = load_trained_model()
	img_preprocessed = preprocess_image(file)
	return predict_class(img_preprocessed,model)
	
	


import tensorflow as tf
import numpy as np

def load_trained_model():
	model = tf.keras.models.load_model(os.getcwd()+"/model/cnnmodel.h5")
	# model.set_weights(os.getcwd()+'/model/final_weights.h5')
	return model

def preprocess_image(filename):
	img_path = UPLOAD_FOLDER+filename
	img = tf.keras.utils.load_img(img_path,target_size=(64,64))

	img_array = tf.keras.preprocessing.image.img_to_array(img)
	img_batch = np.expand_dims(img_array, axis=0)

	img_preprocessed = tf.keras.applications.resnet50.preprocess_input(img_batch)
	return img_preprocessed

def predict_class(img, model):
	prediction = model.predict(img)
	return tf.keras.applications.imagenet_utils.decode_predictions(prediction, top=1)[0]




