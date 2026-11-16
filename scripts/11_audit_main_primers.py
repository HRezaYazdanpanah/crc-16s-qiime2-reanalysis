import csv
import gzip
import re
from itertools import islice
from pathlib import Path

codes = dict(zip("ACGTRYSWKMBDHVN",
                 ["A","C","G","T","AG","CT","CG","AT","GT","AC",
                  "CGT","AGT","ACT","ACG","ACGT"]))

def pattern(sequence):
    return re.compile("".join("[" + codes[b] + "]" for b in sequence))

primers = {1: "GTGCCAGCMGCCGCGGTAA", 2: "GGACTACHVGGGTWTCTAAT"}
readthrough = {1: "ATTAGAWACCCBDGTAGTCC", 2: "TTACCGCGGCKGCTGGCAC"}

with open("metadata/main_subset_80.tsv", newline="") as f:
    samples = list(csv.DictReader(f, delimiter="\t"))

rows, headers = [], []
for s in samples:
    for mate in (1, 2):
        path = Path("data/raw/main") / f"{s['Run']}_{mate}.fastq.gz"
        with gzip.open(path, "rt") as f:
            lines = list(islice(f, 4000))
        assert len(lines) % 4 == 0 and lines, path
        seqs = [x.strip().upper() for x in lines[1::4]]
        p, a = pattern(primers[mate]), pattern(readthrough[mate])
        rows.append({
            "sample-id": s["sample-id"], "Run": s["Run"], "mate": mate,
            "reads_checked": len(seqs),
            "primer_at_start": sum(bool(p.match(x)) for x in seqs),
            "primer_anywhere": sum(bool(p.search(x)) for x in seqs),
            "full_readthrough_match": sum(bool(a.search(x)) for x in seqs),
        })
        headers.append(f"{s['Run']}\tmate={mate}\t{lines[0].strip()}")
assert len(rows) == 160

with open("reports/main_primer_audit.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
    w.writeheader()
    w.writerows(rows)
Path("reports/main_fastq_headers.txt").write_text("\n".join(headers) + "\n")

for mate in (1, 2):
    group = [r for r in rows if r["mate"] == mate]
    print("MATE", mate)
    for key in ("reads_checked", "primer_at_start",
                "primer_anywhere", "full_readthrough_match"):
        print(key, sum(r[key] for r in group))
    print("Files with anchored primer:",
          sum(r["primer_at_start"] > 0 for r in group), "/80")
print("First header examples:")
print("\n".join(headers[:4]))
print("COMPLETE: per-file audit and headers saved in reports/")
