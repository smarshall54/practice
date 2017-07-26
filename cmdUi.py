import datetime
import csv
#import sys

"""
A python program that stores information about users.
Once they are logged in, Users can read and update 
their own information, and request information about 
other users.

The program includes a robust command line menu-
based interface.

There are two permissions levels:
Admins can see all information about everybody
Users can see only name and 
"""

class User(object):
    '''
    right now, User objects don't need to know anything about the Session, so they are a top-level class
    if I implement permissions, then the User method printAllUserInfo might want to know about the current
        login - and whether currentUser is an admin before deciding what it wants to print.
        
    However, it seems cleaner to handle permissions checking in the Session class. Then, this would necessitate 
    the User class having two methods; printAllForUser and printAllForAdmin. This is repetitive as well, and the reason
    is because the method printAllUserInfo breaks MVC separation: it is trying to output to the View)but in reality it is just 
    a model containing data! Of course Session() is handling a lot of control and model tasks, menu is handling model
    and view, etc etc. Full adherence to the standard would require a lot of rearchitecting. But it is good to note.
    '''
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.birthday = datetime.date(1900, 1, 1)
        area = 555
        localph = 555
        persph = 5555
        self.phone = '({}) {}-{}'.format(area, localph, persph)
        # on creation, write user's info to a file (database)
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    def set_username(self, username):
        self.username = username
    def set_password(self, password):
        self.password = password
    def get_age(self):
        # today - self.birthday
        return self.birthday
    def set_age(self, y, m, d):
        self.birthday=datetime.date(y, m, d)
    def set_phone(self, digits):
        area = digits[0:3]
        localph = digits[3:6]
        persph = digits[6:10]
        self.phone = '({}) {}-{}'.format(area, localph, persph)
    def get_phone(self):
        return self.phone
    def __str__(self):
        return 'User object with info: {} {} {} {}'.format(self.username, self.password, self.birthday, self.phone)
    def printAllUserInfo(self):
        print('Your user info is:')
        print('------------------')
        print('User Name: {}'.format(self.get_username()))
        print('Password: {}'.format(self.get_password()))
        print('Birthday: {}'.format(self.get_age()))
        print('Phone Number: {}'.format(self.get_phone()))
    def updateUserInfo(self):
        print('What would you like to update?')
        updateMenu = Menu('Update Your Info', self.username)
        # when info is updated, write the new info to the users file (database)

class Admin(User):
    pass
class Member(User):
    pass
    
class Session(object):
    '''
    this would be the class that object-orients the main session
    this will enable us to track current login/logout/registration,  manage permissions, and
    contain all of the methods for searching the userDB
    
    data to save about the session:
    - current user
    - loaded user "database" (currently read in from csv)
    - loaded menus
    '''
    def __init__(self):
        '''
        initializing this class starts the session by loading the userDB, prompting for a
        valid login, and starting the main menu
        '''
        self.userDB = self.loadUserDB()
        for e in self.userDB:
            print('loaded ',  e)
        self.username = self.login()
        self.currentUser = self.userDB[self.username]
        #not implemented - user privileges
        #self.usertype = self.userDB[self.username].get_privilege()

    def loadUserDB(self):
        '''
        opens a text file in the current directory containing information about existing users.
        reads the file and creates User objects for each one.
        userDB is stored into a dict
        
        returns --> list of User objects
        '''
        f= open('userList.csv')
        reader = csv.reader(f)
        uDict = {}
        for nr, row in enumerate(reader):
            if nr==0:
                header = row
                if False:
                    print(header)
            else: # replace with strptime, but this was good practice for string indexing
                uDict[row[0]] = User(row[0], row[1]) #create a user with the required inputs from the csv
                uDict[row[0]].set_age(int(row[2][0:4]), int(row[2][4:6]), int(row[2][6:])) #parse out the date from the csv (could use strptime method)
                uDict[row[0]].set_phone(row[3]) # plug in more user data
        f.close()
        return uDict
    
    def writeUserDB(self):
        f=open('userList.csv', 'wt')
        writer = csv.writer(f)
        for nr, row in enumerate(writer):
            print(row)
        f.close()
        
    
    def login(self):
        '''
        handles initial login and validation.
        matches username/pw to what exists in the db
        if no uname/pw, offers option to register a new user
        userDB = dict of User objects keyed on their username attribute
            (generated by loadUserDB)
        
        returns --> True if successful login
        returns --> False if unsuccessful
        '''
        uNameValid = False
        while not uNameValid:
            username = input('Please enter your username to get started: ')
            if not username in self.userDB:
                uNameValid = False
                print('That username does not exist in our system. Please try again.')
            else:
                uNameValid = True
        
        pwValid = False
        tryCount = 0
        while not pwValid and tryCount <= 3:
            password = input('Please enter the password for {}: '.format(username))
            
            if password != self.userDB[username].get_password():
                pwValid = False
                print('The password is incorrect.')
                tryCount += 1
            else:
                pwValid = True
                print('Successfully logged in as {}'.format(username))
        if tryCount > 3:
            print('You have exceeded the number of tries and your session has been ended.')
        if pwValid and uNameValid:
            return username
        else: 
            self.login() #just ask for login again... not very secure
            return None
            
    def lookupOther(self):
        otherName = input('Get information about user: ')
        if not otherName in self.userDB.keys():
            print('Sorry, that user does not exist.')
        else:
            self.userDB[otherName].printAllUserInfo()
            
class Menu(Session): #was (object). I think this needs to be a subclass in
                                    # order for the menufuncs to know which class to use
                                    # methods on
    def __init__(self,  menuname,  currentSession): #maybe could stop passing Session objects around if I properly initialize this subclass with the appropriate superclass properties of self.currentUser and self.currentSession...
        """
        menuname --> str
        currentSession --> session object
        """
        self.menuname = menuname
        # assign menu keys to printed option items and functions
        self.menuopts = {1:'Print your User Info', 2:'Update your Info', 3:'Look up another User', 4:'Quit'}
        self.menufuncs = {1: currentSession.currentUser.printAllUserInfo,2: currentSession.currentUser.updateUserInfo, 3:currentSession.lookupOther, 4:self.quitMenu}
        # hardcoded for now since I only have 1 menu defined.
        #for extensibility, this init should open a file e.g. menus.py which defines the menu
        self.quitflag = False
        
    def quitMenu(self):
        self.quitflag = True
        
    def showMenu(self):
        print('---- {} ----'.format(self.menuname))
        print('-------------------')
        for key in self.menuopts:
            print('{}. {}'.format(key,  self.menuopts[key]))
        selection = int(input('Enter the number corresponding to your choice: '))
        self.menufuncs[selection]()
        if self.quitflag:
            return None # this will return the user to the previous level of menu hierarchy
        else:
            return self.showMenu() # this recursive call actually creates the menu loop
    
def main(): # main hook into program
    print('Executed as script') # just checking the if  __name__ == '__main__'
    print("Welcome to Steve's UI")
    currentSession = Session()  #init session (loads userDB and calls login procedure)
    mainMenu = Menu('Main Menu', currentSession) #can i init the menu subclass properly so I don't have to pass in its own superclass currentSession?
    mainMenu.showMenu()
    if mainMenu.quitflag:
        print('Exiting... saving user data...')
        currentSession.writeUserDB()
        print('Goodbye!')
    return None
    
    
if __name__ == '__main__':
    main()
    # instead of calling the main function here, we could also make main() a class
    # and instantiate that class as the main hook into the program. is this valid?
