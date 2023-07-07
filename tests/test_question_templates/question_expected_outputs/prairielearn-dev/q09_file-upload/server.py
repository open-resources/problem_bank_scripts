import problem_bank_helpers as pbh

def imports(data):
    import problem_bank_helpers as pbh
    
def generate(data):
    data2 = pbh.create_data2()
    
    data2["params"]["vars"]["title"] = "File Upload"
    
    # Update the data object with a new dict
    data.update(data2)
    
