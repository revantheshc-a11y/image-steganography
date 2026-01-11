"""
GUI Interface Module
Provides graphical user interface for the application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import ast
from typing import Optional, List
from pathlib import Path

from .caption_generator import CaptionGenerator
from .cipher_engine import CipherEngine
from .metadata_handler import MetadataHandler
from .preview_module import PreviewModule


class SteganographyGUI:
    """Main GUI application for image caption encryption and metadata steganography."""
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Image Caption Encryption and Metadata Steganography")
        self.root.geometry("900x700")
        
        # Initialize components
        self.caption_generator = CaptionGenerator()
        self.cipher_engine: Optional[CipherEngine] = None
        self.selected_image_path: Optional[str] = None
        
        # Create GUI elements
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and arrange GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Image selection section
        ttk.Label(main_frame, text="Image File:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        image_frame.columnconfigure(0, weight=1)
        
        self.image_path_var = tk.StringVar()
        ttk.Entry(image_frame, textvariable=self.image_path_var, state="readonly").grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5)
        )
        ttk.Button(image_frame, text="Browse", command=self._browse_image).grid(
            row=0, column=1
        )
        
        # Caption generation section
        ttk.Label(main_frame, text="Caption Labels:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        
        caption_frame = ttk.Frame(main_frame)
        caption_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        caption_frame.columnconfigure(0, weight=1)
        
        self.labels_entry = ttk.Entry(caption_frame)
        self.labels_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.labels_entry.insert(0, "tree, car, building")
        ttk.Button(caption_frame, text="Generate Caption", command=self._generate_caption).grid(
            row=0, column=1
        )
        
        ttk.Label(main_frame, text="Generated Caption:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        
        self.caption_text = scrolledtext.ScrolledText(main_frame, height=3, wrap=tk.WORD)
        self.caption_text.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Cipher keys section
        keys_frame = ttk.LabelFrame(main_frame, text="Cipher Keys", padding="10")
        keys_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        keys_frame.columnconfigure(1, weight=1)
        
        ttk.Label(keys_frame, text="Hill Cipher Key (2x2 matrix):").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.hill_key_entry = ttk.Entry(keys_frame, width=30)
        self.hill_key_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.hill_key_entry.insert(0, "[[3, 3], [2, 5]]")
        ttk.Label(keys_frame, text="Format: [[a, b], [c, d]]", font=("Arial", 8)).grid(
            row=0, column=2, sticky=tk.W, padx=5
        )
        
        ttk.Label(keys_frame, text="Vigenère Cipher Key:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.vigenere_key_entry = ttk.Entry(keys_frame, width=30)
        self.vigenere_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.vigenere_key_entry.insert(0, "SECRET")
        
        ttk.Button(keys_frame, text="Initialize Ciphers", command=self._initialize_ciphers).grid(
            row=2, column=0, columnspan=3, pady=10
        )
        
        # Encryption section
        encrypt_frame = ttk.LabelFrame(main_frame, text="Encryption", padding="10")
        encrypt_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        encrypt_frame.columnconfigure(1, weight=1)
        
        ttk.Label(encrypt_frame, text="Encrypted Caption:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.encrypted_text = scrolledtext.ScrolledText(encrypt_frame, height=3, wrap=tk.WORD)
        self.encrypted_text.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(encrypt_frame, text="Output File Name:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.output_file_entry = ttk.Entry(encrypt_frame)
        self.output_file_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.output_file_entry.insert(0, "encrypted_image.jpg")
        
        ttk.Button(encrypt_frame, text="Encrypt and Save to Metadata", 
                  command=self._encrypt_and_save).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Verification section
        verify_frame = ttk.LabelFrame(main_frame, text="Verification", padding="10")
        verify_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        verify_frame.columnconfigure(0, weight=1)
        
        ttk.Button(verify_frame, text="Read and Decrypt from Metadata", 
                  command=self._verify_decrypt).grid(row=0, column=0, pady=5)
        
        self.verification_text = scrolledtext.ScrolledText(verify_frame, height=4, wrap=tk.WORD)
        self.verification_text.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="File Preview", padding="10")
        preview_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        preview_frame.columnconfigure(0, weight=1)
        
        ttk.Button(preview_frame, text="Compare Original and Modified Files", 
                  command=self._preview_files).grid(row=0, column=0, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=6, wrap=tk.WORD)
        self.preview_text.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
    
    def _browse_image(self):
        """Browse for an image file."""
        filename = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.selected_image_path = filename
            self.image_path_var.set(filename)
    
    def _generate_caption(self):
        """Generate caption from labels."""
        labels_str = self.labels_entry.get()
        labels = [label.strip() for label in labels_str.split(',') if label.strip()]
        
        if not labels:
            messagebox.showwarning("Warning", "Please enter at least one label.")
            return
        
        caption = self.caption_generator.generate_caption(labels)
        self.caption_text.delete(1.0, tk.END)
        self.caption_text.insert(1.0, caption)
    
    def _initialize_ciphers(self):
        """Initialize cipher engine with provided keys."""
        try:
            # Parse Hill cipher key
            hill_key_str = self.hill_key_entry.get()
            hill_key = ast.literal_eval(hill_key_str)
            
            # Get Vigenère key
            vigenere_key = self.vigenere_key_entry.get()
            
            if not vigenere_key:
                messagebox.showerror("Error", "Vigenère key cannot be empty.")
                return
            
            self.cipher_engine = CipherEngine(hill_key, vigenere_key)
            messagebox.showinfo("Success", "Ciphers initialized successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize ciphers: {str(e)}")
    
    def _encrypt_and_save(self):
        """Encrypt caption and save to image metadata."""
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return
        
        if not self.cipher_engine:
            messagebox.showerror("Error", "Please initialize ciphers first.")
            return
        
        caption = self.caption_text.get(1.0, tk.END).strip()
        if not caption:
            messagebox.showerror("Error", "Please generate a caption first.")
            return
        
        output_filename = self.output_file_entry.get().strip()
        if not output_filename:
            messagebox.showerror("Error", "Please enter an output file name.")
            return
        
        try:
            # Encrypt caption
            encrypted = self.cipher_engine.encrypt(caption)
            self.encrypted_text.delete(1.0, tk.END)
            self.encrypted_text.insert(1.0, encrypted)
            
            # Save to metadata
            handler = MetadataHandler(self.selected_image_path)
            output_path = os.path.join(os.path.dirname(self.selected_image_path), output_filename)
            
            if handler.write_comment(encrypted, output_path):
                messagebox.showinfo("Success", f"Encrypted caption saved to metadata!\nOutput: {output_path}")
            else:
                messagebox.showerror("Error", "Failed to save encrypted caption to metadata.")
            
            handler.close()
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
    
    def _verify_decrypt(self):
        """Read and decrypt caption from metadata."""
        output_filename = self.output_file_entry.get().strip()
        if not output_filename:
            messagebox.showerror("Error", "Please enter the output file name.")
            return
        
        if not self.cipher_engine:
            messagebox.showerror("Error", "Please initialize ciphers first.")
            return
        
        try:
            output_path = os.path.join(os.path.dirname(self.selected_image_path), output_filename)
            if not os.path.exists(output_path):
                messagebox.showerror("Error", f"Output file not found: {output_path}")
                return
            
            # Read from metadata
            handler = MetadataHandler(output_path)
            encrypted_comment = handler.read_comment()
            handler.close()
            
            if not encrypted_comment:
                messagebox.showwarning("Warning", "No encrypted comment found in metadata.")
                return
            
            # Decrypt
            decrypted = self.cipher_engine.decrypt(encrypted_comment)
            
            # Display results
            result = f"Encrypted (from metadata): {encrypted_comment}\n\n"
            result += f"Decrypted: {decrypted}\n\n"
            result += f"Original caption: {self.caption_text.get(1.0, tk.END).strip()}\n\n"
            result += f"Match: {'✓ YES' if decrypted == self.caption_text.get(1.0, tk.END).strip() else '✗ NO'}"
            
            self.verification_text.delete(1.0, tk.END)
            self.verification_text.insert(1.0, result)
        except Exception as e:
            messagebox.showerror("Error", f"Verification failed: {str(e)}")
    
    def _preview_files(self):
        """Preview and compare original and modified files."""
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select an image file.")
            return
        
        output_filename = self.output_file_entry.get().strip()
        if not output_filename:
            messagebox.showerror("Error", "Please enter the output file name.")
            return
        
        try:
            output_path = os.path.join(os.path.dirname(self.selected_image_path), output_filename)
            if not os.path.exists(output_path):
                messagebox.showerror("Error", f"Output file not found: {output_path}")
                return
            
            comparison = PreviewModule.compare_files(self.selected_image_path, output_path)
            
            # Format preview text
            preview_text = "=== ORIGINAL FILE ===\n"
            if comparison['original']:
                for key, value in comparison['original'].items():
                    preview_text += f"{key}: {value}\n"
            else:
                preview_text += "Unable to read file properties\n"
            
            preview_text += "\n=== MODIFIED FILE ===\n"
            if comparison['modified']:
                for key, value in comparison['modified'].items():
                    preview_text += f"{key}: {value}\n"
            else:
                preview_text += "Unable to read file properties\n"
            
            preview_text += "\n=== DIFFERENCES ===\n"
            if comparison['differences']:
                for key, value in comparison['differences'].items():
                    preview_text += f"{key}: {value}\n"
            else:
                preview_text += "No significant differences detected\n"
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
        except Exception as e:
            messagebox.showerror("Error", f"Preview failed: {str(e)}")


def main():
    """Main entry point for GUI application."""
    root = tk.Tk()
    app = SteganographyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

