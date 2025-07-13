"""
Aquest fitxer conté totes les funcions dels instruments que es poden comunicar
amb l'ordinador.
"""
import time
import pyvisa
from pyvisa.constants import Parity


class Comunication:
    """
    Aquesta clase s'encarrega de buscar i
    """

    conected_devices = {}
    datalogger_index = []

    def comunicate():

        rm = pyvisa.ResourceManager()

        if isinstance(rm.list_resources(), tuple):
            rang = len(rm.list_resources())
            print(rang)
            Comunication.get_devices(rm, rang)

    def get_devices(rm, rang):

        if Comunication.datalogger_index == []:
            for device in range(rang):
                dev_rute = rm.list_resources()[device]

                try:
                    inst = rm.open_resource(dev_rute)
                    device_name = inst.query("*IDN?")

                    if device_name not in Comunication.conected_devices:
                        Comunication.conected_devices[device_name] = inst
                        print("Other devices: " +
                              Comunication.conected_devices)

                except pyvisa.errors.VisaIOError:
                    Comunication.datalogger_index.append(dev_rute)

                    inst.close()

            print("Dataloggers: " + str(Comunication.datalogger_index))
            Comunication.comunicate()

        else:
            for device in range(rang):
                dev_rute = rm.list_resources()[device]
                print(dev_rute + " Selected")

                if dev_rute in Comunication.datalogger_index:
                    if dev_rute == "ASRL3::INSTR":
                        print(dev_rute + " Passed")

                    else:
                        print(dev_rute + " OK")
                        inst = rm.open_resource(dev_rute,
                                                baud_rate=57600,
                                                data_bits=8,
                                                write_termination='\n',
                                                read_termination='\n',
                                                parity=Parity.none)

                else:
                    inst = rm.open_resource(dev_rute)

                device_name = inst.query("*IDN?")
                Comunication.conected_devices[device_name] = inst


class DataLogger:
    """
    Aquesta classe conté tots els paràmetres de configuració del
    dispositiu 34970A.

    Atributes:
        >channel_delay_seconds (float): Delay entre setup i la primera mesura

    """

    def __init__(self, device) -> None:  # @None --> Return type
        """
        Inicialitza els atributs de la classe.

        Args:
            No arguments
        """
        self.__device: str = device
        self.__number_of_channels: int = 0
        self.__scan_list: str = ""
        self.__delay_seconds: float = 1.0
        self.__number_of_scans: int = 10
        self.channel_delay_seconds: float = 0.1

    def set_scan_times(self, time_in_sec: int, delay_in_sec: int) -> None:
        """
        Calcula el número d'mesures que cal fer tenint en compte el temps
        total de mesura i el delay entre mesures. Per defecte son 10 segons
        de temps total i 1 segon de temps entre mesures

        Args:
            time_in_sec (float): Temps total a escanejar.
            delay_in_sec (float): Interval entre mesures.
        """
        self.__number_of_scans = int(time_in_sec / delay_in_sec)
        self.__delay_seconds = delay_in_sec

    def set_number_of_mesures(self, mesures: int, delay_in_sec: float) -> None:
        """
        Programa el self.__device per a fer les mesures dessitjades i parar.
        Per defecte són 10 mesures i 1 segon de temps entre mesura.

        Args:
            mesures (int): Nombre de mesures a fer.
            delay_in_sec (float): Interval entre mesures.
        """
        self.__number_of_scans = mesures
        self.__delay_seconds = delay_in_sec

    # def set_channel_delay(self, chan_delay_sec: float) -> None:
    #     """
    #     Programa el temps entre la inicialització del procés de mesura
    #     i la primera mesura del self.__device. Per defecte són 0.1 segons.

    #     """
    #     self.channel_delay_seconds = chan_delay_sec

    def set_channel_param(self, can: str, **kwargs) -> None:
        """
        Canvia el tipus de mesura del canal.

        Args:
            canal (str) Canal o llista de canals.
            configure (str) Configuració: VOLT|INT:DC|AC || TEMP.
        """
        for key, value in kwargs.items():
            if str(key) == "TEMP":
                self.__device.write(f'SENse:FUNCtion "TEMPerature", (@{can})')
                s_t = f'SENSe:TEMPerature:TRANsducer:TC:TYPE {value}, (@{can})'
                self.__device.write(s_t)

            else:
                self.__device.write(
                    f'SENse:FUNCtion "{key}:{value}", (@{can})')

        time.sleep(0.25)

    def configure_measure(
            self, canal: str, n_chan=1, tot=False, **kwargs) -> None:
        """
        Formateja a string els canals que s'han de mesurar.

        canal (any): Cal introduir el número, llista o rang de canals
                            amb la configuració dessitjada en format string,
                            separats per un =.
                            Es poden introduir més de un separats per comes.
                            EX de canals: 101 // 101,102,103 // 101:103

        n_chan (int):   Si a canal s'ha introduit més de un canal, cal
                            especificar aquí quants canals s'han entrat.

        kwargs: parametres a mesurar VOLT|INT="DC|AC" || TEMP="J|K|..."
        """

        self.__number_of_channels += n_chan
        self.__scan_list = self.__scan_list + canal

        config = [f"{magnitut}:{unitat}" for magnitut,
                  unitat in kwargs.items()]

        self.__device.write("CONFigure:" + config[0] + "(@" + canal + ")")
        time.sleep(0.1)

        if tot:
            self.__device.write("ROUTE:SCAN " + "(@" + self.__scan_list + ")")
            time.sleep(0.1)
            self.__device.write("FORMat:READing:CHANnel OFF")
            time.sleep(0.1)
            self.__device.write("FORMat:READing:TIME ON")
            time.sleep(0.1)
            self.__device.write("FORMat:READing:ALARm OFF")
            time.sleep(0.1)
            self.__device.write("ROUT:CHAN:DELAY " +
                                str(self.channel_delay_seconds) + ","
                                + "(@" + self.__scan_list + ")")
            time.sleep(0.1)
            self.__device.write("TRIG:COUNT " + str(self.__number_of_scans))
            time.sleep(0.1)
            self.__device.write("TRIG:SOUR TIMER")
            time.sleep(0.1)
            self.__device.write("TRIG:TIMER " + str(self.__delay_seconds))
            time.sleep(0.1)

    def recollir_dades(self) -> dict:
        """
        Measure all the points and generates a dict with all the measures.

        Args:
            None

        Return:
            Dict
        """
        diccionario = {"d": []}
        num_mesures = int(self.__device.query("DATA:POINTS?"))

        time.sleep(0.25)
        for _ in range(num_mesures):
            result = self.__device.query('DATA:REMOVE? 1')
            time.sleep(0.25)

            lista_result = result.split(",")
            lista_result[1] = str(float(lista_result[1])*1000/1000)

            # for componente in lista_result:
            diccionario["d"].append(lista_result)

        self.__device.write('SYSTem:LOCal')

        return diccionario

    def interval_read(self) -> list:
        """
        Measure all the points and generates a dict with all the measures.

        Return:
            diccionario (dict) --> Diccionari amb el timestamp de les
                                   mesures com a clau i les mesures com a
                                   valors.

            timestamp (float) --> Timestamp de les mesures. S'ha de linkejar
                                  amb els següents loops de test.
        """
        # diccionario{"d": []}
        timestamp = time.time()
        diccionario = {f"{timestamp}": []}

        self.__device.write("INIT")

        for _ in range(self.__number_of_scans):

            # while DataLogger.POINTS == 0:
            #     DataLogger.POINTS = int(self.__device.query(
            #         "DATA:POINTS?").replace("\r", ""))

            for _ in range(self.__number_of_channels):
                time.sleep(0.25)
                result = self.__device.query('DATA:REMOVE? 1')
                time.sleep(0.25)

                lista_result = result.split(",")
                lista_result[1] = str(float(lista_result[1])*1000/1000)

                # for componente in lista_result:
                diccionario[f"{timestamp}"].append(lista_result)

            time.sleep(self.__delay_seconds)

            self.__device.write('SYSTem:LOCal')

        return diccionario, timestamp

    def read_one(self) -> dict:
        """
        Reads and returns one measure when called.
        """
        timestamp = time.time()
        diccionario = {f"{timestamp}": []}

        self.__device.write("INIT")
        time.sleep(0.5)
        diccionario[f"{timestamp}"] = self.__device.query('FETCh?')

        return diccionario


