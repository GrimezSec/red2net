import os
import subprocess
import time
import yaml
from utils.asciiart import join_art_from_files

class Red2NetCLI:
    def __init__(self):
        self.script_dir = "playbooks"
        self.arguments_file = os.path.join(self.script_dir, "arguments.yaml")
        self.scripts = self.load_scripts()
        self.selected_script = None
        self.tests_failed = False

    def load_scripts(self):
        return [file for file in os.listdir(self.script_dir) if file.endswith((".py", ".c", ".sh"))]

    def choose_script(self):
        print("Choose a script:")
        for i, script in enumerate(self.scripts):
            print(f"{i+1}. {script}")
        while True:
            choice = input("Enter script number: ")
            if not choice.isdigit():
                print("Invalid input. Please enter a valid number.")
                continue
            choice = int(choice)
            if 1 <= choice <= len(self.scripts):
                self.selected_script = self.scripts[choice - 1]
                return True
            else:
                print("Invalid choice. Please enter a valid number.")

    def load_arguments(self):
        if os.path.exists(self.arguments_file):
            with open(self.arguments_file, "r") as f:
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

    def run_tests(self):
        if not self.selected_script:
            print("No script selected.")
            return

        arguments = self.load_arguments()
        if not arguments:
            print("Arguments file not found for the selected script.")
            return

        params = self.get_parameters(arguments)

        script_path = os.path.join(self.script_dir, self.selected_script)
        test_command = []

        if self.selected_script.endswith((".sh", ".c")):
            test_command.append(f"./test.{self.selected_script[-2:]}")
        else:
            test_command.extend(["sudo", "python3", os.path.join(self.script_dir, "test.py")])

        for arg, value in params.items():
            test_command.extend(["-" + arg, value])

        print("$ " + " ".join(test_command))
        try:
            subprocess.run(test_command, check=True)
            print("Tests successful")
        except subprocess.CalledProcessError as e:
            print(f"Tests failed: {e.stderr}")
            self.tests_failed = True

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

        for arg, value in params.items():
            if value is not None and arg is not None:  # Validate both arg and value
                command.extend(["-" + arg, value])
            elif value is not None:  # If arg is None, append only value
                command.append(value)

        print("$ " + " ".join(command))
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")

if __name__ == "__main__":
    combined_art = join_art_from_files(str_between=' ')
    print(combined_art)
    
    red2net_cli = Red2NetCLI()
        
    if not red2net_cli.tests_failed:
        print("Tests successful!")
        time.sleep(0.5)   
        red2net_cli.run_script()
    else:
        print("Tests failed")
    while not red2net_cli.choose_script():
        pass
    
    red2net_cli.run_tests()

