import os
import sys
import time
import yaml
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class Red2NetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Red2Net")
        
        self.script_dir = "scripts"
        self.arguments_file = "scripts/arguments.yaml"
        
        self.load_scripts()
        
        self.script_var = tk.StringVar(root)
        self.script_var.set(self.scripts[0])  # Varsayılan olarak ilk scripti seç
        
        self.create_widgets()
        
    def load_scripts(self):
        self.scripts = [file for file in os.listdir(self.script_dir) if file.endswith((".py", ".c"))]
        
    def create_widgets(self):
        tk.Label(self.root, text="Choose a script:").pack()
        self.script_menu = tk.OptionMenu(self.root, self.script_var, *self.scripts)
        self.script_menu.pack()
        
        tk.Button(self.root, text="Run Script", command=self.run_script).pack()
        
        # Terminal output bölümü
        self.output_text = tk.Text(self.root, height=20, width=80, bg="black", fg="white", relief="flat")
        self.output_text.pack(pady=10)
        
    def run_script(self):
        self.output_text.delete(1.0, tk.END)  # Önceki çıktıyı temizle
        
        selected_script = self.script_var.get()
        self.output_text.insert(tk.END, f"{selected_script} starting...\n\n")  # Script başladı mesajını yaz
        
        arguments = self.load_arguments(selected_script)
        if not arguments:
            messagebox.showerror("Error", "Arguments file not found for the selected script.")
            return
        
        params = self.get_parameters(arguments)
        if not params:
            return
        
        command = ["python", os.path.join(self.script_dir, selected_script)]
        for arg, value in params.items():
            command.extend(["-" + arg, value])
        
        # Çalıştırılan komutu ekrana yaz
        self.output_text.insert(tk.END, "$ " + " ".join(command) + "\n\n")
        
        try:
            # Komutu çalıştır ve çıktıyı ekrana yaz
            output = subprocess.run(command, capture_output=True, text=True, check=True)
            self.output_text.insert(tk.END, output.stdout)
        except subprocess.CalledProcessError as e:
            self.output_text.insert(tk.END, f"Error: {e.stderr}\n")
 
    def load_arguments(self, script_name):
        arguments_file = os.path.join(self.script_dir, "arguments.yaml")
        if os.path.exists(arguments_file):
            with open(arguments_file, "r") as f:
                arguments = yaml.safe_load(f)
            if script_name in arguments:
                return arguments[script_name]
        return None
    
    def get_parameters(self, arguments):
        params = {}
        for arg in arguments:
            user_input = simpledialog.askstring("Input", f"Enter value for {arg}:")
            if user_input is None:  # İptal edildi
                return None
            params[arg] = user_input
        return params

def show_ascii_art():
    art_file = os.path.join("utils", "ascii_art.txt")
    if os.path.exists(art_file):
        with open(art_file, "r") as f:
            ascii_art = f.read()
        print(ascii_art)
        time.sleep(3)
        subprocess.call("clear" if os.name == "posix" else "cls", shell=True)  # Terminali temizle
    else:
        print("ASCII art file not found!")

if __name__ == "__main__":
    # Kullanıcı sudo izniyle çalıştırmadıysa uygulamadan çık
    if os.geteuid() != 0:
        print("Please run the application with sudo privileges.")
        exit()
    
    show_ascii_art()  # ASCII artı göster
    root = tk.Tk()
    app = Red2NetApp(root)
    root.mainloop()
