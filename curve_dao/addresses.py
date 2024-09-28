from strenum import StrEnum


class DAO(StrEnum):
    OWNERSHIP = "ownership"
    PARAM = "param"
    EMERGENCY = "emergency"


CURVE_DAO_OWNERSHIP = {
    "agent": "0x40907540d8a6C65c637785e8f8B742ae6b0b9968",
    "voting": "0xE478de485ad2fe566d49342Cbd03E49ed7DB3356",
    "token": "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",
    "quorum": 30,
}

CURVE_DAO_PARAM = {
    "agent": "0x4eeb3ba4f221ca16ed4a0cc7254e2e32df948c5f",
    "voting": "0xbcff8b0b9419b9a88c44546519b1e909cf330399",
    "token": "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2",
    "quorum": 15,
}

EMERGENCY_DAO = {"agent": "0x467947EE34aF926cF1DCac093870f613C96B1E0c"}
GAUGE_CONTROLLER = "0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB"
VOTING_ESCROW = "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2"
veCRV = VOTING_ESCROW
CRV = "0xD533a949740bb3306d119CC777fa900bA034cd52"
CONVEX_VOTERPROXY = "0x989AEB4D175E16225E39E87D0D97A3360524AD80"
ADDRESSPROVIDER = "0x5ffe7FB82894076ECB99A30D6A32e969e6e35E98"  # On all chains


def get_address(vote_type: DAO | str):
    """Get execution address of DAO (e.g. admin role)"""
    return get_dao_parameters(vote_type)["agent"]


def get_dao_parameters(vote_type: DAO | str):
    """
    :param vote_type: Name, agent address or enum
    """
    if not isinstance(vote_type, str):
        raise ValueError(f"Invalid type of vote_type: {type(vote_type)}")

    if vote_type.startswith("0x"):
        # {agent address: enum}
        vote_type = {get_dao_parameters(dao)["agent"].lower(): dao for dao in DAO}[
            vote_type.lower()
        ]
    match DAO(vote_type):
        case DAO.OWNERSHIP:
            return CURVE_DAO_OWNERSHIP
        case DAO.PARAM:
            return CURVE_DAO_PARAM
        case DAO.EMERGENCY:
            return EMERGENCY_DAO
