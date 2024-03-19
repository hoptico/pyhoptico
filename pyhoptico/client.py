import logging

import requests

logger = logging.getLogger(__name__)


class ClientError(Exception):
    pass


class AuthError(ClientError):
    """Thrown when auth fails."""


class ValidationError(ClientError):
    """Thrown when shape of remote data doesn't match expectations."""


class HopticoClient:
    def __init__(self, auth_token, base_url="https://hoptico.com", session=None):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = session or requests.Session()

    def _get(self, path, *args, **kwargs):
        return self._request("GET", path, *args, **kwargs)

    def _post(self, path, *args, **kwargs):
        return self._request("POST", path, *args, **kwargs)

    def _request(self, method, path, *args, **kwargs):
        url = f"{self.base_url}/{path}"

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"token {self.auth_token}"
        kwargs["headers"] = headers

        try:
            response = self.session.request(method, url, *args, **kwargs)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.error(e.response.json())
                raise e
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthError from e
            raise ClientError(f"Bad request: {e}") from e
        except requests.exceptions.RequestException as e:
            logger.exception("Hoptico API error")
            raise ClientError(f"Bad request: {e}") from e

    def search_beverages(self, query):
        return self._get(
            "api/v1/search",
            params={
                "query": query,
            },
        )

    def create_or_update_beverage(
        self,
        *,
        name,
        producer_name,
        producer_type,
        origin_iso3166,
        beverage_type,
        beverage_style_name,
        abv_percent,
        ibu,
    ):
        data = {
            "name": name,
            "producer_name": producer_name,
            "producer_type": producer_type,
            "beverage_type": beverage_type,
            "beverage_style_name": beverage_style_name,
        }
        if abv_percent is not None:
            data["abv_percent"] = abv_percent
        if ibu is not None:
            data["ibu"] = ibu
        if origin_iso3166 is not None:
            data["origin_iso3166"] = origin_iso3166
        return self._post("api/v1/beverages/create-or-update", json=data)
