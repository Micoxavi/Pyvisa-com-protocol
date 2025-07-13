"""
This document contain an object to open and close and edit csv.
"""
import csv
from datetime import datetime


def list_formater(raw_mesures: dict, num_chan: int, sum_time=0.0):
    """
    Funció que formateja les dades que enviar al csv.

    raw_mesures (dict) --> Diccionari amb el timestamp de les mesures com a
                           clau mes les mesures com a valors.

    num_chan (int) --> Número de canals registrats.

    sum_time (float) --> 0.0 per defecte. Es crida quan es vol sumar tenir
                         en compte el temps (timestamp) de un loop anterior
                         en les noves mesures.
    """
    contador = num_chan  # Numero de canals per a dividir la informació
    #                   en bolocs de llistes
    media_tiempo = 0
    llista_temporal_mesures = []
    lista_final = []
    lista_grupos = []  # Llista on guardar la informació dels canals
    #                    per a cada unitat de temps

    for clau, valors in raw_mesures.items():
        for val in valors:

            mesura_sin_unidad = val[0].split(" ")

            if contador == 0:
                for mes in llista_temporal_mesures:
                    lista_grupos.append(mes.replace(".", ","))

                tiempo = media_tiempo/num_chan

                # Mirar si esisteix un registre de un loop anterior. Si no
                # existeix es retorna un 0.

                # Se suma el 0 o el temps del loop anterior al temps actual.
                if sum_time == 0.0:
                    temps_real = str(tiempo).replace(".", ",")

                else:
                    # float(clau) --> timestamp del inici de les mesures en
                    #                 valors absoluts (segons desde 1970)
                    # tiempo --> segons desde el primer registre del loop.
                    # sum_time --> timestamp en valors aboluts del inici del
                    #              primer loop.
                    temps_real = float(clau) + tiempo - sum_time
                    temps_real = str(temps_real).replace(".", ",")

                lista_grupos.insert(0, temps_real)
                lista_final.append(lista_grupos)

                # Reset de les variables per a la seguent mesura
                media_tiempo = 0
                llista_temporal_mesures = []
                contador = num_chan
                lista_grupos = []

            media_tiempo += int(float(val[1])*1000)/1000
            llista_temporal_mesures.append(mesura_sin_unidad[0])
            contador -= 1

    return lista_final


class HeaderError(Exception):
    """
    Raised when the number of headers is smaller than the number of elements

    Atributes:
        message --> error message
    """

    def __init__(self, message) -> None:
        self.message = message

        super().__init__(self.message)


class CsvMaker:
    """
    Aquesta classe conté els paràmetres per a crear mes escriure csv.

    Atributs:
        >name --> nom del dispositiu
        >delimeter --> separador de columnes
        >newline --> caracter de salt de linia
        >encoding --> protocol de codificació dels missatges
        >fecha --> data del dia actual

    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.delimiter = ";"
        self.newline = ""
        self.encoding = "utf-8"
        self.fecha = datetime.today().strftime('%y-%m-%d')

    def configure_csv(
            self, delimiter=";", newline=" ", encoding="utf-8") -> None:
        """
        Congifure the csv parameters.

        delimeter (str): Configura el caràcter que separa els valors.
                             Per defecte --> ";".

        newline (str): Configura el caràcter que marca el salt de linia.
                             Per defecte --> " ".

        encoding (str): Configura el tipus de codificació amb la que
                            escriure el csv. Per defecte --> utf-8.
        """
        self.delimiter = delimiter
        self.newline = newline
        self.encoding = encoding

    def writer(self, w_a: str, *args) -> None:
        """
        Write csv.

        w_a (str): Write mode --> ("w") || Append mode --> ("a")

        args:

            args(0): Llista amb els titols de les columnes a escriure.
                       Ex: titols = ["Voltatge", "Temperatura"]

            args(1): Llista amb els valors registrats

        """
        titles = args[0]

        with open(f"{self.name}_{self.fecha}.csv", mode=w_a,
                  newline=self.newline, encoding=self.encoding) as csvfile:

            writer = csv.writer(csvfile, delimiter=self.delimiter)

            if w_a == "w":
                writer.writerow(titles)
            print(args[1])
            for val in args[1]:
                writer.writerow(val)

    def reader(self) -> None:
        """
        Read csv.
        """
