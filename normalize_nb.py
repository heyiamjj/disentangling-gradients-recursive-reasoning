import json, sys

for name in ['trm_1step_final', 'trm_fullbp_final']:
    path = f'notebooks/{name}.ipynb'
    with open(path, 'r') as f:
        nb = json.load(f)
    
    fixed = 0
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            if 'outputs' not in cell:
                cell['outputs'] = []
                fixed += 1
            if 'execution_count' not in cell:
                cell['execution_count'] = None
                fixed += 1
    
    json_str = json.dumps(nb, indent=1, ensure_ascii=False)
    json_str = json_str.replace('\r\n', '\n')
    with open(path, 'w', newline='\n') as f:
        f.write(json_str)
        f.write('\n')
    print(f'{name}: added outputs/execution_count to {fixed} fields')

# Verify with nbformat
import nbformat
for name in ['trm_1step_final', 'trm_fullbp_final']:
    path = f'notebooks/{name}.ipynb'
    try:
        nb = nbformat.read(path, as_version=4)
        import io
        nbformat.write(nb, io.StringIO())
        print(f'{name}: nbformat round-trip OK')
    except Exception as e:
        print(f'{name}: ERROR - {e}')
