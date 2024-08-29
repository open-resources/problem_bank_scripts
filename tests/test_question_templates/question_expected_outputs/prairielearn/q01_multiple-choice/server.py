import random as rd
import pandas as pd
import problem_bank_helpers as pbh

def generate(data):
    data2 = pbh.create_data2()
    
    # define or load names/items/objects from server files
    names = pbh.names.copy()
    manual_vehicles = pbh.manual_vehicles.copy()
    
    # store phrases etc
    data2["params"]["vars"]["title"] = 'Kinematics'
    data2["params"]["vars"]["name"] = rd.choice(names)
    data2["params"]["vars"]["vehicle"] = rd.choice(manual_vehicles)
    data2["params"]["vars"]["units"] = "m/s"
    
    # Randomize Variables
    v = rd.randint(2,7)
    t = rd.randint(5,10)
    
    # store the variables in the dictionary "params"
    data2["params"]["v"] = v
    data2["params"]["t"] = t
    
    # define possible answers
    data2["params"]["part1"]["ans1"]["value"] = f"`{pbh.roundp(42)}`"
    data2["params"]["part1"]["ans1"]["correct"] = False
    data2["params"]["part1"]["ans1"]["feedback"] = "This is a random number, you probably selected this choice by mistake! Try again please!"
    
    data2["params"]["part1"]["ans2"]["value"] = f"`{pbh.roundp(v*t)}`"
    data2["params"]["part1"]["ans2"]["correct"] = True
    data2["params"]["part1"]["ans2"]["feedback"] = "Great! You got it."
    
    data2["params"]["part1"]["ans3"]["value"] = f"`{pbh.roundp(v+t)}`"
    data2["params"]["part1"]["ans3"]["correct"] = False
    data2["params"]["part1"]["ans3"]["feedback"] = "Hmm, does it make sense to add a velocity and a time? Check the units!"
    
    data2["params"]["part1"]["ans4"]["value"] = f"`{pbh.roundp(v/t)}`"
    data2["params"]["part1"]["ans4"]["correct"] = False
    data2["params"]["part1"]["ans4"]["feedback"] = "Hmm, check the units of the resulting answer: v/t."
    
    data2["params"]["part1"]["ans5"]["value"] = f"`{pbh.roundp(v-t)}`"
    data2["params"]["part1"]["ans5"]["correct"] = False
    data2["params"]["part1"]["ans5"]["feedback"] = "Hmm, does it make sense to subtract a velocity and a time? Check the units!"
    
    data2["params"]["part1"]["ans6"]["value"] = f"`{pbh.roundp(1.3*(v-t))}`"
    data2["params"]["part1"]["ans6"]["correct"] = False
    data2["params"]["part1"]["ans6"]["feedback"] = "Hmm, does it make sense to subtract a velocity and a time? Check the units!"
    
    # Update the data object with a new dict
    data.update(data2)
    
    # Start code added automatically by problem_bank_scripts

    # Convert backticks to code blocks/fences in answer choices.
    pbh.backticks_to_code_tags(data2)

    # Update data with data2
    data.update(data2)

    # End code added in by problem bank scripts

def prepare(data):
    pass
    
def parse(data):
    pass
    
def grade(data):
    pass
    
