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
    data2["params"]["vars"]["title"] = "Distance travelled"
    data2["params"]["vars"]["units"] = "m/s"
    
    # define bounds of the variables
    v = rd.randint(2,7)
    t = rd.randint(5,10)
    
    # store the variables in the dictionary "params"
    data2["params"]["v"] = v
    data2["params"]["t"] = t
    
    # define all options for right side of matching
    data2["params"]["part1"]["option1"]["value"] = True
    data2["params"]["part1"]["option1"]["name"] = "True"
    data2["params"]["part1"]["option2"]["value"] = False
    data2["params"]["part1"]["option2"]["name"] = "False"
    
    data2["params"]["part1"]["statement1"]["value"] = pbh.roundp(42)
    data2["params"]["part1"]["statement1"]["matches"] = "False"
    data2["params"]["part1"]["statement2"]["value"] = pbh.roundp(v*t)
    data2["params"]["part1"]["statement2"]["matches"] = "True"
    data2["params"]["part1"]["statement3"]["value"] = pbh.roundp(v+t)
    data2["params"]["part1"]["statement3"]["matches"] = "False"
    data2["params"]["part1"]["statement4"]["value"] = pbh.roundp(v/t)
    data2["params"]["part1"]["statement4"]["matches"] = "False"
    
    # Update the data object with a new dict
    data.update(data2)
    
def prepare(data):
    pass
    
def parse(data):
    pass
    
def grade(data):
    pass
    
