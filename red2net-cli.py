import os
import subprocess
import yaml
from utils.asciiart import join_art_from_files

class Red2NetCLI:
    def __init__(self):
        self.script_dir = "playbooks"
        self.arguments_file = "playbooks/arguments.yaml"
        self.scripts = self.load_scripts()
        self.selected_script = None

    def load_scripts(self):
        return [file for file in os.listdir(self.script_dir) if file.endswith((".py", ".c", ".sh"))]

    def choose_script(self):
        print("Choose a script:")
        for i, script in enumerate(self.scripts):
            print(f"{i+1}. {script}")
        choice = input("Enter script number: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(self.scripts):
                self.selected_script = self.scripts[choice - 1]
                return True
            else:
                print("Invalid choice. Please enter a valid number.")
                return False
        except ValueError:
            print("Invalid input. Please enter a number.")
            return False

    def load_arguments(self):
        arguments_file = os.path.join(self.script_dir, "arguments.yaml")
        if os.path.exists(arguments_file):
            with open(arguments_file, "r") as f:
                arguments = yaml.safe_load(f)
            if self.selected_script in arguments:
                return arguments[self.selected_script]
        return None

    def get_parameters(self, arguments):
        params = {}
        print("Enter script arguments:")
        for arg in arguments:
            value = input(f"{arg}: ")
            params[arg] = value
        return params

    def run_script(self):
        if not self.selected_script:
            print("No script selected.")
            return

        arguments = self.load_arguments()
        if not arguments:
            print("Arguments file not found for the selected script.")
            return

        params = self.get_parameters(arguments)

        script_path = os.path.join(self.script_dir, self.selected_script)
        command = []

        if self.selected_script.endswith((".sh", ".c")):
            os.chdir(self.script_dir) 
            if self.selected_script.endswith(".c"):
                compiled_name = self.selected_script[:-2]
                if os.path.exists(compiled_name):
                    os.remove(compiled_name)
                subprocess.run(["gcc", "-o", compiled_name, self.selected_script])
                command.append(f"./{compiled_name}") 
            else:
                command.append(f"./{self.selected_script}") 
        else:
            command.extend(["sudo", "python3", script_path])
# Run Python script
        for arg, value in params.items():
            command.extend(["-" + arg, value])

        print("$ " + " ".join(command))

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")

def show_ascii_art():
    art_file = os.path.join("utils", "ascii_art.txt")
    if os.path.exists(art_file):
        with open(art_file, "r") as f:
            ascii_art = f.read()
        print(ascii_art)
    else:
        print("ASCII art file not found!")

if __name__ == "__main__":
    combined_art = join_art_from_files(str_between=' ')
    print(combined_art)
    red2net_cli = Red2NetCLI()
    while not red2net_cli.choose_script():
        pass
    red2net_cli.run_script()
