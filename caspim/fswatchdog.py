import time

import contextlib

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FSWatcher:

    def __init__(self):
        self.observer = Observer()
        self.event_handler = None

    def pause(self):
        if self.event_handler is None:
            return
        self.event_handler.ignore = True

    def resume(self):
        if self.event_handler is None:
            return
        self.observer.event_queue.queue.clear()
        self.event_handler.ignore = False

    def start( self, path, callback=None, recursive=True ):
        self.event_handler = FSHandler( callback )
        self.observer.schedule( self.event_handler, path, recursive=recursive )
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def run(self, directory):
        self.start( directory )

        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print( "Error" )

        self.stop()

    @contextlib.contextmanager
    def ignoreEvents(self):
        self.pause()
        yield
        self.resume()


class WatcherBlocker:
    """
    Context guard.

    Disables watcher callbacks in "with" scope.
    """

    def __init__(self, watcher: FSWatcher):
        self.watcher: FSWatcher = watcher

    def __enter__(self):
        if self.watcher is None:
            return
        self.oldEnabled = self.watcher.setEnabled( False )
        self.watcher.ignoreNextEvent()

    def __exit__(self, exceptionType, value, traceback):
        if self.watcher is None:
            return False                                                            ## do not suppress exceptions
        if self.oldEnabled is None:
            return False                                                            ## do not suppress exceptions
        self.watcher.setEnabled( self.oldEnabled )
        return False                                                                ## do not suppress exceptions



class FSHandler(FileSystemEventHandler):

    def __init__(self, callback=None):
        self.callback = callback
        self.ignore = False

    def on_created(self, event):
        # Take any action here when a file is first created.
        if self.callback is None:
            print( "Received created event - %s." % event.src_path )
            return
        if self.ignore:
            return
        self.callback()
