class User(object):

    def __init__(self,user_id = None):
      if user_id == -1
          self.new_user = True
      else:
          self.new_user = False

          #fetch all records from db about user_id
          self._populateUser()

    def commit(self):
        if self.new_user:
            #Do INSERTs
        else:
            #Do UPDATEs

    def delete(self):
        if self.new_user == False:
            return False

        #Delete user code here

    def _populate(self):
        #Query self.user_id from database and
        #set all instance variables, e.g.
        #self.name = row['name']

    def getFullName(self):
        return self.name

#Create a new user
>>u = User()
>>u.name = 'Jason Martinez'
>>u.password = 'linebreak'
>>u.commit()
>>print u.getFullName()
>>Jason Martinez

#Update existing user
>>u = User(43)
>>u.name = 'New Name Here'
>>u.commit()
>>print u.getFullName()
>>New Name Here