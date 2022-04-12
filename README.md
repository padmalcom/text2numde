# text2numde

This python package converts numbers written as text into float or integer values.

It can furthermore:
- Validate a text to see if it represents a numbers
- Replace numbers in sentences without modifying the sentence around the numbers.

<a href="https://www.buymeacoffee.com/padmalcom" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Example usage

```python
>>> from text2numde import text2num, is_number, sentence2num
>>> text2numde('Eins')
1

>>> text2num('Einhundertunddrei')
103

>>> text2numd'Vierzehnkommaachtneundrei')
14.893

>>> is_number('Einhundertunddrei')
True

>>> is_number('Zehnzehnhundert')
False

>>> sentence2num('Ich habe zwei Hunde und vierzig Voegel.')
Ich habe 2 Hunde und 40 Voegel.

```
