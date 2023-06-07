from flask import Flask, render_template, request
from PIL import Image, ImageOps, ImageFilter
import base64
import io
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.static_folder = 'static'

@app.route("/process", methods=["POST"])
def process():
    # Check if the 'image' file is present in the request
    if "image" not in request.files:
        return "No image file found"

    image_file = request.files["image"]

    # Check if the file is not empty
    if image_file.filename == "":
        return "No selected image file"

    # Save the uploaded file to the upload folder
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_file.filename)
    image_file.save(image_path)

    # Read the uploaded image
    image = cv2.imread(image_path)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Menerima file gambar dari formulir HTML
        image = request.files["image"]

        # Membaca gambar menggunakan PIL
        img = Image.open(image)

        # Memproses gambar berdasarkan opsi yang dipilih
        if "blur" in request.form:
            img = img.filter(ImageFilter.BLUR)
        if "flip" in request.form:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if "mirror" in request.form:
            img = ImageOps.mirror(img)
        if "invert" in request.form:
            img = ImageOps.invert(img)
        if "light" in request.form:
            img = ImageOps.autocontrast(img)
        if "dark" in request.form:
            img = ImageOps.equalize(img)
        if "contour" in request.form:
            img = img.filter(ImageFilter.CONTOUR)

        # Mengonversi gambar ke format base64
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # Mengirim gambar yang telah diproses ke template HTML
        return render_template("index.html", img_data=img_base64)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
