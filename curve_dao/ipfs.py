import logging

import requests
from rich.logging import RichHandler

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

logger = logging.getLogger("rich")


def pin_to_ipfs(description: str, pinata_token: str):
    """Uploads vote description to IPFS via Pinata and returns the IPFS hash.

    NOTE: Needs environment variables for Pinata IPFS access. Please
    set up an IPFS project to generate API key and API secret!
    """

    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    headers = {
        "Authorization": f"Bearer {pinata_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "pinataContent": {"text": description},
        "pinataMetadata": {"name": "pinnie.json"},
        "pinataOptions": {"cidVersion": 1},
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    try:
        assert 200 <= response.status_code < 400
        ipfs_hash = response.json()["IpfsHash"]
        logger.info(f"Pinned Vote description to ipfs:{ipfs_hash}")
        return ipfs_hash

    except Exception:
        logger.exception(f"POST to IPFS failed: {response.status_code}")
        raise
