import problem_bank_helpers as pbh

def imports(data):
    import problem_bank_helpers as pbh
    
def generate(data):
    data2 = pbh.create_data2()
    
    data2["params"]["vars"]["title"] = "File Upload"
    
    # Update the data object with a new dict
    data.update(data2)
    
    # The following code is added in by problem bank scripts automatically to
    # convert backticks to codeblocks/code fences in answers text.
    # This line can be commented out to disable
    pbh.backticks_to_code_tags(value)
    # End code added in by problem bank scripts

