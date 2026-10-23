# Amstrax files
This is a file dump that allows easy access via github for auxiliary files in amstrax


## Simulated runs (900000-999999)

Simulated runs (xams-sim) are reconstructed with an MC global version, `corrections/_global/_global_MC1.json`: the cuts
and settings of the data version v5, with the per-run corrections (elife, gain_to_pe_array, drift_time_gate,
drift_time_cathode) read from the run's own run document (`rundoc://`, calibrated if present, else the simulation's
true value; `amstrax.contexts.for_mc_run`). Per-run MC values therefore never go into the correction files here; only
maps shared by MC runs do (the MC ranges of `pos_rec_map_v0.json`). `_global_v5.json` (and `elife_v3`,
`gain_to_pe_array_v4`, `drift_time_gate_v1`, `drift_time_cathode_v1`) were made for the first MC test runs and are, for
data, identical to v4; data stay on v4.

# This repo is structured as a package. To interact:
## Install:
```bash
git https://github.com/XAMS-nikhef/amstrax_files
pip install -e amstrax_files
```

## Open files
These are some examples of how to interact with the package.

### Example 1. Open a simulation file
Let's see how we can interact with the package. Below is an example of how we can open a simulation file.
rm 
```python
import amstrax_files
# Let's see what kind of simulation files we have
print(amstrax_files.list_files())
# Let's load the example and open it as a dictionary
config = amstrax_files.get_file('example.json')
# We can now treat it as a dictionary
print(config.keys())
```
