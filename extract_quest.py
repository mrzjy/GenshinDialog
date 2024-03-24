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
    for file in glob.iglob(os.path.join(repo, "BinOutput/CodexQuest/*.json")):
        with open(file, "r", encoding="utf-8") as f:
            lines = ""
            for line in f:
                if m := re.search(r"\"textId\": (?P<hash>\d+)", line):
                    replace = map_hash_to_txt.get(m["hash"], "")
                    if replace:
                        replace = json.dumps(replace, ensure_ascii=False)
                    line = line.replace(m["hash"], f"{replace}" if replace else "null")
                lines += line
            sample = json.loads(lines)
            if sample:
                samples.append(sample)

    with open(f"extracted_quest/quest_{lang}.jsonl", "w", encoding="utf-8") as f:
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
    parser.add_argument("--lang", default="EN", type=str, help="language type")
    args = parser.parse_args()

    get_quest_dialogue(args.repo, args.lang)
