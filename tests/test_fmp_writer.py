import pytest
from flopy_owhm_interface.fmp_writer import write_fmp_input

def mock_fmp_package():
    class MockFmp:
        pass
    fmp = MockFmp()
    fmp.farms = [
        {'farm_id': 1, 'name': 'Farm1', 'area': 100.0},
        {'farm_id': 2, 'name': 'Farm2', 'area': 200.0},
    ]
    fmp.farm_dict = {1: 'Farm1', 2: 'Farm2'}
    return fmp

def test_write_fmp_input(tmp_path):
    fmp = mock_fmp_package()
    output_file = tmp_path / 'FMP.dat'
    write_fmp_input(fmp, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'FMP' in content or 'BEGIN FMP' in content
    assert 'Farm1' in content
    assert 'Farm2' in content 