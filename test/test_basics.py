def test_import():
    import amstrax_files


def test_get_file():
    import amstrax_files
    # Let's see what kind of simulation files we have
    print(amstrax_files.list_files())
    # Let's load the example and open it as a dictionary
    config = amstrax_files.get_file('example.json')
    # We can now treat it as a dictionary
    print(config.keys())

    assert 'bla' in config.keys()
