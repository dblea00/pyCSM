import requests


def make_log_pkgs(url, tk, verify=False, cert=None):
    """
    This method will package all log files on the server into a .jar file

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    make_url = f"{url}/system/logpackages"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(make_url, headers=headers, verify=verify, cert=cert)


def get_log_pkgs(url, tk, verify=False, cert=None):
    """
    Gets a list of log packages and their location on the server

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
        """
    get_url = f"{url}/system/logpackages"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)


def backup_server(url, tk, verify=False, cert=None):
    """
    Creates a zip backup of the CSM server data
    that can be used for restoring the server at a later date

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    backup_url = f"{url}/system/backupserver"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(backup_url, headers=headers, verify=verify, cert=cert)


def set_server_as_standby(url, tk, active_server, verify=False, cert=None):
    """
    Issue this command to the server that you want to be the standby server.
    Sets the server passed in to be the active server. All data on
    the called server will be replaced with the data from the active server.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        active_server (str): IP or hostname of the active server.
        This method will use the default port.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    set_url = f"{url}/system/ha/setServerAsStandby/{active_server}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.put(set_url, headers=headers, verify=verify, cert=cert)
