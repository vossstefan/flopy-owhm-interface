"""
DRT input file writer for OWHM.
Extracts drain return data from a FloPy DRT package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_drt_input(drt_package, output_path):
    """
    Convert a FloPy DRT package object to an OWHM-compatible DRT input file.
    Performs input validation and provides clear error messages.
    """
    drts = getattr(drt_package, 'stress_period_data', None)
    if drts is None:
        raise ValueError("DRT package is missing 'stress_period_data'.")
    for per, drt_list in drts.items():
        for idx, drt in enumerate(drt_list):
            _require_field(drt, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(drt, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(drt, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(drt, 'elev', f'stress_period_data[{per}][{idx}]')
            _require_field(drt, 'cond', f'stress_period_data[{per}][{idx}]')
            _require_field(drt, 'return_fraction', f'stress_period_data[{per}][{idx}]')
            layer = drt['k']
            row = drt['i']
            col = drt['j']
            elev = drt['elev']
            cond = drt['cond']
            return_fraction = drt['return_fraction']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(elev, (int, float)):
                raise ValueError(f"elev must be a number in stress_period_data[{per}][{idx}]. Got: {elev}")
            if not isinstance(cond, (int, float)):
                raise ValueError(f"cond must be a number in stress_period_data[{per}][{idx}]. Got: {cond}")
            if not isinstance(return_fraction, (int, float)) or not (0 <= return_fraction <= 1):
                raise ValueError(f"return_fraction must be a number between 0 and 1 in stress_period_data[{per}][{idx}]. Got: {return_fraction}")

    with open(output_path, 'w') as f:
        f.write('# OWHM DRT Input File (auto-generated)\n')
        # DRT block
        f.write('BEGIN DRT\n')
        f.write('  # LAYER   ROW   COL   ELEV   COND   RETURN_FRACTION\n')
        for per, drt_list in drts.items():
            for drt in drt_list:
                layer = drt['k']
                row = drt['i']
                col = drt['j']
                elev = drt['elev']
                cond = drt['cond']
                return_fraction = drt['return_fraction']
                f.write(f'  {layer}   {row}   {col}   {elev}   {cond}   {return_fraction}\n')
        f.write('END DRT\n\n')
        # TODO: Add more DRT blocks as needed (with validation) 