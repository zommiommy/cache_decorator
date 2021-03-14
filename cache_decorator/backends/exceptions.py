class SerializationException(Exception):
    def __init__(self, error_message, path, result, backup_path=None):

        self.path = path
        self.backup_path = backup_path
        self.result = result

        super(SerializationException, self).__init__(error_message)


    
class DeserializationException(Exception):
    def __init__(self, error_message, path, backup_path=None):

        self.path = path
        self.backup_path = backup_path

        super(DeserializationException, self).__init__(error_message)
