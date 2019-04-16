def test_python2_is_installed(host):
    python_file = host.file("/usr/bin/python2")
    assert python_file.exists
