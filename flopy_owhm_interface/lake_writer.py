"""
LAKE input file writer for OWHM.
Extracts lake data from a FloPy LAK package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_lake_input(lak_package, output_path):
    """
    Convert a FloPy LAK package object to an OWHM-compatible LAKE input file.
    This version writes basic LAKE blocks, extracting what is possible from FloPy.
    Performs input validation and provides clear error messages.
    """
    lakes = getattr(lak_package, 'lakes', None)
    if lakes is None:
        raise ValueError("LAK package is missing 'lakes'.")
    for lake_id, lake in lakes.items():
        if not (isinstance(lake_id, int) and lake_id > 0):
            raise ValueError(f"Lake ID {lake_id} must be a positive integer.")
        _require_field(lake, 'layer', f'lakes[{lake_id}]')
        _require_field(lake, 'row', f'lakes[{lake_id}]')
        _require_field(lake, 'col', f'lakes[{lake_id}]')
        _require_field(lake, 'area', f'lakes[{lake_id}]')
        area = lake['area']
        if not (isinstance(area, (int, float)) and area > 0):
            raise ValueError(f"Area for lake {lake_id} must be positive. Got: {area}")

    outlets = getattr(lak_package, 'outlets', None)
    if outlets is not None:
        for idx, outlet in enumerate(outlets):
            _require_field(outlet, 'lake_id', f'outlets[{idx}]')
            _require_field(outlet, 'outlet_id', f'outlets[{idx}]')
            _require_field(outlet, 'type', f'outlets[{idx}]')
            lake_id = outlet['lake_id']
            outlet_id = outlet['outlet_id']
            if not (isinstance(lake_id, int) and lake_id > 0):
                raise ValueError(f"Lake ID {lake_id} in outlets[{idx}] must be a positive integer.")
            if not (isinstance(outlet_id, int) and outlet_id > 0):
                raise ValueError(f"Outlet ID {outlet_id} in outlets[{idx}] must be a positive integer.")
            if lake_id not in lakes:
                raise ValueError(f"Outlet references unknown lake_id {lake_id} in outlets[{idx}].")

    with open(output_path, 'w') as f:
        f.write('# OWHM LAKE Input File (auto-generated)\n')
        # LAKES block
        f.write('BEGIN LAKES\n')
        f.write('  # LAKE_ID   LAYER   ROW   COL   AREA   ETC\n')
        for lake_id, lake in lakes.items():
            layer = lake['layer']
            row = lake['row']
            col = lake['col']
            area = lake['area']
            f.write(f'  {lake_id}   {layer}   {row}   {col}   {area}\n')
        f.write('END LAKES\n\n')

        # OUTLETS block
        f.write('BEGIN OUTLETS\n')
        f.write('  # LAKE_ID   OUTLET_ID   TYPE   ETC\n')
        if outlets:
            for outlet in outlets:
                lake_id = outlet['lake_id']
                outlet_id = outlet['outlet_id']
                outlet_type = outlet['type']
                f.write(f'  {lake_id}   {outlet_id}   {outlet_type}\n')
        f.write('END OUTLETS\n\n')
        # TODO: Add more LAKE blocks as needed (with validation) 