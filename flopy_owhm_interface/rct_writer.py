"""
RCT input file writer for OWHM.
Extracts reaction data from a FloPy RCT package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_rct_input(rct_package, output_path):
    """
    Convert a FloPy RCT package object to an OWHM-compatible RCT input file.
    Performs input validation and provides clear error messages.
    """
    rcts = getattr(rct_package, 'parameters', None)
    if rcts is None:
        raise ValueError("RCT package is missing 'parameters'.")
    # Example: RCT parameters might include 'isothm', 'ireact', 'rc1', 'rc2', 'rc3', 'rc4', 'sp1', 'sp2', 'sp3', 'sp4', etc.
    required_fields = ['isothm', 'ireact', 'rc1', 'rc2', 'rc3', 'rc4', 'sp1', 'sp2', 'sp3', 'sp4']
    for field in required_fields:
        _require_field(rcts, field, 'RCT parameters')
    isothm = rcts['isothm']
    ireact = rcts['ireact']
    rc1 = rcts['rc1']
    rc2 = rcts['rc2']
    rc3 = rcts['rc3']
    rc4 = rcts['rc4']
    sp1 = rcts['sp1']
    sp2 = rcts['sp2']
    sp3 = rcts['sp3']
    sp4 = rcts['sp4']
    if not isinstance(isothm, int):
        raise ValueError(f"isothm must be an integer in RCT parameters. Got: {isothm}")
    if not isinstance(ireact, int):
        raise ValueError(f"ireact must be an integer in RCT parameters. Got: {ireact}")
    for val, name in zip([rc1, rc2, rc3, rc4, sp1, sp2, sp3, sp4], ['rc1','rc2','rc3','rc4','sp1','sp2','sp3','sp4']):
        if not isinstance(val, (int, float)):
            raise ValueError(f"{name} must be a number in RCT parameters. Got: {val}")

    with open(output_path, 'w') as f:
        f.write('# OWHM RCT Input File (auto-generated)\n')
        # RCT block
        f.write('BEGIN RCT\n')
        f.write('  # ISOTHM   IREACT   RC1   RC2   RC3   RC4   SP1   SP2   SP3   SP4\n')
        f.write(f'  {isothm}   {ireact}   {rc1}   {rc2}   {rc3}   {rc4}   {sp1}   {sp2}   {sp3}   {sp4}\n')
        f.write('END RCT\n\n')
        # TODO: Add more RCT blocks as needed (with validation) 