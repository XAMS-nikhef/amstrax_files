# Proposal: a simpler corrections workflow for XAMS

*A. P. Colijn, 2026-10-28. Status: proposal, for discussion.*

## Why

Getting the gains into the online processing for the runs of one morning (SR-2026.3, runs 7790+) took:

1. a new gains file `gain_to_pe_array_v6.json`, because the validator does not allow changing `v5`, not even
   null → value for runs that had never been processed with it;
2. a new global version `PROD2` = {gains v6, position map v2};
3. a restart of the online loop (`--corrections_version` on its command line, screen on stbc-i2);
4. a restart of the dashboard (`XAMS_DASH_CURRENT_VERSIONS` in its environment, screen on stbc-i1);
5. reprocessing of the runs that had already gone through the loop, by hand from the dashboard.

On top of that:

- a range with `null` gains means "1 PE per ADC". With the field on, the online jobs then went over 16 GB, and over
  32 GB after a release with more memory, and were held;
- the S1 classification default `s1_max_area_fraction_top = 0.2` dates from before the gains (areas in ADC). With
  gains, S1s from the upper two thirds of the TPC have a top fraction of 0.2–0.35. They are silently not S1s, so
  `event_info` only holds events near the cathode (run 7801: drift times 30–40 µs only).

None of this is physics. It is bookkeeping, and it sits exactly where we need speed: at the start of a fill.

## What we have

- Correction files per quantity, versioned by file name (`gain_to_pe_array_v6.json`); global versions
  (`_global_PROD2.json`) bundle file names.
- strax lineage holds the **file name**, not the content. That is why a file may never change for runs that were
  processed with it: the data would keep their hash with other values inside. The validator enforces this, strictly
  (any change for an existing run, also null → value).
- The repo already has the intended escape hatch: `_global_ONLINE.json` may be changed, and `_dev` files may use open
  ranges (`"007790-*"`). They are not used: `_global_ONLINE.json` points to old `_dev` files with old settings.

## Proposal

1. **Online processing always runs `ONLINE`; frozen versions only for analysis.**
   - `_global_ONLINE.json` points to `_dev` files that are kept current (gains, position map, …).
   - New gains = a new open range in the `_dev` file, closing the previous one (`"007759-007789"`, `"007790-*"`),
     **before** runs of the new period are processed. The validator rule stays: no change for runs already processed.
   - At the end of a science run (or when an analysis needs it) the `_dev` content is frozen as `vN` / `PRODn`.
     That is the only moment a new version is made.

2. **One place for "the current version".** The online loop and the dashboard read the online/default version from
   one setting (e.g. `daq.settings` in the run DB, next to `active_science_run`), not from a command-line argument in
   one screen and an environment variable in another. Changing it = one DB write, no restarts.

3. **No null gains in online processing.** A run without its own gains gets the last known gains, and the run doc gets
   a flag (`processing_status.provisional_gains`). Never 1 PE per ADC: it breaks the classification and the memory.
   Runs processed this way are reprocessed when the real gains arrive (the flag says which ones).

4. **Classification cuts in the global version.** `s1_max_area_fraction_top`, `s1_min_channels`, `s2_min_channels`
   belong to the version, as they already do in the old `_global_ONLINE.json` / `_global_v0.json`. The amstrax default
   0.2 should go (or become 1.0): it only made sense for areas in ADC.

5. **Later: lineage on content.** If the lineage held a hash of the correction *values* used for the run (not the file
   name), a changed file would automatically give new data hashes. Then mutable files are safe by construction and
   most of the version bookkeeping and the strict validator become unnecessary. Larger change in amstrax; not needed
   for 1–4.

## What it would have meant today

The gains for 7790+ = one PR adding `"007790-*"` to `gain_to_pe_array_dev.json` (validator: future runs only). The loop
and the dashboard already run `ONLINE`; nothing to restart. Until that PR, the runs get the P1 gains with the
provisional flag instead of 1 PE/ADC, so no held jobs. The S1 cut is part of `ONLINE` and was set for PE.

## Steps

1. `_global_ONLINE.json` + `_dev` files up to date (= PROD2 content + current classification cuts); test on a few runs.
2. Loop and dashboard read the version from the run DB setting (small change in `auto_processing.py` and the
   dashboard profile).
3. Fallback to the last gains + flag in amstrax (`xams_config.find_correction_value` or the gains plugin).
4. Remove / raise the `s1_max_area_fraction_top` default in `peak_basics`.
5. README of `corrections/`: the workflow above.
