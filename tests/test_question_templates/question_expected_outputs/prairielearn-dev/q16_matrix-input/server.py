import numpy as np
import problem_bank_helpers as pbh
import prairielearn as pl

def generate(data):
    data2 = pbh.create_data2()
    data2["params"]["title"] = "Matrix Input"
    
    matrix = np.random.random((2,2))
    inv_matrix = np.linalg.inv(matrix)
    
    # store phrases, info etc
    data2["params"]["matrixA"] = pl.to_json(matrix)
    
    # store the correct answers
    data2["correct_answers"]["part1_ans"] = pl.to_json(inv_matrix)
    data2["correct_answers"]["part2_ans"] = pl.to_json(inv_matrix)
    
    data.update(data2)
    
    # Start code added automatically by problem_bank_scripts

    # Convert backticks to code blocks/fences in answer choices.
    pbh.backticks_to_code_tags(data2)

    # Update data with data2
    data.update(data2)

    # End code added in by problem bank scripts

def prepare(data):
    pass
    
def parse(data):
    pass
    
def grade(data):
    pass
    
