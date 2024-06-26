# red2net

Red2Net is a simple network testing tool developed in Python with a CLI version.

## Features

- Run network tests using Python, Bash, or C scripts.
- Users can add new tests by writing scripts and updating the arguments.yaml file.
- Modular structure for easy maintenance and extension.

## Usage

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/GrimezSec/red2net.git
    ```

2. Navigate to the project directory:

    ```
    cd red2net
    ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

4. Run the application:

    ```
    python red2net.py
    ```

5. Choose a script from the dropdown menu, enter the required arguments, and click the "Run Script" button.

## Adding New Tests

To add a new test, follow these steps:

1. Write a new script in the `scripts` directory. The script should accept arguments as specified in the `arguments.yaml` file.

2. Update the `arguments.yaml` file with the arguments required by the new script.

3. Restart the application to see the new test in the dropdown menu.

## TODO
1. Add installation script
2. Add run script
3. Make improvements about sudo privileges
4. Add a function to record network and save with pcap format
