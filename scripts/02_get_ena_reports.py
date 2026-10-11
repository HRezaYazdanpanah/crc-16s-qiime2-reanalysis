import csv
import io
from urllib.parse import urlencode
from urllib.request import urlopen

with open("metadata/pilot_samples.tsv", newline="") as f:
    pilot = list(csv.DictReader(f, delimiter="\t"))

fields = "run_accession,library_layout,fastq_ftp,fastq_bytes,fastq_md5"
files = []

for sample in pilot:
    run = sample["Run"]
    query = urlencode({
        "accession": run,
        "result": "read_run",
        "fields": fields,
        "format": "tsv",
    })
    url = "https://www.ebi.ac.uk/ena/portal/api/filereport?" + query

    with urlopen(url, timeout=60) as response:
        text = response.read().decode("utf-8")

    report = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    assert len(report) == 1, f"{run}: expected one report row"
    row = report[0]
    assert row["run_accession"] == run, f"{run}: accession mismatch"
    assert row["library_layout"] == "PAIRED", f"{run}: unexpected layout"

    paths = row["fastq_ftp"].split(";")
    sizes = row["fastq_bytes"].split(";")
    checksums = row["fastq_md5"].split(";")
    assert len(paths) == len(sizes) == len(checksums) == 2, (
        f"{run}: expected exactly two FASTQ files; inspect manually"
    )

    for mate in (1, 2):
        matches = [
            i for i, path in enumerate(paths)
            if path.endswith(f"/{run}_{mate}.fastq.gz")
        ]
        assert len(matches) == 1, f"{run}: cannot identify mate {mate}"
        i = matches[0]
        files.append({
            "sample": sample["sample"],
            "Run": run,
            "mate": mate,
            "ftp_url": "ftp://" + paths[i],
            "bytes": int(sizes[i]),
            "md5": checksums[i],
        })

    print(f"{run}: two FASTQ files verified in ENA report")

output = "metadata/pilot_fastq_report.tsv"
with open(output, "x", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=list(files[0]), delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(files)

total = sum(row["bytes"] for row in files)
print(f"Saved {len(files)} file records to {output}")
print(f"Total compressed FASTQ size: {total / 1_000_000:.2f} MB")
