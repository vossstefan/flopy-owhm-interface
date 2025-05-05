import pytest
from flopy_owhm_interface.uzf_writer import write_uzf_input

def mock_uzf_package():
    class MockUzf:
        pass
    uzf = MockUzf()
    uzf.stress_period_data = {
        0: [
            {'i': 1, 'j': 1, 'finf': 0.1},
            {'i': 2, 'j': 2, 'finf': 0.2},
        ]
    }
    return uzf

def test_write_uzf_input(tmp_path):
    uzf = mock_uzf_package()
    output_file = tmp_path / 'UZF.dat'
    write_uzf_input(uzf, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'UZF' in content or 'BEGIN UZF' in content
    assert '0.1' in content
    assert '0.2' in content 