from enum import Enum
from tkinter import ttk, constants, StringVar


class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4
    

class BinaariOperaatio:
    def __init__(self, sovelluslogiikka, syote_lukija):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote_lukija = syote_lukija
        self._edellinen_arvo = None  

    def suorita(self):
        raise NotImplementedError("suorita-metodi puuttuu")

    def kumoa(self):
        if self._edellinen_arvo is not None:
            self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)

    def _lue_syote(self):
        try:
            return int(self._syote_lukija())
        except ValueError:
            return 0


class Summa(BinaariOperaatio):
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.plus(self._lue_syote())


class Erotus(BinaariOperaatio):
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.miinus(self._lue_syote())


class Nollaus(BinaariOperaatio):
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()


class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root

        self._syote_kentta = None
        self._kumoa_painike = None
        self._nollaus_painike = None
        self._arvo_var = StringVar()
        self._viimeisin_komento = None

        self._komennot = {
            Komento.SUMMA: Summa(sovelluslogiikka, self._lue_syote),
            Komento.EROTUS: Erotus(sovelluslogiikka, self._lue_syote),
            Komento.NOLLAUS: Nollaus(sovelluslogiikka, self._lue_syote),
        }

    def kaynnista(self):
        arvo_label = ttk.Label(self._root, textvariable=self._arvo_var)
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        arvo_label.grid(row=0, column=0, columnspan=4)

        self._syote_kentta = ttk.Entry(self._root)
        self._syote_kentta.grid(row=1, column=0, columnspan=4)

        ttk.Button(self._root, text="Summa", command=lambda: self._suorita_komento(Komento.SUMMA)).grid(row=2, column=0)
        ttk.Button(self._root, text="Erotus", command=lambda: self._suorita_komento(Komento.EROTUS)).grid(row=2, column=1)
        self._nollaus_painike = ttk.Button(self._root, text="Nollaus", command=lambda: self._suorita_komento(Komento.NOLLAUS))
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike = ttk.Button(
            self._root, text="Kumoa", state=constants.DISABLED, command=self._kumoa
        )
        self._kumoa_painike.grid(row=2, column=3)

    def _lue_syote(self):
        return self._syote_kentta.get()

    def _suorita_komento(self, komento):
        komento_olio = self._komennot[komento]
        komento_olio.suorita()
        self._viimeisin_komento = komento_olio

        self._kumoa_painike["state"] = constants.NORMAL

        if self._sovelluslogiikka.arvo() == 0:
            self._nollaus_painike["state"] = constants.DISABLED
        else:
            self._nollaus_painike["state"] = constants.NORMAL

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())

    def _kumoa(self):
        if self._viimeisin_komento:
            self._viimeisin_komento.kumoa()
            self._viimeisin_komento = None 

            self._kumoa_painike["state"] = constants.DISABLED
            self._arvo_var.set(self._sovelluslogiikka.arvo())

            if self._sovelluslogiikka.arvo() == 0:
                self._nollaus_painike["state"] = constants.DISABLED
            else:
                self._nollaus_painike["state"] = constants.NORMAL
