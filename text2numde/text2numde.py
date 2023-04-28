# Inspired by Greg Hewgill (https://github.com/ghewgill/text2num)

import re

Units = {
    'null': 0,
    'eins': 1,
    "ein": 1,
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
    'neunzig': 90,
}

Hundred = {
    "einhundert": 100,
    "hundert": 100,

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

combinable = ["eintausend", "einhundert"]

Komma = {
    "komma": ','
}

Sign = {
    "plus": '+',
    "minus": '-'
}

All_Numbers: list = list(Units.keys()) + list(Magnitude.keys()) + list(Hundred.keys()) + list(Komma.keys()) + list(["und"])
new_all_numbers = [Units, Magnitude, Hundred, Komma, Sign]
class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def is_number(word):
    try:
        text2num(word)
    except:
        return False
    return True


def sentence2num(s, signed=False):
    # Trennen des Textes in Sätze und Satzzeichen
    sentences = re.split(r"\s*[\.,;\(\)…\[\]:!\?]+\s*", s)
    punctuations = re.findall(r"\s*[\.,;\(\)…\[\]:!\?]+\s*", s)

    # falls die Anzahl der Satzzeichen kleiner ist als die Anzahl der Sätze, wird ein leerer String hinzugefügt
    if len(punctuations) < len(sentences):
        punctuations.append("")

    # Liste für die umgewandelten Segmente wird erstellt
    out_segments: List[str] = []
    for segment, sep in zip(sentences, punctuations):
        # Segment wird in einzelne Tokens aufgeteilt
        tokens = segment.split()
        sentence = []
        # Liste für die umgewandelten Tokens und deren Typ (Zahl oder nicht) wird erstellt
        out_tokens: List[str] = []
        out_tokens_is_num: List[bool] = []
        old_num_result = None
        token_index = 0
        while token_index < len(tokens):
            t = tokens[token_index]
            sentence.append(t)

            try:
                # Prüfung, ob das aktuelle Token eine Zahl repräsentiert
                num_result = text2num(" ".join(sentence))
                old_num_result = num_result
                token_index += 1
            except:
                # " ".join(sentence) kann nicht in eine Zahl umgewandelt werden

                # Das letzte Token muss erneut geprüft werden, falls etwas wie "eins eins eins" vorkommt,
                # was in der Summe ungültig ist, aber separat erlaubt ist
                if not old_num_result is None:
                    out_tokens.append(str(old_num_result))
                    out_tokens_is_num.append(True)
                    sentence.clear()
                else:
                    out_tokens.append(t)
                    out_tokens_is_num.append(False)
                    sentence.clear()
                    token_index += 1
                old_num_result = None

        # Gibt es noch Tokens, die hinzugefügt werden müssen?
        if not old_num_result is None:
            out_tokens.append(str(old_num_result))
            out_tokens_is_num.append(True)

        # Zusammenführen aller Tokens und Berücksichtigung von Vorzeichen
        out_segment = ""
        for index, ot in enumerate(out_tokens):
            if (ot in Sign) and signed:
                if index < len(out_tokens) - 1:
                    if out_tokens_is_num[index + 1] == True:
                        out_segment += Sign[ot]
            else:
                out_segment += ot + " "

        out_segments.append(out_segment.strip())
        out_segments.append(sep)

    # Zusammenfügen aller Segmente zu einem String
    return "".join(out_segments)

def __split_ger__(word):
    """Splits number words into separate words, e.g. einhundertfünzig-> ein hundert fünfzig"""
    
    # Sort all numbers by length to start with the longest 
    sorted_words = sorted(All_Numbers, key=len, reverse=True)
    current_word = ""
    text = word.lower()
    invalid_word = ""
    result = []
    while len(text) > 0:
        # start with the longest
        found = False
        for sw in sorted_words:

            # Check at the beginning of the current sentence for the longest word in ALL_WORDS
            if text.startswith(sw):
                if not sw == "und":
                    result.append(sw)
                text = text[len(sw):]
                text = text.strip()
                found = True 
                break
        if not found:
            raise NumberException("Can't split, unknown number: '"+word+"'")
    return " ".join(result)
    
def text2num(s):
    words = __split_ger__(s)  # ["eintausend", "hundert", "fünf"]
    b = re.split(r"komma", words)
    wlist = re.split(r"[\s-]+", b[0].strip())  # den ersten Teil des Texts in eine Liste von Wörtern aufteilen und Leerzeichen und Bindestriche entfernen
    norm_num = 0  # die Zahl vor dem Komma
    g = 0  # die Zahl innerhalb der Tausender, z.B. "fünf" in "eintausend fünf"
    for word in wlist:

        for d in new_all_numbers:
            if word in d:
                x = d[word]

        x = Units.get(word, None)
        h = Hundred.get(word, None)

        if x is not None:
            g += x
        elif word == "einhundert":
            g += 100
        elif word == "hundert" and g != 0:
            g *= 100
        elif word == "hundert" and h is not None and x is None:
            g += 100
        else:
            x = Magnitude.get(word, None)
            if x is not None and g == 0:
                norm_num += x
            elif x is not None:
                norm_num += g * x
                g = 0
            else:
                raise NumberException("Unknown number: " + word)
    res = norm_num + g  # die Zahl vor dem Komma und die Zahl innerhalb der Tausender addieren

    # floating point number
    if len(b) == 2:  # falls der Text in zwei Teile aufgeteilt wurde (also ein Komma vorhanden ist)
        ak = "0."
        wlist = re.split(r"[\s-]+", b[1].strip())  # den zweiten Teil des Texts in eine Liste von Wörtern aufteilen und Leerzeichen und Bindestriche entfernen
        for word in wlist:
            x = Units.get(word, None)  # das Wort in eine Zahl umwandeln, z.B. "fünf" in 5
            if x is not None:
                ak += str(x)  # die Zahl hinten an den String anhängen, z.B. "0.5"
            else:
                raise NumberException("Unknown number: "+word)  # falls das Wort nicht bekannt ist, eine Fehlermeldung ausgeben
        res += eval(ak)  # die Zahl vor und nach dem Komma addieren
    return res
