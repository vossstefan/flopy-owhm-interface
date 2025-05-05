"""
LMT input file writer for OWHM.
Extracts Link-MT3DMS data from a FloPy LMT package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_lmt_input(lmt_package, output_path):
    """
    Convert a FloPy LMT package object to an OWHM-compatible LMT input file.
    Performs input validation and provides clear error messages.
    """
    lmts = getattr(lmt_package, 'parameters', None)
    if lmts is None:
        raise ValueError("LMT package is missing 'parameters'.")
    # Example: LMT parameters might include 'output_file', 'output_format', etc.
    required_fields = ['output_file', 'output_format']
    for field in required_fields:
        _require_field(lmts, field, 'LMT parameters')
    output_file = lmts['output_file']
    output_format = lmts['output_format']
    if not isinstance(output_file, str):
        raise ValueError(f"output_file must be a string in LMT parameters. Got: {output_file}")
    if not isinstance(output_format, int):
        raise ValueError(f"output_format must be an integer in LMT parameters. Got: {output_format}")

    with open(output_path, 'w') as f:
        f.write('# OWHM LMT Input File (auto-generated)\n')
        # LMT block
        f.write('BEGIN LMT\n')
        f.write('  # OUTPUT_FILE   OUTPUT_FORMAT\n')
        f.write(f'  {output_file}   {output_format}\n')
        f.write('END LMT\n\n')
        # TODO: Add more LMT blocks as needed (with validation) 