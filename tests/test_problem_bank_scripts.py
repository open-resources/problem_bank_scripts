from problem_bank_scripts import __version__
from src.problem_bank_scripts import problem_bank_scripts as pbs
import pandas as pd
import pathlib  
import filecmp
import os
import pytest

def test_version():
    assert __version__ == '0.3.1'

@pytest.fixture(scope="session", autouse= True)
def add_random_seed(paths):
    for file in paths['inputDest'].glob('**/*.md'):
        read_file = file.read_text(encoding='utf8')
        read_file.replace('import random','import random; random.seed(111)')
        file.write_text(read_file,encoding='utf8')
    return

@pytest.fixture(scope="session")
def paths():
    p = {
        'inputDest': pathlib.Path('tests/test_question_templates/question_inputs/'),
        'outputDest': pathlib.Path('tests/test_question_templates/question_generated_outputs/'),
        'compareDest': pathlib.Path('tests/test_question_templates/question_expected_outputs/')
    }
    return p

exclude_question = "symbolic-input" # TODO: excluding symbolic questions, needs to be fixed

def test_prairie_learn(paths):

    outputPath = paths['outputDest'].joinpath('prairielearn/')
    comparePath = paths['compareDest'].joinpath('prairielearn/')

    for file in paths['inputDest'].glob('**/*.md'):
        if file.name not in exclude_question:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            pbs.process_question_pl(file, outputFolder.joinpath(file.name))

    for file in comparePath.glob('**/*'):
        isFile = os.path.isfile(file) 
        notHiddenFile = not file.name.startswith('.')
        notImageFile = not file.name.endswith('.png') 
        notExcludedFile = not (file.parent.name in exclude_question)

        if isFile and notHiddenFile and notImageFile and notExcludedFile:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            assert filecmp.cmp(file, outputFolder.joinpath(file.name), shallow = False)

def test_public(paths):

    outputPath = paths['outputDest'].joinpath('public/')
    comparePath = paths['compareDest'].joinpath('public/')

    for file in paths['inputDest'].glob('**/*.md'):
      if file.name not in exclude_question:
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

    outputPath = paths['outputDest'].joinpath('instructor/') # the path to where the newly generated file will be stored
    comparePath = paths['compareDest'].joinpath('instructor/') # the path to where the existing files to be compared are stored

    for file in paths['inputDest'].glob('**/*.md'):
        if file.name not in exclude_question:
            folder = file.parent.name
            outputFolder = outputPath.joinpath(folder)
            pbs.process_question_md(file, outputFolder.joinpath(file.name), instructor = True)

    for file in comparePath.glob('**/*'):
        isFile = os.path.isfile(file) 
        notHiddenFile = not file.name.startswith('.')
        notImageFile = not file.name.endswith('.png')
        notExcludedFile = not (file.parent.name in exclude_question)

        if isFile and notHiddenFile and notImageFile and notExcludedFile:
            folder = file.parent.name
            outputFoldepir = outputPath.joinpath(folder)
            assert filecmp.cmp(file, outputFolder.joinpath(file.name), shallow = False)
