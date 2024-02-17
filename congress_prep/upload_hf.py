"""
Upload scrapes to HF
"""

from pathlib import Path
from typing import Optional, Union

from huggingface_hub import HfApi
import pandas as pd
import rich


def upload_hf(congress_hf_path: Union[str, Path], congress_nums: list[int], file_types: list[str]):
    """Upload local files to huggingface

    congress_hf_path: directory storing local parquet files
    congress_nums: list of congress numbers e.g. [113, 114, 115]
    file_types: list of file types to upload
    """

    congress_hf_path = Path(congress_hf_path)
    api = HfApi()

    repo_id = f"hyperdemocracy/us-congress"
    api.create_repo(
        repo_id=repo_id,
        repo_type="dataset",
        exist_ok=True,
    )

    fpath = congress_hf_path / "README.md"
    rich.print(f"{fpath=}")
    api.upload_file(
        path_or_fileobj=fpath,
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="dataset",
    )

    for cn in congress_nums:

        rich.print(f"congress_num={cn}")

        # upload billstatus xml files
        # --------------------------------
        file_type = "billstatus_xml"
        if file_type in file_types:
            tag = f"usc-{cn}-billstatus-xml"
            fpath = congress_hf_path / f"{tag}.parquet"
            if fpath.exists():
                rich.print(f"{fpath=}")
                api.upload_file(
                    path_or_fileobj=fpath,
                    path_in_repo=str(Path("data") / file_type / fpath.name),
                    repo_id=repo_id,
                    repo_type="dataset",
                )

        # upload textversions xml files
        # --------------------------------
        for xml_type in ["ddt_xml", "uslm_xml"]:
            file_type = f"textversions_{xml_type}"
            if file_type in file_types:
                tag = "usc-{}-textversions-{}".format(cn, xml_type.replace("_", "-"))
                fpath = congress_hf_path / f"{tag}.parquet"
                if fpath.exists():
                    rich.print(f"{fpath=}")
                    api.upload_file(
                        path_or_fileobj=fpath,
                        path_in_repo=str(Path("data") / file_type / fpath.name),
                        repo_id=repo_id,
                        repo_type="dataset",
                    )

        # upload billstatus parsed files
        # --------------------------------
        file_type = "billstatus_parsed"
        if file_type in file_types:
            tag = f"usc-{cn}-billstatus-parsed"
            fpath = congress_hf_path / f"{tag}.parquet"
            if fpath.exists():
                rich.print(f"{fpath=}")
                api.upload_file(
                    path_or_fileobj=fpath,
                    path_in_repo=str(Path("data") / file_type / fpath.name),
                    repo_id=repo_id,
                    repo_type="dataset",
                )

        # upload unified v1 files
        # --------------------------------
        file_type = "unified_v1"
        if file_type in file_types:
            tag = f"usc-{cn}-unified-v1"
            fpath = congress_hf_path / f"{tag}.parquet"
            if fpath.exists():
                rich.print(f"{fpath=}")
                api.upload_file(
                    path_or_fileobj=fpath,
                    path_in_repo=str(Path("data") / file_type / fpath.name),
                    repo_id=repo_id,
                    repo_type="dataset",
                )



if __name__ == "__main__":

    congress_hf_path = Path("/Users/galtay/data/congress-hf")
    file_types = [
#        "billstatus_xml",
#        "textversions_ddt_xml",
#        "textversions_uslm_xml",
#        "billstatus_parsed",
        "unified_v1",
    ]
    congress_nums = list(range(113, 119))
    upload_hf(congress_hf_path, congress_nums, file_types)
