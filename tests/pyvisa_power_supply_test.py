''' Prova de comunicació amb la font de quatre canals '''
import time
import pyvisa

NUMERO_INSTRUMENTOS = 0

rm = pyvisa.ResourceManager()  # Function used to open the communication
print(rm.list_resources())  # Print the list with all the connected instruments

if isinstance(rm.list_resources(), tuple):  # Check for connected instruments
    NUMERO_INSTRUMENTOS = len(rm.list_resources())
    print(f"Equipos encontrados {NUMERO_INSTRUMENTOS}: ")

    for instrumento in rm.list_resources():
        match instrumento:

            case 'ASRL4::INSTR':
                print('Power Supply')
                power_supply = rm.open_resource('ASRL4::INSTR')

            case other:
                print("Equipo no reconocido")

# Set voltage

# power_supply.write("VSET2:10.5")
# power_supply.write("VSET1:9")

# power_supply.write("ISET1:0.05")
power_supply.write("VSET1:13")
time.sleep(1)

NORMAL = power_supply.query("VOUT1?")
print(f"Normal voltage: {NORMAL}")
time.sleep(1)

power_supply.write("VSET1:20")
time.sleep(2)

HIGH_VOLTAGE = power_supply.query("VOUT1?")
print(f'High voltage: {HIGH_VOLTAGE}')
time.sleep(5)

# power_supply.write("OUT0:1")
# time.sleep(1)

# power_supply.write("OUT1:1")
# time.sleep(1)

# set a step increment or decrement.
# First letter --> V = Voltage | I = Current
# First number --> channel
# After the collon (:) start value, end value, setp value, time value
power_supply.write("VASTEP1:1,30,1,1")
time.sleep(2.5)

NEW_VOLTAGE = power_supply.query("VOUT1?")
time.sleep(1)

while NEW_VOLTAGE != HIGH_VOLTAGE:
    NEW_VOLTAGE = power_supply.query("VOUT1?")
    print(NEW_VOLTAGE)
    time.sleep(0.5)

power_supply.write("VASTEP1:30,1,1,1")
time.sleep(2.5)

while NEW_VOLTAGE != NORMAL:
    NEW_VOLTAGE = power_supply.query("VOUT1?")
    print(NEW_VOLTAGE)
    time.sleep(0.5)

power_supply.write("VASTOP1")

print(f'Resultat final: {power_supply.query("VOUT1?")}')
