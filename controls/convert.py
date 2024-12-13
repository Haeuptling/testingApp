def decimal_to_hex(decimal_val, length=4):
    hex_val = hex(decimal_val)[2:]  # Entfernt das '0x'-Präfix
    padded_hex_val = hex_val.zfill(length)
    return padded_hex_val.upper() # Rückgabe des Hexadezimalwerts in Großbuchstaben

hex_val = decimal_to_hex(65184)
print(hex_val) 

print(decimal_to_hex(16542))  # Ausgabe: 00E8