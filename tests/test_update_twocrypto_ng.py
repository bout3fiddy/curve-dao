import boa
import pytest
import math

import curve_dao


@pytest.fixture
def target():
    return curve_dao.addresses.DAO.OWNERSHIP


@pytest.fixture
def pool(etherscan_api_key):
    return boa.from_etherscan(
        "0x8c65CeC3847ad99BdC02621bDBC89F2acE56934B",
        name="TwoCryptoNG",
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
    return 20000000000000001


@pytest.fixture
def new_mid_fee():
    return 700001


@pytest.fixture
def new_out_fee():
    return 8000001


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
def new_ma_time():
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
    new_fee_gamma,
    new_allowed_extra_profit,
    new_adjustment_step,
    new_ma_time,
    proposal_time_weeks,
):
    actions, description = curve_dao.proposals.update_twocrypto_ng(
        pool,
        ramp_time_weeks,
        new_A,
        new_gamma,
        new_mid_fee,
        new_out_fee,
        new_fee_gamma,
        new_allowed_extra_profit,
        new_adjustment_step,
        new_ma_time,
        proposal_time_weeks,
    )
    assert actions == [
        (
            "0x8c65CeC3847ad99BdC02621bDBC89F2acE56934B",
            "ramp_A_gamma",
            20000001,
            20000000000000001,
            1726688231),
        (
            "0x8c65CeC3847ad99BdC02621bDBC89F2acE56934B",
            "apply_new_parameters",
            700001,                 # new mid_fee
            8000001,                # new out_fee
            300000000000000001,     # new fee_gamma
            10000000001,
            5500000000001,
            int(610 / math.log(2)),  # Update this line
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

    assert pool.A() == 20000001
    assert pool.gamma() == 20000000000000001
    assert pool.mid_fee() == 700001
    assert pool.out_fee() == 8000001
    assert pool.fee_gamma() == 300000000000000001
    assert pool.allowed_extra_profit() == 10000000001
    assert pool.adjustment_step() == 5500000000001
