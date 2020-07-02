# -*- coding: utf-8 -*-
from qcodes import VisaInstrument
from qcodes.utils.validators import Numbers


class N5183A(VisaInstrument):
    """
    This is an adaptation of original Keysight N5183B qcodes driver for 
    Keysight/Agilent RF source N5183A
    """

    def __init__(self, name, address, **kwargs):
        super().__init__(name, address, terminator='\n', **kwargs)

        self.add_parameter('power',
                           label='Power',
                           get_cmd='SOUR:POW?',
                           get_parser=float,
                           set_cmd='SOUR:POW {:.2f}',
                           unit='dBm',
                           vals=Numbers(min_value=-144,max_value=19))

        # Query the instrument to see what frequency range was purchased
        freq_dict = {'501':1e9, '503':3e9, '505':6e9, '520':20e9}

        freq_info = self.ask('*OPT?').split(sep=',')
        max_freq = freq_dict[freq_info[0]]
        self.add_parameter('frequency',
                           label='Frequency',
                           get_cmd='SOUR:FREQ?',
                           get_parser=float,
                           set_cmd='SOUR:FREQ {:.2f}',
                           unit='Hz',
                           vals=Numbers(min_value=9e3,max_value=max_freq))   
        
        self.add_parameter('phase_offset',
                           label='Phase Offset',
                           get_cmd='SOUR:PHAS?',
                           get_parser=float,
                           set_cmd='SOUR:PHAS {:.2f}',
                           unit='rad'
                           )

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

