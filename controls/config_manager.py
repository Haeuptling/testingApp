import configparser
import os

class SingletonMeta(type):
    """
    Eine Metaklasse für die Implementierung des Singleton-Musters.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class ConfigManager(metaclass=SingletonMeta):
    def __init__(self, config_file='models/config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            self.create_default_config()
        self.config.read(self.config_file)

    def create_default_config(self):
        # Erstellen Sie das Verzeichnis, falls es nicht existiert
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        self.config['General'] = {
            'AppName': 'TestintApp',
            'Version': '1.0.0',
            'CurrentFilePath': ''
        }
        self.config['Settings'] = {
            'WindowWidth': '800',
            'WindowHeight': '480',
            'Fullscreen': 'true'
        }
        self.config['Measurement'] = {
            'TotalDurationMin': '1',
            'IntervalTimeS': '5',
            'MaximumPressureDifferenceInPercent': '3',
            'MaximumHumidityDifferenceInPercent': '3'
        }
        self.config['Modbus'] = {
            'Baudrate': '19200',
            'Framing': '8',
            'Parity': 'N',
            'StopBits': '1',
            'DataBits': '8',
            'Timeout': '2',
            'Retries': '3',
            'PortPressureEmitter': '/dev/ttyUSB0',
            'PortDewpointEmitter': '/dev/ttyUSB1',
            'PressureEmitterSlaveId': '70',
            'PressureEmitterStartAdress': '0',
            'PressureEmitterRegisters': '10',
            'DewpointEmiiterSlaveId': '53',
            'DewpointEmiiterStartAdress': '2000',
            'DewpointEmitterRegisters': '20'
        }
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        
    def get_port_pressure_emitter(self):
        return str(self.config['Modbus']['PortPressureEmitter'])
    
    def get_port_dewpoint_emitter(self):
        return str(self.config['Modbus']['PortDewpointEmitter'])

    def get_total_duration_min(self):
        return int(self.config['Measurement']['TotalDurationMin'])

    def get_interval_time_s(self):
        return int(self.config['Measurement']['IntervalTimeS'])

    def get_pressure_emitter_slave_id(self):
        return int(self.config['Modbus']['PressureEmitterSlaveId'])

    def get_pressure_emitter_start_address(self):
        return int(self.config['Modbus']['PressureEmitterStartAdress'])

    def get_pressure_emitter_registers(self):
        return int(self.config['Modbus']['PressureEmitterRegisters'])

    def get_dewpoint_emitter_slave_id(self):
        return int(self.config['Modbus']['DewpointEmiiterSlaveId'])

    def get_dewpoint_emitter_start_address(self):
        return int(self.config['Modbus']['DewpointEmiiterStartAdress'])

    def get_dewpoint_emitter_registers(self):
        return int(self.config['Modbus']['DewpointEmitterRegisters'])

    def get_port(self):
        return str(self.config['Modbus']['Port'])

    def get_baud_rate(self):
        return int(self.config['Modbus']['BaudRate'])

    def get_parity(self):
        return str(self.config['Modbus']['parity'])

    def get_stop_bits(self):
        return int(self.config['Modbus']['StopBits'])

    def get_data_bits(self):
        return int(self.config['Modbus']['DataBits'])

    def get_timeout(self):
        return int(self.config['Modbus']['Timeout'])

    def get_retries(self):
        return int(self.config['Modbus']['Retries'])
    
    def get_window_width(self):
        return int(self.config['Settings']['WindowWidth'])

    def get_window_height(self):
        return int(self.config['Settings']['WindowHeight'])

    def get_fullscreen(self):
        return self.config['Settings']['Fullscreen'].lower() == 'true'
    
    def get_maximum_pressure_difference_in_percent(self):
        return int(self.config['Measurement']['MaximumPressureDifferenceInPercent'])
    
    def get_maximum_relative_humidity_difference_in_percent(self):
        return int(self.config['Measurement']['MaximumHumidityDifferenceInPercent'])
    
    def get_total_duration_min(self):
        return int(self.config['Measurement']['TotalDurationMin'])
    
    def get_interval_time_s(self):
        return int(self.config['Measurement']['IntervalTimeS'])
    
    def set_maximum_pressure_difference_in_percent(self, value):
        self.config['Measurement']['MaximumPressureDifferenceInPercent'] = str(value)
        self.save_config()

    def set_maximum_relative_humidity_difference_in_percent(self, value):
        self.config['Measurement']['MaximumHumidityDifferenceInPercent'] = str(value)
        self.save_config()
        
    def set_total_duration_min(self, value):
        self.config['Measurement']['TotalDurationMin'] = str(value)
        self.save_config()

    def set_interval_time_s(self, value):
        self.config['Measurement']['IntervalTimeS'] = str(value)
        self.save_config()

    def set_pressure_emitter_slave_id(self, value):
        self.config['DEFAULT']['PressureEmitterSlaveId'] = str(value)
        self.save_config()

    def set_pressure_emitter_start_address(self, value):
        self.config['DEFAULT']['PressureEmitterStartAddress'] = str(value)
        self.save_config()

    def set_pressure_emitter_registers(self, value):
        self.config['DEFAULT']['PressureEmitterRegisters'] = str(value)
        self.save_config()

    def set_dewpoint_emitter_slave_id(self, value):
        self.config['DEFAULT']['DewpointEmitterSlaveId'] = str(value)
        self.save_config()

    def set_dewpoint_emitter_start_address(self, value):
        self.config['DEFAULT']['DewpointEmitterStartAddress'] = str(value)
        self.save_config()

    def set_dewpoint_emitter_registers(self, value):
        self.config['DEFAULT']['DewpointEmitterRegisters'] = str(value)
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)