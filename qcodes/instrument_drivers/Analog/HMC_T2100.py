from qcodes import VisaInstrument
from qcodes.utils.validators import Numbers
"""Driver for the Hittite/Analog HMC-T2100 signal generator"""


class HMC_T2100(VisaInstrument):
    """Minimal driver for the Hittite/Analog HMC-T2100 signal generator,
    probably will work with more recent models"""

    def __init__(self, name, address, **kwargs):
        super().__init__(name, address, terminator='\n', **kwargs)

        self.add_parameter('power',
                           label='Power',
                           get_cmd='SOUR:POW?',
                           get_parser=float,
                           set_cmd='SOUR:POW {:.1f}',
                           unit='dBm',
                           vals=Numbers(min_value=-15, max_value=26))

        self.add_parameter('frequency',
                           label='Frequency',
                           get_cmd='SOUR:FREQ?',
                           get_parser=float,
                           set_cmd='SOUR:FREQ {:.6f}',
                           unit='Hz',
                           vals=Numbers(min_value=10e6, max_value=20e9))

        self.add_parameter('rf_output',
                           get_cmd='OUTP:STAT?',
                           set_cmd='OUTP:STAT {}',
                           val_mapping={'on': 1, 'off': 0})

        self.connect_message()

    def get_idn(self):
        IDN = self.ask_raw('*IDN?')
        vendor, model, serial, firmware = map(str.strip, IDN.split(','))
        IDN = {'vendor': vendor, 'model': model,
               'serial': serial, 'firmware': firmware}
        return IDN