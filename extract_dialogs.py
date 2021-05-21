import json
import sys
import argparse
import re
import os
from collections import Counter

sys.setrecursionlimit(1500)

TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def recursive(current_dialog_id, flow, all_flows):
    if current_dialog_id not in dialogId2info:
        return
    if len(dialogId2info[current_dialog_id]["NextDialogs"]) == 0:
        all_flows.append(flow)
        return
    else:
        for next_dialog_id in dialogId2info[current_dialog_id]["NextDialogs"]:
            flow_append = flow + [next_dialog_id]
            recursive(next_dialog_id, flow_append, all_flows)


def get_role(i):
    role = "unknown"
    if "Id" in dialogId2info[i]["TalkRole"] and dialogId2info[i]["TalkRole"]["Id"] != "":
        role = npcId2Name.get(str(dialogId2info[i]["TalkRole"]["Id"]), str(dialogId2info[i]["TalkRole"]["Id"]))
    if "Type" in dialogId2info[i]["TalkRole"] and dialogId2info[i]["TalkRole"]["Type"] == "TALK_ROLE_PLAYER":
        role = "PLAYER"
    return role


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default='PATH_TO_GENSHINDATA', type=str, required=False, help='data dir')
    parser.add_argument('--lang', default='CHS', type=str, required=False, help='language type')
    parser.add_argument('--n_utter', default=4, type=int, required=False, help='max number of utterances for a session')
    args = parser.parse_args()

    with open(os.path.join(args.repo, "TextMap/Text{}.json".format(args.lang)), "r", encoding="utf-8") as f:
        textMapHash = json.load(f)

    npcId2Name = {}
    with open(os.path.join(args.repo, "ExcelBinOutput/NpcExcelConfigData.json"), "r") as f:
        npcList = json.load(f)
        for npc in npcList:
            npcId2Name[str(npc["Id"])] = textMapHash.get(str(npc["NameTextMapHash"]), str(npc["NameTextMapHash"]))

    with open(os.path.join(args.repo, "ExcelBinOutput/DialogExcelConfigData.json"), "r") as f:
        dialogs = json.load(f)

    dialogId2info = {}
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

    already = set()
    scenes = []
    speaker_counter = Counter()
    for dialog_id, dialog in dialogId2info.items():
        speaker = get_role(dialog_id)
        speaker_counter.update([speaker])
        if dialog_id in already:
            continue

        if len(dialog["NextDialogs"]) > 1:
            all_flows = []
            try:
                recursive(dialog_id, flow=[dialog_id], all_flows=all_flows)
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
                    output_dialog.add(str(context[-args.n_utter:]))

    print("Speaker counter (occurrence of speaker in the generated corpus):")
    print(speaker_counter)
    with open("extracted_dialog/output_dialog_{}.txt".format(args.lang), "w") as f:
        print("\n".join(list(output_dialog)), file=f)
    print("Output at extracted_dialog/output_dialog_{}.txt".format(args.lang))