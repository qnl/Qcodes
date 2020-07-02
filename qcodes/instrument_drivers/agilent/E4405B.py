from numpy import pi

from qcodes import VisaInstrument, validators as vals


class E4405B(VisaInstrument):
    """
    This is the code for Agilent/Hewlet-Packard E4405B Spectrum analyzer
    """

    def __init__(self, name, address, **kwargs):
        super().__init__(name, address,  terminator='\n', **kwargs)

        # general commands
        self.add_parameter(name='start_frequency',
                           label='start_frequency',
                           unit='Hz',
                           get_cmd='FREQ:STAR?',
                           set_cmd='FREQ:STAR {}',
                           get_parser=float,
                           vals=vals.Numbers(min_value=100,
                                        max_value=13.2e9))

        self.add_parameter(name='stop_frequency',
                           label='stop_frequency',
                           unit='Hz',
                           get_cmd='FREQ:STOP?',
                           set_cmd='FREQ:STOP {}',
                           get_parser=float,
                           vals=vals.Numbers(min_value=1,
                                        max_value=13.2e9))

        self.add_parameter(name='center_frequency',
                           label='center_frequency',
                           unit='Hz',
                           get_cmd='FREQ:CENTer?',
                           set_cmd='FREQ:CENTer {}',
                           get_parser=float,
                           vals=vals.Numbers(min_value=1,
                                        max_value=13.2e9))

        self.add_parameter(name='span',
                           label='span',
                           unit='Hz',
                           get_cmd='FREQ:SPAN?',
                           set_cmd='FREQ:SPAN {}',
                           get_parser=float,
                           vals=vals.Numbers(min_value=1,
                                        max_value=13.2e9))

        self.add_parameter(name='resolution_bandwidth',
                           label='resolution_bandwidth',
                           unit='Hz',
                           get_cmd='BAND?',
                           set_cmd='BAND {}',
                           get_parser=float,
                           vals=vals.Numbers(min_value=1,
                                        max_value=13.2e9))

        self.add_parameter(name='marker_position',
                           label='marker_position',
                           unit='Hz',
                           get_cmd=':CALC:MARK:X?',
                           set_cmd=':CALC:MARK:MODE POS;:CALC:MARK:X {};',
                           get_parser=float,
                           vals=vals.Numbers(min_value=1,
                                             max_value=13.2e9))

        self.add_parameter(name='marker_high',
                           label='marker_high',
                           unit='dBm',
                           get_cmd=':CALC:MARK:Y?',
                           get_parser=float,
                           vals=vals.Numbers(-100, 20))

    def disconnect(self):
        """Disconnect from the instrument, thereby allowing new instruments to connect"""
        self.__del__()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.disconnect()