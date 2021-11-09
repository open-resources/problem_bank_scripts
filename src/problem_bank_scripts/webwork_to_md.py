"""
@Author:     Parsa Rajabi (@parsa-rajabi)
@Created:    2021
@Description: Converts webwork files from .PL to markdown .MD

Usage:
    webwork_to_md.py <source_path> <destination_path>

Arguments:
    source_path                     Path to root of all the pl source files.
    destination_path                Path to destination of all md output files.
"""
import os
from pathlib import Path
from pprint import pprint
import yaml
import re
import time
from shutil import copy2
import sys
import logging
from docopt import docopt

logging.basicConfig(filename='Webwork_to_md_logs.log', level=logging.INFO)
logging.info('Started Session')

# read passed in arguments
args = docopt(__doc__)
# set source_path with passed in path
source_path = args['<source_path>']
destination_path = args['<destination_path>']

# variable declaration
counter = 0
source_files = []
title = topic = author = editor = date = source = template_version = problem_type = attribution = outcomes = difficulty = randomization = taxonomy = ""
tags = assets = altText = image_line = []
total_start_time = time.process_time()

# Variable declaration for Webwork keywords
metadata_end_src = "DOCUMENT();"
marcos_end_src = "TEXT(beginproblem());"
variables_start_src = "showHint"
problem_body_start_src = "BEGIN_TEXT"
problem_body_end_src = "END_TEXT"
hint_start_src = "BEGIN_HINT"
hint_end_src = "END_HINT"
ans_rule_src = "ans_rule"
ans_src = "ANS"
hint_src = "hint"
image_src = "image"
context_src = "Context"
partial_answer_src = "showPartialCorrectAnswers"


def sanitize_file_path(file_path):
    """
    description: sanitizes the file path to ensure it has a trailing slash at the end
    @param file_path:
    @return: file_path with trailing backslash
    """
    # check if file_path doesn't end with a backslash
    if file_path and file_path[-1] != '/':
        # Add backslash to end of file_path
        file_path += "/"
    return file_path


def split_file(file_content):
    """
    description: splits the file into sections based on the keywords
    @param file_content:
    @return: dictionary of lists that contain problem parts
    """
    # TODO: once all functions are completed, convert global variables above into local variables
    # split the file into bite-size pieces to increase speed and reduce bugs
    metadata_content = file_content[:file_content.find(metadata_end_src)]
    macros = file_content[file_content.find(metadata_end_src):file_content.find(marcos_end_src)]
    question_variables = file_content[file_content.find(marcos_end_src):file_content.find(problem_body_start_src)]
    question_body = [file_content[file_content.find(problem_body_start_src):file_content.rfind(problem_body_end_src)]]
    question_ans = re.findall(r"ANS(\(.+?[?<!)]\));", file_content)
    question_hint = [file_content[file_content.find(hint_start_src):file_content.find(hint_end_src)]]
    question_solution = [file_content[file_content.find(marcos_end_src):file_content.find(problem_body_start_src)]]
    return {'metadata': metadata_content,
            'macros': macros,
            'question_variables': question_variables,
            'question_body': question_body,
            'question_ans': question_ans,
            'question_solution': question_solution,
            'question_hint': question_hint}


def metadata_extract(metadata_content):
    """
    description: extracts metadata variables from the metadata section of the file
    @param metadata_content:
    @return: dictionary of metadata
    """
    metadata = "## "
    chapter_src = "DBchapter"
    section_src = "DBsection"
    author_src = "AuthorText1"
    editor_src = "Editor"
    keywords_src = "KEYWORDS"
    date_src = "Date"

    title_ = topic_ = author_ = editor_ = tags_ = date_ = None

    # Look for keywords declared above and extract them from metadata content
    for item in metadata_content.split("\n"):
        if metadata + chapter_src in item:
            title_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
        if metadata + section_src in item:
            topic_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
        if metadata + author_src in item:
            author_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
        if metadata + editor_src in item:
            editor_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
        else:
            editor_ = 'N/A'
        if keywords_src in item:
            tags_ = item[12:-1].replace("'", "").replace('"', '').strip().split(',')
        if metadata + date_src in item:
            date_ = item[item.find("(") + 1:item.find(")")].replace("'", "")
    return {'title': title_,
            'topic': topic_,
            'author': author_,
            'editor': editor_,
            'tags': tags_,
            'date': date_}


