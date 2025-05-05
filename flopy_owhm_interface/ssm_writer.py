"""
SSM input file writer for OWHM.
Extracts source and sink mixing data from a FloPy SSM package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_ssm_input(ssm_package, output_path):
    """
    Convert a FloPy SSM package object to an OWHM-compatible SSM input file.
    Performs input validation and provides clear error messages.
    """
    ssms = getattr(ssm_package, 'stress_period_data', None)
    if ssms is None:
        raise ValueError("SSM package is missing 'stress_period_data'.")
    for per, ssm_list in ssms.items():
        for idx, ssm in enumerate(ssm_list):
            _require_field(ssm, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(ssm, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(ssm, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(ssm, 'itype', f'stress_period_data[{per}][{idx}]')
            _require_field(ssm, 'c', f'stress_period_data[{per}][{idx}]')
            layer = ssm['k']
            row = ssm['i']
            col = ssm['j']
            itype = ssm['itype']
            c = ssm['c']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(itype, int):
                raise ValueError(f"itype must be an integer in stress_period_data[{per}][{idx}]. Got: {itype}")
            if not isinstance(c, (int, float)):
                raise ValueError(f"c must be a number in stress_period_data[{per}][{idx}]. Got: {c}")

    with open(output_path, 'w') as f:
        f.write('# OWHM SSM Input File (auto-generated)\n')
        # SSM block
        f.write('BEGIN SSM\n')
        f.write('  # LAYER   ROW   COL   ITYPE   C\n')
        for per, ssm_list in ssms.items():
            for ssm in ssm_list:
                layer = ssm['k']
                row = ssm['i']
                col = ssm['j']
                itype = ssm['itype']
                c = ssm['c']
                f.write(f'  {layer}   {row}   {col}   {itype}   {c}\n')
        f.write('END SSM\n\n')
        # TODO: Add more SSM blocks as needed (with validation) 