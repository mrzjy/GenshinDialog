import argparse
import glob
import json
import os
import re


def get_role(utterance):
    role = None
    if utterance["talkRole"].get("id"):
        role = map_npcId_to_name.get(
            str(utterance["talkRole"]["id"]),
            str(utterance["talkRole"]["id"]),
        )
    elif "talkRoleNameTextMapHash" in utterance:
        role = map_hash_to_txt.get(
            str(utterance["talkRoleNameTextMapHash"]), role
        )
    return role


def get_talk(repo, input_path, output_path):
    samples = []
    for file in glob.iglob(os.path.join(repo, input_path)):
        with open(file, "r", encoding="utf-8") as f:
            sample = json.load(f)
            dialog_list = []
            for utterance in sample.get("dialogList", []):
                dialog_list.append({
                    "id": utterance["id"],
                    "nextDialogs": utterance.get("nextDialogs", None),
                    "role": get_role(utterance),
                    "content": map_hash_to_txt.get(str(utterance.get("talkContentTextMapHash")), None),
                    "role_type": utterance["talkRole"].get("type")
                })
            if dialog_list and dialog_list[0]["content"] and not re.search(r"(\(test\)|\$UNRELEASED)",
                                                                           str(dialog_list)):
                samples.append({
                    "id": sample["talkId"],
                    "dialogList": dialog_list
                })

    with open(f"extracted_talk/{output_path}", "w", encoding="utf-8") as f:
        for sample in samples:
            print(json.dumps(sample, ensure_ascii=False), file=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        default="../AnimeGameData",
        type=str,
        required=True,
        help="data dir",
    )
    parser.add_argument("--lang", default="CHS", type=str, help="language type")
    args = parser.parse_args()

    with open(
            os.path.join(args.repo, f"TextMap/TextMap{args.lang}.json"),
            "r",
            encoding="utf-8",
    ) as f:
        map_hash_to_txt = json.load(f)

    map_npcId_to_name = {}
    with open(
            os.path.join(args.repo, "ExcelBinOutput/NpcExcelConfigData.json"),
            "r",
            encoding="utf-8",
    ) as f:
        npcList = json.load(f)
        for npc in npcList:
            npc_id = str(npc["id"])
            map_npcId_to_name[npc_id] = map_hash_to_txt.get(
                str(npc["nameTextMapHash"]), str(npc["nameTextMapHash"])
            )

    get_talk(args.repo, input_path="BinOutput/Talk/Gadget/*.json", output_path=f"talk_gadget_{args.lang}.jsonl")
    get_talk(args.repo, input_path="BinOutput/Talk/NPC/*.json", output_path=f"talk_npc_{args.lang}.jsonl")
    get_talk(args.repo, input_path="BinOutput/Talk/Blossom/*.json", output_path=f"talk_blossom_{args.lang}.jsonl")
    get_talk(args.repo, input_path="BinOutput/Talk/Coop/*.json", output_path=f"talk_coop_{args.lang}.jsonl")
    get_talk(args.repo, input_path="BinOutput/Talk/Activity/*.json", output_path=f"talk_activity_{args.lang}.jsonl")
