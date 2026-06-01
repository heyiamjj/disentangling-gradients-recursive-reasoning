import json, uuid, os

for name in ['trm_1step_final', 'trm_fullbp_final']:
    path = f'notebooks/{name}.ipynb'
    
    with open(path) as f:
        nb = json.load(f)
    
    # Add cell IDs (required by nbformat 5.x / GitHub renderer)
    for cell in nb['cells']:
        if 'id' not in cell or cell['id'] == '':
            cell['id'] = str(uuid.uuid4())[:8]
    
    # Bump minor version
    nb['nbformat_minor'] = 5
    
    # Write with LF endings
    json_str = json.dumps(nb, indent=1, ensure_ascii=False)
    json_str = json_str.replace('\r\n', '\n')
    with open(path, 'w', newline='\n') as f:
        f.write(json_str)
        f.write('\n')
    
    print(f'{name}: added cell IDs, bumped to nbformat 4.5, LF endings')

# Verify with nbformat
import nbformat as nbf
for name in ['trm_1step_final', 'trm_fullbp_final']:
    path = f'notebooks/{name}.ipynb'
    nb = nbf.read(path, as_version=4)
    for cell in nb.cells:
        assert cell.get('id'), f'{name}: cell missing id'
    print(f'{name}: nbformat validation OK ({len(nb.cells)} cells, all have IDs)')
