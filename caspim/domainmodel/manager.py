from datetime import date, datetime

import glob
from icalendar import cal

from caspim import persist
from caspim.domainmodel.task import Task, TaskOccurrence
from caspim.domainmodel.todo import ToDo
from caspim.domainmodel.reminder import Notification
from caspim.domainmodel.item import Item





def extract_ical( content ):
    cal_begin_pos = content.find( "BEGIN:VCALENDAR" )
    if cal_begin_pos < 0:
        return content
    END_SUB = "END:VCALENDAR"
    cal_end_pos = content.find( END_SUB, cal_begin_pos )
    if cal_end_pos < 0:
        return content
    cal_end_pos += len( END_SUB )
    return content[ cal_begin_pos:cal_end_pos ]


class Manager():
    """Root class for domain data structure."""

    ## 1 - renamed modules
    _class_version = 1

    def __init__(self):
        """Constructor."""
        self._tasks = list()
        self._todos = list()
        self.notes = { "Anotaciones": "" }        ## default notes

    def store( self, outputDir ):
        outputFile = outputDir + "/version.obj"

        changed = False
        if persist.store_object( self._class_version, outputFile ) is True:
            changed = True

        outputFile = outputDir + "/tasks.obj"
        if persist.store_object( self.tasks, outputFile ) is True:
            changed = True

        outputFile = outputDir + "/todos.obj"
        if persist.store_object( self.todos, outputFile ) is True:
            changed = True

        outputFile = outputDir + "/notes.obj"
        if persist.store_object( self.notes, outputFile ) is True:
            changed = True

        ## backup data
        objFiles = glob.glob( outputDir + "/*.obj" )
        storedZipFile = outputDir + "/data.zip"
        persist.backup_files( objFiles, storedZipFile )

        return changed

    def load( self, inputDir ):
        inputFile = inputDir + "/version.obj"
        mngrVersion = persist.load_object( inputFile, self._class_version )
        if mngrVersion != self. _class_version:
            pass

        inputFile = inputDir + "/tasks.obj"
        self.tasks = persist.load_object( inputFile, self._class_version )
        if self.tasks is None:
            self.tasks = list()

        inputFile = inputDir + "/todos.obj"
        self.todos = persist.load_object( inputFile, self._class_version )
        if self.todos is None:
            self.todos = list()

        inputFile = inputDir + "/notes.obj"
        self.notes = persist.load_object( inputFile, self._class_version )
        if self.notes is None:
            self.notes = { "Anotaciones": "" }

    ## ======================================================================

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, newList):
        self._tasks = newList

    def getTasks( self ):
        return list( self.tasks )                   ## shallow copy of list

    def getTasksAll(self):
        """Return tasks and all subtasks from tree."""
        return Item.getAllSubItemsFromList( self.tasks )

    def getTaskOccurrencesForDate(self, taskDate: date, includeCompleted=True):
        retList = list()
        allTasks = self.getTasksAll()
        for task in allTasks:
            entry = task.getTaskOccurrenceForDate( taskDate )
            if entry is None:
                continue
            if includeCompleted is False:
                if entry.isCompleted():
                    continue
            retList.append( entry )
        return retList

    def getNextDeadline(self) -> Task:
        retTask: Task = None
        allTasks = self.getTasksAll()
        for task in allTasks:
            if task.isCompleted():
                continue
            if task.occurrenceDue is None:
                continue
            if retTask is None:
                retTask = task
            elif task.occurrenceDue < retTask.occurrenceDue:
                retTask = task
        return retTask

    def getDeadlinedTasks(self):
        retTasks = list()
        allTasks = self.getTasksAll()
        for task in allTasks:
            occurrence: TaskOccurrence = task.currentOccurrence()
            if occurrence.isCompleted():
                continue
            if occurrence.isTimedout():
                retTasks.append( task )
        return retTasks

    def getRemindedTasks(self):
        retTasks = list()
        allTasks = self.getTasksAll()
        for task in allTasks:
            occurrence: TaskOccurrence = task.currentOccurrence()
            if occurrence.isCompleted():
                continue
            if occurrence.isReminded():
                retTasks.append( task )
        return retTasks

    def getTaskCoords(self, task):
        return Item.getItemCoords( self.tasks, task )

    def getTaskByCoords(self, task):
        return Item.getItemFromCoords( self.tasks, task )

    def insertTask( self, task: Task, taskCoords ):
        if taskCoords is None:
            self.tasks.append( task )
            return
        taskCoords = list( taskCoords )     ## make copy
        listPos = taskCoords.pop()
        parentTask = self.getTaskByCoords( taskCoords )
        if parentTask is not None:
            parentTask.addSubItem( task, listPos )
        else:
            self.tasks.insert( listPos, task )

    def addTask( self, task: Task = None ):
        if task is None:
            task = Task()
        self.tasks.append( task )
        task.setParent( None )
        return task

    def addNewTask( self, taskdate: date, title ):
        task = Task()
        task.title = title
        task.setDefaultDate( taskdate )
        self.addTask( task )
        return task

    def addNewTaskDateTime( self, taskdate: datetime, title ):
        task = Task()
        task.title = title
        task.setDefaultDateTime( taskdate )
        self.addTask( task )
        return task

    def removeTask( self, task: Task ):
        return Item.removeSubItemFromList(self.tasks, task)

    def replaceTask( self, oldTask: Task, newTask: Task ):
        return Item.replaceSubItemInList(self.tasks, oldTask, newTask)

    def addNewDeadlineDateTime( self, eventdate: datetime, title ):
        eventTask = Task()
        eventTask.title = title
        eventTask.setDeadlineDateTime( eventdate )
        self.addTask( eventTask )
        return eventTask

    def getNotificationList(self):
        ret = list()
        for i in range(0, len(self.tasks)):
            task = self.tasks[i]
            notifs = task.getNotifications()
            ret.extend( notifs )
        ret.sort( key=Notification.sortByTime )
        return ret
    
    def importICalendar(self, content: str):
        try:
            extracted_ical = extract_ical( content )
            gcal = cal.Calendar.from_ical( extracted_ical )
            tasks = []
            for component in gcal.walk():
                if component.name == "VEVENT":
                    summary    = component.get('summary')
                    location   = component.get('location')
                    start_date = component.get('dtstart').dt
                    start_date = start_date.astimezone()            ## convert to local timezone
                    start_date = start_date.replace(tzinfo=None)
                    end_date   = component.get('dtend').dt
                    end_date   = end_date.astimezone()              ## convert to local timezone
                    end_date   = end_date.replace(tzinfo=None)
                    
                    #TODO: check if task already added
                    
                    task = Task()
                    task.title = f"{summary}, {location}"
                    task.description = component.get('description')
                    task.description = task.description.replace( "=0D=0A", "\n" )
                    task.startDateTime = start_date
                    task.dueDateTime   = end_date
                    task.addReminderDays( 1 )
                    
                    addedTask = self.addTask( task )
                    tasks.append( addedTask )
            return tasks
        except ValueError:
            pass
        return None

    ## ========================================================

    @property
    def todos(self):
        return self._todos

    @todos.setter
    def todos(self, newList):
        self._todos = newList

    def getToDos( self, includeCompleted=True ):
        if includeCompleted:
            return list( self.todos )       ## shallow copy of list
        return [ item for item in self.todos if not item.isCompleted() ]

    def getTodosAll(self):
        """Return todos and all subtodos from tree."""
        return Item.getAllSubItemsFromList( self.todos )

    def getToDoCoords(self, todo):
        return Item.getItemCoords( self.todos, todo )

    def getToDoByCoords(self, todo):
        return Item.getItemFromCoords( self.todos, todo )

    def insertToDo( self, todo: ToDo, todoCoords ):
        if todoCoords is None:
            self.todos.append( todo )
            return
        todoCoords = list( todoCoords )     ## make copy
        listPos = todoCoords.pop()
        parentToDo = self.getToDoByCoords( todoCoords )
        if parentToDo is not None:
            parentToDo.addSubItem( todo, listPos )
        else:
            self.todos.insert( listPos, todo )

    def addToDo( self, todo: ToDo = None ):
        if todo is None:
            todo = ToDo()
        self.todos.append( todo )
        todo.setParent( None )
        return todo

    def addNewToDo( self, title ):
        todo = ToDo()
        todo.title = title
        self.addToDo( todo )
        return todo

    def removeToDo( self, todo: ToDo ):
        return Item.removeSubItemFromList(self.todos, todo)

    def replaceToDo( self, oldToDo: ToDo, newToDo: ToDo ):
        return Item.replaceSubItemInList(self.todos, oldToDo, newToDo)

    def getNextToDo(self) -> ToDo:
        nextToDo = None
        allItems = self.getTodosAll()
        for item in allItems:
            if item.isCompleted():
                continue
            if nextToDo is None:
                nextToDo = item
                continue
            if nextToDo.priority < item.priority:
                nextToDo = item
        return nextToDo

    ## ========================================================

    def getNotes(self):
        return self.notes

    def setNotes(self, notesDict):
        self.notes = notesDict

    def addNote(self, title, content):
        self.notes[title] = content

    def renameNote(self, fromTitle, toTitle):
        self.notes[toTitle] = self.notes.pop(fromTitle)

    def removeNote(self, title):
        del self.notes[title]

    def printTasks(self):
        retStr = ""
        tSize = len(self.tasks)
        for i in range(0, tSize):
            task = self.tasks[i]
            retStr += str(task) + "\n"
        return retStr


## ========================================================


def replace_in_list( aList, oldObject, newObject ):
    for i, _ in enumerate(aList):
        entry = aList[i]
        if entry == oldObject:
            aList[i] = newObject
            break
