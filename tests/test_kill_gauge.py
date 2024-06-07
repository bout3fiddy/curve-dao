import time

import boa
import pytest

import curve_dao


@pytest.fixture
def gauge_to_kill(etherscan_api_key):
    time.sleep(1)  # Etherscan API limit
    return boa.from_etherscan(
        "0x04e80db3f84873e4132b221831af1045d27f140f",
        name="LiquidityGaugeV6",
        api_key=etherscan_api_key,
    )


@pytest.fixture
def local_contract():
    return boa.loads(
        """
@external
def do_nothing():
    pass
    """
    )


@pytest.fixture
def actions(gauge_to_kill, local_contract):
    return [(gauge_to_kill.address, "set_killed", True), (local_contract, "do_nothing")]


@pytest.fixture
def description():
    return "test"


@pytest.fixture
def target():
    return curve_dao.addresses.DAO.OWNERSHIP


@pytest.fixture
def evm_script(target, actions, etherscan_api_key):
    return curve_dao.prepare_evm_script(target, actions, etherscan_api_key)


def test_evm_script(evm_script, local_contract):
    assert (
        evm_script.hex()
        == "0x0000000140907540d8a6c65c637785e8f8b742ae6b0b9968000000c4b61d27f600000000000000000000000004e80db3f84873e4132b221831af1045d27f140f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000060000000000000000000000000000000000000000000000000000000000000002490b22997000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000"
    )


@pytest.mark.ignore_isolation
@pytest.fixture
def test_create_vote(
    target, actions, description, etherscan_api_key, pinata_token, vote_creator
):
    time.sleep(1)  # Etherscan API limit
    with boa.env.prank(vote_creator):
        vote_id = curve_dao.create_vote(
            target, actions, description, etherscan_api_key, pinata_token
        )
    return vote_id


@pytest.mark.ignore_isolation
@pytest.fixture
def test_simulate(test_create_vote, target, etherscan_api_key):
    vote_id = test_create_vote
    assert curve_dao.simulate(vote_id, target, etherscan_api_key)


def test_gauge_killed(test_create_vote, test_simulate, gauge_to_kill):
    assert gauge_to_kill.is_killed() is True
