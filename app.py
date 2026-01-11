"""
Flask web backend for Image Caption Encryption and Metadata Steganography.
"""

import os
import ast
from pathlib import Path
from typing import List

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash

from src.caption_generator import CaptionGenerator
from src.cipher_engine import CipherEngine
from src.metadata_handler import MetadataHandler
from src.preview_module import PreviewModule

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
OUTPUT_FOLDER = BASE_DIR / "outputs"

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["OUTPUT_FOLDER"] = str(OUTPUT_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB

# Ensure folders exist
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

caption_generator = CaptionGenerator()


def parse_hill_key(key_str: str) -> List[List[int]]:
    """Safely parse Hill cipher key string into a matrix."""
    try:
        key = ast.literal_eval(key_str)
        if not isinstance(key, list) or not all(isinstance(row, list) for row in key):
            raise ValueError
        return key
    except Exception as exc:  # noqa: BLE001
        raise ValueError("Invalid Hill cipher key format. Use [[a, b], [c, d]]") from exc


def normalize_text(text: str) -> str:
    """Normalize text for comparison: keep letters, uppercase them."""
    return "".join(c.upper() for c in text if c.isalpha())


@app.route("/")
def index():
    """Main form for uploading image and entering parameters."""
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    """Handle form submission: encrypt caption and write to metadata."""
    if "image" not in request.files:
        flash("No image file part in request", "error")
        return redirect(url_for("index"))

    file = request.files["image"]
    if not file or file.filename == "":
        flash("No image file selected", "error")
        return redirect(url_for("index"))

    # Save uploaded image
    filename = file.filename

    # Basic format validation: this implementation only supports EXIF comments on JPEG images.
    allowed_extensions = {".jpg", ".jpeg", ".JPG", ".JPEG"}
    _, ext = os.path.splitext(filename)
    if ext not in allowed_extensions:
        flash("Only JPEG images (.jpg, .jpeg) are supported for metadata encryption.", "error")
        return redirect(url_for("index"))
    upload_path = UPLOAD_FOLDER / filename
    file.save(upload_path)

    # Read form fields
    labels_str = request.form.get("labels", "")
    hill_key_str = request.form.get("hill_key", "")
    vigenere_key = request.form.get("vigenere_key", "")
    output_name = request.form.get("output_name", "encrypted_" + filename)

    # Validate keys
    if not hill_key_str or not vigenere_key:
        flash("Both Hill and Vigenère keys are required", "error")
        return redirect(url_for("index"))

    try:
        hill_key = parse_hill_key(hill_key_str)
        cipher_engine = CipherEngine(hill_key, vigenere_key)
    except Exception as exc:  # noqa: BLE001
        flash(str(exc), "error")
        return redirect(url_for("index"))

    # Generate caption
    labels = [lbl.strip() for lbl in labels_str.split(",") if lbl.strip()]
    caption = caption_generator.generate_caption(labels) if labels else "No labels provided"

    # Encrypt caption
    encrypted_caption = cipher_engine.encrypt(caption)

    # Write to metadata
    output_path = OUTPUT_FOLDER / output_name
    handler = MetadataHandler(str(upload_path))
    success = handler.write_comment(encrypted_caption, str(output_path))
    handler.close()

    if not success:
        flash("Failed to write encrypted caption to image metadata", "error")
        return redirect(url_for("index"))

    # Read back and decrypt for verification
    verify_handler = MetadataHandler(str(output_path))
    encrypted_from_meta = verify_handler.read_comment()
    verify_handler.close()

    decrypted_caption = (
        cipher_engine.decrypt(encrypted_from_meta) if encrypted_from_meta else "(No comment found)"
    )

    # Normalize for logical comparison (ignore spaces/punctuation, strip padding X)
    normalized_original = normalize_text(caption)
    normalized_decrypted = normalize_text(decrypted_caption).rstrip("X")
    is_match = normalized_original == normalized_decrypted

    comparison = PreviewModule.compare_files(str(upload_path), str(output_path))

    return render_template(
        "result.html",
        original_filename=filename,
        output_filename=output_name,
        caption=caption,
        encrypted_caption=encrypted_caption,
        encrypted_from_meta=encrypted_from_meta,
        decrypted_caption=decrypted_caption,
        comparison=comparison,
        is_match=is_match,
    )


@app.route("/download/<path:filename>")
def download_file(filename: str):  # noqa: D401
    """Download modified image file."""
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

