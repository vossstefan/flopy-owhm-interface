"""
RIV input file writer for OWHM.
Extracts river boundary data from a FloPy RIV package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_riv_input(riv_package, output_path):
    """
    Convert a FloPy RIV package object to an OWHM-compatible RIV input file.
    Performs input validation and provides clear error messages.
    """
    rivs = getattr(riv_package, 'stress_period_data', None)
    if rivs is None:
        raise ValueError("RIV package is missing 'stress_period_data'.")
    for per, riv_list in rivs.items():
        for idx, riv in enumerate(riv_list):
            _require_field(riv, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(riv, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(riv, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(riv, 'stage', f'stress_period_data[{per}][{idx}]')
            _require_field(riv, 'cond', f'stress_period_data[{per}][{idx}]')
            _require_field(riv, 'rbot', f'stress_period_data[{per}][{idx}]')
            layer = riv['k']
            row = riv['i']
            col = riv['j']
            stage = riv['stage']
            cond = riv['cond']
            rbot = riv['rbot']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(stage, (int, float)):
                raise ValueError(f"stage must be a number in stress_period_data[{per}][{idx}]. Got: {stage}")
            if not isinstance(cond, (int, float)):
                raise ValueError(f"cond must be a number in stress_period_data[{per}][{idx}]. Got: {cond}")
            if not isinstance(rbot, (int, float)):
                raise ValueError(f"rbot must be a number in stress_period_data[{per}][{idx}]. Got: {rbot}")

    with open(output_path, 'w') as f:
        f.write('# OWHM RIV Input File (auto-generated)\n')
        # RIV block
        f.write('BEGIN RIV\n')
        f.write('  # LAYER   ROW   COL   STAGE   COND   RBOT\n')
        for per, riv_list in rivs.items():
            for riv in riv_list:
                layer = riv['k']
                row = riv['i']
                col = riv['j']
                stage = riv['stage']
                cond = riv['cond']
                rbot = riv['rbot']
                f.write(f'  {layer}   {row}   {col}   {stage}   {cond}   {rbot}\n')
        f.write('END RIV\n\n')
        # TODO: Add more RIV blocks as needed (with validation) 