import pytest
from flopy_owhm_interface.ssm_writer import write_ssm_input

def mock_ssm_package():
    class MockSsm:
        pass
    ssm = MockSsm()
    ssm.stress_period_data = {
        0: [
            {'k': 1, 'i': 1, 'j': 1, 'itype': 1, 'c': 0.5},
            {'k': 1, 'i': 2, 'j': 2, 'itype': 2, 'c': 0.6},
        ]
    }
    return ssm

def test_write_ssm_input(tmp_path):
    ssm = mock_ssm_package()
    output_file = tmp_path / 'SSM.dat'
    write_ssm_input(ssm, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'SSM' in content or 'BEGIN SSM' in content
    assert '0.5' in content
    assert '0.6' in content 