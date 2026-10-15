"""Download the public UCI Online Retail workbook."""

from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
ZIP_PATH = RAW_DIR / "online-retail.zip"
SOURCE_URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading the UCI dataset from {SOURCE_URL}")
    with urlopen(SOURCE_URL, timeout=60) as response:
        ZIP_PATH.write_bytes(response.read())

    with ZipFile(ZIP_PATH) as archive:
        workbook = next(
            (name for name in archive.namelist() if name.lower().endswith(".xlsx")),
            None,
        )
        if workbook is None:
            raise RuntimeError("The downloaded archive does not contain an .xlsx workbook.")
        target = RAW_DIR / "Online Retail.xlsx"
        target.write_bytes(archive.read(workbook))

    ZIP_PATH.unlink()
    print(f"Saved source workbook to {target}")


if __name__ == "__main__":
    main()
