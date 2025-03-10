from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        print("📸 Receiving file...")

        if "file" not in request.files:
            print("🚨 No file received")
            return jsonify({"message": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            print("🚨 No file selected")
            return jsonify({"message": "No file selected"}), 400

        if not allowed_file(file.filename):
            print("🚨 Invalid file type")
            return jsonify({"message": "Invalid file type"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        print(f"✅ File saved: {file.filename}")
        return jsonify({"message": f"File uploaded successfully as {file.filename}"}), 200

    except Exception as e:
        print(f"🚨 Backend Error: {e}")
        return jsonify({"message": "Server error", "error": str(e)}), 500

if __name__ == "__main__":
    print("🔥 Starting Flask Server on http://127.0.0.1:5000/")
    app.run(debug=False, host="0.0.0.0", port=5000)
