# Curve DAO Operations

This repository contains tools, written in python, for Curve DAO operations. The goal is to provide a simple command-line interface that allows veCRV holders to create and decode on-chain executable proposals, and simple scripts to produce analytics on governance in the Curve DAO.

Such a CLI tool allows independence from a web-ui: after all, decentralisation goes beyond just network decentralisation: it more or less means democratic access to technology.

# Who needs this?

veCRV holders looking to create on-chain proposals such as

- Creating or killing Curve DAO gauges that reward CRV inflation to addresses (liquidity pools or otherwise).
- Creating a smartwallet whitelist to lock veCRV (veCRV restricts smart contracts to lock CRV, subject to a DAO whitelist vote)
- Changing liquidity pool parameters
- Adding gauge types ...
- ... etc.

Curve DAO stakeholders have the ability to change the protocol in many ways. This repository is an attempt to consolidate all on-chain DAO operations into a single tool.

# Setup

...
