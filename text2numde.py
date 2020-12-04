# Based on the work of Greg Hewgill (https://github.com/ghewgill/text2num)

import re

Units = {
    'null': 0,
    'eins': 1,
    'ein': 1,
    'zwei': 2,
    'drei': 3,
    'vier': 4,
    'fünf': 5,
    'sechs': 6,
    'sieben': 7,
    'acht': 8,
    'neun': 9,
    'zehn': 10,
    'elf': 11,
    'zwölf': 12,
    'dreizehn': 13,
    'vierzehn': 14,
    'fünfzehn': 15,
    'sechzehn': 16,
    'siebzehn': 17,
    'achtzehn': 18,
    'neunzehn': 19,
    'zwanzig': 20,
    'dreißig': 30,
    'vierzig': 40,
    'fünfzig': 50,
    'sechzig': 60,
    'siebzig': 70,
    'achtzig': 80,
    'neunzig': 90
}

Hundred = {
    "hundert": 100
}

Magnitude = {
    "tausend":     1_000,
    "million":     1_000_000,
    "millionen":   1_000_000,
    "milliarde":   1_000_000_000,
    "milliarden":  1_000_000_000,
    "billion":     1_000_000_000_000,
    "billionen":   1_000_000_000_000,
    "billiarde":   1_000_000_000_000_000,
    "billiarden":  1_000_000_000_000_000,
    "trillion":    1_000_000_000_000_000_000,
    "trillionen":  1_000_000_000_000_000_000,
    "trilliarde":  1_000_000_000_000_000_000_000,
    "trilliarden": 1_000_000_000_000_000_000_000
}

Komma = {
    "komma": ','
}

All_Numbers = list(Units.keys()) + list(Magnitude.keys()) + list(Hundred.keys()) + list(Komma.keys())

class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

                
def split_ger(word):
    """Splits number words into separate words, e.g. einhundertfünzig-> ein hundert fünfzig"""
    
    # Sort all numbers by length to start with the longest 
    sorted_words = sorted(All_Numbers, key=len, reverse=True)
    
    current_word = ""
    text = word.lower()
    invalid_word = ""
    result = ""
    while len(text) > 0:
        # start with the longest
        found = False
        for sw in sorted_words:
            # Check at the beginning of the current sentence for the longest word in ALL_WORDS
            if text.startswith(sw):
                if not sw == "und":
                    result += sw + " "
                text = text[len(sw):]
                found = True
                break
        if not found:
            text = text[1:]
    return result.strip()
    
def text2num(s):
    words = split_ger(s)
    
    b = re.split(r"komma", words)
    a = re.split(r"[\s-]+", b[0].strip())
    n = 0
    g = 0
    for w in a:
        x = Units.get(w, None)
        if x is not None:
            g += x
        elif w == "hundert" and g != 0:
            g *= 100
        else:
            x = Magnitude.get(w, None)
            if x is not None:
                n += g * x
                g = 0
            else:
                raise NumberException("Unknown number: "+w)
    res = n + g
    
	# floating point number
    if len(b) == 2:
        ak = "0."
        a = re.split(r"[\s-]+", b[1].strip())
        for w in a:
            x = Units.get(w, None)
            if x is not None:
                ak += str(x)
            else:
                raise NumberException("Unknown number: "+w)
        res += eval(ak)
    return res
    
if __name__ == "__main__":
    print(text2num("eins"))
    print(text2num("zwölf"))
    print(text2num("zweiundsiebzig"))
    print(text2num("dreihundert"))
    print(text2num("zwölfhundert"))
    print(text2num("zwölftausenddreihundertundvier"))
    print(text2num("sechs millionen"))
    print(text2num("sechs millionen vierhunderttausendundfünf"))
    print(text2num("einhundertdreiundzwanzig Milliarden vierhundertsechsundfünfzig Millionen siebenhundertneunundachtzigtausendundzwölf"))
    print(text2num("vier trilliarden"))
    
    print(text2num("eins komma zwei"))
    print(text2num("nullkommaneunachtsiebensechs"))
    print(text2num("nullkommazehn"))
    
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