def determine_problem_type(question_ans, filename):
    """
    description: determines the type of problem
    @param question_ans:
    @param filename:
    @return: dictionary of problem type
    """
    # determine what type of question is based on the ANS(type)
    numerical_type = "num_cmp"
    functional_type = "fun_cmp"
    checkbox_type = "checkbox_cmp"
    text_type = "str_cmp"
    question_type = []

    # extracts answer variable from ANS(num_cmp("variable"))
    answer_variable = re.findall(r'"\$([^"]*)"', str(question_ans))
    # extracts problem type from ANS i.e num_cmp, fun_cmp etc.
    answer_type_raw = re.findall(r'\((.*?)\(', str(question_ans))

    # determine answer type based on the raw answer from question
    for answer_type in answer_type_raw:
        if numerical_type in answer_type:
            question_type.append("number-input")
        elif functional_type in answer_type:
            question_type.append("functional")
        elif checkbox_type in answer_type:
            question_type.append("checkbox")
        elif text_type in answer_type:
            question_type.append("text")
        else:
            question_type.append("unknown")

    if not question_type:
        question_type.append("unknown")

    return {
        'answer_variable': answer_variable,
        'answer_type_raw': answer_type_raw,
        'question_type': question_type,
        'filename': filename}


def server(question_solution):
    """
    description: function bundles up the problem's solution in python code
    @param question_solution:
    @return: dictionary of server containing various elements such as import, generate and prepare.
    """
    # server variables
    server_imports = """
import random
import problem_bank_helpers as pbh
""".strip('\n')
    server_generate_names = "# TBD"
    server_generate_phrases = "# TBD"
    server_generate_random_var = "# N/A"
    if len(question_solution) > 0:
        server_generate_random_var = ''.join(f'# {solution.replace("$","").replace("**", "E").strip()}\n' for solution in question_solution)
    server_generate_dic = "# TBD"
    server_generate_answers = "# TBD"
    server_generate = f"""data2 = pbh.create_data2()\n# define or load names/items/objects from server files\n{server_generate_names}\n# store phrases etc\n{server_generate_phrases}\n# Randomize Variables\n{server_generate_random_var}\n# store the variables in the dictionary params\n{server_generate_dic}\n# define possible answers\n{server_generate_answers}\n# Update the data object with a new dict\ndata.update(data2)"""
    server_prepare = """pass
"""
    server_parse = """pass
"""
    server_grade = """pass
"""
    return {'imports': server_imports,
            'generate': server_generate,
            'prepare': server_prepare,
            'parse': server_parse,
            'grade': server_grade}


