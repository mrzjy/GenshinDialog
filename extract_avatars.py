import glob
import json
import argparse
import os
import re
from multiprocessing import Pool

from utils import GenshinLoader


def single_process(file, args):
    lang = re.search("TextMap(?P<lang>[A-Z]+).json$", file)["lang"]
    # load genshin data
    genshin = GenshinLoader(repo=args.repo, lang=lang)
    # output avatar
    output_dir = "extracted_avatar"
    output_file = os.path.join(output_dir, "avatar_{}.json".format(lang))
    with open(output_file, "w", encoding="utf-8") as f:
        json_file = json.dumps(
            genshin.map_avatar_to_info, sort_keys=True, indent=4, ensure_ascii=False
        )
        print(json_file, file=f)
    print("Output avatar at {}".format(output_file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        default="../AnimeGameData",
        type=str,
        # required=True,
        help="data dir",
    )
    args = parser.parse_args()

    files = list(glob.iglob(os.path.join(args.repo, "TextMap/TextMap*.json")))

    pool = Pool(10)
    pool.starmap(single_process, [[file, args] for file in files])

