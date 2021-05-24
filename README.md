# GenshinDialog
This project simply extracts all character conversations in Genshin Project, in a simple format of "speaker \t utterance"

~~~
# Samples of random dialog sessions
# English
['Jean\tThank you for accepting our invitation, traveler.', 'PLAYER\tGoodbye.']
['Alois\tUgh...', 'PLAYER\tAllow me.', 'Noelle\t#Oh? ...You want to escort him yourself, {NICKNAME}?']
['???\tHow about you let me take over?', 'PLAYER\tThe black market?']

# Chinese Simplified
['香菱\t嗯，少一种「噼咔」的感觉。', '派蒙\t这么一说确实不够「噼咔」呢。', 'PLAYER\t为什么派蒙能明白？！', '派蒙\t哼哼哼。']
['清昼\t呵呵，「彩头」…也不知道这个词是谁教他们的。', 'PLAYER\t那你和梵米尔的比试怎么办？']
['派蒙\t对呀对呀！', 'PLAYER\t画作承载的是记忆。', '派蒙\t是的！', 'PLAYER\t别轻易放弃与回忆有关的东西。']
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
3. Language options correspond to languages in Dim's GenshinData/TextMap (e.g., CHS, JA, ES, FR, etc.)
4. There are string variables in the dialogs, which depend on one's main character choice in the game, like the following:
~~~
{NICKNAME}
{PLAYERAVATAR#SEXPRO[INFO_MALE_PRONOUN_BIGBROTHER|INFO_FEMALE_PRONOUN_BIGSISTER]}
{PLAYERAVATAR#SEXPRO[INFO_MALE_PRONOUN_BOYA|INFO_FEMALE_PRONOUN_GIRLA]}
~~~