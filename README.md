# Example

```python
import boa
import curve_dao

contract = boa.load("contracts/contract.vy",
    curve_dao.get_address("ownership"), curve_dao.get_address("param"), curve_dao.get_address("emergency"),  # Set admins
)
ACTIONS = [
    ("0xcontract", "set_something", ("values",), 70, "set"),  # 0xcontract.set_something(("values",), 70, "set)
    (contract, "enact"),  # contract.enact()
]
DESCRIPTION = "Enact something"
vote_id = curve_dao.create_vote("ownership", ACTIONS, DESCRIPTION,
                                etherscan_api_key=os.environ["ETHERSCAN_API_KEY"], pinata_token=os.environ["PINATA_TOKEN"])
if is_simulation:  # forked environment
    curve_dao.simulate(vote_id, "ownership", etherscan_api_key=os.environ["ETHERSCAN_API_KEY"])
```

# What is this?

Simple python package to simulate on-chain CurveDAO proposals and publish proposals for DAO voting on-chain.

# Who needs this?

veCRV holders looking to create on-chain proposals such as

- Creating or killing Curve DAO gauges that reward CRV inflation to addresses (liquidity pools or otherwise).
- Creating a smartwallet whitelist to lock veCRV (veCRV restricts smart contracts to lock CRV, subject to a DAO whitelist vote)
- Changing liquidity pool parameters
- Adding gauge types ...
- ... etc.

Curve DAO stakeholders have the ability to change the protocol in many ways. This repository is an attempt to consolidate all on-chain DAO operations into a single tool.

# How does one install it?

`pip install curve-dao`

# How does one contribute?

1. Fork + Pull Requests.
2. Create issues.
3. ...

# How does one test?

`python -m pytest .`

# How does one build and publish?

1. Update codebase
2. Up version in pyproject.toml
3. `python -m build; python -m twine upload --repository pypi dist/* --verbose`
