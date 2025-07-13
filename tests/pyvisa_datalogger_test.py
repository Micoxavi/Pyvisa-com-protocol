""" Pova de comunicació amb datalogger """

import time
import pyvisa
from pyvisa.constants import Parity

rm = pyvisa.ResourceManager()
print(rm.list_resources())

NUMERO_INSTRUMENTOS = 0
CODIGO_INSTRUMENTO = {}  # Dict which realtes code with instrument name
CANALES = 3
DE_GOLPE = True

if isinstance(rm.list_resources(), tuple):
    # Check for connected instruments
    NUMERO_INSTRUMENTOS = len(rm.list_resources())
    print(f"Equipos encontrados {NUMERO_INSTRUMENTOS}: ")

    for instrumento in rm.list_resources():
        match instrumento:
            case 'ASRL5::INSTR':
                print('Datalogger')
                datalogger = rm.open_resource(instrumento, baud_rate=57600,
                                              data_bits=8,
                                              write_termination='\n',
                                              read_termination='\n',
                                              parity=Parity.none)
            case other:
                print("Equipo no reconocido")

# Set datalogger channel 101 configuration to volts DC
datalogger.write('SENse:FUNCtion "VOLT:DC", (@101)')

# Set datalogger channel 102 configuration to Temperature t-couple = default
datalogger.write('SENse:FUNCtion "TEMPerature", (@102)')

# Set datalogger channel 102 configuration to Temperature with type K t-couple
datalogger.write('SENSe:TEMPerature:TRANsducer:TC:TYPE K, (@102)')

# Confirure channel to register temperature with a type K thermocouple
datalogger.write('CONF:TEMP TC,TYPE K (@102)')

# # query() function send message and returns the values.
# print(datalogger.query("TEMPerature:TRANsducer:TC:TYPE? (@102)"))

# time.sleep(2)
# # To ask the termocouple type
# print(datalogger.query("TEMPerature:TRANsducer:TC:TYPE? (@102)"))

# Configure datalogger to read
datalogger.write('CONF:VOLTage DC (@102)')
datalogger.write('CONF:CURRent DC (@121)')

INTERVALS_SECONDS = 0.5  # Delay in secs, between scans
NUMBER_SCANS = 3  # Number of scan sweeps to measure
CHANNEL_DELAY = 0.1  # Delay, in secs, between relay closure and measurement
POINTS = 0  # number of data POINTS stored
SCAN_LIST = '(@101,102,121)'

# define which channels to scan
datalogger.write("ROUTE:SCAN " + SCAN_LIST)

# Read the measurement time
datalogger.write("FORMat:READing:CHANnel ON")

# set a Delay, in secs, between relay closure and measurement
datalogger.write("ROUT:CHAN:DELAY " + str(CHANNEL_DELAY) + "," + SCAN_LIST)

# set the number of scanns
datalogger.write("TRIG:COUNT " + str(NUMBER_SCANS))

# set the time interval between measurements. It cannot be smaller than the
# channel delay.
datalogger.write("TRIG:SOUR TIMER")
datalogger.write("TRIG:TIMER " + str(INTERVALS_SECONDS))

# example of point reading:
if not DE_GOLPE:
    # initialize the readings
    datalogger.write("INIT")

    for _ in range(NUMBER_SCANS):

        while POINTS == 0:
            # check if there are stored points in the memory
            POINTS = int(datalogger.query("DATA:POINTS?").replace("\r", ""))

        print("...")
        for _ in range(CANALES):
            time.sleep(0.25)
            # read and remove the stored points
            print(datalogger.query('DATA:REMOVE? 1'))
            POINTS = 0

else:
    # initialize the readings
    datalogger.write("INIT")
    time.sleep(1)
    # gather all measurements
    print(datalogger.query('FETCh?'))

datalogger.write('SYSTem:LOCal')
# datalogger.write('SYSTem:REMote')
datalogger.close()
