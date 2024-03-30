import os
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
        self.script_var.set(self.scripts[0]) 
        
        self.create_widgets()
        
    def load_scripts(self):
        self.scripts = [file for file in os.listdir(self.script_dir) if file.endswith((".py", ".c"))]
        
    def create_widgets(self):
        tk.Label(self.root, text="Choose a script:").pack()
        self.script_menu = tk.OptionMenu(self.root, self.script_var, *self.scripts)
        self.script_menu.pack()
        
        tk.Button(self.root, text="Run Script", command=self.run_script).pack()
        
        
        self.output_text = tk.Text(self.root, height=20, width=80, bg="white", fg="#333", relief="flat")
        self.output_text.pack(pady=10)
        
    def run_script(self):
        self.output_text.delete(1.0, tk.END) 
        
        selected_script = self.script_var.get()
        
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
        
        output = subprocess.run(command, capture_output=True, text=True)
        
        
        self.output_text.insert(tk.END, output.stdout)
        
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
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter Arguments")

        for arg in arguments:
            arg_frame = tk.Frame(dialog)
            arg_frame.pack(pady=5)

            tk.Label(arg_frame, text=f"{arg}:", width=10).pack(side=tk.LEFT)

            entry_var = tk.StringVar()
            entry = tk.Entry(arg_frame, textvariable=entry_var)
            entry.pack(side=tk.LEFT)

            params[arg] = entry_var

        ok_button = tk.Button(dialog, text="OK", command=dialog.destroy)
        ok_button.pack(pady=10)

        dialog.transient(self.root)  
        dialog.grab_set() 
        self.root.wait_window(dialog)  


        if not all(param.get() for param in params.values()):
            return None

        return {arg: param.get() for arg, param in params.items()}

def show_ascii_art():
    art_file = os.path.join("utils", "ascii_art.txt")
    if os.path.exists(art_file):
        with open(art_file, "r") as f:
            ascii_art = f.read()
        print(ascii_art)
        time.sleep(3)
        subprocess.call("clear" if os.name == "posix" else "cls", shell=True)
    else:
        print("ASCII art file not found!")

if __name__ == "__main__":
    show_ascii_art()  
    root = tk.Tk()
    app = Red2NetApp(root)
    root.mainloop()
