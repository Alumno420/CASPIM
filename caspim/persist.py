import os
import zipfile
import filecmp
import pickle

import abc




class RenamingUnpickler(pickle.Unpickler):

    def __init__(self, codeVersion, file):
        super().__init__( file )
        self.codeVersion = codeVersion

    def find_class(self, module, name):
        module = module.replace( "hanlendar", "caspim")

        return super().find_class(module, name)



def load_object( inputFile, codeVersion, defaultValue=None ):
    try:
        with open( inputFile, 'rb') as fp:
            return RenamingUnpickler(codeVersion, fp).load()
#             return pickle.load(fp)
    except FileNotFoundError:
        
        return defaultValue
    except Exception:
        print("Error")
        raise


def store_object( inputObject, outputFile ):
    tmpFile = outputFile + "_tmp"
    with open(tmpFile, 'wb') as fp:
        pickle.dump( inputObject, fp )

    if os.path.isfile( outputFile ) is False:
        ## output file does not exist -- rename file
        
        os.rename( tmpFile, outputFile )
        return True

    if filecmp.cmp( tmpFile, outputFile ) is True:
        ## the same files -- remove tmp file
        os.remove( tmpFile )
        return False

    os.remove( outputFile )
    os.rename( tmpFile, outputFile )
    return True


def backup_files( inputFiles, outputArchive ):
    ## create zip
    tmpZipFile = outputArchive + "_tmp"
    zipf = zipfile.ZipFile( tmpZipFile, 'w', zipfile.ZIP_DEFLATED )
    for file in inputFiles:
        zipEntry = os.path.basename( file )
        zipf.write( file, zipEntry )
    zipf.close()

    ## compare content
    storedZipFile = outputArchive
    if os.path.isfile( storedZipFile ) is False:
        ## output file does not exist -- rename file
        os.rename( tmpZipFile, storedZipFile )
        return

    if filecmp.cmp( tmpZipFile, storedZipFile ) is True:
        ## the same files -- remove tmp file
        os.remove( tmpZipFile )
        return

    ## rename files
    counter = 1
    nextFile = "%s.%s" % (storedZipFile, counter)
    while os.path.isfile( nextFile ):
        counter += 1
        nextFile = "%s.%s" % (storedZipFile, counter)

    currFile = storedZipFile
    while counter > 1:
        currFile = "%s.%s" % (storedZipFile, counter - 1)
        os.rename( currFile, nextFile )
        nextFile = currFile
        counter -= 1

    os.rename( storedZipFile, nextFile )
    os.rename( tmpZipFile, storedZipFile )


class Versionable( metaclass=abc.ABCMeta ):

    def __getstate__(self):
        if not hasattr(self, "_class_version"):
            raise Exception("Your class must define _class_version class variable")
        # pylint: disable=E1101
        return dict(_class_version=self._class_version, **self.__dict__)

    def __setstate__(self, dict_):
        version_present_in_pickle = dict_.pop("_class_version", None)
        # pylint: disable=E1101
        if version_present_in_pickle == self._class_version:
            # pylint: disable=W0201
            self.__dict__ = dict_
        else:
            self._convertstate_( dict_, version_present_in_pickle )

    @abc.abstractmethod
    def _convertstate_(self, dict_, dictVersion_ ):
        raise NotImplementedError('You need to define this method in derived class!')
