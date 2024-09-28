import logging
from typing import List, Tuple

import boa
from hexbytes import HexBytes
from rich.logging import RichHandler

from . import proposals  # noqa: F401,E402
from .addresses import DAO, get_address, get_dao_parameters  # noqa: F401
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
    dao: str | DAO,
    actions: List[Tuple],
    description: str,
    etherscan_api_key: str,
    pinata_token: str,
    is_simulation: bool = False,
) -> int:
    evm_script = prepare_evm_script(dao, actions, etherscan_api_key)

    vote_description_data = description
    if not is_simulation:
        vote_description_data = f"ipfs:{pin_to_ipfs(description, pinata_token)}"

    voting = boa.from_etherscan(
        get_dao_parameters(dao)["voting"],
        name="AragonVoting",
        api_key=etherscan_api_key,
    )

    try:
        assert voting.canCreateNewVote(boa.env.eoa)
    except Exception:
        logger.exception(
            "EOA cannot create new vote. Either there isn't enough veCRV balance or"
            "EOA created a vote less than 12 hours ago."
        )

    return voting.newVote(HexBytes(evm_script), vote_description_data, False, False)
