"""
ETS input file writer for OWHM.
Extracts evapotranspiration segment data from a FloPy ETS package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_ets_input(ets_package, output_path):
    """
    Convert a FloPy ETS package object to an OWHM-compatible ETS input file.
    Performs input validation and provides clear error messages.
    """
    etss = getattr(ets_package, 'stress_period_data', None)
    if etss is None:
        raise ValueError("ETS package is missing 'stress_period_data'.")
    for per, ets_list in etss.items():
        for idx, ets in enumerate(ets_list):
            _require_field(ets, 'k', f'stress_period_data[{per}][{idx}]')
            _require_field(ets, 'i', f'stress_period_data[{per}][{idx}]')
            _require_field(ets, 'j', f'stress_period_data[{per}][{idx}]')
            _require_field(ets, 'surf', f'stress_period_data[{per}][{idx}]')
            _require_field(ets, 'pxdp', f'stress_period_data[{per}][{idx}]')
            _require_field(ets, 'petm', f'stress_period_data[{per}][{idx}]')
            _require_field(ets, 'pet', f'stress_period_data[{per}][{idx}]')
            layer = ets['k']
            row = ets['i']
            col = ets['j']
            surf = ets['surf']
            pxdp = ets['pxdp']
            petm = ets['petm']
            pet = ets['pet']
            if not (isinstance(layer, int) and layer > 0):
                raise ValueError(f"Layer must be a positive integer in stress_period_data[{per}][{idx}]. Got: {layer}")
            if not (isinstance(row, int) and row > 0):
                raise ValueError(f"Row must be a positive integer in stress_period_data[{per}][{idx}]. Got: {row}")
            if not (isinstance(col, int) and col > 0):
                raise ValueError(f"Col must be a positive integer in stress_period_data[{per}][{idx}]. Got: {col}")
            if not isinstance(surf, (int, float)):
                raise ValueError(f"surf must be a number in stress_period_data[{per}][{idx}]. Got: {surf}")
            if not isinstance(pxdp, (int, float)):
                raise ValueError(f"pxdp must be a number in stress_period_data[{per}][{idx}]. Got: {pxdp}")
            if not isinstance(petm, (int, float)):
                raise ValueError(f"petm must be a number in stress_period_data[{per}][{idx}]. Got: {petm}")
            if not isinstance(pet, (int, float)):
                raise ValueError(f"pet must be a number in stress_period_data[{per}][{idx}]. Got: {pet}")

    with open(output_path, 'w') as f:
        f.write('# OWHM ETS Input File (auto-generated)\n')
        # ETS block
        f.write('BEGIN ETS\n')
        f.write('  # LAYER   ROW   COL   SURF   PXDP   PETM   PET\n')
        for per, ets_list in etss.items():
            for ets in ets_list:
                layer = ets['k']
                row = ets['i']
                col = ets['j']
                surf = ets['surf']
                pxdp = ets['pxdp']
                petm = ets['petm']
                pet = ets['pet']
                f.write(f'  {layer}   {row}   {col}   {surf}   {pxdp}   {petm}   {pet}\n')
        f.write('END ETS\n\n')
        # TODO: Add more ETS blocks as needed (with validation) 