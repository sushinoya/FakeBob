import sqlite3
from sqlite3 import Error


class Database:

    def __init__(self, databaseFile = "payBob.sqlite"):
        try:
            self.databaseFile = databaseFile
            self.conn = sqlite3.connect(databaseFile)
        except Error as e:
            print(e)


    def create_table(self, conn, create_table_statement):
        try:
            cursor = conn.cursor()
            cursor.execute(create_table_statement)
        except Error as e:
            print(e)

    def setup(self):

        self.makeUsersTable()
        self.makeReceiptsTable()
        self.makeTotalsTable()

    def makeUsersTable(self):
        makeUserandIDtable = """CREATE TABLE IF NOT EXISTS user (
                                id Integer PRIMARY KEY AUTOINCREMENT,
                                username Text NOT NULL UNIQUE,
                                chatID Integer NOT NULL UNIQUE
                            );"""
        self.create_table(self.conn, makeUserandIDtable)


    def makeReceiptsTable(self):
        makeReceipts = """CREATE TABLE IF NOT EXISTS receipt (
                            id Integer PRIMARY KEY AUTOINCREMENT,
                            payer Integer NOT NULL,
                            payee Integer NOT NULL,
                            description Text,
                            amount Float NOT NULL

                        );"""
        self.create_table(self.conn, makeReceipts)


    def makeTotalsTable(self):
        makeTotals = """CREATE TABLE IF NOT EXISTS total (
                                id Integer PRIMARY KEY AUTOINCREMENT,
                                payer Integer NOT NULL,
                                payee Integer NOT NULL,
                                amount Float NOT NULL
                    );"""
        self.create_table(self.conn, makeTotals)
#=============================== USER COMMANDS ================================#

    def addUser(self, username, chatId):
        addUser = "INSERT INTO user(username, chatID) VALUES (?, ?);"


        arguments = (username, chatId,)

        cursor = self.conn.cursor()
        cursor.execute(addUser, arguments)


    def getChatID(self, name):

        selectCommand = "SELECT chatID FROM user WHERE username=?"
        arguments = (name,)

        cursor = self.conn.cursor()
        cursor.execute(selectCommand, arguments)

        rows = cursor.fetchall()

        if rows != []:
            return rows[0][0]
        else:
            return None

    def getUsername(self, chatId):

        selectCommand = "SELECT username FROM user WHERE chatID=?"
        arguments = (chatId,)

        cursor = self.conn.cursor()
        cursor.execute(selectCommand, arguments)

        rows = cursor.fetchall()

        if rows != []:
            return rows[0][0]
        else:
            return None

    #selfHistory returns a list of [description, othersName, amount]
    #[description, othersName, amount(positive for receiving, negative for  giving)]
    def selfHistory(self, id):
         selectCommand = "SELECT * FROM receipt WHERE payer=? OR payee =? ORDER BY id"
         arguments = (id, id)

         cursor = self.conn.cursor()
         cursor.execute(selectCommand, arguments)

         rows = cursor.fetchall()
         list = []
         if rows != []:
             for row in rows:
                 if row[1] == id:
                     list.insert(row[3], row[2], row[4])

                 else:
                     amount = -row[4]
                     list.insert(row[3], row[1], amount)
         else:
             return None
#==============================================================================#


    def owesMoneyTo(self, payer, payee):

        findEntry = "SELECT amount FROM total WHERE payer=? AND payee=?"

        cursor = self.conn.cursor()
        arguments = (payer, payee)
        cursor.execute(findEntry, arguments)
        rows = cursor.fetchall()

        if rows != []:
            return rows[0][0]
        else:

            cursor = self.conn.cursor()
            arguments = (payee, payer)
            cursor.execute(findEntry, arguments)

            rows = cursor.fetchall()

            if rows != []:
                return -1 * rows[0][0]
            else:
                return 0

    def addEntryToTotals(self, payer, payee, amount):
        addCommand = "INSERT INTO total(payer, payee, amount) VALUES (?, ?, ?);"


        arguments = (payer, payee, amount)

        cursor = self.conn.cursor()
        cursor.execute(addCommand, arguments)



#==============================================================================#


def main():

    # TESTS
    db = Database()
    db.setup()
    db.addUser("Suyash", 231)
    print(db.getChatID("Suyash"))
    print(db.getUsername(231))
    print(db.getChatID("Suysdash"))
    print(db.getUsername(12223))
    db.addEntryToTotals("Suyash", "Haozhe", 396.23)
    print(db.owesMoneyTo("Suyash", "Haozhe"))
    print(db.owesMoneyTo("Haozhe", "Suyash"))
    print(db.owesMoneyTo("Shitian", "Suyash"))
    print(db.owesMoneyTo("Haozhe", "Junkai"))


if __name__ == '__main__':
    main()
