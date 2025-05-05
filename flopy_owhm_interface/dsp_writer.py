"""
DSP input file writer for OWHM.
Extracts dispersion data from a FloPy DSP package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_dsp_input(dsp_package, output_path):
    """
    Convert a FloPy DSP package object to an OWHM-compatible DSP input file.
    Performs input validation and provides clear error messages.
    """
    dsps = getattr(dsp_package, 'parameters', None)
    if dsps is None:
        raise ValueError("DSP package is missing 'parameters'.")
    # Example: DSP parameters might include 'al', 'trpt', 'trpv', 'dmcoef', etc.
    required_fields = ['al', 'trpt', 'trpv', 'dmcoef']
    for field in required_fields:
        _require_field(dsps, field, 'DSP parameters')
    al = dsps['al']
    trpt = dsps['trpt']
    trpv = dsps['trpv']
    dmcoef = dsps['dmcoef']
    if not isinstance(al, (int, float)):
        raise ValueError(f"al must be a number in DSP parameters. Got: {al}")
    if not isinstance(trpt, (int, float)):
        raise ValueError(f"trpt must be a number in DSP parameters. Got: {trpt}")
    if not isinstance(trpv, (int, float)):
        raise ValueError(f"trpv must be a number in DSP parameters. Got: {trpv}")
    if not isinstance(dmcoef, (int, float)):
        raise ValueError(f"dmcoef must be a number in DSP parameters. Got: {dmcoef}")

    with open(output_path, 'w') as f:
        f.write('# OWHM DSP Input File (auto-generated)\n')
        # DSP block
        f.write('BEGIN DSP\n')
        f.write('  # AL   TRPT   TRPV   DMCOEF\n')
        f.write(f'  {al}   {trpt}   {trpv}   {dmcoef}\n')
        f.write('END DSP\n\n')
        # TODO: Add more DSP blocks as needed (with validation) 