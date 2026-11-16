import csv
import hashlib
from pathlib import Path

with open("metadata/main_fastq_report.tsv", newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

assert len(rows) == 160, "Expected 160 file records"
assert len({(r["Run"], r["mate"]) for r in rows}) == 160
failures = []

for i, r in enumerate(rows, 1):
    p = Path("data/raw/main") / f"{r['Run']}_{r['mate']}.fastq.gz"
    if not p.is_file():
        failures.append(f"MISSING: {p.name}")
        continue
    if p.stat().st_size != int(r["bytes"]):
        failures.append(f"SIZE MISMATCH: {p.name}")
        continue
    with p.open("rb") as f:
        digest = hashlib.file_digest(f, "md5").hexdigest()
    if digest != r["md5"].lower():
        failures.append(f"MD5 MISMATCH: {p.name}")
        continue
    print(f"{i}/160 VERIFIED: {p.name}", flush=True)

print("Partial files:", [p.name for p in Path("data/raw/main").glob("*.part")])
if failures:
    raise RuntimeError("\n".join(failures))
print("PASS: 160/160 FASTQs match ENA size and MD5.")
