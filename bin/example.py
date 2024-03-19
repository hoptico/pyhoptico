import logging
import os
import json
import sys
from pyhoptico import HopticoClient

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)

    auth_token = os.getenv("HOPTICO_AUTH_TOKEN", None)
    if not auth_token:
        sys.stderr.write("Error: Must set HOPTICO_AUTH_TOKEN.\n")
        sys.exit(1)

    params = {
        "auth_token": auth_token,
    }

    base_url = os.getenv("HOPTICO_BASE_URL", None)
    if base_url:
        params["base_url"] = base_url

    c = HopticoClient(**params)
    query = "Ale"
    logger.info(f"Searching hoptico for beverages matching: [{query}]")
    results = c.search_beverages("Ale")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
