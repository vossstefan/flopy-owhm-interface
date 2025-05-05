"""
Water accounting input file writer for OWHM.
Allows user to specify custom accounting/reporting blocks or data.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_water_accounting_input(accounting_data, output_path, valid_farm_ids=None):
    """
    Write a water accounting input file for OWHM.
    accounting_data: dict or custom structure with accounting/reporting info.
    Performs input validation and provides clear error messages.
    Optionally checks that farm IDs exist in valid_farm_ids.
    """
    with open(output_path, 'w') as f:
        f.write('# OWHM Water Accounting Input File (auto-generated)\n')
        # ACCOUNTING block
        f.write('BEGIN ACCOUNTING\n')
        f.write('  # ACCOUNT_TYPE   OBJECT_ID   PERIOD   VALUE   ETC\n')
        if accounting_data and isinstance(accounting_data, dict):
            for acc_type, records in accounting_data.items():
                for idx, rec in enumerate(records):
                    _require_field(rec, 'object_id', f'{acc_type}[{idx}]')
                    _require_field(rec, 'period', f'{acc_type}[{idx}]')
                    _require_field(rec, 'value', f'{acc_type}[{idx}]')
                    object_id = rec['object_id']
                    period = rec['period']
                    value = rec['value']
                    if not isinstance(object_id, int):
                        raise ValueError(f"object_id must be an integer in {acc_type}[{idx}]. Got: {object_id}")
                    if not isinstance(period, int):
                        raise ValueError(f"period must be an integer in {acc_type}[{idx}]. Got: {period}")
                    if not isinstance(value, (int, float)):
                        raise ValueError(f"value must be a number in {acc_type}[{idx}]. Got: {value}")
                    if acc_type.upper() == 'FARM' and valid_farm_ids is not None:
                        if object_id not in valid_farm_ids:
                            raise ValueError(f"Water accounting refers to unknown farm_id {object_id} not in FMP farm_dict.")
                    f.write(f'  {acc_type}   {object_id}   {period}   {value}\n')
        else:
            f.write('  # TODO: Provide water accounting data\n')
        f.write('END ACCOUNTING\n\n')
        # TODO: Add more accounting/reporting blocks as needed (with validation) 