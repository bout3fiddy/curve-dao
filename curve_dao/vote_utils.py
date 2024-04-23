import sys
import warnings
from typing import Dict, List, Tuple

import boa
from rich.console import Console as RichConsole

warnings.filterwarnings("ignore")

logger = RichConsole(file=sys.stdout)


class MissingVote(Exception):
    """Exception raised when a vote ID is invalid."""


def prepare_evm_script(target: Dict, actions: List[Tuple], etherscan_api_key: str):
    """Generates EVM script to be executed by AragonDAO contracts.

    Args:
        target (dict): CURVE_DAO_OWNERSHIP / CURVE_DAO_PARAMS / EMERGENCY_DAO
        actions (list(tuple)): ("target addr", "fn_name", *args)

    Returns:
        str: Generated EVM script.
    """
    aragon_agent = boa.from_etherscan(
        target["agent"], name="AragonAgent", api_key=etherscan_api_key
    )
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

    return evm_script
