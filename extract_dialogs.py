import json
import argparse
import os

from utils import GenshinLoader


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        default="Path/To/AnimeGameData",
        type=str,
        required=True,
        help="data dir",
    )
    parser.add_argument("--lang", default="CHS", type=str, help="language type")
    parser.add_argument(
        "--n_utter",
        default=1000,
        type=int,
        help="max number of utterances for a session",
    )
    args = parser.parse_args()

    # load genshin data
    genshin = GenshinLoader(repo=args.repo, lang=args.lang)

    # process
    output_dialog_list = genshin.process_dialog(max_utter=args.n_utter)

    # output avatar
    output_dir = "extracted_dialog"
    output_file = os.path.join(output_dir, "avatar_{}.json".format(args.lang))
    with open(output_file, "w", encoding="utf-8") as f:
        json_file = json.dumps(
            genshin.map_avatar_to_info, sort_keys=True, indent=4, ensure_ascii=False
        )
        print(json_file, file=f)
    print("Output avatar at {}".format(output_file))

    # output dialog
    if len(output_dialog_list):
        output_file = os.path.join(output_dir, "dialog_{}.jsonl".format(args.lang))
        with open(output_file, "w", encoding="utf-8") as f:
            for dialog in output_dialog_list:
                print(json.dumps(dialog, ensure_ascii=False), file=f)
        print("Output dialog at {}".format(output_file))
