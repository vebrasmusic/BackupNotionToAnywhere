from abc import ABC, abstractmethod

class StorageInterface(ABC):

    @abstractmethod
    def upload_backup(self, file_path):
        """Uploads a file to the storage destination"""
        pass