def yaml_dump(directory_info, metadata, question_format, image_dic, question_text, question_units, question_parts, question_solution, destination_file_path):
    """
    description: all problem sections are bundled up and dumped into a markdown file (created)
    @param directory_info:
    @param metadata:
    @param question_format:
    @param image_dic:
    @param question_text:
    @param question_units:
    @param question_parts:
    @param question_solution:
    @param destination_file_path:
    @return: none
    """
    # This solution is copied from this SO answer: https://stackoverflow.com/a/45004775/2217577
    yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

    def repr_str(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
        return dumper.org_represent_str(data)

    yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

    source = f"https://github.com/open-resources/webwork-open-problem-library/tree/master/{directory_info['file_dir']}"
    yaml_dict = {}

    # populate yaml_dic with values from args
    yaml_dict['title'] = metadata['title']
    yaml_dict['topic'] = metadata['topic']
    yaml_dict['author'] = metadata['author']
    #yaml_dict['date'] = metadata['date']
    yaml_dict['source'] = source
    yaml_dict['template_version'] = 1.3
    yaml_dict['attribution'] = 'standard'
    yaml_dict['partialCredit'] = 'true'
    yaml_dict['singleVariant'] = 'false'
    #yaml_dict['editor'] = metadata['editor']
    # yaml_dict['type'] = question_type['question_type']
    yaml_dict['outcomes'] = ['TBD']
    yaml_dict['difficulty'] = ['TBD']
    yaml_dict['randomization'] = ['TBD']
    yaml_dict['taxonomy'] = ['TBD']
    yaml_dict['span'] = ['TBD']
    yaml_dict['length'] = ['TBD']
    yaml_dict['tags'] = metadata['tags']
    yaml_dict['assets'] = image_dic['image_name'] if image_dic['image_name'] else ''
    for image in image_dic['image_name']:
        image_dir = directory_info['folder_dir'] + "/" + image
        image_path = Path(directory_info['folder_dir'] + "/" + image)
        if image_path.is_file():
            copy2(image_dir, destination_file_path)
    yaml_dict['server'] = server(question_solution)
    for part_number, part_type in zip(question_parts, question_format):
        if part_number + 1 == 0:
            part_number = str(part_number+2)
        else:
            part_number = str(part_number+1)
        yaml_dict['part' + part_number] = get_part_type(part_type)
    question_images = image_dic['image_line_md']
    Path(destination_file_path + directory_info['filename'] + ".md").write_text('---\n'
                                                                                + yaml.safe_dump(yaml_dict, sort_keys=False)
                                                                                + '---\n\n'
                                                                                + '# {{ params.vars.title }} \n\n'
                                                                                + ''.join(f'{image}\n' for image in question_images)
                                                                                + ''.join(f'\n{question}\n' for part, question in zip(question_parts, question_text) if (part == 0))
                                                                                + ''.join(f'\n## Part {part} \n{question} \n\n\n ### Answer Section\n' for part, question in zip(question_parts, question_text) if (part > 0))
                                                                                + str(question_units) + '\n\n'
                                                                                + '## pl-submission-panel \n\n\n'
                                                                                + '## pl-answer-panel \n\n\n'
                                                                                + '## Rubric \n\n\n'
                                                                                + '## Solution \n\n\n'
                                                                                + '## Comments \n\n\n')
                                                                                # + ''.join(f'{value}' for key, value in section.items())


def get_part_type(part_type):
    """
    description: determines the type of each question part
    @param part_type:
    @return: dictionary containing type of question i.e numerical, text, etc.
    """
    return {"type": part_type,
            "pl-customizations":
                {"weight": "1",
                 "hide-answer-panel": "true"}
            }


def image_extract(question_content):
    """
    description: extracts images from question content
    @param question_content:
    @return: dictionary containing image name and image alt text and image line containing both
    """
    image_src = "image("
    image_line = []
    image_alt_text = []
    image_name = []

    # iterate through each question part in the questions
    for question_part in question_content:
        # determine if the question contains an image
        if image_src in question_part:
            # extract image name and alt text using regex
            image_name = re.findall(' "(.+?)"', str(question_content).strip())
            image_alt_text = re.findall('="(.+?)"', str(question_content).strip())

    # bundle up the image name and alt text to create a .md image line
    for image_alt, image_filename in zip(image_alt_text, image_name):
        if image_alt:
            image_line.append('![' + image_alt.strip() + '](' + image_filename + ')')
        else:
            image_line.append('![](' + image_filename + ')')

    return {'image_name': image_name,
            'image_alt_text': image_alt_text,
            'image_line_md': image_line}


def problem_extract(question_body, image_alt_text):
    """
    description: extracts the question text, parts and units from the question body
    @param question_body:
    @param image_alt_text:
    @return: dictionary containing question text, parts and units
    """
    hint = ''
    question_units = ''
    question_raw = []
    question_split = ''
    part_headers = []
    question_part = []

    # split question into sections based on "$PAR"
    for question in question_body:
        question_split = question.split('$PAR\n')

    # for each section of the question
    for question_section in question_split:
        # if the section is not empty
        if len(question_section) > 0:
            # remote all the \n in the section
            section_clean = question_section.replace('\n', '')
            # find and assign hint (if it exits)
            if section_clean.endswith('</strong>') or section_clean.endswith('</b>'):
                hint = section_clean
            # if hint has not been assigned (no hint exists) OR section does NOT include hint
            if not hint or hint not in section_clean:
                subsection = help_problem_extract_ans_units(section_clean)
                subsection_text = subsection['section']
                question_units = subsection['final_ans_units']
                subsection_multi_part = help_problem_extract_ans_type(subsection_text)
                subsection_multi_part_ans_type = subsection_multi_part['ans_type']
                subsection_clean = subsection_multi_part['problem_clean']
                question_raw = help_problem_extract_append(subsection_clean, question_raw)
                # remove image_alt_text from question_raw and ensure there are no empty questions
                question_raw = [question for question in question_raw if question not in image_alt_text and question]
                question_part = append_part_counter(len(question_raw)-1, part_headers)

    return {'question_text': question_raw,
            'question_parts': question_part,
            'question_units': question_units}


def append_part_counter(part_counter, part_headers):
    """
    description: outputs the unique question parts
    @param part_counter:
    @param part_headers:
    @return: unique part counter
    """
    if part_counter not in part_headers:
        part_headers.append(part_counter)
    return part_headers


def extract_problem_type(problem_subsection, filename):
    """
    description: extracts the problem solution type from each problem  subsection
    @param problem_subsection:
    @param filename:
    @return: extract problem format and then call the determine_problem_type function
    """
    question_format_raw = re.findall("(ANS\(.+?\);)", str(problem_subsection))
    return determine_problem_type(question_format_raw, filename)


def help_problem_extract_ans_units(problem_subsection):
    """
    description: extracts the final answer units and each section of the question
    @param problem_subsection:
    @return: dictionary containing question sections and final answer units
    """
    final_ans_units = ''
    section_clean = ''
    if not problem_subsection.startswith("\\{ image") and not problem_subsection.endswith(") \\}"):
        # if section is the end i.e. ans_rule (determines the length of the answer)
        if problem_subsection.startswith("\\{ans_rule") and problem_subsection.endswith("\\)"):
            # extract the question units using regex
            final_ans_units = re.findall('textrm{(.+?)}', problem_subsection)
        if not problem_subsection.startswith("\\{ans_rule") and not problem_subsection.endswith("\\)"):
            section_clean = problem_subsection
    return {'section': section_clean,
            'final_ans_units': final_ans_units}


def help_problem_extract_ans_type(problem_subsection):
    """
    description: extracts the question's answer type and returns the problem text without the answer type
    @param problem_subsection:
    @return: return dictionary containing question answer type and problem text without answer type
    """
    ans_type = []
    problem_ans_type_removed = []
    if problem_subsection.startswith("END_TEXT"):
        ans_type = re.search(r"END_TEXT(.*)BEGIN_TEXT", str(problem_subsection))
        problem_ans_type_removed = re.sub(r"END_TEXT(.*)BEGIN_TEXT", "", str(problem_subsection))
    else:
        problem_ans_type_removed = problem_subsection

    return {'ans_type': ans_type,
            'problem_clean': problem_ans_type_removed}


def help_problem_extract_append(problem_subsection, final_dic):
    """
    description: extracts the question text clean of any PEAL syntax and appends it to the final dictionary
    @param problem_subsection:
    @param final_dic:
    @return: list that contains clean problems without any PEARL syntax in them
    """
    if len(problem_subsection) > 1:
        problem_stripped = problem_subsection.replace('\\', '').replace('textrm', '').replace('{', '').replace('}', '')\
            .replace('&middot;', '$\\cdot$').replace('END_TEXT', '').replace('BEGIN_TEXT', '').strip()
        if re.match(r'.\) ', problem_stripped):
            subsection_without_part_num = problem_stripped[3:]
            final_dic.append(subsection_without_part_num)
        else:
            final_dic.append(problem_stripped)

    return final_dic


def extract_problem_solution(problem_solution):
    """
    description: extracts the problem solution from the problem solution subsection
    @param problem_solution:
    @return: list containing problem solution
    """
    question_solution = []

    for solution in problem_solution:
        split_solution = solution.split('\n')

        for solution_part in split_solution:
            if len(solution_part) > 0:
                # removes lines with showPartialCorrectAnswers and showHint
                if partial_answer_src not in solution_part and variables_start_src not in solution_part:
                    # removes lines with Context and TEXT(beginproblem());
                    if context_src not in solution_part and marcos_end_src not in solution_part:
                        question_solution.append(solution_part)

    return question_solution


def progress(count, total, status=''):
    """
    description: prints a dynamic progress bar source: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
    @param count:
    @param total:
    @param status:
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s -- %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

# -------------------------------------------------------------------------------------------------------------------- #


# sanitize source path to ensure it has a trailing backslash
source_path = sanitize_file_path(source_path)
# set root destination folder
root_dest_folder = sanitize_file_path(destination_path) + 'source/' + source_path.split('/')[-2] + '/'
# Create root_dest_folder if it doesn't exist
Path(root_dest_folder).mkdir(parents=True, exist_ok=True)

# iterate through all the files and dirs in the source directory
for root, dirs, files in os.walk(source_path):
    # iterate through all the files in the current directory
    for name in dirs:
        dest_folder = os.path.join(root, name).removeprefix(source_path)
        # create dest file structure based on source directory
        Path(root_dest_folder + dest_folder).mkdir(parents=True, exist_ok=True)
    # iterate through each file
    for file in files:
        # if file is a .pg file (PEAL)
        if file.endswith('.pg'):
            # add file path to source_files list
            source_files.append(os.path.join(root, file))

# iterate through every .pg file found in the source directory
for source_filepath in source_files:
    try:
        # start timer for processing file
        file_start_time = time.process_time()
        # extract and build information directory
        dest_file_path = source_filepath[:source_filepath.rfind('/')].removeprefix(source_path)
        filename = source_filepath[source_filepath.rfind('/')+1:-3]
        folder_dir = source_filepath[:source_filepath.rfind('/')]
        file_dir = source_filepath[source_filepath.find("Contrib"):]
        """ 
        Example of dir_info output
        {
        'filename': 'NU_U17-33-02-002',
        'file_dir': 'Contrib/BrockPhysics/College_Physics_Urone/33.Particle_Physics/33-02.Four_Basic_Forces/NU_U17-33-02-002.pg',
        'folder_dir': '../../../webwork-open-problem-library/Contrib/BrockPhysics/College_Physics_Urone/33.Particle_Physics/33-02.Four_Basic_Forces',
        'root_dest_folder': 'source/College_Physics_Urone/',
        'dest_file_path': '33.Particle_Physics/33-02.Four_Basic_Forces'
        }
        """
        dir_info = {
            'filename': filename,
            'file_dir': file_dir,
            'folder_dir': folder_dir,
            'root_dest_folder': root_dest_folder,
            'dest_file_path': dest_file_path
        }
        # each question has a its own unique folder named after the fiile itself i.e question file NU_123.md is within NU_123 folder
        destination_file_path = root_dest_folder + dest_file_path + "/" + filename + "/"
        Path(destination_file_path).mkdir(parents=True, exist_ok=True)
        # open and read question file
        question_file = open(source_filepath, 'r')
        file_contents = question_file.read()
        # split content of the question file into sections
        file_contents_dic = split_file(file_contents)
        # extract metadata from the question file
        metadata_dic = metadata_extract(file_contents_dic['metadata'])
        # extract question body from the question file
        question_body = file_contents_dic['question_body']
        # extract question images from the question body
        image_dic = image_extract(question_body)
        # extract question item such as text, part #s, units from the question body
        question_extract = problem_extract(question_body, image_dic['image_alt_text'])
        question_text = question_extract['question_text']
        question_parts = question_extract['question_parts']
        question_units = question_extract['question_units']
        # determine question type
        question_formats = extract_problem_type(file_contents, dir_info['filename'])['question_type']
        # extract question solution from the question content
        question_solution = extract_problem_solution(file_contents_dic['question_solution'])
        # send all dictionaries to yaml_dump to create yaml files
        yaml_dump(dir_info, metadata_dic, question_formats, image_dic, question_text,
                  question_units, question_parts, question_solution, destination_file_path)
        # end timer for processing file
        end_file_time = time.process_time()
        # calculate total time for processing file
        file_process_time = end_file_time - file_start_time
        # print/update progress bar
        counter += 1
        progress(counter, len(source_files), status="Files Processed: " + str(counter) + "/" + str(len(source_files)))
    except Exception as e:
        print(e)
        logging.error('Error: ' + str(e))
        pass

# ------------------------ STATS ------------------------ #
total_end_time = time.process_time()
process_time_seconds = total_end_time - total_start_time
print('\n---')
print('total time:', round(process_time_seconds / 60, 2), 'minutes,', round(process_time_seconds, 2), 'seconds')
print('avg time per each file:', round(process_time_seconds / counter, 2), 'seconds [', counter, '] files')
logging.info('Session Completed')
