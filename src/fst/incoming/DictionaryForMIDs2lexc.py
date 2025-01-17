"""Convert DictionaryForMIDs dictionary to lexc entries."""

import re
from zipfile import ZipFile

trans_table = [('á', 'a\u0301'),
               ('à$', 'a%^K'),
               ('à(?=[^aeiouáàâéèêíìîóòôúùû-])', 'a-'),
               ('à(?=[aeiouáàâéèêíìîóòôúùû-])', 'a'),
               ('â(?=[^aeiouáàâéèêíìîóòôúùû-]|$)', 'a\u0301%^K'),
               ('â(?=[aeiouáàâéèêíìîóòôúùû-])', 'a\u0301'),
               ('é', 'e\u0301'),
               ('è$', 'e%^K'),
               ('è(?=[^aeiouáàâéèêíìîóòôúùû-])', 'e-'),
               ('è(?=[aeiouáàâéèêíìîóòôúùû-])', 'e'),
               ('ê(?=[^aeiouáàâéèêíìîóòôúùû-]|$)', 'e\u0301%^K'),
               ('ê(?=[aeiouáàâéèêíìîóòôúùû-])', 'e\u0301'),
               ('í', 'i\u0301'),
               ('ì$', 'i%^K'),
               ('ì(?=[^aeiouáàâéèêíìîóòôúùû-])', 'i-'),
               ('ì(?=[aeiouáàâéèêíìîóòôúùû-])', 'i'),
               ('î(?=[^aeiouáàâéèêíìîóòôúùû-]|$)', 'i\u0301%^K'),
               ('î(?=[aeiouáàâéèêíìîóòôúùû-])', 'i\u0301'),
               ('ó', 'o\u0301'),
               ('ò$', 'o%^K'),
               ('ò(?=[^aeiouáàâéèêíìîóòôúùû-])', 'o-'),
               ('ò(?=[aeiouáàâéèêíìîóòôúùû-])', 'o'),
               ('ô(?=[^aeiouáàâéèêíìîóòôúùû-]|$)', 'o\u0301%^K'),
               ('ô(?=[aeiouáàâéèêíìîóòôúùû-])', 'o\u0301'),
               ('ú', 'u\u0301'),
               ('ù$', 'u%^K'),
               ('ù(?=[^aeiouáàâéèêíìîóòôúùû-])', 'u-'),
               ('ù(?=[aeiouáàâéèêíìîóòôúùû-])', 'u'),
               ('û(?=[^aeiouáàâéèêíìîóòôúùû-]|$)', 'u\u0301%^K'),
               ('û(?=[aeiouáàâéèêíìîóòôúùû-])', 'u\u0301')]

lines = []
with ZipFile('DictionaryForMIDs/DictionaryForMIDs_HilEng_KVED.jar') as zf:
    for fname in zf.namelist():
        if re.search(r'directory[0-9]+\.csv', fname):
            with zf.open(fname) as f:
                lines.extend(f.readlines())

# The list in `lines` is a list of strings

cc = 'ANV'  # TODO name the continuation class (this idea stands from AdjectiveNounVerb)
with open('dfm.lexc', 'w') as f:
    print('LEXICON Content', file=f)
    for line in lines:
        line = line.decode('utf8')
        stem, gloss = line.split('\t')
        new_stem = stem.split(',')[0]
        for find, replace in trans_table:
            if re.search(find, new_stem):
                print(find, replace, stem)
                new_stem = re.sub(find, replace, new_stem)
                assert not re.search(find, new_stem)
        gloss = re.sub(r'\[01([^\]]+)\]', r'\1', gloss)
        gloss = re.split(r'(?<!Sp)[!,;.]|\\n', gloss)[0].strip()
        if '[01' in gloss:
            print('DEBUG', repr(line), gloss, gloss)
        gloss = gloss.replace('"', '%"')
        print(f'{new_stem} {cc} "{gloss}" ; !!!{{{stem}}}', file=f)
