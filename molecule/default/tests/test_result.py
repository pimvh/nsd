import testinfra


def test_os_release(host):
    """test host release for good measure"""

    assert host.file("/etc/os-release").contains("Ubuntu")


def test_nsd_running(host):
    """test that the NSD service is running"""

    assert host.service("nsd").is_running


def test_nsd_zone_file_created(host):
    """test that the NSD zone file is created"""

    assert host.file("/etc/nsd/zones/example.com")


def test_nsd_dnssec_env_created(host):
    """test that the NSD dnssec env is created"""

    assert host.file("/etc/nsd/example.com_dnssecpls.env")


def test_nsd_returns_result(host):
    """test that the NSD dnssecpls configuration script is added"""

    lookup = host.run("dig @127.0.0.1 foobar.example.com")
    assert lookup.rc == 0
