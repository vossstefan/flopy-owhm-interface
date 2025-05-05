import pytest
from flopy_owhm_interface.mnw2_writer import write_mnw2_input

def mock_mnw2_package():
    class MockMnw2:
        pass
    mnw2 = MockMnw2()
    mnw2.stress_period_data = {
        0: [
            {'wellid': 'W1', 'k': 1, 'i': 1, 'j': 1, 'qdes': 100.0},
            {'wellid': 'W2', 'k': 1, 'i': 2, 'j': 2, 'qdes': 200.0},
        ]
    }
    return mnw2

def test_write_mnw2_input(tmp_path):
    mnw2 = mock_mnw2_package()
    output_file = tmp_path / 'MNW2.dat'
    write_mnw2_input(mnw2, str(output_file))
    with open(output_file, 'r') as f:
        content = f.read()
    assert 'MNW2' in content or 'BEGIN MNW2' in content
    assert 'W1' in content
    assert 'W2' in content 