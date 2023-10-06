
from caspim import persist

from caspim.domainmodel.item import Item


class ToDo( Item, persist.Versionable ):
    """ToDo is entity without placement in time."""

    ## 0: add subtodos
    ## 1: add base class Item
    _class_version = 1

    def _convertstate_(self, dict_, dictVersion_ ):

        if dictVersion_ is None:
            dictVersion_ = -1

        ## set of conditions converting dict_ to recent version
        if dictVersion_ < 0:
            ## initialize subtodos field
            dict_["subtodos"] = None
            dictVersion_ = 0

        if dictVersion_ == 0:
            ## base class extracted, "subtodos" renamed to "subitems"
            dict_["subitems"] = dict_["subtodos"]
            dict_.pop('subtodos', None)
            dictVersion_ = 1

        # pylint: disable=W0201
        self.__dict__ = dict_

    def addSubtodo(self, todo=None, index=-1):
        if todo is None:
            todo = ToDo()
        return self.addSubItem(todo, index)

    def __str__(self):
        subLen = 0
        if self.subitems is not None:
            subLen = len(self.subitems)
        return "[t:%s d:%s c:%s p:%s subs: %s]" % (
            self.title, self.description,
            self._completed, self.priority, subLen )
