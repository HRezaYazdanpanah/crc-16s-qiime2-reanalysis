import csv
import hashlib
from pathlib import Path
from urllib.request import urlopen

with open("metadata/pilot_fastq_report.tsv", newline="") as f:
    records = list(csv.DictReader(f, delimiter="\t"))

folder = Path("data/raw/pilot")
folder.mkdir(parents=True, exist_ok=True)

def verify(path, row):
    if path.stat().st_size != int(row["bytes"]):
        raise ValueError(f"Size mismatch: {path.name}")
    with path.open("rb") as f:
        actual = hashlib.file_digest(f, "md5").hexdigest()
    if actual != row["md5"]:
        raise ValueError(f"MD5 mismatch: {path.name}")

for row in records:
    name = row["ftp_url"].rsplit("/", 1)[1]
    target = folder / name

    if target.exists():
        verify(target, row)
        print(f"Already verified: {name}", flush=True)
        continue

    partial = folder / (name + ".part")
    print(f"Downloading: {name}", flush=True)

    with urlopen(row["ftp_url"], timeout=120) as response:
        with partial.open("wb") as f:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)

    verify(partial, row)
    partial.rename(target)
    print(f"Verified size and MD5: {name}", flush=True)

print(f"Completed: {len(records)} FASTQ files verified.")
