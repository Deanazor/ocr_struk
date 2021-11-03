from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from config import parse_args
from inference import TextDetector, TextRecognizer, detection, recognition
from draw import pair, to_json
from datetime import datetime
import os

args = parse_args()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploads"

detector = TextDetector(args)
recognizer = TextRecognizer(args)

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
    
    coord_path = detection(args, detector)
    transcript_path = recognition(args, recognizer)

    levels, _, transcripts = pair(coord_path, transcript_path)
    r_json = to_json(levels, transcripts)

    os.remove(args.image_path)

    return jsonify(r_json)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")