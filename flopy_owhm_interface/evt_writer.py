"""
EVT input file writer for OWHM.
Extracts evapotranspiration data from a FloPy EVT package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_evt_input(evt_package, output_path):
    """
    Convert a FloPy EVT package object to an OWHM-compatible EVT input file.
    Performs input validation and provides clear error messages.
    """
    evts = getattr(evt_package, 'stress_period_data', None)
    if evts is None:
        raise ValueError("EVT package is missing 'stress_period_data'.")
    for per, evt_list in evts.items():
        for idx, evt in enumerate(evt_list):
            _require_field(evt, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(evt, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(evt, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(evt, 'surf', f'stress_period_data[{per}][{idx}]')
            _require_field(evt, 'evtr', f'stress_period_data[{per}][{idx}]')
            layer = evt['k']
            row = evt['i']
            col = evt['j']
            surf = evt['surf']
            evtr = evt['evtr']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(surf, (int, float)):
                raise ValueError(f"surf must be a number in stress_period_data[{per}][{idx}]. Got: {surf}")
            if not (isinstance(evtr, (int, float)) and evtr >= 0):
                raise ValueError(f"evtr must be non-negative in stress_period_data[{per}][{idx}]. Got: {evtr}")

    with open(output_path, 'w') as f:
        f.write('# OWHM EVT Input File (auto-generated)\n')
        # EVT block
        f.write('BEGIN EVT\n')
        f.write('  # LAYER   ROW   COL   SURF   EVTR   ETC\n')
        for per, evt_list in evts.items():
            for evt in evt_list:
                layer = evt['k']
                row = evt['i']
                col = evt['j']
                surf = evt['surf']
                evtr = evt['evtr']
                f.write(f'  {layer}   {row}   {col}   {surf}   {evtr}\n')
        f.write('END EVT\n\n')
        # TODO: Add more EVT blocks as needed (with validation) 