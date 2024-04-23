import requests


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

    assert (
        200 <= response.status_code < 400
    ), f"POST to IPFS failed: {response.status_code}"

    return response.json()["IpfsHash"]
