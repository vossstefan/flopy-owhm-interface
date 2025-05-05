"""
MNW2 input file writer for OWHM.
Extracts multi-node well data from a FloPy MNW2 package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_mnw2_input(mnw2_package, output_path):
    """
    Convert a FloPy MNW2 package object to an OWHM-compatible MNW2 input file.
    Performs input validation and provides clear error messages.
    """
    mnw2s = getattr(mnw2_package, 'stress_period_data', None)
    if mnw2s is None:
        raise ValueError("MNW2 package is missing 'stress_period_data'.")
    for per, mnw2_list in mnw2s.items():
        for idx, mnw2 in enumerate(mnw2_list):
            _require_field(mnw2, 'wellid', f'stress_period_data[{per}][{idx}]')
            _require_field(mnw2, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(mnw2, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(mnw2, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(mnw2, 'qdes', f'stress_period_data[{per}][{idx}]')
            wellid = mnw2['wellid']
            layer = mnw2['k']
            row = mnw2['i']
            col = mnw2['j']
            qdes = mnw2['qdes']
            if not isinstance(wellid, (str, int)):
                raise ValueError(f"wellid must be a string or integer in stress_period_data[{per}][{idx}]. Got: {wellid}")
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(qdes, (int, float)):
                raise ValueError(f"qdes must be a number in stress_period_data[{per}][{idx}]. Got: {qdes}")

    with open(output_path, 'w') as f:
        f.write('# OWHM MNW2 Input File (auto-generated)\n')
        # MNW2 block
        f.write('BEGIN MNW2\n')
        f.write('  # WELLID   LAYER   ROW   COL   QDES\n')
        for per, mnw2_list in mnw2s.items():
            for mnw2 in mnw2_list:
                wellid = mnw2['wellid']
                layer = mnw2['k']
                row = mnw2['i']
                col = mnw2['j']
                qdes = mnw2['qdes']
                f.write(f'  {wellid}   {layer}   {row}   {col}   {qdes}\n')
        f.write('END MNW2\n\n')
        # TODO: Add more MNW2 blocks as needed (with validation) 