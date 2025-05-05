import pytest
from flopy_owhm_interface.res_writer import write_res_input

def mock_res_package():
    class MockRes:
        pass
    res = MockRes()
    res.reservoirs = [
        {'res_id': 1, 'row': 1, 'col': 1, 'stage': 20.0, 'area': 300.0},
        {'res_id': 2, 'row': 2, 'col': 2, 'stage': 22.0, 'area': 320.0},
    ]
    return res

def test_write_res_input(tmp_path):
    res = mock_res_package()
    output_file = tmp_path / 'RES.dat'
    write_res_input(res, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'RES' in content or 'BEGIN RES' in content
    assert '1' in content
    assert '2' in content 