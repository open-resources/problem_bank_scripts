import random as rd
import pandas as pd
import problem_bank_helpers as pbh

def generate(data):
    data2 = pbh.create_data2()
    
    # define or load names/items/objects
    names = pbh.names.copy()
    
    # store phrases etc
    data2["params"]["vars"]["title"] = 'Vectors and Scalars'
    data2["params"]["vars"]["name"] = rd.choice(names)
    
    # define useful variables/lists
    vectors = ["displacement", "velocity", "acceleration", "momentum", "force", "lift", "drag", "thrust", "weight"]
    scalars = ["length", "area", "volume", "mass", "density", "pressure", "temperature", "energy", "entropy", "work", "power"]
    
    # Randomly select 2,3,4 scalars and shuffle the lists
    total_choices = 6
    num_scalars = rd.choice([2,3,4])
    num_vectors = total_choices - num_scalars
    select = rd.choice(["vectors","scalars"])
    
    data2["params"]["choice"] = select
    
    # Create ans_choices
    ans_choices = [f"ans{i+1}" for i in range(total_choices)]
    
    rd.shuffle(scalars)
    rd.shuffle(vectors)
    
    # define possible answers
    if select == "vectors":
        for i in range(num_vectors):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = vectors.pop()
            data2["params"]["part1"][choice]["correct"] = True
            data2["params"]["part1"][choice]["feedback"] = "Correct! Nice work"
    
        for i in range(num_scalars):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = scalars.pop()
            data2["params"]["part1"][choice]["correct"] = False
            data2["params"]["part1"][choice]["feedback"] = "Not quite - Try again!"
    
    elif select == "scalars":
        for i in range(num_scalars):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = scalars.pop()
            data2["params"]["part1"][choice]["correct"] = True
            data2["params"]["part1"][choice]["feedback"] = "Correct! Nice work"
    
        for i in range(num_vectors):
            choice = ans_choices.pop(0)
            data2["params"]["part1"][choice]["value"] = vectors.pop()
            data2["params"]["part1"][choice]["correct"] = False
            data2["params"]["part1"][choice]["feedback"] = "Not quite - Try again!"
    
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
    
