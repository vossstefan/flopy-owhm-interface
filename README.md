# flopy_owhm_interface

A Python package to interface between FloPy and MODFLOW-OWHM (MF-OWHM), enabling the use of advanced OWHM features (such as the Farm Process and Multi-Aquifer Wells) from Python.

## Features
- Generate MF-OWHM input files from FloPy models and user data
- Support for Farm Process (FMP) and Multi-Aquifer Wells (MAW)
- Run MF-OWHM from Python and manage input/output files
- Parse OWHM outputs into Python objects
- Windows-only support (for now)

## Planned Features
- Surface Water Routing (SWR) and Streamflow Routing (SFR) support
- Supply/demand and water rights integration
- Advanced boundary conditions
- Water accounting and reporting

## Installation
```
# (To be implemented)
# pip install flopy_owhm_interface
```

## Usage Example
```python
from flopy_owhm_interface import OWHMInterface

# Initialize interface with path to OWHM executable
owhm = OWHMInterface(owhm_exe_path='C:/path/to/mf-owhm.exe')

# Generate OWHM input files from a FloPy model (to be implemented)
owhm.write_input_files(flopy_model)

# Run the model
owhm.run_model()

# Parse outputs (to be implemented)
results = owhm.read_outputs()
```

## Output Parsing
The interface can parse OWHM output files (e.g., FMPWB.CSV, MAW.CSV) and return results as Pandas DataFrames:

```python
results = owhm.read_outputs(workspace='C:/path/to/model')
fmp_df = results['fmp']  # Farm Process results (DataFrame)
maw_df = results['maw']  # Multi-Aquifer Well results (DataFrame)
```

- Output files must be in CSV format (comment lines starting with # or ! are ignored).
- If a file is missing or cannot be parsed, the result will be None.

## Requirements
- Python 3.8+
- Windows OS
- [FloPy](https://github.com/modflowpy/flopy)
- [MF-OWHM](https://code.usgs.gov/modflow/mf-owhm)

## License
MIT (or as appropriate) 