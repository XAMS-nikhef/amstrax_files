# Corrections Directory

This directory contains JSON files that provide correction data for the XAMS project. These files are version-controlled and used in various contexts to apply calibration and correction settings to the detector data.

## Structure

Each correction has its own subdirectory, and each subdirectory contains JSON files corresponding to different versions of the corrections.
Each file name within a subdirectory should start with the name of the subdirectory for organizational clarity. For example, correction files related to "elife" should be located in the elife/ subdirectory and named accordingly, like elife_v0.json.
Example Structure:
```
corrections/
    elife/
        elife_v0.json
    gain_to_pe/
        gain_to_pe_v1.json
    _global/
        _global_ONLINE.json
```
## File Format

Each correction file follows a specific format:

Run ranges: The keys are run ID ranges defined by a start and end run (e.g., "001110-004020"). The values are the correction data to be applied for those runs.
Wildcard run ranges: The end run can be set to "*" to indicate that the correction applies to all future runs. This is allowed only for the _dev version of the corrections and is supposed to be used mainly for online corrections.

Example:

```
{
    "001110-004020": 5600,
    "004021-*": 6000
}
```

## Global Correction Files

Global correction files define a set of corrections that can easily be specified when initialising the context. We use online for live processing, and versioned corrections for the official offline processing.


## Modifying Corrections
Past data modification is not allowed: You cannot modify corrections that apply to past runs.

- New corrections must only apply to future runs: any correction additions must have a start run ID that is greater than or equal to the latest processed run. If you want to modify past corrections, you must create a new version of the correction file.

- Global corrections: Any modifications to global corrections must be restricted. You cannot modify corrections in global files unless the file is related to the ONLINE version or marked as a development version (e.g., _dev). This is to ensure that the global corrections are consistent across all contexts.

## Continuous Integration (CI) Validation

To ensure the integrity of the corrections, a CI pipeline automatically validates any pull requests that modify these files. A GitHub Action is configured to trigger on pull requests to the master branch. The validation includes:

- File structure: Ensuring that the correction files follow the correct directory structure and naming conventions.
- Past data protection: Verifying that no past corrections are modified.
- Global corrections: Ensuring that global corrections are only modified in allowed cases (ONLINE or _dev).


If any of these checks fail, the pull request will be blocked from merging until the issues are resolved.

## How to Add New Corrections

- Do the modifications in a new branch. 
- Create a new JSON file in the appropriate subdirectory or modify an existing one.
- Ensure that the file follows the correct format and naming conventions.
- Open a pull request to the master branch.
- The CI pipeline will automatically validate the changes.
- If the validation fails, address the issues and push the changes to the branch.
- If the validation passes, the pull request can be merged.

