"""
RES input file writer for OWHM.
Extracts reservoir data from a FloPy RES package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_res_input(res_package, output_path):
    """
    Convert a FloPy RES package object to an OWHM-compatible RES input file.
    This version writes basic RES blocks, extracting what is possible from FloPy.
    Performs input validation and provides clear error messages.
    """
    reservoirs = getattr(res_package, 'stress_period_data', None)
    if reservoirs is None:
        raise ValueError("RES package is missing 'stress_period_data'.")
    for per, res_list in reservoirs.items():
        for idx, res in enumerate(res_list):
            _require_field(res, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(res, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(res, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(res, 'stage', f'stress_period_data[{per}][{idx}]')
            _require_field(res, 'area', f'stress_period_data[{per}][{idx}]')
            layer = res['k']
            row = res['i']
            col = res['j']
            stage = res['stage']
            area = res['area']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(stage, (int, float)):
                raise ValueError(f"Stage must be a number in stress_period_data[{per}][{idx}]. Got: {stage}")
            if not (isinstance(area, (int, float)) and area > 0):
                raise ValueError(f"Area must be positive in stress_period_data[{per}][{idx}]. Got: {area}")

    with open(output_path, 'w') as f:
        f.write('# OWHM RES Input File (auto-generated)\n')
        # RESERVOIRS block
        f.write('BEGIN RESERVOIRS\n')
        f.write('  # LAYER   ROW   COL   STAGE   AREA   ETC\n')
        for per, res_list in reservoirs.items():
            for res in res_list:
                layer = res['k']
                row = res['i']
                col = res['j']
                stage = res['stage']
                area = res['area']
                f.write(f'  {layer}   {row}   {col}   {stage}   {area}\n')
        f.write('END RESERVOIRS\n\n')
        # TODO: Add more RES blocks as needed (with validation) 