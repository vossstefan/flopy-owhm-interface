"""
MAW input file writer for OWHM.
Extracts well data from a FloPy MAW package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_maw_input(maw_package, output_path):
    """
    Convert a FloPy MAW package object to an OWHM-compatible MAW input file.
    Extracts well data and writes all major fields. Performs input validation.
    """
    # Try to extract static well info (location, screen, etc.)
    static_data = getattr(maw_package, 'well_info', None)
    if static_data is None:
        static_data = getattr(maw_package, 'static_data', None)
    if static_data is None:
        raise ValueError("MAW package is missing 'well_info' or 'static_data'.")
    for well_id, info in static_data.items():
        _require_field(info, 'layer', f'well_info[{well_id}]')
        _require_field(info, 'row', f'well_info[{well_id}]')
        _require_field(info, 'col', f'well_info[{well_id}]')
        _require_field(info, 'screen_top', f'well_info[{well_id}]')
        _require_field(info, 'screen_bottom', f'well_info[{well_id}]')
        _require_field(info, 'diameter', f'well_info[{well_id}]')
        diameter = info['diameter']
        if not (isinstance(diameter, (int, float)) and diameter > 0):
            raise ValueError(f"Diameter for well {well_id} must be positive. Got: {diameter}")
        if not (info['screen_top'] > info['screen_bottom']):
            raise ValueError(f"screen_top must be greater than screen_bottom for well {well_id}.")

    # Try to extract well stress period data
    maw_data = getattr(maw_package, 'stress_period_data', None)
    if maw_data is None:
        maw_data = getattr(maw_package, 'well_data', None)
    if maw_data is None:
        maw_data = getattr(maw_package, 'well_dict', None)
    if maw_data is None:
        raise ValueError("MAW package is missing 'stress_period_data', 'well_data', or 'well_dict'.")
    for per, wells in maw_data.items():
        for well_id, data in wells.items():
            if well_id not in static_data:
                raise ValueError(f"Well ID {well_id} in stress period {per} not found in static well info.")
            _require_field(data, 'rate', f'stress_period_data[{per}][{well_id}]')
            _require_field(data, 'status', f'stress_period_data[{per}][{well_id}]')
            rate = data['rate']
            if not isinstance(rate, (int, float)):
                raise ValueError(f"Rate for well {well_id} in stress period {per} must be a number. Got: {rate}")
            status = data['status']
            if not (isinstance(status, str) and status):
                raise ValueError(f"Status for well {well_id} in stress period {per} must be a non-empty string. Got: {status}")

    with open(output_path, 'w') as f:
        f.write('# OWHM MAW Input File (auto-generated)\n')
        f.write('BEGIN MAW\n')
        f.write('  # WELL_ID   LAYER   ROW   COL   SCREEN_TOP   SCREEN_BOTTOM   DIAMETER   ETC\n')
        for well_id, info in static_data.items():
            layer = info['layer']
            row = info['row']
            col = info['col']
            screen_top = info['screen_top']
            screen_bottom = info['screen_bottom']
            diameter = info['diameter']
            f.write(f'  {well_id}   {layer}   {row}   {col}   {screen_top}   {screen_bottom}   {diameter}\n')
        f.write('END MAW\n\n')

        # MAW stress period data (e.g., rates, status)
        f.write('BEGIN MAW_SP\n')
        f.write('  # PER   WELL_ID   RATE   STATUS   ETC\n')
        for per, wells in maw_data.items():
            for well_id, data in wells.items():
                rate = data['rate']
                status = data['status']
                f.write(f'  {per}   {well_id}   {rate}   {status}\n')
        f.write('END MAW_SP\n\n') 