import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 5
            return 0

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 3)
            return None

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called()

    def test_tilisiirto(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

    def test_kaksi_eri_tuotetta(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("maija", "67890")

        self.pankki_mock.tilisiirto.assert_called_with("maija", 42, "67890", ANY, 8)

    def test_kaksi_samaa_tuotetta(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("kalle", "11223")

        self.pankki_mock.tilisiirto.assert_called_with("kalle", 42, "11223", ANY, 10)

    def test_tuote_varastossa_ja_tuote_loppu(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  
        self.kauppa.lisaa_koriin(3)  
        self.kauppa.tilimaksu("liisa", "44556")

        self.pankki_mock.tilisiirto.assert_called_with("liisa", 42, "44556", ANY, 5)

if __name__ == "__main__":
    unittest.main()