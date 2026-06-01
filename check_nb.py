import json, sys

for name in ['trm_1step_final', 'trm_fullbp_final']:
    path = f'notebooks/{name}.ipynb'
    with open(path) as f:
        nb = json.load(f)
    
    problems = 0
    for i, cell in enumerate(nb['cells']):
        ct = cell['cell_type']
        src = cell['source']
        
        if ct == 'code':
            if not isinstance(src, list):
                print(f'{name} cell {i}: source is {type(src).__name__}, expected list')
                problems += 1
            else:
                for j, s in enumerate(src):
                    if not isinstance(s, str):
                        print(f'{name} cell {i}: source[{j}] is {type(s).__name__}')
                        problems += 1

    # Check nbformat_minor - GitHub might prefer 5
    print(f'{name}: nbformat={nb["nbformat"]}.{nb["nbformat_minor"]}, problems={problems}')

    # Look for unusual characters
    raw = json.dumps(nb)
    for ch in ['\r', '\x00', '\x01']:
        if ch in raw:
            print(f'{name}: WARNING - contains control char {repr(ch)}')
