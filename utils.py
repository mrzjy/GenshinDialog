import json
import re
import os
from collections import Counter


regexp_noise = re.compile(r"<[^>]+>|#")
regexp_string_var = "\\{[a-zA-Z_\\[\\]\\|]+\\}"


class GenshinLoader:
    def __init__(self, repo: str, lang="CHS"):
        """load Genshin Data."""
        self.lang = lang

        # load textMap
        with open(
            os.path.join(repo, "TextMap/TextMap{}.json".format(lang)),
            "r",
            encoding="utf-8",
        ) as f:
            self.map_hash_to_txt = json.load(f)

        # load avatar info
        self.map_avatar_to_info = get_avatar_info(repo, self.map_hash_to_txt)

        # load npc info
        self.map_npcId_to_name = {}
        with open(
            os.path.join(repo, "ExcelBinOutput/NpcExcelConfigData.json"),
            "r",
            encoding="utf-8",
        ) as f:
            npcList = json.load(f)
            for npc in npcList:
                npc_id = str(npc["id"])
                self.map_npcId_to_name[npc_id] = self.map_hash_to_txt.get(
                    str(npc["nameTextMapHash"]), str(npc["nameTextMapHash"])
                )

        # load raw dialog
        with open(
            os.path.join(repo, "ExcelBinOutput/DialogExcelConfigData.json"),
            "r",
            encoding="utf-8",
        ) as f:
            self.raw_dialog_list = json.load(f)

    def process_dialog(self, max_utter=1000):
        """generate readable in-game conversations"""
        # from story line
        dialog_list = extract_dialogs_from_storylines(
            self.raw_dialog_list,
            self.map_hash_to_txt,
            self.map_npcId_to_name,
            max_utter,
            self.lang,
        )

        # from avatar introduction
        extra_dialog_list = extract_dialogs_from_avatarInfo(
            max_utter, self.map_avatar_to_info, self.lang
        )
        dialog_list.extend(extra_dialog_list)

        # count statistics
        print("Summarizing statistics:")
        string_var_counter = Counter()
        sentence_set = set()
        speaker_set = set()
        num_turns = []
        for dialog in dialog_list:
            num_turns.append(len(dialog))
            for sentence in dialog:
                string_var_counter.update(re.findall(regexp_string_var, sentence))
                speaker, sentence = sentence.split("\t")
                sentence_set.add(sentence)
                speaker_set.add(speaker)
        print("Below are string variables that appear in dialogs...")
        print("\tFrequency\tVariable")
        for string_var, count in string_var_counter.most_common():
            print(f"\t{count}\t{string_var}")

        print(
            f"\nTotal num of dialogs: {len(dialog_list)} "
            f"({len(dialog_list) - len(extra_dialog_list)} storyline + {len(extra_dialog_list)} avatar description)"
        )
        print(f"Total num of unique utterances: {len(sentence_set)}")
        print(f"Total num of unique talking roles: {len(speaker_set)}")
        print(f"Average num of turns per dialog: {sum(num_turns) / len(num_turns)}")
        print()
        return dialog_list


def remove_tags(text):
    text = regexp_noise.sub("", text)
    return text.replace("\\n", "\n")


def get_avatar_info(repo, textMapHash):
    avatar2info = {}
    id2avatar = {}

    with open(
        os.path.join(repo, "ExcelBinOutput/AvatarExcelConfigData.json"),
        "r",
        encoding="utf-8",
    ) as f:
        infoList = json.load(f)
        for info in infoList:
            avatar_name = textMapHash.get(str(info["nameTextMapHash"]), "")
            avatar_desc = textMapHash.get(str(info["descTextMapHash"]), "")
            avatar_id = str(info["id"])
            if not len(avatar_name) or not len(avatar_desc):
                continue
            avatar2info[avatar_name] = {"desc": avatar_desc, "sayings": [], "story": []}
            id2avatar[avatar_id] = avatar_name

    with open(
        os.path.join(repo, "ExcelBinOutput/FetterInfoExcelConfigData.json"),
        "r",
        encoding="utf-8",
    ) as f:
        infoList = json.load(f)
        for info in infoList:
            avatar_name = id2avatar[str(info["avatarId"])]
            if avatar_name not in avatar2info:
                continue
            avatar2info[avatar_name]["native"] = textMapHash.get(
                str(info["avatarNativeTextMapHash"]), ""
            )
            avatar2info[avatar_name]["title"] = textMapHash.get(
                str(info["avatarTitleTextMapHash"]), ""
            )
            avatar2info[avatar_name]["constellation"] = textMapHash.get(
                str(info["avatarConstellationBeforTextMapHash"]), ""
            )
            avatar2info[avatar_name]["element"] = textMapHash.get(
                str(info["avatarVisionBeforTextMapHash"]), ""
            )
            if "InfoBirthMonth" in info and "InfoBirthDay" in info:
                avatar2info[avatar_name]["birthday"] = "{:d}.{:d}".format(
                    info["InfoBirthMonth"], info["InfoBirthDay"]
                )

    with open(
        os.path.join(repo, "ExcelBinOutput/FettersExcelConfigData.json"),
        "r",
        encoding="utf-8",
    ) as f:
        infoList = json.load(f)
        for info in infoList:
            avatar_name = id2avatar[str(info["avatarId"])]
            avatar2info[avatar_name]["sayings"] += [
                "{}\t{}".format(
                    textMapHash.get(str(info["voiceTitleTextMapHash"]), ""),
                    textMapHash.get(str(info["voiceFileTextTextMapHash"]), ""),
                )
            ]

    with open(
        os.path.join(repo, "ExcelBinOutput/FetterStoryExcelConfigData.json"),
        "r",
        encoding="utf-8",
    ) as f:
        infoList = json.load(f)
        for info in infoList:
            avatar_name = id2avatar[str(info["avatarId"])]
            avatar2info[avatar_name]["story"] += [
                "{}\t{}".format(
                    textMapHash.get(str(info["storyTitleTextMapHash"]), ""),
                    textMapHash.get(str(info["storyContextTextMapHash"]), ""),
                )
            ]

    # cleaning
    for avatar_name, infoDict in avatar2info.items():
        new_infoDict = {}
        for key, info in infoDict.items():
            if isinstance(info, list):
                clean_info = [remove_tags(i) for i in info]
            else:
                clean_info = remove_tags(info)
            new_infoDict[key] = clean_info

        avatar2info[avatar_name] = new_infoDict

    return avatar2info


