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
    data2["correct_answers"]["ans"] = ""
    # we can also add alternate correct answers, which will we can grade as correct
    # lets say we want to accept "Love" as an correct answer as an example, we can do:
    data2["params"]["part1"]["alternate_correct_ans"] = [a * stringname, a * "Love"]
    
    # Update the data object with a new dict
    data.update(data2)
    
    # Start code added automatically by problem_bank_scripts

    # Convert backticks to code blocks/fences in answer choices.
    pbh.backticks_to_code_tags(data2)

    # Update data with data2
    data.update(data2)

    # End code added in by problem bank scripts

def grade(data):
    # Since we want an alternate correct answer, we can check for it here, and override the automatic 
    # score if it is correct
    if data["submitted_answers"]["ans"] in data["params"]["part1"]["alternate_correct_ans"]:
        data["partial_scores"]["ans"] = { "score": 1 }
    
def prepare(data):
    pass
    
def parse(data):
    pass
    
