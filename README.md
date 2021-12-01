# Amstrax files
This is a file dump that allows easy access via github for auxiliary files in amstrax


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
