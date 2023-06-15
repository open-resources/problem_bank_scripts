import random
import pandas as pd
import problem_bank_helpers as pbh

def imports(data):
    import random
    import pandas as pd
    import problem_bank_helpers as pbh
    
def generate(data):
    data2 = pbh.create_data2()
    
    # define or load names/items/objects
    names = pbh.names.copy()
    manual_vehicles = pbh.manual_vehicles.copy()
    
    # store phrases etc
    data2["params"]["vars"]["name"] = random.choice(names)
    data2["params"]["vars"]["vehicle"] = random.choice(manual_vehicles)
    data2["params"]["vars"]["title"] = "Integer Math"
    data2["params"]["vars"]["units"] = "m/s"
    
    # define bounds of the variables
    n = random.randint(2,100)
    
    # store the variables in the dictionary "params"
    data2["params"]["n"] = n
    
    # define correct answers
    data2["correct_answers"]["part1_ans"] = int(n*10)
    
    # Update the data object with a new dict
    data.update(data2)
    
def prepare(data):
    pass
    
def parse(data):
    pass
    
def grade(data):
    pass
    
