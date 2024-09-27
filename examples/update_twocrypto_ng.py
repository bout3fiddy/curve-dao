import os

import boa
from rich import print
import math
from curve_dao import create_vote, get_address, simulate
from curve_dao.proposals import update_twocrypto_ng

# Load environment variables and fork the Ethereum mainnet
boa.fork(os.getenv("RPC_ETHEREUM"))

# Set up constants
VOTE_CREATOR_SIM = "0xE6DA683076b7eD6ce7eC972f21Eb8F91e9137a17"
POOL_ADDRESS = "0x8c65cec3847ad99bdc02621bdbc89f2ace56934b"
RAMP_TIME_WEEKS = 1

# new parameters
NEW_A = 20000001
NEW_GAMMA = 20000000000000001
NEW_MID_FEE = 700001
NEW_OUT_FEE = 8000001
NEW_FEE_GAMMA = 300000000000000001
NEW_ALLOWED_EXTRA_PROFIT = 10000000001
NEW_ADJUSTMENT_STEP = 5500000000001
NEW_MA_TIME = 610

# proposal time
PROPOSAL_TIME_WEEKS = 1

# Load the TwocrptoNG contract
pool = boa.from_etherscan(
    POOL_ADDRESS, name="TwocrptoNG", api_key=os.getenv("ETHERSCAN_API_KEY")
)

# Generate proposal actions and description
actions, description = update_twocrypto_ng(
    pool,
    RAMP_TIME_WEEKS,
    NEW_A,
    NEW_GAMMA,
    NEW_MID_FEE,
    NEW_OUT_FEE,
    NEW_FEE_GAMMA,
    NEW_ALLOWED_EXTRA_PROFIT,
    NEW_ADJUSTMENT_STEP,
    NEW_MA_TIME,
    PROPOSAL_TIME_WEEKS,
)

# Create and submit the proposal
with boa.env.prank(VOTE_CREATOR_SIM):
    vote_id = create_vote(
        get_address("ownership"),
        actions,
        description,
        os.getenv("ETHERSCAN_API_KEY"),
        os.getenv("PINATA_TOKEN"),
    )
print(f"Vote ID: {vote_id}")

# Simulate the proposal execution
simulate(vote_id, get_address("ownership"), os.getenv("ETHERSCAN_API_KEY"))

# Time travel to after the ramp period
boa.env.time_travel(seconds=60 * 60 * 24 * 8)  # 8 days (7 days ramp + 1 day buffer)

# Verify the new parameters

assert pool.A() == NEW_A
assert pool.gamma() == NEW_GAMMA
assert pool.mid_fee() == NEW_MID_FEE
assert pool.out_fee() == NEW_OUT_FEE
assert pool.fee_gamma() == NEW_FEE_GAMMA
assert pool.allowed_extra_profit() == NEW_ALLOWED_EXTRA_PROFIT
assert pool.adjustment_step() == NEW_ADJUSTMENT_STEP
print(f"Expected MA time (contract value): {NEW_MA_TIME}")
print(f"Actual MA time (contract value): {pool.ma_time()}")

# Define an acceptable error margin (e.g., 0.5%)
ERROR_MARGIN = 5

# Check if the actual value is within the acceptable range
lower_bound = NEW_MA_TIME * (1 - ERROR_MARGIN)
upper_bound = NEW_MA_TIME * (1 + ERROR_MARGIN)

assert lower_bound <= pool.ma_time() <= upper_bound, (
    f"MA time {pool.ma_time()} is outside the acceptable range "
    f"[{lower_bound}, {upper_bound}]"
)

print("All parameters updated successfully!")
