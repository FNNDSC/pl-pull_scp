"""Perform tasks against a remote host."""
from typing     import List

from .config    import LOCAL_FILE_DIRECTORY

from .client    import RemoteClient
from .files     import fetch_local_files


# def initiate_client(ssh_remote_client: RemoteClient):
#     """
#     Initialize remote host client and execute actions.

#     :param ssh_remote_client: Remote server.
#     :type ssh_remote_client: RemoteClient
#     """
#     upload_files_to_remote(ssh_remote_client)
#     commandList_execOnRemote(
#         ssh_remote_client,
#         commands=[
#             "mkdir /uploads",
#             "cd /uploads/ && ls",
#         ],
#     )


def upload_files_to_remote(ssh_remote_client: RemoteClient):
    """
    Upload files to remote via SCP.

    :param ssh_remote_client: Remote server.
    :type ssh_remote_client: RemoteClient
    """
    local_files = fetch_local_files(LOCAL_FILE_DIRECTORY)
    ssh_remote_client.bulk_upload(local_files)


def commandList_execOnRemote(
    ssh_remote_client: RemoteClient, l_commands: List[str] = None
) -> list:
    """
    Execute UNIX command on the remote host. Commands are passed as a
    list -- each list element is executed in turn.

    :param ssh_remote_client: Remote server.
    :type ssh_remote_client: RemoteClient
    :param commands: List of commands to run on remote host.
    :type commands: List[str]
    """
    l_ret  : list = ssh_remote_client.commandList_exec(l_commands)
    return l_ret
