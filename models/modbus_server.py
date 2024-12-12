from PyQt5.QtCore import QObject, pyqtSignal
from pymodbus.client import ModbusSerialClient as ModbusClient
from controls.config_manager import ConfigManager

class ModbusServer(QObject):
    errorOccurred = pyqtSignal(str)
    serverRegisterAnswer = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modbus_client = None
        config = ConfigManager()

        self.m_port = config.get_port()
        self.m_baudRate = config.get_baud_rate()
        self.m_parity = config.get_parity()
        self.m_stopBits = config.get_stop_bits()
        self.m_dataBits = config.get_data_bits()
        self.m_timeout = config.get_timeout()
        self.m_retries = config.get_retries()
        

    def __del__(self):
        if self.modbus_client:
            self.modbus_client.close()

    def connect_modbus(self, port):
        print("connectModbus")

        if not self.modbus_client:
            self.modbus_client = ModbusClient(
                #method='rtu',
                port=port,
                baudrate=self.m_baudRate,
                parity=self.m_parity,
                stopbits=self.m_stopBits,
                bytesize=self.m_dataBits,
                timeout=self.m_timeout
            )

        if not self.modbus_client.connect():
            print("connection err")
            self.errorOccurred.emit("Connection error")
            #return False

        print("Modbus Connected")
        return True

    def handle_read_registers(self, start_address, number_of_registers, slave_id):
        register_values = []

        if self.modbus_client:
            result = self.modbus_client.read_holding_registers(
                address=start_address,
                count=number_of_registers,
                unit=slave_id
            )

            if not result.isError():
                print("Reading registers requested. --------------------------")
                for i in range(number_of_registers):
                    register_values.append(result.getRegister(i))

                self.serverRegisterAnswer.emit(register_values)
            else:
                print(f"Error while reading registers: {result}")
                self.errorOccurred.emit(str(result))