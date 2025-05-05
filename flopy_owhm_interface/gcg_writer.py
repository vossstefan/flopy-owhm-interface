"""
GCG input file writer for OWHM.
Extracts GCG solver data from a FloPy GCG package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_gcg_input(gcg_package, output_path):
    """
    Convert a FloPy GCG package object to an OWHM-compatible GCG input file.
    Performs input validation and provides clear error messages.
    """
    gcgs = getattr(gcg_package, 'parameters', None)
    if gcgs is None:
        raise ValueError("GCG package is missing 'parameters'.")
    # Example: GCG parameters might include 'mxiter', 'iter1', 'isolve', 'cclose', 'iprgcg', etc.
    required_fields = ['mxiter', 'iter1', 'isolve', 'cclose', 'iprgcg']
    for field in required_fields:
        _require_field(gcgs, field, 'GCG parameters')
    mxiter = gcgs['mxiter']
    iter1 = gcgs['iter1']
    isolve = gcgs['isolve']
    cclose = gcgs['cclose']
    iprgcg = gcgs['iprgcg']
    if not isinstance(mxiter, int):
        raise ValueError(f"mxiter must be an integer in GCG parameters. Got: {mxiter}")
    if not isinstance(iter1, int):
        raise ValueError(f"iter1 must be an integer in GCG parameters. Got: {iter1}")
    if not isinstance(isolve, int):
        raise ValueError(f"isolve must be an integer in GCG parameters. Got: {isolve}")
    if not isinstance(cclose, (int, float)):
        raise ValueError(f"cclose must be a number in GCG parameters. Got: {cclose}")
    if not isinstance(iprgcg, int):
        raise ValueError(f"iprgcg must be an integer in GCG parameters. Got: {iprgcg}")

    with open(output_path, 'w') as f:
        f.write('# OWHM GCG Input File (auto-generated)\n')
        # GCG block
        f.write('BEGIN GCG\n')
        f.write('  # MXITER   ITER1   ISOLVE   CCLOSE   IPRGCG\n')
        f.write(f'  {mxiter}   {iter1}   {isolve}   {cclose}   {iprgcg}\n')
        f.write('END GCG\n\n')
        # TODO: Add more GCG blocks as needed (with validation) 