class PowerSupply:
    """
    Aquesta classe conté tots els paràmetres de configuració del
    dispositiu RS-A3305P.

    Atributes:
            self.__device (str): nom del dispositiu
    """

    def __init__(self, device) -> None:
        """
        Inicialitza els atributs de la classe.

        Args:
            No arguments.
        """
        self.__device = device

    def set_font(self, chan: int, **kwargs) -> None:
        """
        Canvia de current a voltatge els diferents canals.
        Arg:
            chan (int): Canal.
            kwargs (any): Voltatge i/o intensitat en format:
                          V=x.
                          I=x.
        """
        for magnitud, unidad in kwargs.items():

            self.__device.write(str(magnitud).upper() + f"SET{chan}:{unidad}")
            time.sleep(0.5)

    def on_off(self, chan: int, mode: int) -> None:
        """
        Encén o apaga els canals de la font.
        Arg:
            chan (int): Canal.
            mode (int): 1 = ON, 0 = OFF.
        """
        self.__device.write(f"OUT{mode}:{chan}")
        time.sleep(0.5)

    def steps_until(self, chan: int, unit: str, *args) -> None:
        """
        Augmenta o disminueix el voltatge o corrent en pasos definits.
        Arg:
            chan (int): Canal.
            unit (str): VOLT = Voltatge, INT = Intensitat.
            args (any): Els valors han de ser separats per comes en el ordre
                        seguent:
                        V inicial, V final, steps en V, temps entre steps en V.
        """
        match unit:
            case "VOLT": text = "V"
            case "INT": text = "I"

        self.__device.write(text + f"ASTEP{chan}:{args}")
        time.sleep(0.5)

    def read_val(self, chan: int, unit: str) -> float:
        """
        Llegeix els valors en el canal triat.
        Arg:
            chan (int): Canal.
            unit (str): VOLT = Voltatge, INT = Intensitat.
        Return:
            float
        """
        match unit:
            case "VOLT": text = "V"
            case "INT": text = "I"

        return self.__device.query(text + f"OUT{chan}?")

    def stop_at(self, chan: int, unit: str) -> None:
        """
        Para el increment o decrement de voltatge/intensitat en el canal triat.
        Arg:
            chan (int): Canal.
            unit (str): VOLT = Voltatge, INT = Intensitat.
        """
        match unit:
            case "VOLT": text = "V"
            case "INT": text = "I"

        self.__device.write(text + f"ASTOP{chan}")
