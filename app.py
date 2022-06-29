import os
from urllib import response
import requests
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template

# Define a flask app
app = Flask(__name__)


img_folder = os.path.join('static','images')
app.config['UPLOAD_FOLDER'] = img_folder


@app.route("/")
def index():
  return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("within slash")
    if request.method == 'POST':
        print('within POST request')
        f = request.files['file']
        f.save('static/images/'+ secure_filename(f.filename))
        
        url = 'https://obj-det-7kpokr4waq-el.a.run.app'

        # Make prediction
        files = {'file': open('static/images/'+f.filename, 'rb')}
        response= requests.post(url = url, files = files)
        print(response.status_code)
        #get_detected_object=run_inference('static/images/'+f.filename)
        #print(get_detected_object.shape)
        
        #_, im_arr = cv2.imencode('.jpg', req)  # im_arr: image in Numpy one-dim array format.
        #im_bytes = im_arr.tobytes()
        #im_b64 = base64.b64encode(im_bytes).decode()        
  
        #im_b64 = base64.b64encode(response.json()['image']).decode()
        im_b64 = response.json()['image']
        boxes = response.json()['bbox']
        confidences = response.json()['confidence']
        class_ = response.json()['class']

        return render_template("uploaded.html", display_detection = 'data:image/png;base64, '+im_b64, bbox = boxes, conf = confidences, cl = class_)
        

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=int(os.environ.get("PORT",1010)))






