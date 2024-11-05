import os
from synology_api import filestation

class Synology:

    def __init__(self):
        ip_address = os.getenv("SERVER_IP_ADDRESS")
        if not ip_address:
            raise ValueError("SERVER_IP_ADDRESS is not set.")
        self.ip_address = ip_address
        port = os.getenv("SERVER_PORT")
        if not port:
            raise ValueError("SERVER_PORT is not set.")
        self.port = port
        username = os.getenv("SERVER_USERNAME")
        if not username:
            raise ValueError("SERVER_USERNAME is not set.")
        self.username = username
        password = os.getenv("SERVER_PASSWORD")
        if not password:
            raise ValueError("SERVER_PASSWORD is not set.")
        self.password = password
        dest_path = os.getenv("DEST_PATH")
        if not dest_path:
            raise ValueError("DEST_PATH is not set.")
        self.dest_path = dest_path

    def save_to_server(self, upload_file):
        fl = filestation.FileStation(self.ip_address, self.port, self.username, self.password,
                                     secure=False, cert_verify=False, dsm_version=6, debug=True, otp_code=None)

        fl.upload_file(self.dest_path, upload_file)