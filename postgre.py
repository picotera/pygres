import psycopg2
import os

from ConfigParser import SafeConfigParser

class PostgresConnection(object):
    '''
    A generic class of connections, in case we'll have more inheritants
    '''
    def __init__(self, config):
    
        self.__loadConfig(config)
        self.__connect()
        self.__setup()        

    def __loadConfig(self, configFile):
    
        parser = SafeConfigParser()
        parser.read(configFile)
        
        env = parser.getboolean('POSTGRESQL','env_variables')
        # If these are environment variables, which is the case in openshift
        if env:
            self.host = os.environ[parser.get('POSTGRESQL','host')]
            self.port = os.environ[parser.get('POSTGRESQL','port')]
        else:
            self.host = parser.get('POSTGRESQL','host')
            self.port = parser.getint('POSTGRESQL','port')
            
        self.database = parser.get('POSTGRESQL','database')
        self.user = parser.get('POSTGRESQL','user')
        self.password = parser.get('POSTGRESQL','password')
        
    def __setup(self):
        '''
        Important stuff to do before we start working
        '''
        self.cur.execute('CREATE TABLE IF NOT EXISTS Articles(id serial, data text)')
        self.con.commit()
        
    def __connect(self):
        '''
        Connect to the database
        '''
        self.con = psycopg2.connect(host=self.host, port=self.port, database=self.database, user=self.user, password=self.password)
        self.cur = self.con.cursor()

class PostgresArticles(PostgresConnection):
    '''
    A class for handling articles
    '''
    def __init__(self, config='postgres.ini'):
        PostgresConnection.__init__(self, config)
        # Do stuff?
    
    def AddArticle(self, data):
        self.cur.execute("INSERT INTO Articles (data) VALUES(%s) RETURNING id", (data,))
        id = self.cur.fetchone()[0]
        self.con.commit()
        
        return id
        
    def GetArticle(self, id):
        
        self.cur.execute("SELECT * FROM Articles WHERE id=%s", (id,))
        data = self.cur.fetchone()[1]
        return data
        
def main():
    postgres = PostgresArticles()
    id = postgres.AddArticle(r"1) As you enter through the Shaded Woods door (after <producing the symbol of the King by wearing the King's Ring) on left is a corpse with Soul of a Nameless Soldier and Petrified Dragon Bone. To the right behind stairs in corner, is a corpse with Fire Seed. Another corpse near the tall grass has Poison Throwing Knife x10. There is a roaming pack of dogs in the tall grass that inflict bleed and petrification. In the grass is a corpse in with Alluring Skull x3. If you follow the ridge to the left you come across a mimic chest. Attack it and kill it to get Sunset Staff and Dark Mask. In a little wooden hut nearby is a the Foregarden bonfire. You may meet Lucatiel of Mirrah here, and if you kept her alive during three earlier boss fights, she will give you her sword and armor (Mirrah Greatsword, Lucatiel's Set).")

    print id
    
    print postgres.GetArticle(id)

if __name__ == "__main__":
    main()