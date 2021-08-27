"""Conftest for nornir_netconf UnitTests."""
import os
from nornir import InitNornir
import pytest
from nornir.core.state import GlobalState

global_data = GlobalState(dry_run=True)
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

# If NORNIR_LOG set to True, the log won't be deleted in teardown.
nornir_logfile = os.environ.get("NORNIR_LOG", False)


@pytest.fixture(scope="session", autouse=True)
def nornir():
    """Initializes nornir"""
    nr_nr = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": f"{DIR_PATH}/inventory_data/hosts.yaml",
                "group_file": f"{DIR_PATH}/inventory_data/groups.yaml",
                "defaults_file": f"{DIR_PATH}/inventory_data/defaults.yaml",
            },
        },
        logging={"log_file": f"{DIR_PATH}/unit/test_data/nornir_test.log", "level": "DEBUG"},
        dry_run=True,
    )
    nr_nr.data = global_data
    return nr_nr


@pytest.fixture(scope="session", autouse=True)
def teardown_class():
    """Teardown the automatically created log file by Nornir."""
    if not nornir_logfile:
        nornir_log = f"{DIR_PATH}/unit/test_data/nornir_test.log"
        if os.path.exists(nornir_log):
            os.remove(nornir_log)


@pytest.fixture(scope="function", autouse=True)
def reset_data():
    """Reset Data."""
    global_data.dry_run = True
    global_data.reset_failed_hosts()
