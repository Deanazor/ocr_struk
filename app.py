from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from config import parse_args
from inference import TextDetector, TextRecognizer, detection, recognition
from draw import pair, to_json
from datetime import datetime
from base64 import b64decode
import numpy as np
import os, cv2

args = parse_args()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploads"

detector = TextDetector(args)
recognizer = TextRecognizer(args)

def something(args, templates:list=None):
    coord_path = detection(args, detector)
    transcript_path = recognition(args, recognizer)

    levels, _, transcripts = pair(coord_path, transcript_path)
    r_json = to_json(levels, transcripts, templates)

    return r_json

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files.get("image")
    if not file:
        return {
                "error": "Image is required"
        }, 400

    supported_mimetypes = ["image/jpeg", "image/png"]
    mimetype = file.content_type
    if mimetype not in supported_mimetypes:
        return {
                "error": "Unsupported image type"
        }, 415
    
    current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename = current_time + '-' + file.filename
    filename = secure_filename(filename)

    args.image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(args.image_path)
    
    r_json = something(args)
    os.remove(args.image_path)

    return jsonify(r_json)

def base64_to_cv(uri):
    encoded_data = uri.split(',')[1]
    arr =  np.fromstring(b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

@app.route("/predict_json", methods=["POST"])
def Predict():
    data = request.json
    # print(data)

    templates = data["additional_params"]["template"]
    image = data["images"][0].split(":")[1]
    mimetype, base64 = image.split(";")

    supported_mimetypes = ["image/jpeg"]
    if mimetype not in supported_mimetypes:
        return {
                "error": "Unsupported image type"
        }, 415
    
    img = base64_to_cv(base64)

    current_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    filename = current_time + "-" + "pred.jpg"
    filename = secure_filename(filename)

    args.image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    cv2.imwrite(args.image_path, img)

    r_json = something(args, templates)
    os.remove(args.image_path)

    return jsonify(r_json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")