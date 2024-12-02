KAPASITEETTI = 5
OLETUSKASVATUS = 5


class IntJoukko:
    def __init__(self, kapasiteetti=KAPASITEETTI, kasvatuskoko=OLETUSKASVATUS):
        if not isinstance(kapasiteetti, int) or kapasiteetti <= 0:
            raise ValueError("Kapasiteetin on oltava positiivinen kokonaisluku")
        if not isinstance(kasvatuskoko, int) or kasvatuskoko <= 0:
            raise ValueError("Kasvatuskoon on oltava positiivinen kokonaisluku")

        self.kapasiteetti = kapasiteetti
        self.kasvatuskoko = kasvatuskoko
        self.ljono = [0] * self.kapasiteetti
        self.alkioiden_lkm = 0

    def kuuluu(self, numero):
        return numero in self.ljono[:self.alkioiden_lkm]

    def lisaa(self, numero):
        if self.kuuluu(numero):
            return False

        if self.alkioiden_lkm == len(self.ljono):
            self._kasvata_kapasiteettia()

        self.ljono[self.alkioiden_lkm] = numero
        self.alkioiden_lkm += 1
        return True

    def poista(self, numero):
        if numero not in self.ljono[:self.alkioiden_lkm]:
            return False

        kohta = self.ljono.index(numero)
        self.ljono[kohta:self.alkioiden_lkm - 1] = self.ljono[kohta + 1 : self.alkioiden_lkm]
        self.alkioiden_lkm -= 1
        return True

    def _kasvata_kapasiteettia(self):
        self.ljono.extend([0] * self.kasvatuskoko)

    def mahtavuus(self):
        return self.alkioiden_lkm

    def to_int_list(self):
        return self.ljono[:self.alkioiden_lkm]

    @staticmethod
    def yhdiste(joukko_a, joukko_b):
        tulos = IntJoukko()
        for numero in joukko_a.to_int_list() + joukko_b.to_int_list():
            tulos.lisaa(numero)
        return tulos

    @staticmethod
    def leikkaus(joukko_a, joukko_b):
        tulos = IntJoukko()
        for numero in joukko_a.to_int_list():
            if numero in joukko_b.to_int_list():
                tulos.lisaa(numero)
        return tulos

    @staticmethod
    def erotus(joukko_a, joukko_b):
        tulos = IntJoukko()
        for numero in joukko_a.to_int_list():
            if numero not in joukko_b.to_int_list():
                tulos.lisaa(numero)
        return tulos

    def __str__(self):
        return "{" + ", ".join(map(str, self.to_int_list())) + "}"
