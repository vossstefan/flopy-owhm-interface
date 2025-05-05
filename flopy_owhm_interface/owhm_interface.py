import subprocess
from typing import Optional, Dict
import pandas as pd
import logging
from .fmp_writer import write_fmp_input
from .maw_writer import write_maw_input
from .sfr_writer import write_sfr_input
from .swr_writer import write_swr_input
from .lake_writer import write_lake_input
from .drn_writer import write_drn_input
from .res_writer import write_res_input
from .water_accounting_writer import write_water_accounting_input
from .output_parsers import (
    parse_sfr_output, parse_swr_output, parse_lak_output,
    parse_drn_output, parse_res_output, parse_accounting_output
)

class OWHMInterface:
    """
    Interface for running MODFLOW-OWHM (MF-OWHM) models and integrating with FloPy.
    """
    def __init__(self, owhm_exe_path: str):
        self.owhm_exe_path = owhm_exe_path
        # Set up logging
        self.logger = logging.getLogger("OWHMInterface")
        if not self.logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        # TODO: Store model workspace, input/output file paths, etc.

    def write_input_files(self, flopy_model, workspace: Optional[str] = None, water_accounting: Optional[dict] = None):
        """
        Generate OWHM input files from a FloPy model, including FMP, MAW, SFR, SWR, LAK, DRN, RES, and water accounting support.
        """
        if hasattr(flopy_model, 'fmp') and flopy_model.fmp is not None:
            output_path = 'FMP.dat' if workspace is None else f'{workspace}/FMP.dat'
            write_fmp_input(flopy_model.fmp, output_path)
            self.logger.info(f"Wrote FMP input to {output_path}")
        if hasattr(flopy_model, 'maw') and flopy_model.maw is not None:
            output_path = 'MAW.dat' if workspace is None else f'{workspace}/MAW.dat'
            write_maw_input(flopy_model.maw, output_path)
            self.logger.info(f"Wrote MAW input to {output_path}")
        if hasattr(flopy_model, 'sfr') and flopy_model.sfr is not None:
            output_path = 'SFR.dat' if workspace is None else f'{workspace}/SFR.dat'
            write_sfr_input(flopy_model.sfr, output_path)
            self.logger.info(f"Wrote SFR input to {output_path}")
        if hasattr(flopy_model, 'swr') and flopy_model.swr is not None:
            output_path = 'SWR.dat' if workspace is None else f'{workspace}/SWR.dat'
            write_swr_input(flopy_model.swr, output_path)
            self.logger.info(f"Wrote SWR input to {output_path}")
        if hasattr(flopy_model, 'lak') and flopy_model.lak is not None:
            output_path = 'LAK.dat' if workspace is None else f'{workspace}/LAK.dat'
            write_lake_input(flopy_model.lak, output_path)
            self.logger.info(f"Wrote LAK input to {output_path}")
        if hasattr(flopy_model, 'drn') and flopy_model.drn is not None:
            output_path = 'DRN.dat' if workspace is None else f'{workspace}/DRN.dat'
            write_drn_input(flopy_model.drn, output_path)
            self.logger.info(f"Wrote DRN input to {output_path}")
        if hasattr(flopy_model, 'res') and flopy_model.res is not None:
            output_path = 'RES.dat' if workspace is None else f'{workspace}/RES.dat'
            write_res_input(flopy_model.res, output_path)
            self.logger.info(f"Wrote RES input to {output_path}")
        if water_accounting is not None:
            output_path = 'ACCOUNTING.dat' if workspace is None else f'{workspace}/ACCOUNTING.dat'
            write_water_accounting_input(water_accounting, output_path)
            self.logger.info(f"Wrote water accounting input to {output_path}")
        # TODO: Add more package writers for drains, reservoirs, advanced boundaries, etc.

    def run_model(self, workspace: Optional[str] = None):
        """
        Run the MF-OWHM executable in the specified workspace. Logs output and errors.
        """
        cmd = [self.owhm_exe_path]
        try:
            self.logger.info(f"Running MF-OWHM: {' '.join(cmd)} in {workspace or '.'}")
            result = subprocess.run(cmd, cwd=workspace, check=True, capture_output=True, text=True)
            self.logger.info("MF-OWHM run completed successfully.")
            if result.stdout:
                self.logger.info(f"MF-OWHM output:\n{result.stdout}")
            if result.stderr:
                self.logger.warning(f"MF-OWHM errors:\n{result.stderr}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"MF-OWHM run failed: {e}")
            if e.stdout:
                self.logger.error(f"Output:\n{e.stdout}")
            if e.stderr:
                self.logger.error(f"Errors:\n{e.stderr}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error running MF-OWHM: {e}")
            raise

    def read_outputs(self, workspace: Optional[str] = None,
                     fmp_output: Optional[str] = None,
                     maw_output: Optional[str] = None,
                     sfr_output: Optional[str] = None,
                     swr_output: Optional[str] = None,
                     lak_output: Optional[str] = None,
                     drn_output: Optional[str] = None,
                     res_output: Optional[str] = None,
                     accounting_output: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """
        Parse OWHM output files and return results as Pandas DataFrames.
        User can specify output file paths or use defaults.
        Returns a dict with keys for each supported output type.
        """
        results = {}
        # FMP
        fmp_path = fmp_output or (f'{workspace}/FMPWB.CSV' if workspace else 'FMPWB.CSV')
        try:
            results['fmp'] = _parse_csv_output(fmp_path)
            self.logger.info(f"Parsed FMP output from {fmp_path}")
        except Exception as e:
            self.logger.warning(f"Could not parse FMP output: {e}")
            results['fmp'] = None
        # MAW
        maw_path = maw_output or (f'{workspace}/MAW.CSV' if workspace else 'MAW.CSV')
        try:
            results['maw'] = _parse_csv_output(maw_path)
            self.logger.info(f"Parsed MAW output from {maw_path}")
        except Exception as e:
            self.logger.warning(f"Could not parse MAW output: {e}")
            results['maw'] = None
        # SFR
        sfr_path = sfr_output or (f'{workspace}/SFR.CSV' if workspace else 'SFR.CSV')
        try:
            results['sfr'] = parse_sfr_output(sfr_path)
            self.logger.info(f"Parsed SFR output from {sfr_path}")
        except Exception as e:
            self.logger.warning(f"Could not parse SFR output: {e}")
            results['sfr'] = None
        # SWR
        swr_path = swr_output or (f'{workspace}/SWR.CSV' if workspace else 'SWR.CSV')
        try:
            results['swr'] = parse_swr_output(swr_path)
            self.logger.info(f"Parsed SWR output from {swr_path}")
        except Exception as e:
            self.logger.warning(f"Could not parse SWR output: {e}")
            results['swr'] = None
        # LAK
        lak_path = lak_output or (f'{workspace}/LAK.CSV' if workspace else 'LAK.CSV')
        try:
            results['lak'] = parse_lak_output(lak_path)
            self.logger.info(f"Parsed LAK output from {lak_path}")
        except Exception as e:
            self.logger.warning(f"Could not parse LAK output: {e}")
            results['lak'] = None
        # DRN
        drn_path = drn_output or (f'{workspace}/DRN.CSV' if workspace else 'DRN.CSV')
        try:
            results['drn'] = parse_drn_output(drn_path)
            self.logger.info(f"Parsed DRN output from {drn_path}")
        except Exception as e:
            self.logger.warning(f"Could not parse DRN output: {e}")
            results['drn'] = None
        # RES
        res_path = res_output or (f'{workspace}/RES.CSV' if workspace else 'RES.CSV')
        try:
            results['res'] = parse_res_output(res_path)
            self.logger.info(f"Parsed RES output from {res_path}")
        except Exception as e:
            self.logger.warning(f"Could not parse RES output: {e}")
            results['res'] = None
        # Water Accounting
        acc_path = accounting_output or (f'{workspace}/ACCOUNTING.CSV' if workspace else 'ACCOUNTING.CSV')
        try:
            results['accounting'] = parse_accounting_output(acc_path)
            self.logger.info(f"Parsed water accounting output from {acc_path}")
        except Exception as e:
            self.logger.warning(f"Could not parse water accounting output: {e}")
            results['accounting'] = None
        return results

def _parse_csv_output(path: str) -> pd.DataFrame:
    """
    Parse a CSV output file and return as a Pandas DataFrame.
    Handles comment lines and missing values.
    """
    with open(path, 'r') as f:
        lines = [line for line in f if not line.strip().startswith(('#', '!'))]
    from io import StringIO
    data = StringIO(''.join(lines))
    df = pd.read_csv(data)
    return df 