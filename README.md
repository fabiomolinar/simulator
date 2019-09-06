# Simulator

A small experiment into trying to create my own Python based simulation tool.

This project also serves as a reference to create other Python projects.

Below the results from runing a RC (resistor-capacitor) circuit.

![RC simulation result](https://i.ibb.co/ZxfYqf8/rc-simulation-run.png)

## Running the simulation

To run the model, it sufices to run the `run_sim.py` python script which is located at the project folder. In other words, from the project directory, run this command: `python run_sim.py`.

## To do

- <span style="text-decoration: line-through">Store variables to be ploted on the Plot class</span> [done]
    - Problem: Some variables have largely different scales than others; therefore, when ploted on the same scale, it's not possible to see them clearly.
    - Solution: use the plots.Line class which is capable to handle scaling.
- <span style="text-decoration: line-through">Add improved PID regulator algorithm.</span> [done]
- Add a performance measuring class.
- Add information about time constant to each model.
- Add to the simulator information if cycle time is to slow compared with models' time constants.
    - Problem: if the cycle time is too big to impact the dynamics of the models, I need to warn it.
- Change place where data is stored.
    - Problem: each model is holding its own data. That's not effective. Not all data may be necessary and doing operation on arrays isn't as fast as doing on simple numbers. Furthermore, the models' `calculate` method is damn ugly.
    - Solution: create a DataHolder class which will hold only the selected data and will get updated at each cycle.


## Python

Notes related to creating this Python project.

### Structure

To make modules visible to each other, they should all be contained within one single package inside the project folder. In other words, the project should follow this structure:

    project_folder
        project_package
            __init__.py
            package1
                __init__.py
                module1.py
                module2.py
            package2
                __init__.py
                module3.py
                module4.py
        [other files]

Other files could be scripts, tests, README.md, LICENSE, .gitignore, etc.

### VScode

#### Debugging

Since this project is configured to be a package, a script (`run_sim.py`) was created at the project folder to load the project package and run it. Therefore, in order to debug it on VScode, it is necessary to create a new debug configuration to run the debugger from the aforementioned script and with from the project's directory path. The following configuration is used:

    {
        "name": "Python: run_sim.py",
        "type": "python",
        "request": "launch",
        "program": "${workspaceFolder}/run_sim.py"
    }

#### Unit tests

Since the tests are not inside the same package as the project package, on the test modules it's necessary to import the project modules using absolute paths. For example, instead of doing **from ...models import rc**, it's necessary to do **from simulator.models import rc**.

To run the tests, it sufices to run the following command from the project's directory (if not actually using VScode's extensions): `python -m unittest discover -v` (for the verbose option).

#### Unit tests debugging

Since the tests package is outside the project package, it's necessary to add a debugger configuration in order to be able to debug the tests. The following configuration is used (calling the `unittest` as a module):

    {
        "name": "Python: Debugging",
        "type": "python",
        "request": "launch",
        "module": "unittest"
    }

This setup runs the tests with the debugger.