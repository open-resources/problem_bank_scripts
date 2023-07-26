import random as rd; rd.seed(111)
import pandas as pd
import problem_bank_helpers as pbh

def imports(data):
    import random as rd; rd.seed(111)
    import pandas as pd
    import problem_bank_helpers as pbh
    
def generate(data):
    data2 = pbh.create_data2()
    
    # define or load names/items/objects
    names = pbh.names.copy()
    manual_vehicles = pbh.manual_vehicles.copy()
    
    # store phrases etc
    data2["params"]["vars"]["name"] = rd.choice(names)
    data2["params"]["vars"]["vehicle"] = rd.choice(manual_vehicles)
    data2["params"]["vars"]["title"] = "Integer Math"
    data2["params"]["vars"]["units"] = "m/s"
    
    # define bounds of the variables
    n = rd.randint(2,100)
    
    # store the variables in the dictionary "params"
    data2["params"]["n"] = n
    
    # define correct answers
    data2["correct_answers"]["part1_ans"] = int(n*10)
    
    # Update the data object with a new dict
    data.update(data2)
    
    # The following code is added in by problem bank scripts automatically to
    # convert backticks to codeblocks/code fences in answers text.
    # This line can be commented out to disable
    pbh.backticks_to_code_tags(value)
    # End code added in by problem bank scripts

def prepare(data):
    pass
    
def parse(data):
    pass
    
def grade(data):
    pass
    
