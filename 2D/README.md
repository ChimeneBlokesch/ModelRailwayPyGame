# Model Railway 2D

## How to Play
1. Install the packages using pip ([requirements.txt](../requirements.txt)) or conda ([environment.yml](../environment.yml)).
2. Run `python main.py` in the terminal.
3. Click on the line to select the command line.
4. Type commands while the command line is selected, use enter to execute the command.

## Commands
The available commands have the following format. The variables are described as `<variable_name>`.
- `add straight <x1> <y1> <x2> <y2>`
- `add curve <x1> <y1> <x2> <y2>`
- `add train <x> <y> <angle> <name>`

The folder names in [sprites/trains](sprites/trains/) are the possible values for `<name>`.

<img src="images/0_init.png" alt="Start application" width="500"/>
<br>
<img src="images/1_command.png" alt="Show command" width="500"/>
<br>
<img src="images/2_added.png" alt="Added straight rails" width="500"/>
