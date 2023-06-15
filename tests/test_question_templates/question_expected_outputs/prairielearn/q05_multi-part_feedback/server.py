import random
import numpy as np
import pandas as pd
import problem_bank_helpers as pbh

# Feedback params
rtol = 0.03
errorCheck = 'True'

feedback_dict = {'vars': ['part1_ans'],
                 'stringData': ['E'],
                 'units': ['$~\mathrm{N}/\mathrm{C}$']
                 }

def imports(data):
    import random
    import numpy as np
    import pandas as pd
    import problem_bank_helpers as pbh
    
    # Feedback params
    rtol = 0.03
    errorCheck = 'True'
    
    feedback_dict = {'vars': ['part1_ans'],
                     'stringData': ['E'],
                     'units': ['$~\mathrm{N}/\mathrm{C}$']
                     }
    
def generate(data):
    data2 = pbh.create_data2()
    
    # Sample random numbers
    L = random.choice(np.linspace(7, 15, num = 9))
    q = random.choice(np.linspace(1, 9, num = 41))
    p = random.choice(np.linspace(-10, -6, num = 5))
    d = random.choice(np.linspace(0.5, 2.5, num = 21))
    
    # Put these numbers into data['params']
    data2["params"]["L"] = "{:.0f}".format(L)
    data2["params"]["q"] = "{:.1f}".format(q)
    data2["params"]["p"] = "{:.0f}".format(p)
    data2["params"]["d"] = "{:.1f}".format(d)
    
    # Compute the solutions
    e0 = 8.85e-12 # C^2/N m^2
    E = float((q*10**p/(L/100)**2)/e0) # N/C
    
    # Put the solutions into data['correct_answers']
    data2['correct_answers']['part1_ans'] = E
    
    # Write the solutions formatted using scientific notation while keeping 3 sig figs.
    data2['correct_answers']['part1_ans_str'] = pbh.roundp(E, sigfigs=3, format = 'sci')
    
    # define possible answers
    
    data2["params"]["part2"]["ans1"]["value"] = 'points towards the negative plate'
    data2["params"]["part2"]["ans1"]["correct"] = True
    
    data2["params"]["part2"]["ans2"]["value"] = 'points towards the positive plate'
    data2["params"]["part2"]["ans2"]["correct"] = False
    
    data2["params"]["part2"]["ans3"]["value"] = 'points parallel to the plates'
    data2["params"]["part2"]["ans3"]["correct"] = False
    
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
    # To enable error checking, set check = 'true'.
    
    for i,k in enumerate(feedback_dict['vars']):
        data["feedback"][k] = pbh.ErrorCheck(errorCheck, data["submitted_answers"][k], data["correct_answers"][k], feedback_dict['stringData'][i], rtol)
    
