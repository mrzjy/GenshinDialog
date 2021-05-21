# GenshinDialog
This project simply extracts all character conversations in Genshin Project

~~~
# Samples of random dialog sessions
['Jean\tThank you for accepting our invitation, traveler.', 'PLAYER\tGoodbye.']
['Alois\tUgh...', 'PLAYER\tAllow me.', 'Noelle\t#Oh? ...You want to escort him yourself, {NICKNAME}?']
['???\tHow about you let me take over?', 'PLAYER\tThe black market?']
~~~

### Requirement
~~~
Python 3.6
~~~

### Steps
1. Get GenshinData from [Dim's project](https://github.com/Dimbreath/GenshinData), you could git clone or download the zip and extract it.

2. Run extract_dialogs.py file
~~~
// Command line
python python extract_dialogs.py --repo=PATH/TO/GenshinData --lang=CHS --n_utter=4
~~~
3. See the output file at "extracted_dialog/output_dialog_{lang}.txt"

Notes:

1. Each line of the output corresponds to a dialog session, which contains at most n_utter utterances)
2. There are already extracted outputs in the extracted_dialog folder for 4 languages