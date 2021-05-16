# Author: Firas Moosvi and Graham Bovett
# Date: 2021-05-09
# This file contains many helper functions that will be used across the question bank project.

def rounded(num, digits_after_decimal = 2):

    """
    Rounding as expected by normal sensible people.

    This needs to be heavily tested!!

    WARNING: This does not do sig figs yet!

    # TODO: flesh out this doc string, you should be ashamed Firas.

    """

    # Solution attributed to: https://stackoverflow.com/a/53329223

    if type(num) == str:
        return num
    elif type(num) == dict:
        return num
    else:
        from decimal import Decimal, getcontext, ROUND_HALF_UP

        round_context = getcontext()
        round_context.rounding = ROUND_HALF_UP

        tmp = Decimal(num).quantize(Decimal('1.'+'0'*digits_after_decimal))

        return str(tmp)

# def convert_to_md():

#     mdtext = pathlib.Path(path).read_text()

#     # Deal with YAML header
#     header_text = mdtext.rsplit('---\n')[1]
#     header = yaml.safe_load('---\n' + header_text)

#     # Deal with Markdown Body
#     body = mdtext.rsplit('---\n')[2]
    
#     # Set up the markdown parser
#     # to be honest, not fully sure what's going on here, see this issue: https://github.com/executablebooks/markdown-it-py/issues/164

#     mdit = MarkdownIt()
#     env = {}

#     # Set up tokens by parsing the md file
#     tokens = mdit.parse(body, env)

#     blocks = {}

#     block_count = 0

#     num_titles = 0

#     for x,t in enumerate(tokens):

#         if t.tag == 'h1' and t.nesting == 1: # title
#             blocks['title'] = [x,]
#             num_titles += 1

#         elif t.tag == 'h2' and t.nesting == 1:
#             block_count += 1

#             if block_count == 1:
#                 blocks['block{0}'.format(block_count)] = [x,]
#             else:
#                 blocks['block{0}'.format(block_count-1)].append(x)
#                 blocks['block{0}'.format(block_count)] = [x,]

#         #print(t,'\n')

#     # Add -1 to the end of the last block
#     blocks['block{0}'.format(block_count)].append(len(tokens))

#     # Assert statements (turn into tests!)
#     assert num_titles == 1, "I see {0} Level 1 Headers (#) in this file, there should only be one!".format(num_titles)
#     assert block_count > 1, "I see {0} Level 2 Headers (##) in this file, there should be at least 1".format(block_count -1)

#     # Add the end of the title block; # small hack
#     blocks['title'].append(blocks['block1'][0])

#     ## Process the blocks into markdown

#     body_parts = {}

#     part_counter = 0

#     for k,v in blocks.items():

#         rendered_part = MDRenderer().render(tokens[v[0]:v[1]], mdit.options, env)

#         if k == 'title':
#             body_parts['title'] = rendered_part

#         elif 'Rubric' in rendered_part:
#             body_parts['Rubric'] = rendered_part

#         elif 'Solution' in rendered_part:
#             body_parts['Solution'] = rendered_part

#         elif 'Comments' in rendered_part:
#             body_parts['Comments'] = rendered_part

#         else:
#             part_counter +=1
#             body_parts['part{0}'.format(part_counter)] = rendered_part



def dict_to_md(md_dict, remove_keys = [None,]):

    """
    Takes a dictionary, and turns it into an md file

    # TODO: flesh out this doc string, you should be ashamed Firas.
    """

    md_string = ""

    for k,v in md_dict.items():
        if k in remove_keys:
            continue
        else:
            md_string += md_dict[k]

    return md_string