# GenshinDialog

本项目抽取原神游戏的对话语料、材料、武器等语料

(Also take a look at [StarrailDialogue](https://github.com/mrzjy/StarrailDialogue) if you're interested)

This project simply extracts all character conversations in Genshin Impact, in a simple format of "speaker \t utterance"

- Current game version 4.0

Welcome to the nation of Hydro !!

|              Stat               |                        Count                         | 
|:-------------------------------:|:----------------------------------------------------:|
|  Total num of roles (speakers)  |                        2,416                         |
|     Total num of utterances     |                       158,039                        |
|  Total num of dialog sessions   | 20,348 (14,965 storyline + 5,383 avatar description) |
| Average num of turns per dialog |                         9.19                         |

- Note

stats above are from lang=CHS, which is slightly different with other languages

There are scenarios where user chooses different responses and thus lead to different dialog path, each path is treated as a unique dialog, which is why you might see multiple dialogs that share most content except only for one or two utterances.

- Random samples
~~~
# lang=EN
[
    "Paimon\tOoh! Did you just feel the elements of the world?",
    "Paimon\tSeems all you had to do was just touch the statue and you got the power of Anemo!",
    "Paimon\tAs much as they may want it, people in this world can never get a hold of powers as easily as you...",
    "Traveller\tI think I know why, it's because...",
    "Paimon\tAh-ha, it's because you're not from this world to begin with.",
    "Paimon\tIf we keep heading west from here, we'll eventually reach Mondstadt, the City of Freedom.",
    "Paimon\tMondstadt is the city of wind, because they worship the God of Anemo.",
    "Paimon\tSo perhaps, because you got power from the God of Anemo, you can find some clues there.",
    "Paimon\tThere are also lots of bards there, so perhaps one of them has heard news of your {Msister}{Fbrother}.",
    "Paimon\tLet's move then!",
    "Paimon\tThe elements in this world responded to your prayers and Paimon thinks that's a lovely sign."
],
# lang=CHS
[
    "标识牌\t「夏日特供葡萄汁 两瓶一摩拉」",
    "派蒙\t居然有这么好的事！",
    "标识牌\t「已售罄 多谢惠顾」",
    "派蒙\t好吧…"
],
~~~
- Random avatars
~~~
# lang=JP
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

### Extract dialogs
1. Get GenshinData from [Dim's project](https://github.com/Dimbreath/GenshinData), you could git clone or download the zip and extract it.

**Note**: Search for yourself where Dim's project data is... (No longer in Github)

3. Run extract_dialogs.py file
~~~
// Command line
python python extract_dialogs.py --repo=PATH/TO/GenshinData --lang=CHS

// The output are like the following
Summarizing statistics:
Below are string variables that appear in dialogs...
        Frequency       Variable
        16047   {NICKNAME}
        2680    {MATEAVATARSEXPRO[INFO_MALE_PRONOUN_BROTHER|INFO_FEMALE_PRONOUN_SISTER]}
        1269    {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BROTHER|INFO_FEMALE_PRONOUN_SISTERA]}
        944     {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_SISTER|INFO_FEMALE_PRONOUN_BROTHER]}
        739     {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_HE|INFO_FEMALE_PRONOUN_SHE]}
        464     {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_SHE|INFO_FEMALE_PRONOUN_HE]}
        458     {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYC|INFO_FEMALE_PRONOUN_GIRLC]}
        400     {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BIGBROTHER|INFO_FEMALE_PRONOUN_BIGSISTER]}
        300     {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOY|INFO_FEMALE_PRONOUN_GIRL]}
        192     {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BROTHER|INFO_FEMALE_PRONOUN_YING]}
        192     {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_UNCLE|INFO_FEMALE_PRONOUN_AUNT]}
        144     {MATEAVATARSEXPRO[INFO_MALE_PRONOUN_BOY|INFO_FEMALE_PRONOUN_GIRL]}
        80      {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_GIRLD|INFO_FEMALE_PRONOUN_BOYD]}
        80      {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_YING|INFO_FEMALE_PRONOUN_KONG]}
        56      {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_YING|INFO_FEMALE_PRONOUN_BROTHER]}
        54      {MATEAVATARSEXPRO[INFO_MALE_PRONOUN_HE|INFO_FEMALE_PRONOUN_SHE]}
        48      {PLAYERAVATARSEXPRO[INFO_FEMALE_PRONOUN_SISTER|INFO_MALE_PRONOUN_BROTHER]}
        36      {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_HERO|INFO_FEMALE_PRONOUN_HEROINE]}
        34      {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_SHE|INFO_MALE_PRONOUN_HE]}
        33      {MATEAVATARSEXPRO[INFO_MALE_PRONOUN_BOYD|INFO_FEMALE_PRONOUN_GIRLD]}
        23      {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_HE|INFO_MALE_PRONOUN_SHE]}
        16      {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BROANDSIS|INFO_FEMALE_PRONOUN_SISANDSIS]}
        15      {QuestNpcID}
        14      {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_CUTEBIGBROTHER|INFO_FEMALE_PRONOUN_CUTEBIGSISTER]}
        11      {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BROTHER|INFO_MALE_PRONOUN_BROANDSIS]}
        8       {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_XIABOY|INFO_FEMALE_PRONOUN_XIAGIRL]}
        5       {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYE|INFO_FEMALE_PRONOUN_GIRLE]}
        4       {MATEAVATARSEXPRO[INFO_FEMALE_PRONOUN_HE|INFO_MALE_PRONOUN_SHE]}
        2       {QuestGatherID}
        2       {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYA|INFO_FEMALE_PRONOUN_GIRLA]}
        1       {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYA|INFO_FEMALE_PRONOUN_GIRLB]}
        1       {PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYA|INFO_FEMALE_PRONOUN_GIRLC]}

Total num of dialogs: 78279 (74999 from storyline, 3280 from avatar description)
Total num of unique utterances: 77981
Total num of unique talking roles: 1119
Average num of turns per dialog: 23.405562155878332

Output avatar at extracted_dialog/avatar_CHS.json
Output dialog at extracted_dialog/dialog_CHS.json
~~~

Notes:

1. output is a json file (could be viewed by most txt viewer), the structure is a list of list, it's a list of dialog and each dialog is then a list of utterance
2. There are already sampled outputs in the extracted_dialog folder for 3 languages, but you need to run the command yourself in order to get ***FULL dialogs*** (output file size is around 100+MB for each language)
3. Language options correspond to languages in Dim's GenshinData/TextMap (e.g., CHS, JA, ES, FR, etc.)
4. There are string variables in the dialogs, whose real value depends on one's main character choice in the game. Note that these string variables might have different names in different languages


### Extract miscellaneous things
~~~
// Command line
python extract_misc.py --repo=PATH/TO/GenshinData --lang=CHS

// This ends in excel files generated in extracted_misc
~~~