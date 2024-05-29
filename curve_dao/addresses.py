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

EMERGENCY_DAO = "0x467947EE34aF926cF1DCac093870f613C96B1E0c"
GAUGE_CONTROLLER = "0x2F50D538606Fa9EDD2B11E2446BEb18C9D5846bB"
VOTING_ESCROW = "0x5f3b5DfEb7B28CDbD7FAba78963EE202a494e2A2"
veCRV = VOTING_ESCROW
CRV = "0xD533a949740bb3306d119CC777fa900bA034cd52"
CONVEX_VOTERPROXY = "0x989AEB4D175E16225E39E87D0D97A3360524AD80"
ADDRESSPROVIDER = "0x5ffe7FB82894076ECB99A30D6A32e969e6e35E98"  # On all chains


def get_dao_voting_contract(vote_type: str):
    target = get_target(vote_type)
    return target["voting"]


def get_target(vote_type: str):
    match vote_type:
        case "ownership":
            return CURVE_DAO_OWNERSHIP
        case "parameter":
            return CURVE_DAO_PARAM
        case "emergency":
            return EMERGENCY_DAO
