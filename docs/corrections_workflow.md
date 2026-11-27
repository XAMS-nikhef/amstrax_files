# Corrections workflow

*Adopted 2026-11-27 from the proposal of 2026-10-28 (PR #34). The proposal text is kept at the end.*

Online processing runs one mutable version, `ONLINE`; frozen versions (`vN`, `PRODn`) are made only for analysis.
"Which version" lives in the run database, not in command lines or environment files.

## The rules

1. **Online = `ONLINE`.** `_global_ONLINE.json` points to the online files (`gain_to_pe_array_online.json`,
   `elife_online.json`, …) and holds the classification cuts. Online files end in an open range (`"007963-999999"`)
   that covers every new run.
2. **New gains (or elife) for new runs** = one PR that closes the open range and opens a new one, **before** runs of the
   new period are processed:
   ```json
   "007963-008199": [...old...],
   "008200-999999": [...new...]
   ```
   The validator allows only this tail change in online files. No run in the new range may have been processed with
   the file yet.
3. **No null gains online.** A run without its own gains takes the last known gains (the open last range). The online
   loop flags it in the run document, `provisional_gains: {value: true, corrections_version, time}`, so it can be
   reprocessed when its own gains are in. The validator rejects new `null` ranges in online / `_dev` gains files
   (null = 1 PE per ADC: wrong classification, jobs over the memory limit).
4. **Classification cuts belong to the version** (`s1_max_area_fraction_top`, `s1_min_channels`, `s2_min_channels`, …).
   The amstrax default of `s1_max_area_fraction_top` is 1.0 (no cut) since 2026-11-27; 0.2 dated from areas in ADC.
5. **Frozen versions** (`vN` files, `_global_PRODn.json`) are made at the end of a science run or when an analysis
   needs them, from the online content or from a corrections development. They never change afterwards.

## Where "the current version" is set (run database, `daq.settings`)

| Document | Read by | Effect |
|---|---|---|
| `{name: "online_corrections_version", value: "ONLINE"}` | online loop (`auto_processing.py --corrections_version db`), every iteration | version of new online jobs; no restart. Without the document: `ONLINE` |
| `{name: "current_corrections_versions", value: ["PROD6", "ONLINE", …]}` | dashboard (`backend/common/profile.py current_versions`), every request | versions whose data count as current; first = submit default. Without the document: `XAMS_DASH_CURRENT_VERSIONS` |

Changing either is one database write (XAMS rule: writes to the run database need an explicit OK).

## Status (2026-11-27)

| Point of the proposal | Status |
|---|---|
| 1. online on a mutable version, frozen versions for analysis | in place since 2026-11-02 (`ONLINE` with `_online` files and the tail rule of the validator) |
| 2. one setting in the run database | amstrax + dashboard read it (this change); active once the documents exist and the loop runs with `--corrections_version db` |
| 3. no null gains online + flag | open last range in the online gains file; validator rule; flag written by the online loop (this change) |
| 4. classification cuts in the version, drop the 0.2 default | cuts in every current global; default 1.0 (this change). Only PROD0-2 used the default |
| 5. lineage on correction content | not done (larger change in amstrax) |

---

## Proposal (2026-10-28, as discussed)

*A. P. Colijn, 2026-10-28. Status then: proposal, for discussion.*

### Why

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

### What we had

- Correction files per quantity, versioned by file name (`gain_to_pe_array_v6.json`); global versions
  (`_global_PROD2.json`) bundle file names.
- strax lineage holds the **file name**, not the content. That is why a file may never change for runs that were
  processed with it: the data would keep their hash with other values inside. The validator enforces this.
- The intended escape hatch: `_global_ONLINE.json` may be changed, and `_dev` files may use open ranges.

### Proposal

1. Online processing always runs `ONLINE`; frozen versions only for analysis.
2. One place for "the current version" (run database), read by the online loop and the dashboard; no restarts.
3. No null gains in online processing: last known gains + a flag on the run.
4. Classification cuts in the global version; the amstrax default 0.2 goes.
5. Later: lineage on the correction content instead of the file name.
