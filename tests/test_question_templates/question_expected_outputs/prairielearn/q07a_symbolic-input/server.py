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
    
    # store phrases etc
    data2["params"]["vars"]["title"] = 'Centripetal Motion'
    
    # Declare math symbols to be used by sympy
    m, v, r = sp.symbols('m v r')
    
    # Describe the solution equation
    F = m*v**2/r
    
    # Answer to fill in the blank input stored as JSON.
    data2['correct_answers']['part1_ans'] = pl.to_json(F)
    
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
    
