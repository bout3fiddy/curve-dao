import boa
import pytest
import math

import curve_dao


@pytest.fixture
def target():
    return curve_dao.addresses.DAO.PARAM


@pytest.fixture
def pool(etherscan_api_key):
    return boa.from_etherscan(
        "0x7fb53345f1b21ab5d9510adb38f7d3590be6364b",  # TwoCrypto pool address
        name="TwoCrypto",
        api_key=etherscan_api_key,
    )


@pytest.fixture
def ramp_time_weeks():
    return 1


@pytest.fixture
def new_A():
    return 20000001


@pytest.fixture
def new_gamma():
    return 10000000000000001


@pytest.fixture
def new_mid_fee():
    return 3000001


@pytest.fixture
def new_out_fee():
    return 45000001


@pytest.fixture
def new_admin_fee():
    return 5000000001


@pytest.fixture
def new_fee_gamma():
    return 300000000000000001


@pytest.fixture
def new_allowed_extra_profit():
    return 10000000001


@pytest.fixture
def new_adjustment_step():
    return 5500000000001


@pytest.fixture
def new_ma_half_time():
    return 610


@pytest.fixture
def proposal_time_weeks():
    return 1


@pytest.fixture
def actions_and_description(
    pool,
    ramp_time_weeks,
    new_A,
    new_gamma,
    new_mid_fee,
    new_out_fee,
    new_admin_fee,
    new_fee_gamma,
    new_allowed_extra_profit,
    new_adjustment_step,
    new_ma_half_time,
    proposal_time_weeks,
):
    actions, description = curve_dao.proposals.update_twocrypto(
        pool,
        ramp_time_weeks,
        new_A,
        new_gamma,
        new_mid_fee,
        new_out_fee,
        new_admin_fee,
        new_fee_gamma,
        new_allowed_extra_profit,
        new_adjustment_step,
        new_ma_half_time,
        proposal_time_weeks,
    )
    assert actions == [
        (
            "0x5a8fdC979ba9b6179916404414F7BA4D8B77C8A1",  # owner proxy address
            "ramp_A_gamma",
            pool,   # Use the pool object directly
            20000001,
            10000000000000001,
            1726688231
        ),
        (
            "0x5a8fdC979ba9b6179916404414F7BA4D8B77C8A1",  # owner proxy address
            "commit_new_parameters",
            pool,   # Use the pool object directly
            3000001,                # new mid_fee
            45000001,               # new out_fee
            5000000001,             # new admin_fee
            300000000000000001,     # new fee_gamma
            10000000001,
            5500000000001,
            610,  # new ma_half_time (without conversion)
        ),
    ]
    return actions, description


def test_simulate_success(
    pool, vote_creator, target, etherscan_api_key, pinata_token, actions_and_description
):
    actions, description = actions_and_description

    with boa.env.prank(vote_creator):
        vote_id = curve_dao.create_vote(
            target, actions, description, etherscan_api_key, pinata_token
        )

    assert curve_dao.simulate(vote_id, target, etherscan_api_key)

    boa.env.time_travel(
        seconds=60 * 60 * 24 * 8
    )  # sleep 7(+1) days for ramp to complete

    A_gamma = pool.future_A_gamma()
    A = A_gamma >> 128
    gamma = A_gamma & ((1 << 128) - 1)

    assert A == 20000001
    assert gamma == 10000000000000001
    assert pool.future_mid_fee() == 3000001
    assert pool.future_out_fee() == 45000001
    assert pool.future_admin_fee() == 5000000001
    assert pool.future_fee_gamma() == 300000000000000001
    assert pool.future_allowed_extra_profit() == 10000000001
    assert pool.future_adjustment_step() == 5500000000001
    assert pool.future_ma_half_time() == 610
