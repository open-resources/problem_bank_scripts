from problem_bank_scripts import __version__
from src.problem_bank_scripts import problem_bank_scripts as pbs
import pandas as pd
import pathlib  
import filecmp

def test_version():
    assert __version__ == '0.0.7'

# def test_rounded():

#     value = 100 / 3

#     rounded_value = pbs.rounded(value, digits_after_decimal = 3)

#     assert rounded_value == str(33.333)

def test_prairie():
    inputDest = pathlib.Path('tests/test_question_templates/question_inputs/q01_multiple-choice/q01_multiple-choice.md')
    outputDest = pathlib.Path('tests/test_question_templates/question_generated_outputs/q01_multiple-choice/q01_multiple-choice.md')
    pbs.process_question_pl(inputDest, outputDest)
    compareDest = pathlib.Path('tests/test_question_templates/question_expected_outputs/q01_multiple-choice/question.html')
    assert filecmp.cmp(outputDest.parent / 'question.html', compareDest, shallow = False)