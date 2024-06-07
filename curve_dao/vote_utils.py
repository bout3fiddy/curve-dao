import logging
import warnings
from typing import List, Tuple

import boa
from hexbytes import HexBytes
from rich.logging import RichHandler

from curve_dao.addresses import DAO, get_dao_parameters

warnings.filterwarnings("ignore")

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("rich")


class MissingVote(Exception):
    """Exception raised when a vote ID is invalid."""


def prepare_evm_script(dao: str | DAO, actions: List[Tuple], etherscan_api_key: str):
    """Generates EVM script to be executed by AragonDAO contracts.

    Args:
        target (dict): CURVE_DAO_OWNERSHIP / CURVE_DAO_PARAMS / EMERGENCY_DAO
        actions (list(tuple)): ("target addr", "fn_name", *args)

    Returns:
        str: Generated EVM script.
    """
    aragon_agent = boa.from_etherscan(
        get_dao_parameters(dao)["agent"], name="AragonAgent", api_key=etherscan_api_key
    )

    logger.info("Preparing EVM script")
    evm_script = bytes.fromhex("00000001")

    for action in actions:
        address, fn_name, *args = action
        contract = boa.from_etherscan(
            address=address, name="TargetContract", api_key=etherscan_api_key
        )
        contract_function = getattr(contract, fn_name)

        calldata = contract_function.prepare_calldata(*args)
        agent_calldata = aragon_agent.execute.prepare_calldata(address, 0, calldata)

        length = bytes.fromhex(hex(len(agent_calldata.hex()) // 2)[2:].zfill(8))
        evm_script = (
            evm_script
            + bytes.fromhex(aragon_agent.address[2:])
            + length
            + agent_calldata
        )

    evm_script = HexBytes(evm_script)
    logger.info(f"EVM script generated: {evm_script}")

    return evm_script
