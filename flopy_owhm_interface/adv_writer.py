"""
ADV input file writer for OWHM.
Extracts advection data from a FloPy ADV package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_adv_input(adv_package, output_path):
    """
    Convert a FloPy ADV package object to an OWHM-compatible ADV input file.
    Performs input validation and provides clear error messages.
    """
    advs = getattr(adv_package, 'parameters', None)
    if advs is None:
        raise ValueError("ADV package is missing 'parameters'.")
    # Example: ADV parameters might include 'mixelm', 'percel', 'nadvfd', etc.
    required_fields = ['mixelm', 'percel', 'nadvfd']
    for field in required_fields:
        _require_field(advs, field, 'ADV parameters')
    mixelm = advs['mixelm']
    percel = advs['percel']
    nadvfd = advs['nadvfd']
    if not isinstance(mixelm, int):
        raise ValueError(f"mixelm must be an integer in ADV parameters. Got: {mixelm}")
    if not isinstance(percel, (int, float)):
        raise ValueError(f"percel must be a number in ADV parameters. Got: {percel}")
    if not isinstance(nadvfd, int):
        raise ValueError(f"nadvfd must be an integer in ADV parameters. Got: {nadvfd}")

    with open(output_path, 'w') as f:
        f.write('# OWHM ADV Input File (auto-generated)\n')
        # ADV block
        f.write('BEGIN ADV\n')
        f.write('  # MIXELM   PERCEL   NADVFD\n')
        f.write(f'  {mixelm}   {percel}   {nadvfd}\n')
        f.write('END ADV\n\n')
        # TODO: Add more ADV blocks as needed (with validation) 