import pytest
from flopy_owhm_interface.lake_writer import write_lake_input

def mock_lake_package():
    class MockLake:
        pass
    lake = MockLake()
    lake.lakes = [
        {'lake_id': 1, 'row': 1, 'col': 1, 'stage': 10.0, 'area': 100.0},
        {'lake_id': 2, 'row': 2, 'col': 2, 'stage': 12.0, 'area': 120.0},
    ]
    return lake

def test_write_lake_input(tmp_path):
    lake = mock_lake_package()
    output_file = tmp_path / 'LAK.dat'
    write_lake_input(lake, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'LAK' in content or 'BEGIN LAK' in content
    assert '1' in content
    assert '2' in content 