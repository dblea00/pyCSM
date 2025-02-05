import json
import time
from datetime import datetime
import requests


def create_session(url, tk, name, sess_type, desc=None,
                   verify=False, cert=None):
    """
    Create a copy services manager session. A session must be created before
    copy sets can be placed into the session and managed by the server.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session that will be created.
        sess_type: The type of session to create.
        desc (str) (Optional): description for the session
    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    create_url = f"{url}/sessions/{name}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        "type": sess_type,
        "description": desc
    }
    return requests.put(create_url, headers=headers, data=params,
                        verify=verify, cert=cert)


def delete_session(url, tk, name, verify=False, cert=None):
    """
    Deletes a copy services manager session.
    Only inactive sessions can be deleted.

     Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session that will be deleted.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    delete_url = f"{url}/sessions/{name}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.delete(delete_url, headers=headers,
                           verify=verify, cert=cert)


def get_session_info(url, tk, name, verify=False, cert=None):
    """
    This method returns the detailed information for a given session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    getsi_url = f"{url}/sessions/{name}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(getsi_url, headers=headers, verify=verify, cert=cert)


def get_session_overviews(url, tk, verify=False, cert=None):
    """
    This method returns the overview summary information
    for all sessions managed by the server

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    gets_url = f"{url}/sessions"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(gets_url, headers=headers, verify=verify, cert=cert)


def get_commands(url, tk, name, verify=False, cert=None):
    """
    Returns the list of available commands
    for a session based on the session's current state

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.

    Returns:
        JSON String representing the result of the command.
        'I' = successful, 'W' = warning, 'E' = error.
    """
    getc_url = f"{url}/sessions/{name}/availablecommands"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(getc_url, headers=headers, verify=verify, cert=cert)


def get_options(url, tk, name, verify=False, cert=None):
    """
    Gets the options for the given session. The results returned
    from this method will vary depending on the session type.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.

    Returns:
        JSON String representing the result of the command.
    """
    geto_url = f"{url}/sessions/{name}/options"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(geto_url, headers=headers, verify=verify, cert=cert)


def description(url, tk, name, desc, verify=False, cert=None):
    """
    Changes the description field for a given session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        desc (str): description for the session

    Returns:
        JSON String representing the result of the command.
    """
    desc_url = f"{url}/sessions/{name}/description"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        "description": desc
    }
    return requests.post(desc_url, headers=headers, data=params,
                         verify=verify, cert=cert)


def run_command(url, tk, ses_name, com_name, verify=False, cert=None):
    """
    Run a command against a session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        ses_name (str): The name of the session.
        com_name (str): The name of the command.

    Returns:
        JSON String representing the result of the command.
    """
    runc_url = f"{url}/sessions/{ses_name}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        "cmd": com_name
    }
    return requests.post(runc_url, headers=headers, data=params,
                         verify=verify, cert=cert)


def wait_for_state(url, tk, ses_name, state, minutes=5, debug=False,
                   verify=False, cert=None):
    """
    Runs until the session is in a given state
    or until it times out and returns the results.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        ses_name (str): The name of the session.
        state (str): state of the server that user wants to wait for.
        minutes (double): amount of minutes before it times out
        debug (boolean): True if you want the state and
        status to print in console

    Returns:
        JSON String representing the result of the command.
    """
    start_time = datetime.utcnow()
    resp = get_session_info(url, tk, ses_name, verify=verify, cert=cert)
    time_passed = (datetime.utcnow() - start_time).total_seconds()
    while str(json.loads(resp.text)['state']) != state \
            and time_passed < minutes * 60:
        if debug:
            print("Status: " + json.loads(resp.text)['status']
                  + ", State: " + json.loads(resp.text)['state'])
        time.sleep(10)
        resp = get_session_info(url, tk, ses_name)
        if resp.status_code == 401:
            return resp
        time_passed = (datetime.utcnow() - start_time).total_seconds()

    if time_passed < minutes * 60:
        if debug:
            print(f"Session has reached {state} state.")
        return resp
    else:
        if debug:
            print(f'Timeout: Command exceeded {minutes} minutes.')
        return resp


def sgc_recover(url, tk, ses_name, com_name, role, backup_id,
                verify=False, cert=None):
    """
    Run a specified command that requires a backup ID parameter
    on a specified SGC session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        ses_name (str): The name of the session.
        com_name (str): The name of the command.
        role: The name of role where the backups reside.
        backup_id: The ID of the backup to send to the run command.

    Returns:
        JSON String representing the result of the command.
    """
    rec_url = f"{url}/sessions/{ses_name}/backups/{role}/{backup_id}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    params = {
        "cmd": com_name
    }
    return requests.post(rec_url, headers=headers, data=params,
                         verify=verify, cert=cert)


def get_backup_details(url, tk, name, role, backup_id,
                       verify=False, cert=None):
    """
    Gets detailed information for a given backup in a session.

    Args:
        url (str): Base url of CSM server. ex. https://servername:port/CSM/web.
        tk (str): Rest token for the CSM server.
        name (str): The name of the session.
        role: The name of role where the backups reside.
        backup_id: The ID of the backup to send to the run command.

    Returns:
        JSON String representing the result of the command.
    """
    get_url = f"{url}/sessions/{name}/backups/{role}/{backup_id}"
    headers = {
        "Accept-Language": "en-US",
        "X-Auth-Token": str(tk),
    }
    return requests.get(get_url, headers=headers, verify=verify, cert=cert)
