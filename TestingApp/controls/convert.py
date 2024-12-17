import struct

def hex_to_float(hex_val):
    if hex_val.startswith('0x'):
        hex_val = hex_val[2:]
    
    hex_val = hex_val.zfill(8)
    
    bytes_val = bytes.fromhex(hex_val)
    
    float_val = struct.unpack('!f', bytes_val)[0]
    
    return float_val

def decimal_to_hex(decimal_val, length=4):
    hex_val = hex(decimal_val)[2:] 
    padded_hex_val = hex_val.zfill(length)
    return padded_hex_val.upper() 

def hex_to_decimal(hex_val):
    decimal_val = int(hex_val, 16)
    return decimal_val


hex_val = decimal_to_hex(45242)+  decimal_to_hex(36720)
print(hex_val)  #



print(hex_to_float(hex_val))

# print(decimal_to_hex(16542))  # Ausgabe: 00E8

# def generate_decimal(input_number):
#     """
#     Diese Funktion generiert Dezimalzahlen basierend auf der Eingabe:
#     :param input_number: Zahl zwischen 0 und 4
#     :return: Generierte Dezimalzahl
#     """
#     if not (0 <= input_number <= 4):
#         raise ValueError("Die Eingabe muss zwischen 0 und 4 liegen.")

#     # Berechnung der Dezimalzahl
#     return 10 ** -input_number

# print(generate_decimal(0))  # Ausgabe: 1
# print(generate_decimal(2))  # Ausgabe: 0.01
# print(generate_decimal(3))  # Ausgabe: 0.001
# print(generate_decimal(4))  # Ausgabe: 0.0001
# print(generate_decimal(5))  # ValueError: Die Eingabe muss zwischen 0 und 4 liegen.
