from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import torch
import torch.nn.functional as F
from io import BytesIO
import base64
from model import DenseNetCustom, transform, device  # your model code

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # <-- allow all origins for development

# Load your trained model
model = DenseNetCustom(num_classes=2).to(device)
model.load_state_dict(torch.load(
    r"C:\Users\julia\VisuAl\VisuAl\extension\densenet_fake_detector_small.pth",
    map_location=device
))
model.eval()

class_labels = ["real", "fake"]

# Prediction function
def predict_fake(image: Image.Image):
    img_tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(img_tensor)
        probs = F.softmax(outputs, dim=1).squeeze().tolist()
        return {label: probs[i] for i, label in enumerate(class_labels)}

# Endpoint for base64 images
@app.route("/upload_images", methods=["POST"])
def upload_images():
    b64_images = request.json.get("images", [])
    results = []

    for idx, b64 in enumerate(b64_images):
        try:
            img_data = base64.b64decode(b64.split(",")[1])
            img = Image.open(BytesIO(img_data)).convert("RGB")
            prediction = predict_fake(img)
            results.append({"index": idx, "prediction": prediction})
        except Exception as e:
            results.append({"index": idx, "error": str(e)})

    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5000)
