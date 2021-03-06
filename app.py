from __future__ import division, print_function

import sys
import os
import glob
import re
import numpy as np


from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer


app = Flask(__name__)


MODEL_PATH ='model_vgg19_6.h5'


model = load_model(MODEL_PATH)




def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = x/255.  
    x = x.reshape((1, x.shape[0], x.shape[1], x.shape[2]))
    
    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
            preds = "That's a Audi!"
    elif preds==1:
            preds = "That's a BMW!"
    elif preds==2:
            preds = "That's a Ferrari!"
    elif preds==3:
            preds = "That's a Jaguar!"
    elif preds==4:
            preds = "That's a Lamborghini!"
    elif preds==5:
            preds = "That's a Mercedes!"
    else :
            preds = "N/A"
    
    
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)