import argparse
import glob
import json
import os
import re


def get_quest_dialogue(repo, lang):
    with open(
            os.path.join(repo, f"TextMap/TextMap{lang}.json"),
            "r",
            encoding="utf-8",
    ) as f:
        map_hash_to_txt = json.load(f)

    samples = []
    for file in glob.iglob(os.path.join(repo, "BinOutput/Talk/Gadget/*.json")):
        with open(file, "r", encoding="utf-8") as f:
            sample = json.load(f)
            dialog_list = []
            for utterance in sample.get("dialogList", []):
                dialog_list.append({
                    "id": utterance["id"],
                    "nextDialogs": utterance.get("nextDialogs", None),
                    "role": map_hash_to_txt.get(str(utterance.get("talkRoleNameTextMapHash")), None),
                    "content": map_hash_to_txt.get(str(utterance.get("talkContentTextMapHash")), None),
                    "role_type": utterance["talkRole"].get("type")
                })
            if dialog_list and dialog_list[0]["content"]:
                samples.append({
                    "id": sample["talkId"],
                    "dialogList": dialog_list
                })

    with open(f"extracted_talk/talk_gadget_{lang}.jsonl", "w", encoding="utf-8") as f:
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

    get_quest_dialogue(args.repo, args.lang)
