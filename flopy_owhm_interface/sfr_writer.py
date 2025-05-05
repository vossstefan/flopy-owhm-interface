"""
SFR input file writer for OWHM.
Extracts reach and segment data from a FloPy SFR package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_sfr_input(sfr_package, output_path):
    """
    Convert a FloPy SFR package object to an OWHM-compatible SFR input file.
    This version writes basic SFR blocks, extracting what is possible from FloPy.
    Performs input validation and provides clear error messages.
    """
    segments = getattr(sfr_package, 'segments', None)
    if segments is None:
        raise ValueError("SFR package is missing 'segments'.")
    for seg_id, seg in segments.items():
        if not (isinstance(seg_id, int) and seg_id > 0):
            raise ValueError(f"Segment ID {seg_id} must be a positive integer.")
        _require_field(seg, 'upstream', f'segments[{seg_id}]')
        _require_field(seg, 'downstream', f'segments[{seg_id}]')
        _require_field(seg, 'length', f'segments[{seg_id}]')
        length = seg['length']
        if not (isinstance(length, (int, float)) and length > 0):
            raise ValueError(f"Length for segment {seg_id} must be positive. Got: {length}")
        # Cross-check: referenced upstream/downstream segments should exist (if not -1)
        for ref in ['upstream', 'downstream']:
            ref_id = seg[ref]
            if ref_id != -1 and ref_id not in segments:
                raise ValueError(f"{ref} segment {ref_id} referenced by segment {seg_id} not found in segments.")

    reaches = getattr(sfr_package, 'reaches', None)
    if reaches is None:
        raise ValueError("SFR package is missing 'reaches'.")
    for reach_id, reach in reaches.items():
        if not (isinstance(reach_id, int) and reach_id > 0):
            raise ValueError(f"Reach ID {reach_id} must be a positive integer.")
        _require_field(reach, 'segment', f'reaches[{reach_id}]')
        _require_field(reach, 'layer', f'reaches[{reach_id}]')
        _require_field(reach, 'row', f'reaches[{reach_id}]')
        _require_field(reach, 'col', f'reaches[{reach_id}]')
        _require_field(reach, 'length', f'reaches[{reach_id}]')
        length = reach['length']
        if not (isinstance(length, (int, float)) and length > 0):
            raise ValueError(f"Length for reach {reach_id} must be positive. Got: {length}")
        # Cross-check: referenced segment must exist
        segment = reach['segment']
        if segment not in segments:
            raise ValueError(f"Segment {segment} referenced by reach {reach_id} not found in segments.")

    with open(output_path, 'w') as f:
        f.write('# OWHM SFR Input File (auto-generated)\n')
        # SEGMENTS block
        f.write('BEGIN SEGMENTS\n')
        f.write('  # SEGMENT   UPSTREAM   DOWNSTREAM   LENGTH   ETC\n')
        for seg_id, seg in segments.items():
            upstream = seg['upstream']
            downstream = seg['downstream']
            length = seg['length']
            f.write(f'  {seg_id}   {upstream}   {downstream}   {length}\n')
        f.write('END SEGMENTS\n\n')

        # REACHES block
        f.write('BEGIN REACHES\n')
        f.write('  # REACH   SEGMENT   LAYER   ROW   COL   LENGTH   ETC\n')
        for reach_id, reach in reaches.items():
            segment = reach['segment']
            layer = reach['layer']
            row = reach['row']
            col = reach['col']
            length = reach['length']
            f.write(f'  {reach_id}   {segment}   {layer}   {row}   {col}   {length}\n')
        f.write('END REACHES\n\n')
        # TODO: Add more SFR blocks as needed (with validation) 