import pprint
import sys

import boa
from rich.console import Console as RichConsole

from .addresses import CONVEX_VOTERPROXY

logger = RichConsole(file=sys.stdout)


def simulate(vote_id: int, voting_contract: str, etherscan_api_key: str):
    logger.info("--------- SIMULATE VOTE ---------")

    voting_contract = boa.from_etherscan(
        voting_contract, "AragonVoting", api_key=etherscan_api_key
    )

    # print vote details to console first:
    logger.info("Vote stats before Convex Vote:")
    vote_stats = voting_contract.getVote(vote_id)
    logger.info(pprint.pformat(vote_stats, indent=4))

    # vote
    logger.info("Simulate Convex 'yes' vote")
    with boa.env.prank(CONVEX_VOTERPROXY):
        voting_contract.vote(vote_id, True, False)

    # sleep for a week so it has time to pass
    num_seconds = voting_contract.voteTime()
    boa.env.time_travel(seconds=num_seconds)

    # get vote stats:
    logger.info("Vote stats after 1 week:")
    vote_stats = voting_contract.getVote(vote_id)
    pprint.pformat(vote_stats, indent=4)

    # moment of truth - execute the vote!
    logger.info("Simulate proposal execution")
    with boa.env.prank(boa.env.generate_address()):
        voting_contract.executeVote(vote_id)
    logger.info("Vote Executed!")
