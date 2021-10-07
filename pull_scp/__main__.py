from pull_scp.pull_scp import Pull_scp

import  pudb

from .config import (
    SCP_DESTINATION_FOLDER,
    SSH_KEY_FILEPATH,
    SSH_PASSWORD,
    SSH_REMOTE_HOST,
    SSH_USERNAME,
)

# from paramiko_tutorial import initiate_client
from .client import RemoteClient

# Create SSH remote client connection
ssh_remote_client = RemoteClient(
    SSH_REMOTE_HOST,
    SSH_USERNAME,
    SSH_PASSWORD,
    SSH_KEY_FILEPATH,
    SCP_DESTINATION_FOLDER,
)

def main():
    chris_app = Pull_scp(ssh_remote_client)
    chris_app.launch()


if __name__ == "__main__":
    main()
