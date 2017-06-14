assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    # lookp through both elements and combine the items
    return [a+b for a in A for b in B]

# 9 rows for the sudoku puzzle
rows = 'ABCDEFGHI'
# 9 columns
cols = '123456789'
# get all boxes with the cross product function
boxes = cross(rows, cols)
# create a list of lists each containing the boxes in that row
row_units = [cross(r, cols) for r in rows]
# create a list of lists each containing the boxes in that column
column_units = [cross(rows, c) for c in cols]
# create a list of lists each containing the boxes in that square
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Add the units that are diaganol of the puzzle
# first get the elements that are diagonal from left to right
diagonal_left_right_units = [
    [rd+cd for rd, cd in zip(rows, cols)]
]
# tnen get the elements that are diagonal from left to right
diagonal_right_left_units = [
    [rd+cd for rd, cd in zip(rows, reversed(cols))]
]
# store both units into as diagonal_units
diagonal_units = diagonal_left_right_units + diagonal_right_left_units
# keep all units in unitlist
unitlist = row_units + column_units + square_units + diagonal_units
# map each box to it's corresponding units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# map each box to other boxes that share a unit 
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    from collections import defaultdict

    # loop through all units
    for unit in unitlist:
        # to go through two value boxes
        # if value is listed twice list
        two_values_boxes = defaultdict(list)
        # for each box in the unit
        for box in unit:
            # if there are only 2 values
            if len(values[box]) == 2:
                # store the box in a list with the values as a key
                two_values_boxes[values[box]].append(box)

        # now loop through the map (values, boxes) to look for twins
        for val in two_values_boxes:
            # if the value is mapped to two boxes, there are twins
            if len(two_values_boxes[val]) == 2:
                # get the other boxes from the unit
                remaining_boxes = set(unit) - set(two_values_boxes[val])
                for remaining_box in remaining_boxes:
                    # loop through each number individually
                    for v in val:
                        # remove the value from the box
                        assign_value(
                            values, remaining_box, 
                            values[remaining_box].replace(v, ''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # function that will replace '.' with '123456789'
    val_fn = lambda i: '123456789' if i == '.' else i
    # create a dictionary that maps each box to a value provied by the grid
    # if the value is empty ('.') it will be replaced with all possible values
    return dict((box, val_fn(val)) for box, val in zip(boxes, grid))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # return if values is False (solve function was unable to solve puzzle)
    if values is False:
        print("Failed to solve")
        return

    # line will be the horizontal line across the puzzle
    line = '- ' * 11
    # start the current row with a
    current_row = 'A'
    cells = []
    # for each row in row units (use row units because it's in alphabetical order) 
    for row in row_units:
        # loop through boxes in row
        for box in row:
            # if the box is not the current row
            if box[0] != current_row:
                # print the saved cell values
                print(" ".join(cells))
                # if the current_row (last row) was C or F
                # print the line
                if current_row in ('C', 'F'):
                    print(line)
                # clear the cell values
                cells = []
                # update the current row
                current_row = box[0]

            # add box value to cell
            cells.append(values[box])
            # if box column is 3 or 6
            # add a vertical line
            if box[1] in ('3', '6'):
                cells.append('|')

    # if any cells are left, print
    if cells:
        print(" ".join(cells))
    return


def eliminate(values):
    # find all the boxes that only have 1 value
    solved_boxes = [box for box in values if len(values[box]) == 1]
    # for each box
    for box in solved_boxes:
        # find peers of box
        prs = peers[box]
        # for each peer
        for peer_box in prs:
            # remove solved box value from peers' possible value
            assign_value(
                values, peer_box, 
                values[peer_box].replace(values[box], ''))
    return values


def only_choice(values):
    # loop through each unit
    for unit in unitlist:
        # for each possible digit
        for digit in '123456789':
            # get boxes that contain digit within the particular unit
            boxes_with_digit = [box for box in unit if digit in values[box]]
            # if there is only one box in the unit with that digit 
            if len(boxes_with_digit) == 1:
                # assign the digit to the box
                assign_value(values, boxes_with_digit[0], digit)
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values if len(values[box]) == 1])
        # eliminate any solved unit values from peers
        values = eliminate(values)
        # look for naked twins
        values = naked_twins(values)
        # look for peers that only have one choice
        values = only_choice(values)
        solved_values_after = len([box for box in values if len(values[box]) == 1])
        # if no more boxes are being solved stop loop
        stalled = solved_values_before == solved_values_after
        # if any box has 0 possible solutions, the puzzle cannot be solved
        if len([box for box in values if len(values[box]) == 0]):
            return False
    return values


def search(values):
    # solve puzzle with elimanation, naked twins, and only choice strategy
    values = reduce_puzzle(values)
    # if that failed to solve return
    if values is False:
        return False ## Failed earlier
    # if all boxes contain a single value, consider it solved
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
 
 
def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # build the values dict with grid values
    # then search to solve the puzzle
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
