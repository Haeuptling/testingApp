# def decimal_to_hex(decimal_val, length=4):
#     hex_val = hex(decimal_val)[2:]  # Entfernt das '0x'-Präfix
#     padded_hex_val = hex_val.zfill(length)
#     return padded_hex_val.upper() # Rückgabe des Hexadezimalwerts in Großbuchstaben

# hex_val = decimal_to_hex(65184)
# print(hex_val) 

# print(decimal_to_hex(16542))  # Ausgabe: 00E8

def generate_decimal(input_number):
    """
    Diese Funktion generiert Dezimalzahlen basierend auf der Eingabe:
    :param input_number: Zahl zwischen 0 und 4
    :return: Generierte Dezimalzahl
    """
    if not (0 <= input_number <= 4):
        raise ValueError("Die Eingabe muss zwischen 0 und 4 liegen.")

    # Berechnung der Dezimalzahl
    return 10 ** -input_number

print(generate_decimal(0))  # Ausgabe: 1
print(generate_decimal(2))  # Ausgabe: 0.01
print(generate_decimal(3))  # Ausgabe: 0.001
print(generate_decimal(4))  # Ausgabe: 0.0001
print(generate_decimal(5))  # ValueError: Die Eingabe muss zwischen 0 und 4 liegen.
