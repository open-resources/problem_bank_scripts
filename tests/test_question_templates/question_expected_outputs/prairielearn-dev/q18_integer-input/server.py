import random; random.seed(111)
from statistics import median
import problem_bank_helpers as pbh

def imports(data):
    import random; random.seed(111)
    from statistics import median
    import problem_bank_helpers as pbh
    
def generate(data):
    data2 = pbh.create_data2()
    
    numbers = sorted(random.randint(1, 100) for _ in range(9))
    # store the variables in the dictionary "params"
    data2["params"]["numbers"] = numbers
    
    # define correct answers
    data2["correct_answers"]["part1_ans"] = median(numbers)
    
    # Update the data object with a new dict
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
    
