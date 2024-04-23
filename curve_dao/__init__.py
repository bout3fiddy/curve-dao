import logging
from typing import Dict, List, Tuple

import boa
from hexbytes import HexBytes
from rich.logging import RichHandler

from .ipfs import pin_to_ipfs  # noqa: F401
from .simulate import simulate  # noqa: F401
from .vote_utils import prepare_evm_script  # noqa: F401

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("rich")


def create_vote(
    target: Dict,
    actions: List[Tuple],
    description: str,
    etherscan_api_key: str,
    pinata_token: str,
) -> int:
    evm_script = prepare_evm_script(target, actions, etherscan_api_key)
    ipfs_hash_of_description = pin_to_ipfs(description, pinata_token)

    voting = boa.from_etherscan(
        target["voting"], name="AragonVoting", api_key=etherscan_api_key
    )

    try:
        assert voting.canCreateNewVote(boa.env.eoa)
    except Exception:
        logger.exception(
            "EOA cannot create new vote. Either there isn't enough veCRV balance or"
            "EOA created a vote less than 12 hours ago."
        )

    return voting.newVote(
        HexBytes(evm_script), f"ipfs:{ipfs_hash_of_description}", False, False
    )
