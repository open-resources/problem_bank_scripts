import random as rd; rd.seed(111)
import pandas as pd
import sympy as sp
import problem_bank_scripts.prairielearn as pl
import problem_bank_helpers as pbh

def imports(data):
    import random as rd; rd.seed(111)
    import pandas as pd
    import sympy as sp
    import problem_bank_scripts.prairielearn as pl
    import problem_bank_helpers as pbh
    
def generate(data):
    data2 = pbh.create_data2()
    
    # define or load names/items/objects
    names = pbh.names.copy()
    vehicles = pbh.vehicles.copy()
    
    # store phrases etc
    data2["params"]["vars"]["title"] = 'Symbolic Input 2 - Trig'
    data2["params"]["vars"]["name"] = rd.choice(names)
    data2["params"]["vars"]["vehicle"] = rd.choice(vehicles)
    
    # Declare math symbols to be used by sympy
    mu_s, g , theta = sp.symbols('mu_s g theta')
    
    # Describe the solution equation
    amax = g*(mu_s*sp.cos(theta) - sp.sin(theta))
    
    # Answer to fill in the blank input -- must be stored as JSON.
    data2['correct_answers']['part1_ans'] = pl.to_json(amax)
    
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
    
