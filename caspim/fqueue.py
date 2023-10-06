
import os

import pqueue
from filelock import Timeout, FileLock


# script_dir = os.path.dirname(__file__)
# tmp_dir    = os.path.realpath( os.path.join( script_dir, os.pardir, os.pardir, 'tmp' ) )



queue_path      = os.path.join( '/tmp', 'hanlendar.spool' )
queue_info_path = os.path.join( queue_path, 'info' )
queue_lock      = os.path.join( '/tmp', 'hanlendar.spool.lock' )


## ensure directory exists (required for watchdog)
os.makedirs( queue_path, exist_ok = True )


def get_from_queue( nowait=False ):
    with FileLock( queue_lock ):
        quene = pqueue.Queue( queue_path )
        if nowait:
            message = quene.get()
        else:
            message = quene.get_nowait()
        quene.task_done()
        return message
    return None


def put_to_queue( message_type, value ):
    with FileLock( queue_lock ):
        quene = pqueue.Queue( queue_path )
        message = (message_type, value)
        print( "adding to queue:", message )
        quene.put( message )
