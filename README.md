# Image Caption Encryption and Metadata Steganography Using Classical Ciphers

A Python application that hides encrypted textual captions inside image metadata (EXIF comments) using classical ciphers.

## Features

- **Caption Generator**: Generate captions from labels with learning capability
- **Two-Stage Encryption**: Hill Cipher + Vigenère Cipher pipeline
- **Metadata Steganography**: Hide encrypted captions in EXIF metadata without altering image pixels
- **Web Interface**: User-friendly Flask web application for all operations
- **Preview Module**: Compare original and modified file properties
- **Learning Component**: Dictionary grows over time based on user input

## Important: Image Format Requirements

⚠️ **Only JPEG images (.jpg, .jpeg) are supported** for metadata steganography.

- PNG, GIF, and other formats are **not supported** because they don't reliably support EXIF metadata comments
- The application will automatically reject non-JPEG files with a clear error message
- Convert your images to JPEG format before uploading

## Project Structure

```
steg/
├── app.py                         # Flask web backend
├── src/
│   ├── __init__.py
│   ├── caption_generator.py       # Caption generation with learning
│   ├── cipher_engine.py           # Two-stage cipher pipeline
│   ├── metadata_handler.py         # EXIF metadata operations
│   ├── preview_module.py           # File comparison and preview
│   ├── gui_interface.py           # Tkinter GUI implementation
│   └── ciphers/
│       ├── __init__.py
│       ├── hill_cipher.py          # Hill cipher implementation
│       └── vigenere_cipher.py      # Vigenère cipher implementation
├── templates/
│   ├── index.html                  # Web frontend main page
│   └── result.html                 # Web results/verification page
├── static/
│   └── css/
│       └── style.css               # Web frontend styling
├── data/
│   └── caption_dictionary.json     # Learned labels (auto-generated, git-ignored)
├── uploads/                        # Uploaded images (git-ignored)
├── outputs/                        # Encrypted images (git-ignored)
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## Installation

1. Clone or download this repository
2. Navigate to the `steg` directory:
   ```bash
   cd steg
   ```
3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - **Windows (PowerShell)**: `.\venv\Scripts\Activate.ps1`
   - **Windows (CMD)**: `venv\Scripts\activate.bat`
   - **Linux/Mac**: `source venv/bin/activate`
5. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Run the Web App (Flask)

1. Make sure you're in the `steg` directory and your virtual environment is activated
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to: `http://127.0.0.1:5000/`

### Web Workflow

1. **Select Image**: Use the web form to choose a **JPEG image file** (.jpg or .jpeg only)
2. **Enter Labels**: Provide labels (comma-separated) to generate a caption (e.g., "tree, car, building")
3. **Initialize Ciphers**: Enter keys for both ciphers:
   - **Hill Cipher**: 2x2 matrix, e.g., `[[3, 3], [2, 5]]`
     - The matrix must be invertible modulo 26
   - **Vigenère Cipher**: String key, e.g., `SECRET`
4. **Set Output Name**: Optionally specify a custom output filename (default: `encrypted_image.jpg`)
5. **Encrypt and Save**: Submit the form to encrypt the caption and store it in the image's EXIF metadata
6. **Verify**: The result page shows:
   - Original and encrypted captions
   - Decrypted caption for verification
   - Comparison between original and modified file properties
   - Download link for the encrypted image

## Cipher Details

### Hill Cipher
- Matrix-based substitution cipher
- Uses 2x2 key matrix
- Key matrix must be invertible modulo 26
- Only processes uppercase alphabetic characters

### Vigenère Cipher
- Polyalphabetic substitution cipher
- Uses a keyword for encryption
- More secure than simple substitution
- Works with uppercase alphabetic characters

### Two-Stage Pipeline
- **Encryption**: Plaintext → Hill Cipher → Vigenère Cipher → Ciphertext
- **Decryption**: Ciphertext → Vigenère Decrypt → Hill Decrypt → Plaintext

## Learning Component

The caption generator learns from user input:
- Labels entered by users are saved to `data/caption_dictionary.json`
- Dictionary grows over time with each use
- Can be used for auto-suggestions in future runs

## Requirements

- **Python 3.7+**
- **Pillow (PIL) >= 10.0.0** - for image and EXIF handling
- **NumPy >= 1.24.0** - for matrix operations
- **Flask >= 3.0.0** - for the web backend

## Technical Notes

- The encrypted caption is stored in the EXIF **ImageDescription** field (tag 270)
- Image pixels are **not modified**, only metadata is changed
- Original image properties (size, format, quality) are preserved
- Both ciphers work with uppercase alphabetic characters only
- Non-alphabetic characters are filtered out during encryption/decryption
- The application validates file formats and provides clear error messages

## Troubleshooting

### "FAILED TO WRITE ENCRYPTED CAPTION TO IMAGE METADATA"
- **Solution**: Make sure you're using a JPEG image (.jpg or .jpeg format)
- PNG, GIF, and other formats are not supported

### "Only JPEG images are supported"
- The application detected a non-JPEG file
- Convert your image to JPEG format and try again

### ModuleNotFoundError
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure your virtual environment is activated

## License

This project is provided as-is for educational purposes.
