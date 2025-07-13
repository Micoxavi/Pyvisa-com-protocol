"""
Exemple de test automatitzat de recollida de dades de temperatura i de
corrent per a diferents voltatges de funcionament. Els instruments utilitzats
per aquest  exemple són: Datalogger 34970A i Font programable RS-A3305P.
"""

# El primer pas es importar les llibreries. Es faran servir 2: pyvisa i time
import time
# Time es la llibreria integrada de python que permet crear delays entre les
# linees de codi. Aquesta es farà servir per a donar temps a l'instrument al
# que enviem les comandes a assimilar la primera ordre abans d'enviar una
# segona.

import pyvisa
# Pyvisa llibreria es fa servir per a la comunicació entre Dispositiu - PC.
# De tots els mètodes que proporciona es faran servir 5:

from pyvisa.constants import Parity
# S'importa el mètode Parity per a configurar el datalogger.

# METODES DE PYVISA:

#   ResourceManarger(), list_resources(), open_resource() --> per a establir
#                                                             comunicació
#   write(), query() --> per a enviar i rebre dades.

# --------------------------------------------------------------------------- #

# El segon pas és importar els instruments que es vulguin fer servir. Per a
# aquest exemple caldrà importar Datalogger i PowerSupply del fitxer
# visa_instruments.py

# Per últim cal importar CsvMaker, que és la classe que escriu les dades a
# excel, i list_formater, que és el mètode que prepara les dades per a
# escriure-les al csv.

from visa_instruments import DataLogger, PowerSupply
from csv_editor import CsvMaker, list_formater

