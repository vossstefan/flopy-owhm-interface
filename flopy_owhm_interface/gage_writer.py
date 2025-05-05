"""
GAGE input file writer for OWHM.
Extracts gage data from a FloPy GAGE package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_gage_input(gage_package, output_path):
    """
    Convert a FloPy GAGE package object to an OWHM-compatible GAGE input file.
    Performs input validation and provides clear error messages.
    """
    gages = getattr(gage_package, 'stress_period_data', None)
    if gages is None:
        raise ValueError("GAGE package is missing 'stress_period_data'.")
    for per, gage_list in gages.items():
        for idx, gage in enumerate(gage_list):
            _require_field(gage, 'unit', f'stress_period_data[{per}][{idx}]')
            _require_field(gage, 'outtype', f'stress_period_data[{per}][{idx}]')
            unit = gage['unit']
            outtype = gage['outtype']
            if not isinstance(unit, int) or unit <= 0:
                raise ValueError(f"unit must be a positive integer in stress_period_data[{per}][{idx}]. Got: {unit}")
            if not isinstance(outtype, int) or outtype < 0:
                raise ValueError(f"outtype must be a non-negative integer in stress_period_data[{per}][{idx}]. Got: {outtype}")

    with open(output_path, 'w') as f:
        f.write('# OWHM GAGE Input File (auto-generated)\n')
        # GAGE block
        f.write('BEGIN GAGE\n')
        f.write('  # UNIT   OUTTYPE\n')
        for per, gage_list in gages.items():
            for gage in gage_list:
                unit = gage['unit']
                outtype = gage['outtype']
                f.write(f'  {unit}   {outtype}\n')
        f.write('END GAGE\n\n')
        # TODO: Add more GAGE blocks as needed (with validation) 