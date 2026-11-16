import csv
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen

with open("metadata/main_fastq_report.tsv", newline="") as f:
    records = list(csv.DictReader(f, delimiter="\t"))

with open("metadata/main_subset_80.tsv", newline="") as f:
    selected = list(csv.DictReader(f, delimiter="\t"))

assert len(records) == 160
assert {r["Run"] for r in records} == {r["Run"] for r in selected}
assert len({(r["Run"], r["mate"]) for r in records}) == 160
assert all(
    {r["mate"] for r in records if r["Run"] == s["Run"]} == {"1", "2"}
    for s in selected
)

folder = Path("data/raw/main")

def verify(path, row):
    if path.stat().st_size != int(row["bytes"]):
        raise ValueError(f"Size mismatch: {path.name}")
    with path.open("rb") as f:
        actual = hashlib.file_digest(f, "md5").hexdigest()
    if actual != row["md5"]:
        raise ValueError(f"MD5 mismatch: {path.name}")

def download(row):
    name = f"{row['Run']}_{row['mate']}.fastq.gz"
    assert row["ftp_url"].endswith("/" + name)
    target = folder / name
    partial = folder / (name + ".part")

    if target.exists():
        verify(target, row)
        return f"ALREADY VERIFIED: {name}"

    pilot = Path("data/raw/pilot") / name
    if pilot.exists():
        verify(pilot, row)
        import shutil
        shutil.copyfile(pilot, partial)
        verify(partial, row)
        partial.replace(target)
        return f"REUSED VERIFIED PILOT FASTQ: {name}"

    for attempt in range(1, 4):
        try:
            print(f"DOWNLOAD attempt={attempt}: {name}", flush=True)
            with urlopen(row["ftp_url"], timeout=120) as response:
                with partial.open("wb") as f:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
            verify(partial, row)
            partial.replace(target)
            return f"VERIFIED: {name}"
        except Exception as error:
            print(f"RETRY/ERROR {name}: {error}", flush=True)
            if attempt == 3:
                raise
            time.sleep(5 * attempt)

started = time.monotonic()
with ThreadPoolExecutor(max_workers=2) as pool:
    for number, message in enumerate(pool.map(download, records), 1):
        print(f"{number}/160 {message}", flush=True)

for row in records:
    verify(folder / f"{row['Run']}_{row['mate']}.fastq.gz", row)

elapsed = time.monotonic() - started
print(f"\nCOMPLETE: 160/160 FASTQs verified; elapsed={elapsed / 60:.2f} min")
print("Download only. No trimming or denoising performed.")
