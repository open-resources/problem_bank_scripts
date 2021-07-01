from problem_bank_scripts import __version__
from src.problem_bank_scripts import problem_bank_scripts as pbs
import pandas as pd
import pathlib  
import filecmp
import os
import pytest

def test_version():
    assert __version__ == '0.1.1'

# def test_rounded():

#     value = 100 / 3

#     rounded_value = pbs.rounded(value, digits_after_decimal = 3)

#     assert rounded_value == str(33.333)


@pytest.fixture
def paths():
    p = {
        'inputDest': pathlib.Path('tests/test_question_templates/question_inputs/'),
        'outputDest': pathlib.Path('tests/test_question_templates/question_generated_outputs/'),
        'compareDest': pathlib.Path('tests/test_question_templates/question_expected_outputs/')
    }
    return p

def test_prairie_learn(paths):

    outputPath = paths['outputDest'].joinpath('prairielearn/')
    comparePath = paths['compareDest'].joinpath('prairielearn/')

    for file in paths['inputDest'].glob('**/*'):
      if os.path.isfile(file):
          if file.name.endswith('.md'):
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            pbs.process_question_pl(file, outputFolder.joinpath(file.name))

    for file in comparePath.glob('**/*'):
        isFile = os.path.isfile(file) 
        notHiddenFile = not file.name.startswith('.')
        notImageFile = not file.name.endswith('.png') 
        notJsonFile = not file.name.endswith('.json')
        if isFile and notHiddenFile and notImageFile and notJsonFile:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            assert filecmp.cmp(file, outputFolder.joinpath(file.name), shallow = False)

def test_public(paths):

    outputPath = paths['outputDest'].joinpath('public/')
    comparePath = paths['compareDest'].joinpath('public/')

    for file in paths['inputDest'].glob('**/*'):
      if os.path.isfile(file):
          if file.name.endswith('.md'):
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            pbs.process_question_md(file, outputFolder.joinpath(file.name), instructor = False)
    
    for file in comparePath.glob('**/*'):
        isFile = os.path.isfile(file) 
        notHiddenFile = not file.name.startswith('.')
        notImageFile = not file.name.endswith('.png') 
        if isFile and notHiddenFile and notImageFile:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            assert filecmp.cmp(file, outputFolder.joinpath(file.name), shallow = False)

def test_instructor(paths):

    outputPath = paths['outputDest'].joinpath('instructor/')
    comparePath = paths['compareDest'].joinpath('instructor/')

    for file in paths['inputDest'].glob('**/*'):
      if os.path.isfile(file):
          if file.name.endswith('.md'):
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            pbs.process_question_md(file, outputFolder.joinpath(file.name), instructor = True)
    
    for file in comparePath.glob('**/*'):
        isFile = os.path.isfile(file) 
        notHiddenFile = not file.name.startswith('.')
        notImageFile = not file.name.endswith('.png') 
        if isFile and notHiddenFile and notImageFile:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            assert filecmp.cmp(file, outputFolder.joinpath(file.name), shallow = False)