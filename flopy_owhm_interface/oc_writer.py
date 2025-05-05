"""
OC input file writer for OWHM.
Extracts output control data from a FloPy OC package if possible.
Performs input validation and provides clear error messages.
Supports CSV, listing, and custom output options.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_oc_input(oc_package, output_path):
    """
    Convert a FloPy OC package object to an OWHM-compatible OC input file.
    Performs input validation and provides clear error messages.
    Supports CSV, listing, and custom output options.
    """
    ocs = getattr(oc_package, 'parameters', None)
    if ocs is None:
        raise ValueError("OC package is missing 'parameters'.")
    # Example: OC parameters might include 'csv_output', 'listing_output', 'custom_blocks', etc.
    required_fields = ['csv_output', 'listing_output']
    for field in required_fields:
        _require_field(ocs, field, 'OC parameters')
    csv_output = ocs['csv_output']
    listing_output = ocs['listing_output']
    custom_blocks = ocs.get('custom_blocks', [])
    if not isinstance(csv_output, bool):
        raise ValueError(f"csv_output must be a boolean in OC parameters. Got: {csv_output}")
    if not isinstance(listing_output, bool):
        raise ValueError(f"listing_output must be a boolean in OC parameters. Got: {listing_output}")
    if not isinstance(custom_blocks, list):
        raise ValueError(f"custom_blocks must be a list in OC parameters. Got: {custom_blocks}")

    with open(output_path, 'w') as f:
        f.write('# OWHM OC Input File (auto-generated)\n')
        # OC block
        f.write('BEGIN OC\n')
        f.write(f'  CSV_OUTPUT   {int(csv_output)}\n')
        f.write(f'  LISTING_OUTPUT   {int(listing_output)}\n')
        for block in custom_blocks:
            if not isinstance(block, str):
                raise ValueError(f"Each custom block must be a string. Got: {block}")
            f.write(f'  {block}\n')
        f.write('END OC\n\n')
        # TODO: Add more OC blocks as needed (with validation) 