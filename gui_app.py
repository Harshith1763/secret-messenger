import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from morse import text_to_morse, morse_to_text
from steg import encode_image, decode_image
from PIL import Image

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse/Steganography Tool")
        self.root.geometry("700x550")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        
        # Morse Tab
        self.morse_tab = ttk.Frame(self.notebook)
        self.setup_morse_ui()
        
        # Steganography Tab
        self.steg_tab = ttk.Frame(self.notebook)
        self.setup_steg_ui()
        
        self.notebook.add(self.morse_tab, text="Morse Translator")
        self.notebook.add(self.steg_tab, text="Steganography")
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

    def setup_morse_ui(self):
        """Setup Morse code translation UI"""
        # Mode selection
        ttk.Label(self.morse_tab, text="Translation Direction:").pack(pady=5)
        
        self.mode_var = tk.StringVar(value="text_to_morse")
        ttk.Radiobutton(
            self.morse_tab, 
            text="Text → Morse",
            variable=self.mode_var,
            value="text_to_morse"
        ).pack()
        
        ttk.Radiobutton(
            self.morse_tab,
            text="Morse → Text",
            variable=self.mode_var,
            value="morse_to_text"
        ).pack()
        
        # Input
        ttk.Label(self.morse_tab, text="Input:").pack(pady=5)
        self.input_text = tk.Text(self.morse_tab, height=5, width=50)
        self.input_text.pack(padx=10)
        
        # Translate button
        ttk.Button(
            self.morse_tab,
            text="Translate",
            command=self.translate_morse
        ).pack(pady=10)
        
        # Output
        ttk.Label(self.morse_tab, text="Output:").pack(pady=5)
        self.output_text = tk.Text(self.morse_tab, height=5, width=50, state="disabled")
        self.output_text.pack(padx=10)

    def setup_steg_ui(self):
        """Setup steganography UI"""
        # Encode Section
        encode_frame = ttk.LabelFrame(self.steg_tab, text="Encode Message")
        encode_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(encode_frame, text="Image:").grid(row=0, column=0, sticky="w")
        self.img_path = tk.StringVar()
        ttk.Entry(encode_frame, textvariable=self.img_path, width=40).grid(row=1, column=0, padx=5)
        ttk.Button(encode_frame, text="Browse", command=self.browse_image).grid(row=1, column=1)
        
        ttk.Label(encode_frame, text="Message:").grid(row=2, column=0, sticky="w", pady=(10,0))
        self.message_entry = tk.Text(encode_frame, height=5, width=40)
        self.message_entry.grid(row=3, column=0, columnspan=2, padx=5)
        
        ttk.Label(encode_frame, text="Password:").grid(row=4, column=0, sticky="w", pady=(10,0))
        self.password_entry = ttk.Entry(encode_frame, show="*", width=40)
        self.password_entry.grid(row=5, column=0, padx=5)
        
        ttk.Button(encode_frame, text="Encode and Save", command=self.encode).grid(row=6, column=0, pady=10)
        
        # Decode Section
        decode_frame = ttk.LabelFrame(self.steg_tab, text="Decode Message")
        decode_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(decode_frame, text="Image:").grid(row=0, column=0, sticky="w")
        self.decode_img_path = tk.StringVar()
        ttk.Entry(decode_frame, textvariable=self.decode_img_path, width=40).grid(row=1, column=0, padx=5)
        ttk.Button(decode_frame, text="Browse", command=self.browse_decode_image).grid(row=1, column=1)
        
        ttk.Label(decode_frame, text="Password:").grid(row=2, column=0, sticky="w", pady=(10,0))
        self.decode_password = ttk.Entry(decode_frame, show="*", width=40)
        self.decode_password.grid(row=3, column=0, padx=5)
        
        ttk.Button(decode_frame, text="Decode", command=self.decode).grid(row=4, column=0, pady=10)
        
        self.decode_output = tk.Text(decode_frame, height=5, width=40, state="disabled")
        self.decode_output.grid(row=5, column=0, columnspan=2, padx=5)

    def translate_morse(self):
        """Handle Morse code translation"""
        input_content = self.input_text.get("1.0", tk.END).strip()
        
        if not input_content:
            messagebox.showwarning("Warning", "Please enter some text!")
            return
        
        try:
            if self.mode_var.get() == "text_to_morse":
                result = text_to_morse(input_content)
            else:
                result = morse_to_text(input_content)
            
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", result)
            self.output_text.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Translation failed: {str(e)}")

    def browse_image(self):
        """Browse for image to encode"""
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if path:
            self.img_path.set(path)

    def browse_decode_image(self):
        """Browse for image to decode"""
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if path:
            self.decode_img_path.set(path)

    def encode(self):
        """Handle image encoding"""
        try:
            if not self.img_path.get():
                raise ValueError("Please select an image")
            
            message = self.message_entry.get("1.0", tk.END).strip()
            if not message:
                raise ValueError("Please enter a message")
            
            password = self.password_entry.get()
            if not password:
                raise ValueError("Please enter a password")
            
            encoded_img = encode_image(
                self.img_path.get(),
                message,
                password
            )
            
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")]
            )
            
            if save_path:
                encoded_img.save(save_path)
                messagebox.showinfo("Success", "Message encoded successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decode(self):
        """Handle image decoding"""
        try:
            if not self.decode_img_path.get():
                raise ValueError("Please select an image")
            
            password = self.decode_password.get()
            if not password:
                raise ValueError("Please enter a password")
            
            message = decode_image(
                self.decode_img_path.get(),
                password
            )
            
            self.decode_output.config(state="normal")
            self.decode_output.delete("1.0", tk.END)
            self.decode_output.insert("1.0", message)
            self.decode_output.config(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()