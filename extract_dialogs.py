import json
import sys
import argparse
import re
import os
from collections import Counter

sys.setrecursionlimit(1500)

TAG_RE = re.compile(r'<[^>]+>|#')


def remove_tags(text):
    return TAG_RE.sub('', text)


def extract_dialogs_from_avatarInfo(args, avatar2info):
    dialogs = []
    for avatar, info in avatar2info.items():
        sayings_list = info.get("sayings", [])
        for sayings in sayings_list:
            topic, content = sayings.split("\t")
            if "{NICKNAME}" in content and "\\n" in content:
                # sayings of traveller involve paimon, which can be further splitted as dialogs
                sub_dialog = []
                for turn in content.split("\\n"):
                    turn = turn.replace(": ", "：")
                    splits = turn.split("：")
                    if len(splits) != 2:
                        splits = [splits[0], "：".join(splits[1:])]

                    sub_dialog.append("{}\t{}".format(splits[0] if splits[0] != "{NICKNAME}" else "PLAYER", splits[1]))

                if len(sub_dialog) > args.n_utter:
                    for i in range(len(sub_dialog) - args.n_utter):
                        dialogs.append(sub_dialog[i:i+args.n_utter])
                else:
                    dialogs.append(sub_dialog)
                continue
            dialogs.append(["PLAYER\t{}".format(topic), "{}\t{}".format(avatar, content)])
    return dialogs


def get_dialogs(args, textMapHash, avatar2info):
    npcId2Name = {}
    dialogId2info = {}

    with open(os.path.join(args.repo, "ExcelBinOutput/NpcExcelConfigData.json"), "r", encoding="utf-8") as f:
        npcList = json.load(f)
        for npc in npcList:
            npcId2Name[str(npc["Id"])] = textMapHash.get(str(npc["NameTextMapHash"]), str(npc["NameTextMapHash"]))

    with open(os.path.join(args.repo, "ExcelBinOutput/DialogExcelConfigData.json"), "r", encoding="utf-8") as f:
        dialogs = json.load(f)

    count = 0
    all_role_ids = set()
    all_types = set()
    for i, dialog in enumerate(dialogs):
        all_types.update([dialog["TalkRole"].get("Type", "")])
        all_role_ids.update([dialog["TalkRole"].get("Id", "")])
        dialog = {k: v if "TextMapHash" not in k else textMapHash.get(str(v), v) for k, v in dialog.items()}
        dialog_id = dialog["Id"]
        del dialog["Id"]
        dialogId2info[dialog_id] = dialog
        if len(dialog["NextDialogs"]) > 1:
            count += 1

    print("Total num of roles in dialogs:", len(all_role_ids))
    print("Total num of utterances:", len(dialogId2info))

    def trace_dialog_flow(current_dialog_id, flow, all_flows):
        if current_dialog_id not in dialogId2info:
            return
        if len(dialogId2info[current_dialog_id]["NextDialogs"]) == 0:
            all_flows.append(flow)
            return
        else:
            for next_dialog_id in dialogId2info[current_dialog_id]["NextDialogs"]:
                flow_append = flow + [next_dialog_id]
                trace_dialog_flow(next_dialog_id, flow_append, all_flows)

    def get_role(i):
        role = "unknown"
        if "Id" in dialogId2info[i]["TalkRole"] and dialogId2info[i]["TalkRole"]["Id"] != "":
            role = npcId2Name.get(str(dialogId2info[i]["TalkRole"]["Id"]), str(dialogId2info[i]["TalkRole"]["Id"]))
        if "Type" in dialogId2info[i]["TalkRole"] and dialogId2info[i]["TalkRole"]["Type"] == "TALK_ROLE_PLAYER":
            role = "PLAYER"
        return role

    already = set()
    scenes = []
    for dialog_id, dialog in dialogId2info.items():
        if dialog_id in already:
            continue

        if len(dialog["NextDialogs"]) > 1:
            all_flows = []
            try:
                trace_dialog_flow(dialog_id, flow=[dialog_id], all_flows=all_flows)
            except:
                pass
            for flow in all_flows:
                already.update([i for i in flow])

            scenes.append(all_flows)

    output_dialog = set()
    for i, scene in enumerate(scenes):
        for m, flow in enumerate(scene):
            context = []
            for j in flow:
                sentence = remove_tags(dialogId2info[j]["TalkContentTextMapHash"])
                speaker = get_role(j)
                if speaker == "unknown" or speaker == "":
                    try_name = dialogId2info[j]["TalkRoleNameTextMapHash"]
                    speaker = try_name if try_name == "" else "unknown"
                if sentence != "":
                    context.append(speaker + "\t" + sentence)
                if len(context[-args.n_utter:]) > 1:

                    if args.speaker != "":
                        if speaker != args.speaker:
                            continue

                    output_dialog.add(str(context[-args.n_utter:]))

    extra_dialogs = extract_dialogs_from_avatarInfo(args, avatar2info)
    for d in extra_dialogs:
        output_dialog.add(str(d))
    print("Total num of dialog sessions: {}".format(len(output_dialog)))
    return output_dialog


