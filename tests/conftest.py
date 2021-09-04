"""Conftest for nornir_netconf UnitTests."""
import os
import shutil

import docker
import pytest
from nornir import InitNornir
from nornir.core.state import GlobalState

# pytest mark decorator to skip integration tests if INTEGRATION_TESTS=True
# These tests will connect to local lab environment to validate actual responses
# from locallly hosted network devices.
skip_integration_tests = pytest.mark.skipif(
    os.environ.get("SKIP_INTEGRATION_TESTS", True), reason="Do not run integration tests"
)

global_data = GlobalState(dry_run=True)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# If NORNIR_LOG set to True, the log won't be deleted in teardown.
nornir_logfile = os.environ.get("NORNIR_LOG", False)


@pytest.fixture(scope="session", autouse=True)
def get_test_env() -> str:
    """Determine if env is local or if tests are executing within a container."""
    try:
        # Container of interest
        container = "netconf1"
        client = docker.from_env()
        # Create a list to work with.
        container_names = [container.name for container in client.containers.list()]
        if container in container_names:
            return "local"
    except docker.errors.DockerException:
        return "container"


@pytest.fixture(scope="session", autouse=True)
def nornir(get_test_env):
    """Initializes nornir"""
    nr_nr = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": f"{DIR_PATH}/inventory_data/hosts-{get_test_env}.yml",
                "group_file": f"{DIR_PATH}/inventory_data/groups.yml",
                "defaults_file": f"{DIR_PATH}/inventory_data/defaults.yml",
            },
        },
        logging={"log_file": f"{DIR_PATH}/test_data/nornir_test.log", "level": "DEBUG"},
        dry_run=True,
    )
    nr_nr.data = global_data
    return nr_nr


@pytest.fixture(scope="session", autouse=True)
def nornir_unittest(get_test_env):
    """Initializes nornir"""
    nr_nr = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": f"{DIR_PATH}/inventory_data/hosts-{get_test_env}.yml",
                "group_file": f"{DIR_PATH}/inventory_data/groups.yml",
                "defaults_file": f"{DIR_PATH}/inventory_data/defaults.yml",
            },
        },
        logging={"log_file": f"{DIR_PATH}/test_data/nornir_test.log", "level": "DEBUG"},
        dry_run=True,
    )
    nr_nr.data = global_data
    return nr_nr


@pytest.fixture(scope="session", autouse=True)
def schema_path():
    """Schema path, test data."""
    return "tests/test_data/schema_path"


@pytest.fixture(scope="session", autouse=True)
def test_folder():
    """Test folder."""
    return "tests/test_data/test_folder"


@pytest.fixture(scope="session", autouse=True)
def teardown_class(schema_path, test_folder):
    """Teardown the random artifacts created by pytesting."""
    if not nornir_logfile:
        nornir_log = f"{DIR_PATH}/test_data/nornir_test.log"
        if os.path.exists(nornir_log):
            os.remove(nornir_log)

    # Remove test data folders
    folders = [test_folder, schema_path]
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)


@pytest.fixture(scope="function", autouse=True)
def reset_data():
    """Reset Data."""
    global_data.dry_run = True
    global_data.reset_failed_hosts()


class FakeRpcObject:
    """Test Class."""

    def __init__(self):
        self.ok = False
        self.data_xml = False
        self.error = ""
        self.errors = ""

    def set_ok(self, set: bool):
        """Set ok."""
        if set:
            self.ok = True

    def set_data_xml(self, set: bool):
        """Set data_xml."""
        if set:
            self.data_xml = True


# PAYLOADS


@pytest.fixture(scope="function", autouse=True)
def sros_config_payload():
    return """
<config>
    <configure xmlns="urn:nokia.com:sros:ns:yang:sr:conf">
        <router>
            <router-name>Base</router-name>
            <interface>
                <interface-name>L3-OAM-eNodeB069420-W1</interface-name>
                <admin-state>disable</admin-state>
                <ingress-stats>false</ingress-stats>
            </interface>
        </router>
    </configure>
</config>
        """