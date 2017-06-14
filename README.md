# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We reduced the search space, number of possibilites by eliminating the two values from each box that is a peer of the 2 or more boxes that only had those two values as possible solutions. If two boxes within a unit share the exact two possible values, then the other 7 boxes could not possibly have either of those two values as a possible solution. Only the two boxes can have either of the two values. This logic helps us constrain the possible solutions for the remaining boxes in the unit, by eliminating those two values as possible solutions.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We reduced the number of possiblities by adding the units that are diagonal across the entire puzzle as peers of one another. A "unit" is a group of boxes that must obey the rule of having the numbers 1 through appear only once. This additional constraint for the diagonal from left to right and diagnol right to left was added to the total units. Our eliminate function, looks for a box that has only value, will remove the value of the box from it's peer boxes. Which with our addition of diagonal units, would include the boxes diagonal to it (if the box is within the two diagonal units). Our only_choice function, looks for a box within a unit with one of it's possible values distinct from the other boxes in the unit. The diagonal units were included in this as well. Our naked twins, function also goes through the all units, including diagonal units, and looks for two boxes within the unit that share the same two values. The values are then removed from the remaining boxes within the unit. While using these functions to apply the constraints across all units, we were able to solve the puzzle.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

