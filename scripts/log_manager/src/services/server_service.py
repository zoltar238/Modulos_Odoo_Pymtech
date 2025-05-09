import subprocess
import platform

def check_server_status(host: str) -> str:
    """
    Returns True if the server is up, False if not.
    :param host: The host to check.
    :return: True if the server is up, False if not.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    native_ping_command = ['ping', param, '1', host]
    nmap_ping_command = ['nmap', '-sn', host]
    print(subprocess.call(nmap_ping_command))

    try:
        # Check initial answer
        if subprocess.call(native_ping_command) == 0:
            return "Server is up"
        else:
            # Check with nmap
            if subprocess.call(nmap_ping_command) == 0:
                return "Server is up"
            else:
                return "Server is down"

    except subprocess.CalledProcessError:
        return "Error checking server status"

