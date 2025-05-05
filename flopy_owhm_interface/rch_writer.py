"""
RCH input file writer for OWHM.
Extracts recharge data from a FloPy RCH package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_rch_input(rch_package, output_path):
    """
    Convert a FloPy RCH package object to an OWHM-compatible RCH input file.
    Performs input validation and provides clear error messages.
    """
    rchs = getattr(rch_package, 'stress_period_data', None)
    if rchs is None:
        raise ValueError("RCH package is missing 'stress_period_data'.")
    for per, rch_list in rchs.items():
        for idx, rch in enumerate(rch_list):
            _require_field(rch, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(rch, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(rch, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(rch, 'recharge', f'stress_period_data[{per}][{idx}]')
            layer = rch['k']
            row = rch['i']
            col = rch['j']
            recharge = rch['recharge']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(recharge, (int, float)):
                raise ValueError(f"recharge must be a number in stress_period_data[{per}][{idx}]. Got: {recharge}")

    with open(output_path, 'w') as f:
        f.write('# OWHM RCH Input File (auto-generated)\n')
        # RCH block
        f.write('BEGIN RCH\n')
        f.write('  # LAYER   ROW   COL   RECHARGE\n')
        for per, rch_list in rchs.items():
            for rch in rch_list:
                layer = rch['k']
                row = rch['i']
                col = rch['j']
                recharge = rch['recharge']
                f.write(f'  {layer}   {row}   {col}   {recharge}\n')
        f.write('END RCH\n\n')
        # TODO: Add more RCH blocks as needed (with validation) 