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

1. Pull Requests.
2. Create issues.
3. ...

# How does one build and publish?

1. Update codebase
2. Up version in pyproject.toml
3. `python -m build; python -m twine upload --repository pypi dist/* --verbose`
