import problem_bank_helpers as pbh

def generate(data):
    data2 = pbh.create_data2()
    
    data2["params"]["vars"]["title"] = "Describe an Experiment"
    
    # Update the data object with a new dict
    data.update(data2)
    
    # Start code added automatically by problem_bank_scripts

    # Convert backticks to code blocks/fences in answer choices.
    pbh.backticks_to_code_tags(data2)

    # Update data with data2
    data.update(data2)

    # End code added in by problem bank scripts

