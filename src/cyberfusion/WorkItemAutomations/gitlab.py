import gitlab


def get_gitlab_connector(url: str, private_token: str) -> gitlab.client.Gitlab:
    """Get GitLab connector."""
    connector = gitlab.Gitlab(url=url, private_token=private_token)

    connector.auth()

    return connector
