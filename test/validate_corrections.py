import json
import os
import subprocess


def get_diff_files(directory):
    """Get a list of modified files in the pull request from the given directory."""
    # Compare the current branch with the target branch (usually 'origin/master')
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/master", "HEAD", "--", directory], capture_output=True, text=True
    )
    changed_files = result.stdout.strip().split("\n")
    changed_files = [f for f in changed_files if f.endswith(".json")]

    # because we put correction files in the corrections directory ( gain_to_pe/gain_to_pe_v1.json )
    # we need to append the directory path to the file name
    # changed_files = [os.path.join('_'.join(f.split('_')[:-1]), f) for f in changed_files]

    return [f for f in changed_files if f]


def validate_correction_file(file_path):
    """Validate that no past data is modified in the correction file."""
    
    # Load the current (pre-PR) version of the file from master branch
    current_version = subprocess.run(
        ["git", "show", f"origin/master:{file_path}"], capture_output=True, text=True
    ).stdout
    
    if current_version:
        current_corrections = json.loads(current_version)
    else:
        current_corrections = {}
    
    # Load the proposed version from the PR
    with open(file_path, "r") as f:
        proposed_corrections = json.load(f)
    
    print(f"-- Current correction ranges:")
    print(current_corrections)
    print(f"-- Proposed correction ranges:")
    print(proposed_corrections)

    # Flatten the ranges into individual runs
    def flatten_ranges(corrections):
        flat = {}
        for range_key, value in corrections.items():
            start, end = map(int, range_key.split('-'))
            for run_id in range(start, end + 1):
                flat[run_id] = value
        return flat
    
    flat_current = flatten_ranges(current_corrections)
    flat_proposed = flatten_ranges(proposed_corrections)
    
    # Check if any run that was covered in the past has a different value now
    for run_id, current_value in flat_current.items():
        proposed_value = flat_proposed.get(run_id)
        if proposed_value is not None and proposed_value != current_value:
            print(f"Error: Proposed value for run {run_id} modifies past data.")
            return False
    
    print(f"Validation passed for {file_path}.")
    return True


def validate_global_corrections(file_path):
    # Just check that if the is not "ONLINE" in the filename,
    # There is no value inside that has a "_dev" in it.

    with open(file_path, "r") as f:
        proposed_corrections = json.load(f)

    if "ONLINE" not in file_path:
        for run_range, proposed_value in proposed_corrections.items():
            # if prposed value is a string
            if isinstance(proposed_value, str):
                if "_dev" in proposed_value:
                    print(f"Error: Found '_dev' in global correction {file_path}.")
                    return False


    # Do not allow to change anything in a global correction file that is not ONLINE or ends with _dev
    # Load the current (pre-PR) version of the file from master branch

    if "ONLINE" not in file_path and "_dev" not in file_path:

        current_version = subprocess.run(
            ["git", "show", f"origin/master:{file_path}"], capture_output=True, text=True
        ).stdout

        if current_version:
            print(f"Found current version of {file_path}, current_version = {current_version}")
            current_corrections = json.loads(current_version)

            for run_range, proposed_value in proposed_corrections.items():
                if run_range in current_corrections:
                    current_value = current_corrections[run_range]
                    if proposed_value != current_value:
                        print(f"Error: Global correction {file_path} is being modified.")
                        return False




    print(f"Validation passed for {file_path}.")
    return True


def check_name_matches_dirname(directory):

    all_match = True

    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                # check if the filename starts with the directory name
                if not file.startswith(os.path.basename(root)):
                    print(f"Error: File {file} does not start with {os.path.basename(root)}")
                    all_match = False

    return all_match


def main():
    """Main function to validate all modified correction files."""
    corrections_dir = "corrections/"
    modified_files = get_diff_files(corrections_dir)
    print(f"Modified files: {modified_files}")

    assert check_name_matches_dirname(corrections_dir), """
    Error: Not all files start with the directory name.
    Please make sure that the correction files are in the correct directory.
    For example, elife_v0.json should be in corrections/elife/.
    """

    if not modified_files:
        print("No correction files modified.")
        return

    for file_name in modified_files:
        print(f"Validating {file_name}...")

        if "_global" in file_name:
            validate = validate_global_corrections(file_name)
        else:
            validate = validate_correction_file(file_name)

        if not validate:
            print(f"Validation failed for {file_name}.")
            exit(1)


    print("All correction files validated successfully.")
    exit(0)


if __name__ == "__main__":
    main()