def extract_dialogs_from_storylines(
    raw_dialog_list, map_hash_to_txt, map_npcId_to_name, max_utter, lang
):
    map_id_to_utterance = {}

    # dialogs from story lines
    for utter in raw_dialog_list:
        map_id_to_utterance[utter["id"]] = utter

    for uid, utter in map_id_to_utterance.items():
        for next_uid in utter["nextDialogs"]:
            if next_uid not in map_id_to_utterance:
                continue
            map_id_to_utterance[next_uid]["has_previous"] = True

    def trace_dialog_flow(cur_flow, all_flows):
        cur_uid = cur_flow[-1]
        if cur_uid not in map_id_to_utterance:
            return
        if len(map_id_to_utterance[cur_uid]["nextDialogs"]) == 0 and len(cur_flow) >= 2:
            all_flows.append(cur_flow)
            return
        else:
            for next_uid in map_id_to_utterance[cur_uid]["nextDialogs"]:
                if next_uid in cur_flow:  # must not form a cycle
                    continue
                next_flow = cur_flow + [next_uid]
                trace_dialog_flow(next_flow, all_flows)

    dialog_flows = []
    for uid, utter in map_id_to_utterance.items():
        # only trace dialog flows from dialog beginnings
        if "has_previous" in utter.keys() or not len(utter["nextDialogs"]):
            continue
        cur_dialog_flows = []
        trace_dialog_flow([uid], cur_dialog_flows)
        dialog_flows.extend(cur_dialog_flows)

    dialog_list = []
    for dialog_flow in dialog_flows:
        context = []
        speaker_set = set()
        for uid in dialog_flow:
            sentence_hash = str(map_id_to_utterance[uid]["talkContentTextMapHash"])
            if sentence_hash not in map_hash_to_txt:
                continue
            sentence = remove_tags(map_hash_to_txt[sentence_hash])
            speaker = get_role(
                uid, map_npcId_to_name, map_id_to_utterance, map_hash_to_txt, lang
            )
            speaker_set.add(speaker)
            if speaker == "unknown" or speaker == "":
                role_hash = str(map_id_to_utterance[uid]["talkRoleNameTextMapHash"])
                try_role_name = map_hash_to_txt.get(role_hash, "")
                speaker = try_role_name if try_role_name == "" else "unknown"
            context.append(speaker + "\t" + sentence)

        # each dialog must involves at least 2 speakers
        if len(context) and len(speaker_set) > 1:
            dialog_list.append(context[-max_utter:])
    return dialog_list


def extract_dialogs_from_avatarInfo(max_utter, avatar2info, lang):
    """We treat character sayings as dialog between traveller and character"""
    dialogs = []
    role = "Traveller" if lang != "CHS" else "旅行者"
    for avatar, info in avatar2info.items():
        sayings_list = info.get("sayings", [])
        for sayings in sayings_list:
            topic, content = sayings.split("\t")
            content = content.replace("\\n", "\n")
            if "{NICKNAME}" in content and "\\n" in content:
                # sayings of traveller involve paimon, which can be further splitted as dialogs
                sub_dialog = []
                for turn in content.split("\n"):
                    turn = turn.replace(": ", "：")
                    splits = turn.split("：")
                    if len(splits) != 2:
                        splits = [splits[0], "：".join(splits[1:])]

                    sub_dialog.append(
                        "{}\t{}".format(
                            splits[0] if splits[0] != "{NICKNAME}" else role,
                            splits[1],
                        )
                    )

                if len(sub_dialog) > max_utter:
                    for i in range(len(sub_dialog) - max_utter):
                        dialogs.append(sub_dialog[i : i + max_utter])
                else:
                    dialogs.append(sub_dialog)
                continue
            dialogs.append(
                [f"{role}\t{topic}", f"{avatar}\t{content}"]
            )
    return dialogs


def get_role(uid, map_npcId_to_name, map_id_to_utterance, map_hash_to_txt, lang="CHS"):
    role = "unknown"
    if map_id_to_utterance[uid]["talkRole"].get("id"):
        role = map_npcId_to_name.get(
            str(map_id_to_utterance[uid]["talkRole"]["id"]),
            str(map_id_to_utterance[uid]["talkRole"]["id"]),
        )
    else:
        role = map_hash_to_txt.get(
            str(map_id_to_utterance[uid]["talkRoleNameTextMapHash"]), role
        )

    if (
        "type" in map_id_to_utterance[uid]["talkRole"]
        and map_id_to_utterance[uid]["talkRole"]["type"] == "TALK_ROLE_PLAYER"
    ):
        role = "Traveller" if lang != "CHS" else "旅行者"
    return role
