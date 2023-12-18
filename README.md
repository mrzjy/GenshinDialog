<div align=center><img src="./img/image.png"/></div>

# GenshinDialog
This project simply extracts all character conversations in Genshin Project from the legendary [Dimbreath](https://github.com/Dimbreath)'s works.

本项目抽取原神游戏的对话语料、材料、武器等语料，感谢 [Dimbreath](https://github.com/Dimbreath) 的神奇项目。

Other projects you might be interested in:
- [StarrailDialogue](https://github.com/mrzjy/StarrailDialogue): Same but for Honkai: Star Rail 
- [hoyo_public_wiki_parser](https://github.com/mrzjy/hoyo_public_wiki_parser): Parse Hoyoverse public wiki data
  - Recommended: Typically this is where you could get more complete dialogues throughout various quests, together with quest descriptions

### Description

This project simply extracts all character conversations in Genshin Impact in a chatgpt-message-like format

- Current game version 4.2

> **I, Focalors, hereby welcome you to the Nation of Hydro!**

|              Stat               |                        Count                         | 
|:-------------------------------:|:----------------------------------------------------:|
|  Total num of roles (speakers)  |                        2,418                         |
|     Total num of utterances     |                       158,039                        |
| Average num of turns per dialog |                        9.09                          |

- Note

Stats above are from lang=CHS, which is slightly different from other languages

We provide 3 examples of what this project extracts:

- Random avatar example

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

- Random dialogue example

~~~
# lang=EN
[
   {
      "role":"Signboard",
      "content":"\"Summer-special grape juice. Two bottles for one Mora.\""
   },
   {
      "role":"Paimon",
      "content":"What a bargain!"
   },
   {
      "role":"Signboard",
      "content":"\"Sold out. Thank you.\""
   },
   {
      "role":"Paimon",
      "content":"Alright then..."
   }
],
# lang=CHS
[
   {
      "role":"标识牌",
      "content":"「夏日特供葡萄汁 两瓶一摩拉」"
   },
   {
      "role":"派蒙",
      "content":"居然有这么好的事！"
   },
   {
      "role":"标识牌",
      "content":"「已售罄 多谢惠顾」"
   },
   {
      "role":"派蒙",
      "content":"好吧…"
   }
],
~~~

- Random raw_dialogue example

(You can restore dialogue branches (choices) through "nextDialogs" field)

~~~
[
  {
    "role": "明蕴镇告示牌",
    "nextDialogs": [3471302, 3471303, 3471304],
    "content": "「鉴于此前发生了二哥与中原杂碎的不幸事件，我决定再次启用这里的信息公告版。以后，但凡有值得同步的事情，都请大家在这里留言说明。」",
    "id": 3471301
  },
  {
    "role": "旅行者",
    "nextDialogs": [3471305],
    "content": "阅读最新的留言…",
    "id": 3471302
  },
  {
    "role": "旅行者",
    "nextDialogs": [3471306],
    "content": "阅读较早的留言…",
    "id": 3471303
  },
  {
    "role": "旅行者",
    "nextDialogs": [],
    "content": "离开",
    "id": 3471304
  },
  ...
]
~~~

### Requirement
~~~
Python 3.6+
~~~

### Steps
1. Get GenshinData from [Dim's project](https://github.com/Dimbreath/GenshinData), you could git clone or download the zip and extract it.

**Note**: Search for yourself where Dim's project data is... (No longer in Github)

2. Run extract_dialogs.py. This process results in 3 output files in "extracted_dialog" folder:

- avatar.json: the parsed avatar information and descriptions
- dialog.jsonl: the parsed Genshin dialogues
- raw_dialog.jsonl: the raw Genshin dialogues (you can restore different dialogue branches yourself)

~~~
// Command line
python python extract_dialogs.py --repo=PATH/TO/GenshinData --lang=CHS --ignore_dialogue_branch

// The output are like the following
Below are string variables that appear in dialogs...
	Frequency	Variable
	84388	{NICKNAME}
	2746	{MATEAVATARSEXPRO[INFO_MALE_PRONOUN_BROTHER|INFO_FEMALE_PRONOUN_SISTER]}
	1273	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BROTHER|INFO_FEMALE_PRONOUN_SISTERA]}
	1051	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_HE|INFO_FEMALE_PRONOUN_SHE]}
	944	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_SISTER|INFO_FEMALE_PRONOUN_BROTHER]}
	896	{PLAYERAVATARSEXPRO[INFO_FEMALE_PRONOUN_SHE|INFO_MALE_PRONOUN_HE]}
	490	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYC|INFO_FEMALE_PRONOUN_GIRLC]}
	468	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_SHE|INFO_FEMALE_PRONOUN_HE]}
	441	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_YING|INFO_FEMALE_PRONOUN_BROTHER]}
	436	{PLAYERAVATARSEXPRO[INFO_FEMALE_PRONOUN_SISTER|INFO_MALE_PRONOUN_BROTHER]}
	408	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BIGBROTHER|INFO_FEMALE_PRONOUN_BIGSISTER]}
	336	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_GIRLD|INFO_FEMALE_PRONOUN_BOYD]}
	302	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOY|INFO_FEMALE_PRONOUN_GIRL]}
	211	{MATEAVATARSEXPRO[INFO_MALE_PRONOUN_HE|INFO_FEMALE_PRONOUN_SHE]}
	192	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BROTHER|INFO_FEMALE_PRONOUN_YING]}
	192	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_UNCLE|INFO_FEMALE_PRONOUN_AUNT]}
	144	{MATEAVATARSEXPRO[INFO_MALE_PRONOUN_BOY|INFO_FEMALE_PRONOUN_GIRL]}
	80	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_YING|INFO_FEMALE_PRONOUN_KONG]}
	64	{RUBY[D]Otets}
	36	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_HERO|INFO_FEMALE_PRONOUN_HEROINE]}
	34	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_SHE|INFO_MALE_PRONOUN_HE]}
	33	{MATEAVATARSEXPRO[INFO_MALE_PRONOUN_BOYD|INFO_FEMALE_PRONOUN_GIRLD]}
	31	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_HE|INFO_MALE_PRONOUN_SHE]}
	16	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BROANDSIS|INFO_FEMALE_PRONOUN_SISANDSIS]}
	16	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BROTHER|INFO_FEMALE_PRONOUN_SISTER]}
	15	{QuestNpcID}
	14	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_CUTEBIGBROTHER|INFO_FEMALE_PRONOUN_CUTEBIGSISTER]}
	11	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BROTHER|INFO_MALE_PRONOUN_BROANDSIS]}
	8	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_XIABOY|INFO_FEMALE_PRONOUN_XIAGIRL]}
	5	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYE|INFO_FEMALE_PRONOUN_GIRLE]}
	4	{MATEAVATARSEXPRO[INFO_FEMALE_PRONOUN_HE|INFO_MALE_PRONOUN_SHE]}
	2	{QuestGatherID}
	2	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYA|INFO_FEMALE_PRONOUN_GIRLA]}
	1	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYA|INFO_FEMALE_PRONOUN_GIRLB]}
	1	{PLAYERAVATARSEXPRO[INFO_MALE_PRONOUN_BOYA|INFO_FEMALE_PRONOUN_GIRLC]}

