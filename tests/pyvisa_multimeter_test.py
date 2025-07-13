""" Prova de comunicació amb el multimetre """

# import time
import pyvisa

NUMERO_INSTRUMENTOS = 0

rm = pyvisa.ResourceManager()  # Function used to open the communication
print(rm.list_resources())  # Print the list with all the connected instruments

if isinstance(rm.list_resources(), tuple):
    NUMERO_INSTRUMENTOS = len(rm.list_resources())
    print(f"Dispositivos encontrados: {NUMERO_INSTRUMENTOS}")

    for instrumento in rm.list_resources():
        match instrumento:

            case 'ASRL3::INSTR':
                print('Datalogger')

            case 'USB0::0x2A8D::0x1301::MY57216075::INSTR':
                NOMBRE = 'USB0::0x2A8D::0x1301::MY57216075::INSTR'
                print('Multimeter')
                multimeter = rm.open_resource(f'{NOMBRE}')

            case other:
                print('Equipo no reconocido')

else:
    print("No s'ha trobat cap instrument.")

# multimeter.write('CONFigure:VOLTage:DC')
# multimeter.write('CONFigure:VOLTage:AC')

# multimeter.write('CONFigure:CURRent:DC')
# multimeter.write('CONFigure:CURRent:AC')


multimeter.write('SYSTem:LOCal')
# multimeter.write('SYSTem:REMote')


print("Voltege set up")
