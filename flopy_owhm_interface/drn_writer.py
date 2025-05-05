"""
DRN input file writer for OWHM.
Extracts drain data from a FloPy DRN package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_drn_input(drn_package, output_path):
    """
    Convert a FloPy DRN package object to an OWHM-compatible DRN input file.
    This version writes basic DRN blocks, extracting what is possible from FloPy.
    Performs input validation and provides clear error messages.
    """
    drains = getattr(drn_package, 'stress_period_data', None)
    if drains is None:
        raise ValueError("DRN package is missing 'stress_period_data'.")
    for per, drain_list in drains.items():
        for idx, drain in enumerate(drain_list):
            _require_field(drain, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(drain, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(drain, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(drain, 'elevation', f'stress_period_data[{per}][{idx}]')
            _require_field(drain, 'conductance', f'stress_period_data[{per}][{idx}]')
            layer = drain['k']
            row = drain['i']
            col = drain['j']
            elevation = drain['elevation']
            conductance = drain['conductance']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(elevation, (int, float)):
                raise ValueError(f"Elevation must be a number in stress_period_data[{per}][{idx}]. Got: {elevation}")
            if not (isinstance(conductance, (int, float)) and conductance > 0):
                raise ValueError(f"Conductance must be positive in stress_period_data[{per}][{idx}]. Got: {conductance}")

    with open(output_path, 'w') as f:
        f.write('# OWHM DRN Input File (auto-generated)\n')
        # DRAINS block
        f.write('BEGIN DRAINS\n')
        f.write('  # LAYER   ROW   COL   ELEVATION   CONDUCTANCE   ETC\n')
        for per, drain_list in drains.items():
            for drain in drain_list:
                layer = drain['k']
                row = drain['i']
                col = drain['j']
                elevation = drain['elevation']
                conductance = drain['conductance']
                f.write(f'  {layer}   {row}   {col}   {elevation}   {conductance}\n')
        f.write('END DRAINS\n\n')
        # TODO: Add more DRN blocks as needed (with validation) 