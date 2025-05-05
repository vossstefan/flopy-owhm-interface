"""
FMP input file writer for OWHM.
Extracts all major FMP blocks from a FloPy FMP package if possible.
Performs input validation and provides clear error messages.
"""

def _require_field(obj, field, context):
    if field not in obj:
        raise ValueError(f"Missing required field '{field}' in {context}.")
    return obj[field]

def write_fmp_input(fmp_package, output_path, water_accounting=None):
    """
    Convert a FloPy FMP package object to an OWHM-compatible FMP input file.
    This version writes all major FMP blocks, extracting what is possible from FloPy.
    Performs input validation and provides clear error messages.
    Optionally checks water accounting farm IDs for consistency.
    """
    # FARM block
    farm_dict = getattr(fmp_package, 'farm_dict', None)
    if farm_dict is None:
        raise ValueError("FMP package is missing 'farm_dict'. Ensure you are passing a valid FloPy FMP package.")
    farm_ids = list(farm_dict.keys())
    for farm_id, info in farm_dict.items():
        _require_field(info, 'area', f'farm_dict[{farm_id}]')
        _require_field(info, 'name', f'farm_dict[{farm_id}]')
        area = info['area']
        if not (isinstance(area, (int, float)) and area > 0):
            raise ValueError(f"Area for farm {farm_id} must be positive. Got: {area}")

    # DEMAND block
    sp_data = getattr(fmp_package, 'stress_period_data', None)
    if sp_data is None:
        sp_data = getattr(fmp_package, 'irrigation', None)
    if sp_data is None:
        raise ValueError("FMP package is missing 'stress_period_data' or 'irrigation'.")
    for per, farm_demands in sp_data.items():
        for farm_id in farm_ids:
            if farm_id not in farm_demands:
                raise ValueError(f"Missing demand for farm {farm_id} in stress period {per}.")
            demand = farm_demands[farm_id]
            if not (isinstance(demand, (int, float)) and demand >= 0):
                raise ValueError(f"Demand for farm {farm_id} in stress period {per} must be non-negative. Got: {demand}")

    # Cross-check: water accounting farm IDs must exist in FMP
    if water_accounting and isinstance(water_accounting, dict):
        for acc_type, records in water_accounting.items():
            if acc_type.upper() == 'FARM':
                for rec in records:
                    farm_id = rec.get('object_id', None)
                    if farm_id not in farm_ids:
                        raise ValueError(f"Water accounting refers to unknown farm_id {farm_id} not in FMP farm_dict.")

    # SUPPLY block
    supply_data = getattr(fmp_package, 'supply', None)

    # CROP block
    crop_data = getattr(fmp_package, 'crop_data', None)
    if crop_data is None:
        crop_data = getattr(fmp_package, 'cropinfo', None)
    if crop_data is None:
        crop_data = getattr(fmp_package, 'crop_dict', None)

    # SOIL block
    soil_data = getattr(fmp_package, 'soil_data', None)
    if soil_data is None:
        soil_data = getattr(fmp_package, 'soilinfo', None)
    if soil_data is None:
        soil_data = getattr(fmp_package, 'soil_dict', None)

    # WELL block
    well_data = getattr(fmp_package, 'well_data', None)
    if well_data is None:
        well_data = getattr(fmp_package, 'wellinfo', None)
    if well_data is None:
        well_data = getattr(fmp_package, 'well_dict', None)

    # DELIVERY block
    delivery_data = getattr(fmp_package, 'delivery', None)

    # WATER_RIGHTS block
    water_rights_data = getattr(fmp_package, 'water_rights', None)

    # AUXILIARY block
    auxiliary_data = getattr(fmp_package, 'auxiliary', None)

    with open(output_path, 'w') as f:
        f.write('# OWHM FMP Input File (auto-generated)\n')

        # FARM block
        f.write('BEGIN FARM\n')
        f.write('  # ID   AREA   NAME\n')
        for farm_id in farm_ids:
            info = farm_dict[farm_id]
            area = info['area']
            name = info['name']
            f.write(f'  {farm_id}   {area}   {name}\n')
        f.write('END FARM\n\n')

        # DEMAND block
        f.write('BEGIN DEMAND\n')
        f.write('  # PER   FARM_ID   DEMAND\n')
        for per, farm_demands in sp_data.items():
            for farm_id in farm_ids:
                demand = farm_demands[farm_id]
                f.write(f'  {per}   {farm_id}   {demand}\n')
        f.write('END DEMAND\n\n')

        # SUPPLY block
        f.write('BEGIN SUPPLY\n')
        f.write('  # PER   FARM_ID   SUPPLY_TYPE   AMOUNT\n')
        if supply_data:
            for per, farm_supplies in supply_data.items():
                for farm_id, supply in farm_supplies.items():
                    # Example: supply could be a dict with type and amount
                    supply_type = supply.get('type', 'UNKNOWN')
                    amount = supply.get('amount', 0.0)
                    f.write(f'  {per}   {farm_id}   {supply_type}   {amount}\n')
        else:
            f.write('  # TODO: Provide supply data for each farm and stress period\n')
        f.write('END SUPPLY\n\n')

        # CROP block
        f.write('BEGIN CROP\n')
        f.write('  # ID   NAME   ET   ROOT_DEPTH   ETC\n')
        if crop_data:
            for crop_id, crop in crop_data.items():
                name = crop.get('name', str(crop_id))
                et = crop.get('et', 0.0)
                root_depth = crop.get('root_depth', 0.0)
                # Add more fields as needed
                f.write(f'  {crop_id}   {name}   {et}   {root_depth}\n')
        else:
            f.write('  # TODO: Provide crop data\n')
        f.write('END CROP\n\n')

        # SOIL block
        f.write('BEGIN SOIL\n')
        f.write('  # ID   NAME   FIELD_CAPACITY   WILTING_POINT   ETC\n')
        if soil_data:
            for soil_id, soil in soil_data.items():
                name = soil.get('name', str(soil_id))
                fc = soil.get('field_capacity', 0.0)
                wp = soil.get('wilting_point', 0.0)
                # Add more fields as needed
                f.write(f'  {soil_id}   {name}   {fc}   {wp}\n')
        else:
            f.write('  # TODO: Provide soil data\n')
        f.write('END SOIL\n\n')

        # WELL block
        f.write('BEGIN WELL\n')
        f.write('  # FARM_ID   WELL_ID   LAYER   ROW   COL   ETC\n')
        if well_data:
            for farm_id, wells in well_data.items():
                for well in wells:
                    well_id = well.get('well_id', 'UNKNOWN')
                    layer = well.get('layer', 1)
                    row = well.get('row', 1)
                    col = well.get('col', 1)
                    # Add more fields as needed
                    f.write(f'  {farm_id}   {well_id}   {layer}   {row}   {col}\n')
        else:
            f.write('  # TODO: Provide well data\n')
        f.write('END WELL\n\n')

        # DELIVERY block
        f.write('BEGIN DELIVERY\n')
        f.write('  # FARM_ID   DELIVERY_TYPE   AMOUNT   ETC\n')
        if delivery_data:
            for farm_id, deliveries in delivery_data.items():
                for delivery in deliveries:
                    delivery_type = delivery.get('type', 'UNKNOWN')
                    amount = delivery.get('amount', 0.0)
                    # Add more fields as needed
                    f.write(f'  {farm_id}   {delivery_type}   {amount}\n')
        else:
            f.write('  # TODO: Provide delivery system data\n')
        f.write('END DELIVERY\n\n')

        # WATER_RIGHTS block
        f.write('BEGIN WATER_RIGHTS\n')
        f.write('  # FARM_ID   RIGHT_TYPE   AMOUNT   ETC\n')
        if water_rights_data:
            for farm_id, rights in water_rights_data.items():
                for right in rights:
                    right_type = right.get('type', 'UNKNOWN')
                    amount = right.get('amount', 0.0)
                    # Add more fields as needed
                    f.write(f'  {farm_id}   {right_type}   {amount}\n')
        else:
            f.write('  # TODO: Provide water rights data\n')
        f.write('END WATER_RIGHTS\n\n')

        # AUXILIARY block
        f.write('BEGIN AUXILIARY\n')
        f.write('  # FARM_ID   AUX_NAME   VALUE\n')
        if auxiliary_data:
            for farm_id, auxs in auxiliary_data.items():
                for aux in auxs:
                    aux_name = aux.get('name', 'UNKNOWN')
                    value = aux.get('value', 0.0)
                    f.write(f'  {farm_id}   {aux_name}   {value}\n')
        else:
            f.write('  # TODO: Provide auxiliary data\n')
        f.write('END AUXILIARY\n\n') 