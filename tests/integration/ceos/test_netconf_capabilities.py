"""Test NETCONF capabilities."""
from nornir_netconf.plugins.tasks import netconf_capabilities

CAP = "http://openconfig.net/yang/policy-forwarding?module=openconfig-policy-forwarding&revision=2021-08-06"
HOST = "ceos"


def test_netconf_capabilities(nornir):
    """Test NETCONF Capabilities."""
    nr = nornir.filter(vendor="arista")
    result = nr.run(netconf_capabilities)

    assert not result.failed
    assert CAP in result[HOST][0].result