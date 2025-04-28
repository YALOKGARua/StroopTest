Stroop Test
A psychological Stroop Test implemented in Python using Pygame. The project features three test parts, localization (English, Russian, Ukrainian), customizable screen resolution and display modes, and interactive feedback. Color buttons shuffle after each response (correct or incorrect), button text adapts for readability, and text/square positions in parts 2 and 3 are randomized.
Features

Three Test Parts:
Select the color matching the word's meaning.
Select the color of the displayed square.
Select the color of the text, ignoring its meaning.


Localization: Supports English, Russian, and Ukrainian languages.
Settings: Adjust screen resolution and display mode (fullscreen, no-frame, windowed).
Interactivity: Color buttons shuffle after each response, with adaptive text color (white for dark buttons, black for light).
Results: Displays average reaction time, coefficient, and accuracy.
Compatibility: Supports Pyodide for browser-based execution.

Requirements

Python 3.13.2
Pygame 2.6.1

Installation

Clone the repository:git clone https://github.com/<your-username>/StroopTest.git
cd StroopTest


(Optional) Create a virtual environment:python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies:pip install -r requirements.txt



Running the Project

Ensure main.py, localization.py, and config.json are in the same directory.
Run the game:python main.py



Usage

Main Menu: Select "Play" to start the test, "Settings" to configure options, or "Exit" to quit.
Settings: Modify language, screen resolution, or display mode.
Game:
Part 1: Choose the button matching the word's meaning (e.g., "Red" → red button).
Part 2: Choose the button matching the square's color.
Part 3: Choose the button matching the text's color, ignoring its meaning (e.g., "Red" in blue → blue button).


Results: View average reaction time, coefficient, and accuracy; choose "Restart" or "Main Menu."

Project Structure

main.py: Core game logic, rendering, and event handling.
localization.py: Manages translations and color definitions.
config.json: Configuration for screen settings, language, and game parameters.
requirements.txt: Lists dependencies.
.gitignore: Ignores temporary and environment files.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for bug fixes, features, or improvements.
