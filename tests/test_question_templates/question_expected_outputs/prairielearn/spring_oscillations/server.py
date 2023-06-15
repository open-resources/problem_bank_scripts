import random
import math
import pandas as pd
import problem_bank_helpers as pbh

def imports(data):
    import random
    import math
    import pandas as pd
    import problem_bank_helpers as pbh
    
def generate(data):
    data2 = pbh.create_data2()
    
    # store phrases etc
    data2["params"]["vars"]["title"] = "Simple harmonic spring"
    data2["params"]["vars"]["units1"] ="m/s"
    data2["params"]["vars"]["units2"] ="N/m"
    data2["params"]["vars"]["units3"] = "m"
    
    # define bounds of the variables
    m = random.randint(315,335)
    T = pbh.roundp(random.uniform(0.2,2.0), sigfigs=2)
    E = pbh.roundp(random.uniform(4,7), sigfigs = 2)
    
    # store the variables in the dictionary "params"
    data2["params"]["m"] = m
    data2["params"]["T"] = T
    data2["params"]["E"] = E
    
    # define correct answers
    # m is divided by 1000 since it is given in grams
    data2["correct_answers"]["part1_ans"] = pbh.roundp(math.sqrt(2*E/(m/1000)), sigfigs = 2)
    data2["correct_answers"]["part2_ans"] = pbh.roundp((m/1000)*((2*math.pi/T)**2), sigfigs = 2)
    data2["correct_answers"]["part3_ans"] = pbh.roundp(math.sqrt(2*E/((m/1000)*((2*math.pi/T)**2))), sigfigs = 2)
    
    # Update the data object with a new dict
    data.update(data2)
    
def prepare(data):
    pass
    
def parse(data):
    pass
    
def grade(data):
    pass      
    
