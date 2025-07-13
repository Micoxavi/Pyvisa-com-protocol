import time
import pyvisa
from pyvisa.constants import Parity
from visa_instruments import Comunication, DataLogger
# rm = pyvisa.ResourceManager()
# # La funció ResourceManager s'obté la matriu d'informació dels elements
# # connectats al ordinador compatibles amb pyvisa.

# print(rm.list_resources())
# # La funció list_resources() genera una tupla amb tots el instruments
# # connectats. En cas de no trobar cap, es genera una variable buida.

# # Per a comprobar la comunicació correcte entre dispositius i
# # ordinador, es farà servir la funció isinstance() que comproba el
# # tipus de una variable, en aquest cas de una tupla. Si
# # list_resources() no és una tupla, no hi haurà una bona comunicació.

# # ATENCIÓ: El datalogger apareix sempre com connectat potser degut al
# #          software del keysight. Pot ser que aparegui error de
# #          connexió degut a això.

# if isinstance(rm.list_resources(), tuple):

#     NUMERO_INSTRUMENTOS = len(rm.list_resources())
#     print(f"Número d'aparells connectats: {NUMERO_INSTRUMENTOS}")

#     for instrumento in rm.list_resources():

#         match instrumento:
#             # Es recorren els elements de la tupla per a mirar quins
#             # aparells s'han connectat i assignar-los a una variable
#             # amb la que treballar. Els casos a comparar son els
#             # obtinguts amb el mètode rm.list_resources()

#             case 'ASRL5::INSTR':
#                 print('HP Datalogger')
#                 hp_datalogger = rm.open_resource(instrumento,
#                                                  baud_rate=57600,
#                                                  data_bits=8,
#                                                  write_termination='\n',
#                                                  read_termination='\n',
#                                                  parity=Parity.none)

#             case 'ASRL4::INSTR':
#                 print('Power Supply')
#                 power_supply = rm.open_resource(instrumento)

#             case other:
#                 print("Instrument no reconegut.")
# else:
#     print("Error de comunicació: No s'ha trobat cap instrument.")

dispositivos = Comunication
dispositivos.comunicate()

for dispositivo in dispositivos.conected_devices:
    # print(dispositivo)
    # print(dispositivos.conected_devices[dispositivo])
    match dispositivo:
        case 'HEWLETT-PACKARD,34970A,0,3-1-2\r':
            # print(dispositivos.conected_devices[dispositivo])
            d1 = DataLogger(dispositivos.conected_devices[dispositivo])
            # print(d1.channel_delay_seconds)
