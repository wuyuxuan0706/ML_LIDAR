import os
import struct as st

import numpy as np


class ReadMcsFiles():
    def __init__(self, mcs_path):
        self.mcs_path = mcs_path
        self.plc = None
        self.ph = None

    def extract_para(self):
        mcs_files = os.listdir(self.mcs_path)
        self.plc = np.zeros((len(mcs_files),), dtype=int)  # Pass Length in channels
        pcp = np.zeros((len(mcs_files),), dtype=int)  # Pass Count Preset
        str_time = ['NaN'] * len(mcs_files)  # Start Time
        str_date = ['NaN'] * len(mcs_files)  # Start Date

        for ifile in range(len(mcs_files)):
            file_path = os.path.join(self.mcs_path, mcs_files[ifile])
            try:
                with open(file_path, 'rb') as fid:
                    # Read and unpack the first 2 bytes for plc
                    fid.seek(10, 0)
                    data = fid.read(2)
                    if len(data) == 2:
                        self.plc[ifile] = np.array(st.unpack('1h', data))[0]
                    else:
                        print(
                            f"Warning: Insufficient data for plc in file {mcs_files[ifile]}. Expected 2 bytes, got {len(data)} bytes.")

                    # Read and unpack the next 4 bytes for pcp
                    fid.seek(16, 0)
                    data = fid.read(4)
                    if len(data) == 4:
                        pcp[ifile] = np.array(st.unpack('1i', data))[0]
                    else:
                        print(
                            f"Warning: Insufficient data for pcp in file {mcs_files[ifile]}. Expected 4 bytes, got {len(data)} bytes.")

                    # Read and unpack the 8 bytes for str_time
                    fid.seek(20, 0)
                    data = fid.read(8)
                    if len(data) == 8:
                        str_time[ifile] = st.unpack('2s1s2s1s2s', data)
                    else:
                        print(
                            f"Warning: Insufficient data for str_time in file {mcs_files[ifile]}. Expected 8 bytes, got {len(data)} bytes.")

                    # Read and unpack the 8 bytes for str_date
                    fid.seek(28, 0)
                    data = fid.read(8)
                    if len(data) == 8:
                        str_date[ifile] = st.unpack('2s2s4s', data)
                    else:
                        print(
                            f"Warning: Insufficient data for str_date in file {mcs_files[ifile]}. Expected 8 bytes, got {len(data)} bytes.")

            except Exception as e:
                print(f"Error processing file {mcs_files[ifile]}: {e}")

        return self.plc, pcp, str_time, str_date

    def extract_photoncounts(self):
        mcsfiles = os.listdir(self.mcs_path)
        self.ph = np.zeros((self.plc[0], len(mcsfiles)), dtype=int)
        for itick in range(len(mcsfiles)):
            file_path = os.path.join(self.mcs_path, mcsfiles[itick])
            with open(file_path, 'rb') as fid:
                fid.seek(256, 0)
                self.ph[:, itick] = np.array(st.unpack(str(self.plc[0]) + 'i', fid.read(self.plc[0] * 4)))
        return self.ph
