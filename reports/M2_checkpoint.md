# M2 checkpoint — pilot import and initial QC

## Completed
- Built pilot manifest and metadata for 8 samples.
- Imported paired-end reads with PairedEndFastqManifestPhred33V2.
- Created and inspected demux.qzv.
- Reviewed per-sample sequence counts and forward/reverse quality profiles.

## Outputs
- metadata/pilot_manifest.tsv
- metadata/pilot_metadata.tsv
- artifacts/pilot/demux.qza
- artifacts/pilot/demux.qzv

## QC observations
- Samples: 8.
- Total forward reads: 343605.
- Total reverse reads: 343605.
- Forward and reverse counts match within every sample.
- Minimum reads per direction per sample: 17776 (sample 2547670).
- Median reads per direction per sample: 44298.5.
- Maximum reads per direction per sample: 75291 (sample 2771670).
- In the sequence-length summary of the 10000-read subsample,
  all displayed percentiles are 251 nt in both directions.
- Reverse reads show a more pronounced late-read quality decline.
- Equal read counts do not imply equal sequence quality.

## Current scope and limits
- Continue with the existing 8-sample pilot for the next processing stage.
- These counts are before denoising, merging, and chimera removal.
- No sample exclusion or rarefaction depth has been selected.
- Primer handling and trimming/truncation parameters remain undecided.
- No biological comparison by diagnosis has been performed.

## M3 entry
- Verify target region, primers, and expected amplicon length.
- Choose processing parameters using quality and overlap requirements.
- Evaluate read retention after processing before expanding the run.
