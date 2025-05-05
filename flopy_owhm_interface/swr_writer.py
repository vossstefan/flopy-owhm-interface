"""
SWR input file writer for OWHM.
Extracts reach and connection data from a FloPy SWR package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_swr_input(swr_package, output_path):
    """
    Convert a FloPy SWR package object to an OWHM-compatible SWR input file.
    This version writes basic SWR blocks, extracting what is possible from FloPy.
    Performs input validation and provides clear error messages.
    """
    reaches = getattr(swr_package, 'reaches', None)
    if reaches is None:
        raise ValueError("SWR package is missing 'reaches'.")
    for reach_id, reach in reaches.items():
        if not (isinstance(reach_id, int) and reach_id > 0):
            raise ValueError(f"Reach ID {reach_id} must be a positive integer.")
        _require_field(reach, 'layer', f'reaches[{reach_id}]')
        _require_field(reach, 'row', f'reaches[{reach_id}]')
        _require_field(reach, 'col', f'reaches[{reach_id}]')
        _require_field(reach, 'length', f'reaches[{reach_id}]')
        length = reach['length']
        if not (isinstance(length, (int, float)) and length > 0):
            raise ValueError(f"Length for reach {reach_id} must be positive. Got: {length}")

    connections = getattr(swr_package, 'connections', None)
    if connections is None:
        raise ValueError("SWR package is missing 'connections'.")
    for idx, conn in enumerate(connections):
        _require_field(conn, 'reach1', f'connections[{idx}]')
        _require_field(conn, 'reach2', f'connections[{idx}]')
        _require_field(conn, 'type', f'connections[{idx}]')
        reach1 = conn['reach1']
        reach2 = conn['reach2']
        if reach1 not in reaches:
            raise ValueError(f"Connection reach1 {reach1} in connections[{idx}] not found in reaches.")
        if reach2 not in reaches:
            raise ValueError(f"Connection reach2 {reach2} in connections[{idx}] not found in reaches.")

    with open(output_path, 'w') as f:
        f.write('# OWHM SWR Input File (auto-generated)\n')
        # REACHES block
        f.write('BEGIN REACHES\n')
        f.write('  # REACH   LAYER   ROW   COL   LENGTH   ETC\n')
        for reach_id, reach in reaches.items():
            layer = reach['layer']
            row = reach['row']
            col = reach['col']
            length = reach['length']
            f.write(f'  {reach_id}   {layer}   {row}   {col}   {length}\n')
        f.write('END REACHES\n\n')

        # CONNECTIONS block
        f.write('BEGIN CONNECTIONS\n')
        f.write('  # REACH1   REACH2   TYPE   ETC\n')
        for conn in connections:
            reach1 = conn['reach1']
            reach2 = conn['reach2']
            conn_type = conn['type']
            f.write(f'  {reach1}   {reach2}   {conn_type}\n')
        f.write('END CONNECTIONS\n\n')
        # TODO: Add more SWR blocks as needed (with validation) 