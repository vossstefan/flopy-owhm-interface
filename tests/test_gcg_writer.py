import pytest
from flopy_owhm_interface.gcg_writer import write_gcg_input

def mock_gcg_package():
    class MockGcg:
        pass
    gcg = MockGcg()
    gcg.parameters = {
        'mxiter': 10,
        'iter1': 5,
        'isolve': 2,
        'cclose': 1e-5,
        'iprgcg': 1
    }
    return gcg

def test_write_gcg_input(tmp_path):
    gcg = mock_gcg_package()
    output_file = tmp_path / 'GCG.dat'
    write_gcg_input(gcg, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'GCG' in content or 'BEGIN GCG' in content
    assert '10' in content
    assert '5' in content
    assert '2' in content
    assert '1e-05' in content or '0.00001' in content
    assert '1' in content 