Total num of dialogs: 20630 (14965 storyline + 5665 avatar description)
Total num of unique utterances: 158396
Total num of unique talking roles: 2417
Average num of turns per dialog: 9.094280174503151

Output avatar at extracted_dialog/avatar_CHS.json
Output dialog at extracted_dialog/dialog_CHS.json
~~~

Note:

1. The dialogue output is in jsonl format: each line is a JSON structure. The JSON structure is a list of utterance dicts (containing role and content fields (which is just like ChatGPT messages))
2. There are already sampled outputs in the extracted_dialog folder for 3 languages, but you need to run the command yourself in order to get ***FULL dialogs*** (output file size is around 100+MB for each language)
3. Language options correspond to languages in Dim's GenshinData/TextMap (e.g., CHS, JA, ES, FR, etc.)
4. There are string variables in the dialogs, whose real value depends on one's main character choice in the game. Note that these string variables might have different names in different languages

### Known Issues

1. The current way of dealing with dialogue branches is naive and not satisfying, must work on a better way of representing branches. This is why raw_dialog.jsonl is also provided (you can restore dialogue branches yourself).
2. Some dialogues are **incomplete**, the relation between different sessions are unknown. (Better check out [hoyo_public_wiki_parser](https://github.com/mrzjy/hoyo_public_wiki_parser) to get more complete dialogues within a quest) 


### Extract miscellaneous things
~~~
// Command line
python extract_misc.py --repo=PATH/TO/GenshinData --lang=CHS

// This ends in excel files generated in extracted_misc
~~~
