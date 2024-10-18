import json
import os
import subprocess

def get_diff_files(directory):
    """Get a list of modified files in the pull request from the given directory."""
    # Fetch the diff between the current branch and master
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD^", "--", directory], capture_output=True, text=True
    )
    changed_files = result.stdout.strip().split("\n")
    return [f for f in changed_files if f]

def get_all_files(directory):
    """Get a list of all files in the given directory."""
    return [f for f in os.listdir(directory) if os.path.isfile(os.path)]

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

    # Get the current time to define what is considered a "past" correction
    current_time = "999999"  # Treat anything before the latest run ID as "past"

    for run_range, proposed_value in proposed_corrections.items():
        start_run, end_run = run_range.split("-")
        start_run = start_run.zfill(6)
        end_run = end_run.zfill(6)

        # Treat '*' as "infinite future"
        if end_run == "*":
            end_run = "999999"

        # Check if the run range exists in the current corrections
        if run_range in current_corrections:
            current_value = current_corrections[run_range]

            # Ensure no modification of past ranges
            if int(end_run) < int(current_time) and proposed_value != current_value:
                print(f"Error: Past range {run_range} is being modified.")
                return False
        else:
            # Ensure new ranges are added only in the future
            if int(start_run) < int(current_time):
                print(f"Error: New range {run_range} starts in the past.")
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
            if "_dev" in proposed_value:
                print(f"Error: Found '_dev' in global correction {file_path}.")
                return False

    print(f"Validation passed for {file_path}.")
    return True

def main():
    """Main function to validate all modified correction files."""
    corrections_dir = "corrections/"
    modified_files = get_diff_files(corrections_dir)

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
