import os

import boa
from rich import print
import math
from curve_dao import create_vote, get_address, simulate
from curve_dao.proposals import update_twocrypto

# Load environment variables and fork the Ethereum mainnet
boa.fork(os.getenv("RPC_ETHEREUM"))

# Set up constants
VOTE_CREATOR_SIM = "0xE6DA683076b7eD6ce7eC972f21Eb8F91e9137a17"
POOL_ADDRESS = "0x7fb53345f1b21ab5d9510adb38f7d3590be6364b"
RAMP_TIME_WEEKS = 1

# new parameters
NEW_A = 20000001
NEW_GAMMA = 10000000000000001
NEW_MID_FEE = 3000001
NEW_OUT_FEE = 45000001
NEW_ADMIN_FEE = 5000000001
NEW_FEE_GAMMA = 300000000000000001
NEW_ALLOWED_EXTRA_PROFIT = 10000000001
NEW_ADJUSTMENT_STEP = 5500000000001
NEW_MA_HALF_TIME = 610

# proposal time
PROPOSAL_TIME_WEEKS = 1

# Load the TwocrptoNG contract
pool = boa.from_etherscan(
    POOL_ADDRESS, name="TwocrptoNG", api_key=os.getenv("ETHERSCAN_API_KEY")
)

# Generate proposal actions and description
actions, description = update_twocrypto(
    pool,
    RAMP_TIME_WEEKS,
    NEW_A,
    NEW_GAMMA,
    NEW_MID_FEE,
    NEW_OUT_FEE,
    NEW_ADMIN_FEE,
    NEW_FEE_GAMMA,
    NEW_ALLOWED_EXTRA_PROFIT,
    NEW_ADJUSTMENT_STEP,
    NEW_MA_HALF_TIME,
    PROPOSAL_TIME_WEEKS,
)

# Create and submit the proposal
with boa.env.prank(VOTE_CREATOR_SIM):
    vote_id = create_vote(
        get_address("param"),
        actions,
        description,
        os.getenv("ETHERSCAN_API_KEY"),
        os.getenv("PINATA_TOKEN"),
    )
print(f"Vote ID: {vote_id}")

# Simulate the proposal execution
simulate(vote_id, get_address("param"), os.getenv("ETHERSCAN_API_KEY"))

# Time travel to after the ramp period
boa.env.time_travel(seconds=60 * 60 * 24 * 8)  # 8 days (7 days ramp + 1 day buffer)

# Verify the new parameters

A_gamma = pool.future_A_gamma()
A = A_gamma >> 128
gamma = A_gamma & ((1 << 128) - 1)    

assert A == NEW_A
assert gamma == NEW_GAMMA
assert pool.future_mid_fee() == NEW_MID_FEE
assert pool.future_out_fee() == NEW_OUT_FEE
assert pool.future_admin_fee() == NEW_ADMIN_FEE
assert pool.future_fee_gamma() == NEW_FEE_GAMMA
assert pool.future_allowed_extra_profit() == NEW_ALLOWED_EXTRA_PROFIT
assert pool.future_adjustment_step() == NEW_ADJUSTMENT_STEP
assert pool.future_ma_half_time() == NEW_MA_HALF_TIME

print("All parameters updated successfully!")
