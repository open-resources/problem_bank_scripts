import base64 
import problem_bank_helpers as pbh

def imports(data):
    import base64 
    import problem_bank_helpers as pbh
    
def generate(data):
    data2 = pbh.create_data2()
    
    data2["params"]["vars"]["title"] = "Moving and copying files"
    
    # Update the data object with a new dict
    data.update(data2)
    
def grade(data):
    files = { f['name']: f['contents'] for f in data['submitted_answers'].get('_files', []) }
    data['feedback']['results'] = []
    data['score'] = 0
    
    with open('workspace/file1.txt', 'rb') as f:
        file1_content = base64.b64encode(f.read()).decode()
    with open('workspace/file2.txt', 'rb') as f:
        file2_content = base64.b64encode(f.read()).decode()
    
    if 'newdir/file1_new.txt' not in files:
        data['feedback']['results'].append('newdir/file1_new.txt was not created.')
    elif files['newdir/file1_new.txt'] != file1_content:
        data['feedback']['results'].append('newdir/file1_new.txt was created, but it is not based on file1.txt.')
    elif 'file1.txt' in files:
        data['feedback']['results'].append('newdir/file1_new.txt was created properly, but the old file still exists.')
        data['score'] += 0.2
    else:
        data['feedback']['results'].append('file1.txt moved successfully.')
        data['score'] += 0.4
    
    if 'newdir/file2_new.txt' not in files:
        data['feedback']['results'].append('newdir/file2_new.txt was not created.')
    elif files['newdir/file2_new.txt'] != file2_content:
        data['feedback']['results'].append('newdir/file2_new.txt was created, but it is not based on file2.txt.')
    elif 'file2.txt' not in files:
        data['feedback']['results'].append('newdir/file2_new.txt was created properly, but the old file no longer exists.')
        data['score'] += 0.2
    else:
        data['feedback']['results'].append('file2.txt copied successfully.')
        data['score'] += 0.4
    
    if files and 'filebad.txt' in files:
        data['feedback']['results'].append('filebad.txt still exists.')
    else:
        data['feedback']['results'].append('filebad.txt deleted successfully.')
        data['score'] += 0.2
    
def prepare(data):
    pass
    
def parse(data):
    if '_files' in data['format_errors']:
        del data['format_errors']['_files']
    
