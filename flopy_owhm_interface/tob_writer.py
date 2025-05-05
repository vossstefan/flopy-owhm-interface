"""
TOB input file writer for OWHM.
Extracts transport observation data from a FloPy TOB package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_tob_input(tob_package, output_path):
    """
    Convert a FloPy TOB package object to an OWHM-compatible TOB input file.
    Performs input validation and provides clear error messages.
    """
    tobs = getattr(tob_package, 'observation_data', None)
    if tobs is None:
        raise ValueError("TOB package is missing 'observation_data'.")
    for idx, tob in enumerate(tobs):
        _require_field(tob, 'k', f'observation_data[{idx}]')
        _require_field(tob, 'i', f'observation_data[{idx}]')
        _require_field(tob, 'j', f'observation_data[{idx}]')
        _require_field(tob, 'obsname', f'observation_data[{idx}]')
        _require_field(tob, 'obstype', f'observation_data[{idx}]')
        layer = tob['k']
        row = tob['i']
        col = tob['j']
        obsname = tob['obsname']
        obstype = tob['obstype']
        if not (isinstance(layer, int) and layer > 0):
            raise ValueError(f"Layer must be a positive integer in observation_data[{idx}]. Got: {layer}")
        if not (isinstance(row, int) and row > 0):
            raise ValueError(f"Row must be a positive integer in observation_data[{idx}]. Got: {row}")
        if not (isinstance(col, int) and col > 0):
            raise ValueError(f"Col must be a positive integer in observation_data[{idx}]. Got: {col}")
        if not isinstance(obsname, str):
            raise ValueError(f"obsname must be a string in observation_data[{idx}]. Got: {obsname}")
        if not isinstance(obstype, str):
            raise ValueError(f"obstype must be a string in observation_data[{idx}]. Got: {obstype}")

    with open(output_path, 'w') as f:
        f.write('# OWHM TOB Input File (auto-generated)\n')
        # TOB block
        f.write('BEGIN TOB\n')
        f.write('  # LAYER   ROW   COL   OBSNAME   OBSTYPE\n')
        for tob in tobs:
            layer = tob['k']
            row = tob['i']
            col = tob['j']
            obsname = tob['obsname']
            obstype = tob['obstype']
            f.write(f'  {layer}   {row}   {col}   {obsname}   {obstype}\n')
        f.write('END TOB\n\n')
        # TODO: Add more TOB blocks as needed (with validation) 