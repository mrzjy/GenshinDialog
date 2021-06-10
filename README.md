# GenshinDialog
This project simply extracts all character conversations in Genshin Project, in a simple format of "speaker \t utterance"

- Current state of dialog extraction (Game version 1.6.0)

| Num  | Count | 
:-----------: | :-----------:  |
| Total num of roles (speakers)   | 1,160  |
| Total num of utterances  | 52,611  |
| Total num of dialog sessions  | 21,950 |

- Samples of random dialog sessions
~~~
# lang=EN
['Jean\tThank you for accepting our invitation, traveler.', 'PLAYER\tGoodbye.']
['Alois\tUgh...', 'PLAYER\tAllow me.', 'Noelle\t#Oh? ...You want to escort him yourself, {NICKNAME}?']
['???\tHow about you let me take over?', 'PLAYER\tThe black market?']

# lang=CHS
['香菱\t嗯，少一种「噼咔」的感觉。', '派蒙\t这么一说确实不够「噼咔」呢。', 'PLAYER\t为什么派蒙能明白？！', '派蒙\t哼哼哼。']
['清昼\t呵呵，「彩头」…也不知道这个词是谁教他们的。', 'PLAYER\t那你和梵米尔的比试怎么办？']
['派蒙\t对呀对呀！', 'PLAYER\t画作承载的是记忆。', '派蒙\t是的！', 'PLAYER\t别轻易放弃与回忆有关的东西。']
~~~
- Samples of avatar information
~~~
# lang=JA
"七七": {
        "birthday": "3.3",
        "constellation": "法鈴座",
        "desc": "薬舗「不卜廬」の薬採り兼弟子、紙のように白い顔色で不死身。口数が少なく、あまり表情がない。",
        "element": "氷",
        "native": "不卜廬",
        "sayings": [
            "初めまして…\t七七、キョンシーだ。…ん？あと何だっけ。",
            "世間話·独り言\tん、今…何を話そうとしたっけ…",
            ...,
            "突破した感想·結\tあなたがいてくれたおかげだ、ありがとう…もうひとつ願いを叶えてくれる？これからは七七に守らせてほしいけど、いいかな？"
        ],
        "story": [
            "キャラクター詳細\tキョンシーなのだから、表情が固いことも許されるだろう。\\nキョンシーではあるが、七七はきちんと体を鍛えている。\\n記憶力は極めて悪い。それは、七七が人に対して冷たい理由の1つだった。\\n七七の外見は、ずっと亡くなった時のままであるため、実年齢は推測不可能である。\\nキョンシーを動かすには、勅令が必要だ。しかし、ある原因で七七は自分で自分に勅令を下しているのだ。",
            ...,
        ],
        "title": "冷たき黄泉帰り"
    }
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
Note: Add --speaker=xxx (replace xxx by a character name, e.g., Keqing when lang=EN) to your command if you'd only like to extract xxx's dialogs (make sure you type the speaker correctly and note for capital letters)

3. See the output dialog and other info at "extracted_dialog"

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