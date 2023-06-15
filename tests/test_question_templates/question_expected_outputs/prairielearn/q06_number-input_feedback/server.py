import random as rd; rd.seed(111)
import numpy as np
import pandas as pd
import problem_bank_helpers as pbh

# Feedback params
rtol = 0.03
errorCheck = 'True'

feedback_dict = {'vars': ['part1_ans'],
                 'stringData': ['I'],
                 'units': ['$~\mathrm{A}$']
                 }

def imports(data):
    import random as rd; rd.seed(111)
    import numpy as np
    import pandas as pd
    import problem_bank_helpers as pbh
    
    # Feedback params
    rtol = 0.03
    errorCheck = 'True'
    
    feedback_dict = {'vars': ['part1_ans'],
                     'stringData': ['I'],
                     'units': ['$~\mathrm{A}$']
                     }
    
def generate(data):
    data2 = pbh.create_data2()
    
    # define bounds of the variables
    n = rd.choice(np.linspace(10, 35, num = 6)) # cm^-1
    r = rd.choice(np.linspace(1, 3, num = 21)) # cm
    v = rd.choice(np.linspace(1, 3, num = 21))
    p = rd.choice([4, 5, 6])
    
    # store the variables in the dictionary "params"
    data2["params"]["n"] = "{:.0f}".format(n)
    data2["params"]["r"] = "{:.2f}".format(r)
    data2["params"]["v"] = "{:.2f}".format(v)
    data2["params"]["p"] = "{:.0f}".format(p)
    
    # fix units
    n = n*100 # m^-1
    r = r/100 # m
    v = v*10**p # m/s
    
    # define some constants
    mu0 = 4e-7*np.pi
    m = 9.11e-31 # kg
    q = 1.6e-19 # C
    
    # calculate the correct
    I = m*v/(mu0*n*q*r) # A
    
    # define correct answers
    data2["correct_answers"]["part1_ans"] = I
    
    # Write the solution formatted using scientific notation while keeping 3 sig figs.
    data2["correct_answers"]["part1_ans_str"] = "{:.2e}".format(I)
    
    # Update the data object with a new dict
    data.update(data2)
    
def prepare(data):
    pass
    
def parse(data):
    # Call a function to check if the submitted answers should be re-expressed using scientific notation.
    for i,k in enumerate(feedback_dict['vars']):
        data["submitted_answers"][k + '_str'] = pbh.sigFigCheck(data["submitted_answers"][k], feedback_dict['stringData'][i], feedback_dict['units'][i])
    
def grade(data):
    # Call a function to check for easily-identifiable errors.
    # The syntax is pbh.ErrorCheck(errorCheck, submittedAnswer, correctAnswer, LaTeXsyntax, relativeTolerance)
    # To enable error checking, set errorCheck = 'true'.
    
    for i,k in enumerate(feedback_dict['vars']):
        data["feedback"][k] = pbh.ErrorCheck(errorCheck, data["submitted_answers"][k], data["correct_answers"][k], feedback_dict['stringData'][i], rtol)
    
