"""
CHD input file writer for OWHM.
Extracts constant head boundary data from a FloPy CHD package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_chd_input(chd_package, output_path):
    """
    Convert a FloPy CHD package object to an OWHM-compatible CHD input file.
    Performs input validation and provides clear error messages.
    """
    chds = getattr(chd_package, 'stress_period_data', None)
    if chds is None:
        raise ValueError("CHD package is missing 'stress_period_data'.")
    for per, chd_list in chds.items():
        for idx, chd in enumerate(chd_list):
            _require_field(chd, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(chd, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(chd, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(chd, 'shead', f'stress_period_data[{per}][{idx}]')
            _require_field(chd, 'ehead', f'stress_period_data[{per}][{idx}]')
            layer = chd['k']
            row = chd['i']
            col = chd['j']
            shead = chd['shead']
            ehead = chd['ehead']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(shead, (int, float)):
                raise ValueError(f"shead must be a number in stress_period_data[{per}][{idx}]. Got: {shead}")
            if not isinstance(ehead, (int, float)):
                raise ValueError(f"ehead must be a number in stress_period_data[{per}][{idx}]. Got: {ehead}")

    with open(output_path, 'w') as f:
        f.write('# OWHM CHD Input File (auto-generated)\n')
        # CHD block
        f.write('BEGIN CHD\n')
        f.write('  # LAYER   ROW   COL   SHEAD   EHEAD\n')
        for per, chd_list in chds.items():
            for chd in chd_list:
                layer = chd['k']
                row = chd['i']
                col = chd['j']
                shead = chd['shead']
                ehead = chd['ehead']
                f.write(f'  {layer}   {row}   {col}   {shead}   {ehead}\n')
        f.write('END CHD\n\n')
        # TODO: Add more CHD blocks as needed (with validation) 