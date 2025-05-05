"""
GHB input file writer for OWHM.
Extracts general-head boundary data from a FloPy GHB package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_ghb_input(ghb_package, output_path):
    """
    Convert a FloPy GHB package object to an OWHM-compatible GHB input file.
    Performs input validation and provides clear error messages.
    """
    ghbs = getattr(ghb_package, 'stress_period_data', None)
    if ghbs is None:
        raise ValueError("GHB package is missing 'stress_period_data'.")
    for per, ghb_list in ghbs.items():
        for idx, ghb in enumerate(ghb_list):
            _require_field(ghb, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(ghb, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(ghb, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(ghb, 'bhead', f'stress_period_data[{per}][{idx}]')
            _require_field(ghb, 'cond', f'stress_period_data[{per}][{idx}]')
            layer = ghb['k']
            row = ghb['i']
            col = ghb['j']
            bhead = ghb['bhead']
            cond = ghb['cond']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(bhead, (int, float)):
                raise ValueError(f"bhead must be a number in stress_period_data[{per}][{idx}]. Got: {bhead}")
            if not (isinstance(cond, (int, float)) and cond > 0):
                raise ValueError(f"cond must be positive in stress_period_data[{per}][{idx}]. Got: {cond}")

    with open(output_path, 'w') as f:
        f.write('# OWHM GHB Input File (auto-generated)\n')
        # GHB block
        f.write('BEGIN GHB\n')
        f.write('  # LAYER   ROW   COL   BHEAD   COND   ETC\n')
        for per, ghb_list in ghbs.items():
            for ghb in ghb_list:
                layer = ghb['k']
                row = ghb['i']
                col = ghb['j']
                bhead = ghb['bhead']
                cond = ghb['cond']
                f.write(f'  {layer}   {row}   {col}   {bhead}   {cond}\n')
        f.write('END GHB\n\n')
        # TODO: Add more GHB blocks as needed (with validation) 