from problem_bank_scripts import __version__
from src.problem_bank_scripts import problem_bank_scripts as pbs
import pandas as pd
import pathlib  
import filecmp
import os

def test_version():
    assert __version__ == '0.1.1'

# def test_rounded():

#     value = 100 / 3

#     rounded_value = pbs.rounded(value, digits_after_decimal = 3)

#     assert rounded_value == str(33.333)

def test_prairie():
    inputDest = pathlib.Path('tests/test_question_templates/question_inputs/')
    outputDest = pathlib.Path('tests/test_question_templates/question_generated_outputs/')
    compareDest = pathlib.Path('tests/test_question_templates/question_expected_outputs/')

    for file in inputDest.glob('**/*'):
      if os.path.isfile(file):
          if file.name.endswith('.md'):
            folder = file.parent.name
            outputFolder = outputDest.joinpath(folder)
            pbs.process_question_pl(file, outputFolder.joinpath(file.name))

    for file in compareDest.glob('**/*'):
        isFile = os.path.isfile(file) 
        notHiddenFile = not file.name.startswith('.')
        notImageFile = not file.name.endswith('.png') 
        notJsonFile = not file.name.endswith('.json')
        if isFile and notHiddenFile and notImageFile and notJsonFile:
            folder = file.parent.name
            outputFolder = outputDest.joinpath(folder)
            assert filecmp.cmp(file, outputFolder.joinpath(file.name), shallow = False)
