import random as rd
import math
import problem_bank_helpers as pbh

def imports(data):
    import random as rd
    import math
    import problem_bank_helpers as pbh
    
def generate(data):
    # randomized question
    numbers = list(range(4, 11))
    rd.shuffle(numbers)
    randInt = rd.choice(numbers)
    question_dict = {
        f"{randInt}th power": randInt,
        f"{randInt}th root": 1/randInt
    }
    question_list = list(question_dict.keys())
    question = rd.choice(question_list)
    
    data["params"]["question"] = question
    data["params"]["num"] = question_dict[question]
    
    
    # randomized variable names
    name_list = ["giraffe", "warthog", "dog", "crab"]
    function_name = rd.choice(name_list)
    data["params"]["fname"] = function_name
    
    
    # create some example inputs and outputs
    for i in range(3):
        input = numbers.pop(0)
        data["params"]["input" + str(i)] = input
        data["params"]["output" + str(i)] = math.pow(input, question_dict[question])
    
    # variables detected by autograder
    ## list of variables provided to students
    data["params"]["names_for_user"] = [
        {"name": "x", "description": "A random input number", "type": "int"}
    ]
    
    ## list of variables/references extracted from student answer
    data["params"]["names_from_user"] = [
        {"name": function_name, "description": f"receives a single numerical input, returns its {question}", "type": "function"}
    ]
    
def prepare(data):
    pass
    
def parse(data):
    pass
    
def grade(data):
    pass
    
