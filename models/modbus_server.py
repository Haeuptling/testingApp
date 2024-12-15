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


        self.baudRate = config.get_baud_rate()
        self.parity = config.get_parity()
        self.stop_bits = config.get_stop_bits()
        self.data_bits = config.get_data_bits()
        self.timeout = config.get_timeout()
        self.retries = config.get_retries()
        

    def __del__(self):
        if self.modbus_client:
            self.modbus_client.close()

    def connect_modbus(self, port):
        print("connectModbus")

        if not self.modbus_client:
            self.modbus_client = ModbusClient(
                method='rtu',
                port=port,
                baudrate=self.baudRate,
                parity=self.parity,
                stopbits=self.stop_bits,
                bytesize=self.data_bits,
                timeout=self.timeout
            )

        if not self.modbus_client.connect():
            print("connection err")
            self.errorOccurred.emit("Connection error")
            #return False

        print("Modbus Connected")
        return True

    """"
    Liest die angeforderten Register aus und sendet die Werte zurück.
    :param start_address: Die Startadresse der zu lesenden Register.
    :param number_of_registers: Die Anzahl der zu lesenden Register.
    :param slave_id: Die Slave-ID des Modbus-Geräts.
    """
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