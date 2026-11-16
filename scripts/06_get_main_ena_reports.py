import csv
import io
import re
import shutil
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

with open("metadata/main_subset_80.tsv", newline="") as f:
    samples = list(csv.DictReader(f, delimiter="\t"))

assert len(samples) == 80
assert len({r["Run"] for r in samples}) == 80

cache = Path("metadata/ena_main_reports")
output = Path("metadata/main_fastq_report.tsv")
fields = "run_accession,library_layout,fastq_ftp,fastq_bytes,fastq_md5"
records = []

for number, sample in enumerate(samples, 1):
    run = sample["Run"]
    saved = cache / f"{run}.tsv"

    if saved.exists():
        text = saved.read_text()
    else:
        query = urlencode({
            "accession": run,
            "result": "read_run",
            "fields": fields,
            "format": "tsv",
        })
        url = "https://www.ebi.ac.uk/ena/portal/api/filereport?" + query

        for attempt in range(1, 4):
            try:
                with urlopen(url, timeout=60) as response:
                    text = response.read().decode("utf-8")
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(5 * attempt)

    report = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    assert len(report) == 1, f"{run}: expected exactly one report row"
    row = report[0]
    assert row["run_accession"] == run, f"{run}: accession mismatch"
    assert row["library_layout"] == "PAIRED", f"{run}: unexpected layout"

    paths = row["fastq_ftp"].split(";")
    sizes = row["fastq_bytes"].split(";")
    hashes = row["fastq_md5"].split(";")
    assert len(paths) == len(sizes) == len(hashes) == 2, (
        f"{run}: expected exactly two FASTQs; manual review required"
    )

    for mate in (1, 2):
        matches = [
            i for i, path in enumerate(paths)
            if path.endswith(f"/{run}_{mate}.fastq.gz")
        ]
        assert len(matches) == 1, f"{run}: cannot identify mate {mate}"
        i = matches[0]
        assert int(sizes[i]) > 0, f"{run}: invalid file size"
        assert re.fullmatch(r"[0-9a-fA-F]{32}", hashes[i]), (
            f"{run}: invalid MD5"
        )
        records.append({
            "sample-id": sample["sample-id"],
            "Run": run,
            "mate": mate,
            "ftp_url": "ftp://" + paths[i],
            "bytes": int(sizes[i]),
            "md5": hashes[i].lower(),
        })

    if not saved.exists():
        temporary = saved.with_suffix(".tsv.part")
        temporary.write_text(text)
        temporary.replace(saved)

    print(f"{number}/80 {run}: paired files verified", flush=True)
    time.sleep(0.2)

assert len(records) == 160
assert len({r["ftp_url"] for r in records}) == 160

if output.exists():
    with output.open(newline="") as f:
        previous = list(csv.DictReader(f, delimiter="\t"))
    normalized = [{k: str(v) for k, v in r.items()} for r in records]
    assert previous == normalized, "Existing report differs; do not overwrite"
else:
    temporary = output.with_suffix(".tsv.part")
    with temporary.open("w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=list(records[0]),
            delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(records)
    temporary.replace(output)

total = sum(r["bytes"] for r in records)
free = shutil.disk_usage(".").free
print(f"\nCOMPLETE: {len(samples)} runs; {len(records)} FASTQ files")
print(f"Compressed FASTQ total: {total / 2**30:.3f} GiB")
print(f"Current free project disk: {free / 2**30:.2f} GiB")
print(f"Report: {output}")
print("No FASTQ files downloaded.")
