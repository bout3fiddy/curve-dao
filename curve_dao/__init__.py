from typing import Dict

import boa
from hexbytes import HexBytes

from .ipfs import pin_to_ipfs  # noqa: F401
from .simulate import simulate  # noqa: F401
from .vote_utils import prepare_evm_script  # noqa: F401


def create_vote(
    target: Dict, evm_script: str, etherscan_api_key: str, ipfs_hash_of_description: str
):
    voting = boa.from_etherscan(
        target["voting"], "AragonVoting", api_key=etherscan_api_key
    )
    assert voting.canCreateNewVote(boa.env.eoa)
    return voting.newVote(
        HexBytes(evm_script), f"ipfs:{ipfs_hash_of_description}", False, False
    )
