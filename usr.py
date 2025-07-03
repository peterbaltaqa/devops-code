from hash import hash

class Usr:
    def __init__(self, usrname, pw, isadmin = False):
        self.usrname = usrname
        self.pw = hash(pw)
        self.isadmin = isadmin

        self.data = (self.usrname, self.pw, self.isadmin)
