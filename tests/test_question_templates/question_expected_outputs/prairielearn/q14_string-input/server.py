import random; random.seed(111) 
import problem_bank_helpers as pbh

def imports(data):
    import random; random.seed(111) 
    import problem_bank_helpers as pbh
    
def generate(data):
    data2 = pbh.create_data2()
    
    a = random.randint(2, 4)
    stringname = "love"
    
    data2["params"]["vars"]["title"] = "Code Output"
    data2["params"]["vars"]["a"] = a
    data2["params"]["vars"]["stringname"] = stringname
    data2["correct_answers"]["ans1"] = a * stringname
    
    # Update the data object with a new dict
    data.update(data2)
    
