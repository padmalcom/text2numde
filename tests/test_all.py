from unittest import TestCase
from text2numde import text2num, is_number, sentence2num


class TestTextToNumDe(TestCase):

	def test_all(self):
		assert 1 == text2num("eins")
		assert 12 == text2num("zwölf")
		assert 72 == text2num("zweiundsiebzig")
		assert 300 == text2num("dreihundert")
		assert 1200 == text2num("zwölfhundert")
		assert 12304 == text2num("zwölftausenddreihundertundvier")
		assert 6000000 == text2num("sechs millionen")
		assert 6400005 == text2num("sechs millionen vierhunderttausendundfünf")
		assert 123456789012 == text2num("einhundertdreiundzwanzig Milliarden vierhundertsechsundfünfzig Millionen siebenhundertneunundachtzigtausendundzwölf")
		assert 1_000_000_000_000_000_000_000 * 4 == text2num("vier trilliarden")

		assert 1.2 == text2num("eins komma zwei")
		assert 0.9876 == text2num("nullkommaneunachtsiebensechs")
		assert 0.10 == text2num("nullkommazehn")

		assert False == is_number("Haus")
		assert False == is_number("einsBahn")
		assert True == is_number("einhundertdrei")

		assert "Ich habe eine 1." == sentence2num("Ich habe eine eins.")
		assert "Ich habe 26 Hunde und 103 Katzen." == sentence2num("Ich habe sechsundzwanzig Hunde und einhundertdrei Katzen.")
		assert "Ich habe 1.5 Kilo abgenommen." == sentence2num("Ich habe einskommafünf Kilo abgenommen.")