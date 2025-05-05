"""
UZF input file writer for OWHM.
Extracts unsaturated zone flow data from a FloPy UZF package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_uzf_input(uzf_package, output_path):
    """
    Convert a FloPy UZF package object to an OWHM-compatible UZF input file.
    Performs input validation and provides clear error messages.
    """
    uzfs = getattr(uzf_package, 'stress_period_data', None)
    if uzfs is None:
        raise ValueError("UZF package is missing 'stress_period_data'.")
    for per, uzf_list in uzfs.items():
        for idx, uzf in enumerate(uzf_list):
            _require_field(uzf, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(uzf, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(uzf, 'finf', f'stress_period_data[{per}][{idx}]')
            row = uzf['i']
            col = uzf['j']
            finf = uzf['finf']
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(finf, (int, float)):
                raise ValueError(f"finf must be a number in stress_period_data[{per}][{idx}]. Got: {finf}")

    with open(output_path, 'w') as f:
        f.write('# OWHM UZF Input File (auto-generated)\n')
        # UZF block
        f.write('BEGIN UZF\n')
        f.write('  # ROW   COL   FINF\n')
        for per, uzf_list in uzfs.items():
            for uzf in uzf_list:
                row = uzf['i']
                col = uzf['j']
                finf = uzf['finf']
                f.write(f'  {row}   {col}   {finf}\n')
        f.write('END UZF\n\n')
        # TODO: Add more UZF blocks as needed (with validation) 