def get_avatar_info(repo, textMapHash):
    avatar2info = {}
    id2avatar = {}

    with open(os.path.join(repo, "ExcelBinOutput/AvatarExcelConfigData.json"), "r", encoding="utf-8") as f:
        infoList = json.load(f)
        for info in infoList:
            avatar_name = textMapHash.get(str(info["NameTextMapHash"]), "")
            avatar_desc = textMapHash.get(str(info["DescTextMapHash"]), "")
            avatar_id = str(info["Id"])
            if not len(avatar_name) or not len(avatar_desc):
                continue
            avatar2info[avatar_name] = {"desc": avatar_desc, "sayings": [], "story": []}
            id2avatar[avatar_id] = avatar_name

    with open(os.path.join(repo, "ExcelBinOutput/FetterInfoExcelConfigData.json"), "r", encoding="utf-8") as f:
        infoList = json.load(f)
        for info in infoList:
            avatar_name = id2avatar[str(info["AvatarId"])]
            if avatar_name not in avatar2info:
                continue
            avatar2info[avatar_name]["native"] = textMapHash.get(str(info["AvatarNativeTextMapHash"]), "")
            avatar2info[avatar_name]["title"] = textMapHash.get(str(info["AvatarTitleTextMapHash"]), "")
            avatar2info[avatar_name]["constellation"] = textMapHash.get(
                str(info["AvatarConstellationBeforTextMapHash"]), "")
            avatar2info[avatar_name]["element"] = textMapHash.get(str(info["AvatarVisionBeforTextMapHash"]), "")
            if "InfoBirthMonth" in info and "InfoBirthDay" in info:
                avatar2info[avatar_name]["birthday"] = "{:d}.{:d}".format(info["InfoBirthMonth"], info["InfoBirthDay"])

    with open(os.path.join(repo, "ExcelBinOutput/FettersExcelConfigData.json"), "r", encoding="utf-8") as f:
        infoList = json.load(f)
        for info in infoList:
            avatar_name = id2avatar[str(info["AvatarId"])]
            avatar2info[avatar_name]["sayings"] += ["{}\t{}".format(
                textMapHash.get(str(info["VoiceTitleTextMapHash"]), ""),
                textMapHash.get(str(info["VoiceFileTextTextMapHash"]), ""))]

    with open(os.path.join(repo, "ExcelBinOutput/FetterStoryExcelConfigData.json"), "r", encoding="utf-8") as f:
        infoList = json.load(f)
        for info in infoList:
            avatar_name = id2avatar[str(info["AvatarId"])]
            avatar2info[avatar_name]["story"] += ["{}\t{}".format(
                textMapHash.get(str(info["StoryTitleTextMapHash"]), ""),
                textMapHash.get(str(info["StoryContextTextMapHash"]), ""))]

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default='PATH_TO_GENSHINDATA', type=str, required=True, help='data dir')
    parser.add_argument('--lang', default='CHS', type=str, required=False, help='language type')
    parser.add_argument('--n_utter', default=4, type=int, required=False, help='max number of utterances for a session')
    parser.add_argument('--speaker', default="", type=str, required=False,
                        help='extract dialogs of all speakers by default, however one can specify a speaker name so as '
                             'to only extract his/her dialog')
    args = parser.parse_args()

    with open(os.path.join(args.repo, "TextMap/TextMap{}.json".format(args.lang)), "r", encoding="utf-8") as f:
        textMapHash = json.load(f)

    avatar2info = get_avatar_info(args.repo, textMapHash)
    with open("extracted_dialog/output_avatar_{}.json".format(args.lang), "w", encoding='utf-8') as f:
        json_file = json.dumps(avatar2info, sort_keys=True, indent=4, ensure_ascii=False)
        print(json_file, file=f)
    print("Output at extracted_dialog/output_avatar_{}.json".format(args.lang))

    output_dialog = get_dialogs(args, textMapHash, avatar2info)
    if len(output_dialog):
        output_file = "extracted_dialog/output_dialog_{}.txt".format(args.lang)
        if args.speaker != "":
            output_file = "extracted_dialog/output_dialog_{}_{}.txt".format(args.lang, args.speaker)
        with open(output_file, "w", encoding='utf-8') as f:
            print("\n".join(list(output_dialog)), file=f)
        print("Output at {}".format(output_file))
    else:
        if args.speaker != "":
            print("No dialogs found. check if the speaker {} exists".format(args.speaker))
        else:
            print("No dialogs found.")