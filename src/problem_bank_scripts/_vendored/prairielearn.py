# See https://github.com/PrairieLearn/PrairieLearn/blob/9e0914d484d0c00bd58b9ee2fc0d9a4b15e8d936/apps/prairielearn/python/prairielearn.py#L1810C1-L1812C55 for source
# Instead of also vendoring that file, I just copied the function here, to avoid pulling in a GPL-licensed requirement for a MIT-licensed project

def full_unidecode(input_str: str) -> str:
    return input_str.replace("\u2212", "-")

def __getattr__(name: str):
    return lambda *args, **kwargs: None