import os
import uuid
import sqlite3
import collections
import datetime

class ProjDBManager(object):
    def __init__(self):
        self.dbPath = os.environ['HOME']+".stetsonProjMngr.db"

    def initNewDB(self):
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE projects
            (ID INT PRIMARY KEY,
            CREATED_USER TEXT,
            CREATED_DATE DATE,
            PROJECT_NAME TEXT,
            PROJECT_TYPE TEXT);''')
        conn.commit()
        conn.close()

    def addProject(self, project):
        if not isinstance(project, StetsonProj):
            raise TypeError("Project to be added must be a StetsonProj object.")

        items = [(category, value) for category, value in project.items()]
        conn = sqlite3.connect(self.dbPath)
        conn.executemany('INSERT INTO projects VALUES (?,?)', items)
        conn.execute("INSERT INTO projects (ID,CREATED_USER,CREATED_DATE,PROJECT_NAME,PROJECT_TYPE) \
            VALUES (1, 'allen', '11/16/2016', 'Stetson Project Manager', 'home')")
        conn.commit()
        conn.close()

    def getRecords(self):
        conn = sqlite3.connect(self.dbPath)
        cursor = conn.execute("SELECT * FROM projects")
        for row in cursor:
            print(row)
        conn.close()

class StetsonProj(collections.OrderedDict):
    def __init__(self):
        super(StetsonProj, self).__init__()
        self['ID'] = str(uuid.uuid4())
        self['CLIENTS'] = []
        self['CONTACTS'] = []
        self['COLOR'] = ""
        self['DATE_CREATED'] = datetime.datetime.now().strftime("%Y.%m.%d_%H:%M:%S")
        self['DATE_MODIFIED'] = datetime.datetime.now().strftime("%Y.%m.%d_%H:%M:%S")
        self['DESCRIPTION'] = ""
        self['DIRECTORY_NAS'] = ""
        self['DIRECTORIES_LOCAL'] = ""
        self['FILE_TYPES'] = []
        self['GIT_ENABLED'] = False
        self['GIT_ROOT'] = ""
        self['IMG_PREVIEW'] = ""
        self['INTEGRATIONS'] = []
        self['IS_ARCHIVED'] = False
        self['LAST_SYNC_DATE'] = datetime.datetime.now() - datetime.timedelta(365) # Init with dummy value
        self['LAST_SYNC_HOST'] = ""
        self['NOTES'] = {}
        self['OWNER'] = None
        self['PROJECT_CATEGORY'] = None
        self['PROJECT_NAME'] = None
        self['PROJECT_STATUS'] = None
        self['PROJECT_TYPE'] = None
        self['TAGS'] = []
        self['THUMBNAIL'] = None
        self['USER_CONTRIBUTORS'] = None
        self['USER_CREATED'] = os.environ['USERNAME']
        self['USER_MODIFIED'] = None
        self['WORKPLACE'] = None


class StetsonBillingHistory(object):
    def __init__(self):
        pass
