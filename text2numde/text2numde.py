# Inspired by Greg Hewgill (https://github.com/ghewgill/text2num)

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

Komma = {
    "komma": ','
}

Sign = {
    "plus": '+',
    "minus": '-'
}

All_Numbers = list(Units.keys()) + list(Magnitude.keys()) + list(Hundred.keys()) + list(Komma.keys()) + list(["und"])

class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def is_number(word):
    try:
        text2num(word)
    except:
        return False
    return True

def sentence2num(s, signed = False):
    sentences = re.split(r"\s*[\.,;\(\)…\[\]:!\?]+\s*", s)
    punctuations = re.findall(r"\s*[\.,;\(\)…\[\]:!\?]+\s*", s)
    
    if len(punctuations) < len(sentences):
        punctuations.append("")
    
    out_segments: List[str] = []    
    for segment, sep in zip(sentences, punctuations):
        tokens = segment.split()
        sentence = []
        out_tokens: List[str] = []
        out_tokens_is_num: List[bool] = []
        old_num_result = None
        token_index = 0

        while token_index < len(tokens):
            t = tokens[token_index]
            sentence.append(t)
                                
            try:
                num_result = text2num(" ".join(sentence))
                old_num_result = num_result
                token_index += 1
            except:
                # " ".join(sentence) cannot be resolved to a number
                
                # last token has to be tested again in case there is sth like "eins eins eins"
                # which is invalid in sum but separately allowed
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
                
        # any remaining tokens to add?
        if not old_num_result is None:
            out_tokens.append(str(old_num_result))
            out_tokens_is_num.append(True)
            
        # join all and keep track on signs
        out_segment = ""
        for index, ot in enumerate(out_tokens):
            if (ot in Sign) and signed:
                if index < len(out_tokens)-1:
                    if out_tokens_is_num[index+1] == True:
                        out_segment += Sign[ot]
            else:
                out_segment +=ot + " "
                    
        out_segments.append(out_segment.strip())
        out_segments.append(sep)
    
    
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
    words = __split_ger__(s)
    b = re.split(r"komma", words)
    a = re.split(r"[\s-]+", b[0].strip())
    n = 0
    h = 0
    g = 0
    if a[0] == "ein" and a[1] == "hundert":
        a = a[1:]
    for w in a:
        x = Units.get(w, None)
        h = Hundred.get(w, None)
        if x is not None:
            g += x
        elif w == "hundert" and g != 0:
            g *= 100
        elif w == "hundert" and h is not None and x is None:
            g += 100
        else:
            x = Magnitude.get(w, None)
            if x is not None:
                n += g * x
                g = 0
            else:
                raise NumberException("Unknown number: " + w)
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
                raise NumberException("Unknown number: " + w)
        res += eval(ak)
    return res
