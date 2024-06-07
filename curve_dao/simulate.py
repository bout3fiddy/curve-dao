import logging

import boa
from rich.logging import RichHandler
from rich.panel import Panel
from rich.pretty import Pretty

from .addresses import CONVEX_VOTERPROXY, DAO, get_dao_parameters

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("rich")


def simulate(vote_id: int, dao: str | DAO, etherscan_api_key: str):
    logger.info("Simulating Vote")

    voting_contract = boa.from_etherscan(
        get_dao_parameters(dao)["voting"], "AragonVoting", api_key=etherscan_api_key
    )

    # print vote details to console first:
    logger.info("Vote stats before Convex Vote:")
    vote_stats = Panel(Pretty(voting_contract.getVote(vote_id)))
    logger.info(vote_stats)

    # vote
    logger.info("Simulate Convex 'yes' vote")
    voting_contract.canVote(vote_id, CONVEX_VOTERPROXY)
    with boa.env.prank(CONVEX_VOTERPROXY):
        voting_contract.vote(vote_id, True, False)

    # sleep for a week so it has time to pass
    num_seconds = voting_contract.voteTime()
    boa.env.time_travel(seconds=num_seconds)

    # get vote stats:
    logger.info("Vote stats after 1 week:")
    vote_stats = Panel(Pretty(voting_contract.getVote(vote_id)))
    logger.info(vote_stats)

    # moment of truth - execute the vote!
    logger.info("Simulate proposal execution")
    assert voting_contract.canExecute(vote_id)
    with boa.env.prank(boa.env.generate_address()):
        voting_contract.executeVote(vote_id)

    logger.info("Vote Executed!")
    return True
