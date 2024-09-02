import argparse
import json
import os
import re
import glob
import pandas as pd


class GenshinLoader:
    def __init__(self, repo: str, lang="CHS"):
        """load Genshin Data."""
        self.repo = repo
        self.lang = lang

        # load textMap
        with open(
            os.path.join(repo, "TextMap", "TextMap{}.json".format(lang)),
            "r",
            encoding="utf-8",
        ) as f:
            self.map_hash_to_txt = json.load(f)

        # load material
        self.map_materialId_to_info = {}
        with open(
            os.path.join(repo, "ExcelBinOutput", "MaterialExcelConfigData.json"),
            "r",
            encoding="utf-8",
        ) as f:
            material_list = json.load(f)
            for material in material_list:
                material_id = material["id"]
                del material["id"]
                self.map_materialId_to_info[material_id] = material

        # load weapon
        self.map_weaponId_to_info = {}
        with open(
            os.path.join(self.repo, "ExcelBinOutput", "WeaponExcelConfigData.json"),
            "r",
            encoding="utf-8",
        ) as f:
            weapon_list = json.load(f)
            for weapon in weapon_list:
                weapon_id = weapon["id"]
                del weapon["id"]
                self.map_weaponId_to_info[weapon_id] = weapon

        # load reliquary
        self.map_relicId_to_info = {}
        with open(
            os.path.join(self.repo, "ExcelBinOutput", "ReliquaryExcelConfigData.json"),
            "r",
            encoding="utf-8",
        ) as f:
            relic_list = json.load(f)
            for relic in relic_list:
                relic_id = relic["id"]
                self.map_relicId_to_info[relic_id] = relic

    def output_excel(self, map_dict, out_file, skip_columns=None):
        columns = set()
        for mid, info in map_dict.items():
            columns.update(list(info.keys()))

        columns = list(columns)
        if skip_columns and isinstance(skip_columns, set):
            columns = [c for c in list(columns) if c.lower() not in skip_columns]
        columns = sorted(columns)

        data_list = []
        for idx, info in map_dict.items():
            is_skip = False
            for k, v in info.items():
                if not v:
                    info[k] = ""
                if "text" in k.lower():
                    info[k] = self.map_hash_to_txt.get(str(v), str(v))
                    if k == "nameTextMapHash" and (not info[k] or "test" in info[k]):
                        is_skip = True
                        break
            if is_skip:
                continue
            data_list.append([idx] + [info.get(col, "") for col in columns])

        # save as excel
        df = pd.DataFrame(data_list, columns=["id"] + columns)
        df.to_excel(out_file, index=False)

        print(f"{len(data_list)} data extracted at {out_file}")

    def process_wings(self):
        """add story context for fly cloaks (wings)"""
        all_readable_files = list(
            glob.iglob(os.path.join(self.repo, "Readable", self.lang, "*"))
        )
        files = [f for f in all_readable_files if "Wings" in f]
        for wing_story_file in files:
            material_id = re.match(".+Wings(\d+).txt", wing_story_file).group(1)
            with open(wing_story_file, "r", encoding="utf-8") as g:
                story = "".join(g.readlines())
            self.map_materialId_to_info[int(material_id)]["ReadableText"] = story

    def process_weapons(self):
        """add story context and 5-level weapon skill descriptions"""
        all_readable_files = list(
            glob.iglob(os.path.join(self.repo, "Readable", self.lang, "*"))
        )
        files = [f for f in all_readable_files if "Weapon" in f]
        # load story
        for weapon_file in files:
            # 使用单个正则表达式匹配两种格式
            match = re.match(r".+Weapon(\d+)(?:_(\d))?.txt", weapon_file)
            if not match:
                continue  # 如果文件名不匹配，跳过

            idx1 = int(match.group(1))
            idx2 = match.group(2)  # idx2 可能是 None

            # 读取文件内容
            with open(weapon_file, "r", encoding="utf-8") as g:
                story = "".join(g.readlines()).strip("\n")

            # 根据 idx2 的存在与否决定字典键名
            readable_text_key = f"ReadableText{idx2}" if idx2 else "ReadableText1"

            # 更新字典中的内容
            self.map_weaponId_to_info[idx1][readable_text_key] = story

        # load skill description
        map_skillId_to_affixList = {}
        map_affixId_to_info = {}
        with open(
            os.path.join(self.repo, "ExcelBinOutput", "EquipAffixExcelConfigData.json"),
            "r",
            encoding="utf-8",
        ) as f:
            skill_list = json.load(f)
            for skill in skill_list:
                map_affixId_to_info[skill["affixId"]] = skill
                if skill["id"] not in map_skillId_to_affixList:
                    map_skillId_to_affixList[skill["id"]] = []
                map_skillId_to_affixList[skill["id"]] += [skill["affixId"]]

        # mix skill descriptions (from level 1 to level 5)
        for weapon_id, info in self.map_weaponId_to_info.items():
            skill_id = info["skillAffix"][0]
            if skill_id in map_skillId_to_affixList:
                affixes = map_skillId_to_affixList[skill_id]
                name_hash = str(map_affixId_to_info[affixes[0]]["nameTextMapHash"])
                skill_name = self.map_hash_to_txt.get(name_hash, "")
                skill_descs = []
                for aid in affixes:
                    desc_hash = str(map_affixId_to_info[aid]["descTextMapHash"])
                    skill_desc = self.map_hash_to_txt.get(desc_hash, "")
                    skill_descs.append(
                        re.sub("(<color=#99FFFFFF>|</color>)", "", skill_desc)
                    )
                self.map_weaponId_to_info[weapon_id]["skillName"] = skill_name
                self.map_weaponId_to_info[weapon_id]["skillDesc"] = "\n".join(
                    skill_descs
                )
            del self.map_weaponId_to_info[weapon_id]["skillAffix"]

    def process_reliquary(self):
        """add story context and set skill descriptions"""
        all_readable_files = list(
            glob.iglob(os.path.join(self.repo, "Readable", self.lang, "*"))
        )
        files = [f for f in all_readable_files if "Relic" in f]
        # load story
        map_icon_to_story = {}
        for file in files:
            idx = re.match(".+Relic([\d_]+).txt", file).group(1)
            with open(file, "r", encoding="utf-8") as g:
                story = "".join(g.readlines()).strip("\n")
            if not story:
                continue
            map_icon_to_story[idx] = story
        for idx, info in self.map_relicId_to_info.items():
            icon = re.match(".+_(\d+_\d+)$", info["icon"]).group(1)
            if icon not in map_icon_to_story:
                continue
            self.map_relicId_to_info[idx]["ReadableText"] = map_icon_to_story[icon]

        # load skill description
        map_skillId_to_affixList = {}
        map_affixId_to_info = {}
        with open(
            os.path.join(self.repo, "ExcelBinOutput", "EquipAffixExcelConfigData.json"),
            "r",
            encoding="utf-8",
        ) as f:
            for skill in json.load(f):
                map_affixId_to_info[skill["affixId"]] = skill
                if skill["id"] not in map_skillId_to_affixList:
                    map_skillId_to_affixList[skill["id"]] = []
                map_skillId_to_affixList[skill["id"]] += [skill["affixId"]]

        # load relic set
        with open(
            os.path.join(
                self.repo, "ExcelBinOutput", "ReliquarySetExcelConfigData.json"
            ),
            "r",
            encoding="utf-8",
        ) as f:
            for relic_set in json.load(f):
                if "EquipAffixId" not in relic_set:
                    continue
                skill_id = relic_set["EquipAffixId"]
                affixes = map_skillId_to_affixList[skill_id]
                name_hash = str(map_affixId_to_info[affixes[0]]["nameTextMapHash"])
                skill_name = self.map_hash_to_txt.get(name_hash, "")
                skill_descs = []
                for aid in affixes:
                    desc_hash = str(map_affixId_to_info[aid]["descTextMapHash"])
                    skill_desc = self.map_hash_to_txt.get(desc_hash, "")
                    skill_descs.append(skill_desc)

                for idx in relic_set["containsList"]:
                    self.map_relicId_to_info[idx]["setSkillName"] = skill_name
                    self.map_relicId_to_info[idx]["setSkillDesc"] = "\n".join(
                        skill_descs
                    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo", default="Path/To/AnimeGameData", type=str, help="data dir"
    )
    parser.add_argument("--lang", default="CHS", type=str, help="language type")
    args = parser.parse_args()

    output_dir = "extracted_misc"

    genshin = GenshinLoader(repo=args.repo, lang=args.lang)
    genshin.process_wings()
    genshin.output_excel(
        map_dict=genshin.map_materialId_to_info,
        out_file=os.path.join(output_dir, f"material_{args.lang}.xlsx"),
    )

    genshin.process_weapons()
    genshin.output_excel(
        map_dict=genshin.map_weaponId_to_info,
        out_file=os.path.join(output_dir, f"weapon_{args.lang}.xlsx"),
    )

    genshin.process_reliquary()
    genshin.output_excel(
        map_dict=genshin.map_relicId_to_info,
        out_file=os.path.join(output_dir, f"reliquary_{args.lang}.xlsx"),
    )