# Inicialització del programa:
if __name__ == "__main__":
    # Linia de protecció no permet executar el codi desde un altre arxiu que
    # el cridi.

    CANALS_MESURA = 3  # Definim el número de canals on registrarem
    total_mesures = []  # Definim una llista per a més endavant.
    r_man = pyvisa.ResourceManager()
    # La funció ResourceMan s'obté la matriu d'informació dels elements
    # connectats al ordinador compatibles amb pyvisa.

    print(r_man.list_resources())
    # La funció list_resources() genera una tupla amb tots el instruments
    # connectats. En cas de no trobar cap, es genera una variable buida.

    # Per a comprobar la comunicació correcte entre dispositius i
    # ordinador, es farà servir la funció isinstance() que comproba el
    # tipus de una variable, en aquest cas de una tupla. Si
    # list_resources() no és una tupla, no hi haurà una bona comunicació.

    # ATENCIÓ: El datalogger apareix sempre com connectat potser degut al
    #          software del keysight. Pot ser que aparegui error de
    #          connexió degut a això.

    if isinstance(r_man.list_resources(), tuple):

        numero_instrumentos = len(r_man.list_resources())
        print(f"Número d'aparells connectats: {numero_instrumentos}")

        for instrumento in r_man.list_resources():

            match instrumento:
                # Es recorren els elements de la tupla per a mirar quins
                # aparells s'han connectat i assignar-los a una variable
                # amb la que treballar. Els casos a comparar son els
                # obtinguts amb el mètode r_man.list_resources()

                case 'ASRL7::INSTR':
                    print('Datalogger')
                    try:
                        datalogger = r_man.open_resource(
                            instrumento,
                            baud_rate=57600,
                            data_bits=8,
                            write_termination='\n',
                            read_termination='\n',
                            parity=Parity.none)

                    except pyvisa.VisaIOError:
                        print("No s'ha trobat cap dispositiu. ")
                        #  sys.exit()

                case 'ASRL4::INSTR':
                    print('Power Supply')
                    power_supply = r_man.open_resource(instrumento)

                case other:
                    print("Instrument no reconegut.")
    else:
        raise pyvisa.VisaIOError

    # Cridem l'objecte Datalogger i l'introduim les dades obtingudes amb
    # el pyvisa
    d1 = DataLogger(datalogger)

    # Cridem l'objecte PowerSupply i l'introduim les dades obtingudes amb
    # el pyvisa
    power = PowerSupply(power_supply)

    # CONFIGURACIÓ DATALOGGER

    # print(help(Datalogger))
    # La funció help serveix per a obternir informació de les diferents
    # funcions que tenen els objectes; com pot ser les dades a entrar
    # quan es criden, els paràmetres que retornen etc,.

    d1.set_scan_times(30, 3)
    # Configurar el datalogger per a mesurar durant 5 minuts amb un
    # intervaL de 30s.

    d1.set_channel_param("101", VOLT="DC")
    time.sleep(0.25)
    d1.set_channel_param("102", TEMP="K")
    time.sleep(0.25)
    d1.set_channel_param("122", INT="DC")
    # Canvia el tipus de mesura del dataloggee en el canal especificat
    time.sleep(0.25)

    d1.configure_measure("101", VOLT="DC")
    # Aquesta funció configura el datalogger per a realitzar la mesura.
    # Els parametres que configura són els que s'han definit anteriorment.
    # En cas de no haver definit res, s'estableixen uns parámetres per defecte.

    # d1.configure_measure("101,102,103", "VOLT:DC", n_chan=3)
    # n_chan=x es fa servir quan s'introdueix més de un canal de cop.

    d1.configure_measure("102", TEMP="K")
    # Per a configurar temperatura.

    d1.configure_measure("122", INT="DC", tot=True)
    # tot=True es fa servir quan ja s'han introduït tots els canals.
    # Per defecte te el valor de False.

    # CONFIGURACIÓ FONT

    # print(help(PowerSupply))
    power.set_font(1, V=9, I=0.06)

    # Per a configurar els canals de la font cal perimer escriure
    # el canal 1 o 2, i després les magnituds amb unitats que es
    # volen configurar. Es poden entrar les dos alhora o només una
    # sempre que es segueixi el format correcte.

    # Es crea un loop amb 3 iteracions. A cadascuna d'elles es fa una cicle
    # de medicions. En cas de haver de modificar el voltatge, aquest es
    # modifica abans d'executar el cicle de lectura.

    for increments in range(3):
        if increments == 0:
            # PRIMER_LOOP --> dades del datalogger.
            # TIMESTAMP --> temps absolut de referencia en segons.
            # A la primera iteració es recull el timestamp per a prendre'l
            # com a referencia de l'inici de la prova en tots els loops.
            PRIMER_LOOP, TIMESTAMP = d1.interval_read()
            # Al no enviar un temps de referencia es fa servir el valor per
            # defecte 0,0.
            primera_lista = list_formater(PRIMER_LOOP, CANALS_MESURA)

        elif increments == 1:
            # En el segon loop es modifica el voltatge a 13.5V i es torna
            # a mesurar. El timestamp no el necessitem per això el símbol
            # ( _ ). (no es guarda el valor).
            power.set_font(1, V=13.5)
            SEGON_LOOP, _ = d1.interval_read()
            # Enviem el timestamp de la primera mesura al formater per a
            # tenir la referencia de temps.
            segona_lista = list_formater(
                SEGON_LOOP, CANALS_MESURA, sum_time=TIMESTAMP)

        else:
            # En el tercer loop es puja el voltatje a 16 i es fa servir de
            # nou el timestamp del loop 1.
            power.set_font(1, V=16)
            TERCER_LOOP, _ = d1.interval_read()
            tercera_lista = list_formater(
                TERCER_LOOP, CANALS_MESURA, sum_time=TIMESTAMP)

    # Es recullen totes les mesures ja preparades per a ser escrites al excel
    # i es guarden en una llista.
    for mesures in primera_lista:
        total_mesures.append(mesures)

    for mesures in segona_lista:
        total_mesures.append(mesures)

    for mesures in tercera_lista:
        total_mesures.append(mesures)

    # Es crida la classe creadora de csv i se li introdueix el nom desitjat.
    csv = CsvMaker("prova_1_visa")
    # S'introdueixen el métode d'escriptura, les capçaleres i les dades a
    # escriure en el csv.
    csv.writer("w", ["Temps", "Voltatge", "Temperatura",
               "Intensitat"], total_mesures)
