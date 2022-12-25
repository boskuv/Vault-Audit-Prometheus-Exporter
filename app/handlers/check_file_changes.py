from watchdog.observers import Observer


class FileObserver(Observer):
    def __init__(self, event_handler, path_from_config):
        super().__init__()

        self.schedule(event_handler, path=path_from_config)
