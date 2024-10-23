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

See the end of this document for a detailed explanation of the validation rules.

## Continuous Integration (CI) Validation

To ensure the integrity of the corrections, a CI pipeline automatically validates any pull requests that modify these files. A GitHub Action is configured to trigger on pull requests to the master branch. The validation includes:

- File structure: Ensuring that the correction files follow the correct directory structure and naming conventions.
- Past data protection: Verifying that no past corrections are modified.
- Global corrections: Ensuring that global corrections are only modified in allowed cases (ONLINE or _dev).

If any of these checks fail, the pull request will be blocked from merging until the issues are resolved.

### How does it work? 

The CI pipeline uses a Python script to validate the correction files. The workflow is defined in the .github/workflows/validate_correction.yml file. The python script is located in the test/ directory. The workflow runs the script on every pull request to the master branch. If the script fails, the pull request will be blocked from merging. Usually there is no need to modify the workflow, but it might be necessary to update the script if the validation rules change (for example, if new validation checks are added or if the format of the correction files changes).

## How to Add New Corrections

- Do the modifications in a new branch. 
- Create a new JSON file in the appropriate subdirectory or modify an existing one.
- Ensure that the file follows the correct format and naming conventions.
- Open a pull request to the master branch.
- The CI pipeline will automatically validate the changes.
- If the validation fails, address the issues and push the changes to the branch.
- If the validation passes, the pull request can be merged.

-----------------------------



# Correction Validation Rules

This document explains the validation rules for corrections when making changes or pull requests. The goal is to prevent any modification of values for runs that have already been processed, while allowing flexibility to extend ranges and add future corrections.

## Allowed Operations

1. **Extending a Range into the Future**  
   *Current Correction File:*
   ```json
   {
       "001110-004020": 5600,
       "004021-006000": 6000
   }
   ```
   *Proposed Change (Extending the last range):*
   ```json
   {
       "001110-004020": 5600,
       "004021-006500": 6000
   }
   ```
   **Explanation:**  
   This is allowed because you are only extending the **end of the last range** into the future. You’re not modifying any values for runs that were already covered (e.g., 004021-006000), and you're just extending the coverage.

2. **Adding a New Future Range**  
   *Current Correction File:*
   ```json
   {
       "001110-004020": 5600,
       "004021-006000": 6000
   }
   ```
   *Proposed Change (Adding a new range after the last one):*
   ```json
   {
       "001110-004020": 5600,
       "004021-006000": 6000,
       "006001-007000": 6200
   }
   ```
   **Explanation:**  
   This is allowed because the new range starts **after the last range**, so you’re not modifying any values that have already been processed.

3. **Adding a New Range Before the First One**  
   *Current Correction File:*
   ```json
   {
       "001110-004020": 5600,
       "004021-006000": 6000
   }
   ```
   *Proposed Change (Adding a new range before the first one):*
   ```json
   {
       "000500-001109": 5400,
       "001110-004020": 5600,
       "004021-006000": 6000
   }
   ```
   **Explanation:**  
   This is allowed because the new range starts **before the first existing range**, and it doesn't overlap or modify any runs that were already included.

4. **Extending the Start of a Range Backward**  
   *Current Correction File:*
   ```json
   {
       "001110-004020": 5600,
       "004021-006000": 6000
   }
   ```
   *Proposed Change (Extending the start of a range backward):*
   ```json
   {
       "001000-004020": 5600,
       "004021-006000": 6000
   }
   ```
   **Explanation:**  
   This is allowed because you're extending the start of the range **backward into previously uncovered runs**. However, you’re not modifying any values for runs that were already included.

## Not Allowed Operations

1. **Modifying a Value in an Existing Range**  
   *Current Correction File:*
   ```json
   {
       "001110-004020": 5600,
       "004021-006000": 6000
   }
   ```
   *Proposed Change (Modifying an existing value):*
   ```json
   {
       "001110-004020": 5700,  // Changed value
       "004021-006000": 6000
   }
   ```
   **Explanation:**  
   This is **not allowed** because you’re changing the value for an existing range that already covers processed runs (`001110-004020`).

2. **Overlapping Ranges**  
   *Current Correction File:*
   ```json
   {
       "001110-004020": 5600,
       "004021-006000": 6000
   }
   ```
   *Proposed Change (Overlapping the ranges):*
   ```json
   {
       "001110-004020": 5600,
       "003500-004500": 5800,  // Overlaps with existing range
       "004021-006000": 6000
   }
   ```
   **Explanation:**  
   This is **not allowed** because the new range (`003500-004500`) overlaps with the existing range (`001110-004020`), and you’re introducing a new value (`5800`) for runs that are already covered.


3. **Modifying a Past Range**  
   *Current Correction File:*
   ```json
   {
       "001110-004020": 5600,
       "004021-006000": 6000
   }
   ```
   *Proposed Change (Changing an already covered range):*
   ```json
   {
       "001110-003500": 5600,  // Changed range end
       "003501-004020": 5800,  // Changed value for runs already processed
       "004021-006000": 6000
   }
   ```
   **Explanation:**  
   This is **not allowed** because you're modifying the end of an existing range and changing the value for runs that were already included in a processed range (`003501-004020`).

## Summary of the Rules

- **Allowed**:
  - Extend a range into the future.
  - Add new ranges in the future (after the latest range).
  - Add new ranges before the first existing range.
  - Extend the start of a range backward, if it doesn’t overlap with another range.

- **Not Allowed**:
  - Modifying the value for any run that was already covered.
  - Overlapping ranges (unless they have the same value).
  - Changing the start or end of a range to cover runs that were already included.

By following these rules, you ensure that no corrections are modified for any data that has already been processed, while still allowing flexibility to add or extend ranges in the future.
