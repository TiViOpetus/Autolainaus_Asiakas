"""A module to connect to a PostgreSQL database and do basic CRUD-operations (Create, Read, Update and Delete)
"""
# MODUULI POSTGRESQL TIETOKANTAPALVELIMEN KÄYTTÄMISEEN
# ====================================================

# KIRJASTOT JA MODUULIT
# ---------------------

# Ladattavat kirjastot
import psycopg2 # PostgreSQL-ajuri
import datetime
import json

# LUOKAT
# ------

class DbConnection():
    """A class to crate PostgreSQL Database connections and various data operations"""
    
    # Konstruktori
    def __init__(self, settings: dict):
        self.server = settings['server']
        self.port = settings['port']
        self.databaseName = settings['database']
        self.userName = settings['userName']
        self.password = settings['password']

        # Yhteysmerkkijono
        self.connectionString =f'dbname={self.databaseName} user={self.userName} password={self.password} host={self.server} port={self.port}'
        
    # Metodi tietojen lisäämiseen (INSERT)
    def addToTable(self, table: str, data: dict) -> None:
        """Inserts a record (row) to a table according to a dictionary
        containing field names (columns) as keys and values

        Args:
            table (str): Name of the table
            data (dict): Field names and values
        """

        # Muodostetaan lista sarakkeiden (kenttien) nimistä ja arvoista SQL laustetta varten
        keys = data.keys() # Luetaan sanakirjan avaimet
        columns = '' # SQL-lauseeseen tarvittava sarakemerkkijono
        values = '' # SQL-lauseen arvot merkkijonona

        # Luetaan kaikki avaimet sekä arvot ja lisätään ne listoihin
        for key in keys:
            columns += key + ', ' # Lisätään pilkku
            rawValue = data[key] # Luetaan sanakirjan arvo

            # Lisätään puolilainausmerkit, jos kyseessä on merkkijono
            if isinstance(rawValue, str):
                value = f'\'{rawValue}\'' # \' mahdollistaa puolilainausmerkin lisäämisen
            else:
                value = f'{rawValue}'
            values += value + ', ' # Lisätään arvo sekä pilkku ja välilyönti

        # Poistetaan sarakkeista ja arvoista viimeinen pilkku ja välilyönti
        columns = columns[:-2]
        values = values[:-2]


        # Yritetään avata yhteys tietokantaan ja lisätä tietue
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään lopullinen SQL-lause
            sqlClause = f'INSERT INTO {table} ({columns}) VALUES ({values})'
            
            # Suoritetaan SQL-lause
            cursor.execute(sqlClause)

            # Vahvistetaan tapahtuma (transaction)
            currentConnection.commit()

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys
                
    # Tee metodi tietojen lukemiseen, taulun kaikki sarakkeet
    def readAllColumnsFromTable(self, table: str) -> list | None:
        """Returns all columns and rows from a table

        Args:
            table (str): Name of the table

        Returns:
            list: List of tuples. One tuple contains a row
        """
        records = []
        # Yritetään avata yhteys tietokantaan ja lisätä tietue
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään lopullinen SQL-lause
            sqlClause = f'SELECT * FROM {table}'
            
            # Suoritetaan SQL-lause
            cursor.execute(sqlClause)

            records= cursor.fetchall()

            return records

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys
        
    # Metodi tietojen lukemiseen, taulun valitut sarakkeet
    def readColumsFromTable(self, table: str, columns: list) -> list:
        """Returns all rows from a table. Columns are defined for the result set

        Args:
            table (str): Name of the table
            colums (list): Column names to include in the result set

        Returns:
            list: List of tuples. One tuple contains a row
        """

        # Yritetään avata yhteys tietokantaan ja luetaan tietueet
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Muodostetaan sarakelistasta merkkijono
            columnString = ''
            for column in columns:
                columnString = columnString + str(column) + ', '
                
            cleanedColumnString = columnString[:-2] # Poistetaan lopusta pilkku ja välilyönti
            
            # Määritellään lopullinen SQL-lause
            sqlClause = f'SELECT {cleanedColumnString} FROM {table}'

            # Suoritetaan SQL-lause ja luetaan tulokset kursorista
            cursor.execute(sqlClause)
            records= cursor.fetchall()
            return records

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

    # Metodi, jolla hetaan ehdot täyttävät rivit taulusta
    # Metodi tietojen lukemiseen, taulun valitut sarakkeet
    def filterColumsFromTable(self, table: str, columns: list, filter:str) -> list:
        """Filters data from table or viwe according to filter string

        Args:
            table (str): Name of the table or view
            columns (list): Columns to include into a resultset
            filter (str): SQL code for the WHERE clause

        Raises:
            e: an error message generated by driver or database

        Returns:
            list: The resultset as list of tuples
        """

        # Yritetään avata yhteys tietokantaan ja hakea tiedot
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Muodostetaan sarakelistasta merkkijono
            columnString = ''
            for column in columns:
                columnString = columnString + str(column) + ', '
                
            cleanedColumnString = columnString[:-2] # Poistetaan lopusta pilkku ja välilyönti
            
            # Määritellään lopullinen SQL-lause
            sqlClause = f'SELECT {cleanedColumnString} FROM {table} WHERE {filter};'
            # Suoritetaan SQL-lause ja luetaan tulokset kursorista
            cursor.execute(sqlClause)
            records= cursor.fetchall()
            return records

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

    # Metodi, joka hakee tietokantapalvelimen aikaleiman
    def getPgTimestamp(self) -> str:
        """Reads PostgreSQL server's current timestamp and converts it to
        ISO date and time string

        Raises:
            e: An error message to propagate

        Returns:
            str: Date, time and timezone in ISO format
        """

        # Yritetään avata yhteys tietokantaan ja hakea tiedot
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään SQL lause, joka palauttaa aikaleiman ja aikavyöhykkeen 
            sqlClause = f'SELECT CURRENT_TIMESTAMP;'

            # Suoritetaan SQL-lause ja luetaan tulokset kursorista
            cursor.execute(sqlClause)
            records= cursor.fetchall()
            row = records[0] # Listasta monikko (tuple)
            column = row[0] # Monikosta arvo, joka tulee funktion tuottamana
            isoDateTime = f'{column}' # Arvo merkkijonoksi muutettuna
            return isoDateTime

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

    # Metodi tietojen muokkaamiseen, yksittäinen sarake
    def modifyTableData(self, table: str, column: str, newValue, criteriaColumn: str, criteriaValue):
        """Updataes a column according to a filtering criteria

        Args:
            table (str): Name of the table
            column (str): Name of the column to be updated
            newValue (any): The new value for the column
            criteriaColumn (str): A column to use in WHERE-claus
            criteriaValue (any): The value of criteria colunm

        Raises:
            e: Error message to be propagated

        """
        # Yritetään avata yhteys tietokantaan ja päivittää tietueita
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään lopullinen SQL-lause
            sqlClause = f'UPDATE {table} SET  {column} = {newValue} WHERE {criteriaColumn} = {criteriaValue}'

            # Suoritetaan SQL-lause
            cursor.execute(sqlClause)

            # Vahvistetaan tapahtuma (transaction)
            currentConnection.commit()

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

    def updateReturnTimeStamp(self, table: str, column: str,criteriaColumn: str, criteriaValue):
        """Updataes a column according to a filtering criteria

        Args:
            table (str): Name of the table
            column (str): Name of the column to be updated
            newValue (any): The new value for the column
            criteriaColumn (str): A column to use in WHERE-claus
            criteriaValue (any): The value of criteria colunm

        Raises:
            e: Error message to be propagated

        """
        # Yritetään avata yhteys tietokantaan ja päivittää tietueita
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään lopullinen SQL-lause
            sqlClause = f'UPDATE {table} SET {column} = CURRENT_TIMESTAMP WHERE {column} IS NULL AND {criteriaColumn} = {criteriaValue}'

            # Suoritetaan SQL-lause
            cursor.execute(sqlClause)

            # Vahvistetaan tapahtuma (transaction)
            currentConnection.commit()

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

    # 
    # Päivitetään taulun binäärisaraketta          
    def updateBinaryField(self, table: str, column: str, criteriaColumn: str, criteriaValue, data):
        """Updates a given bytea column in a table accordinto to a criteria

        Args:
            table (str): Name of the table to update
            column (str): Name of the column to updata
            criteriaColumn (str): Name of the column used to filter rows
            criteriaValue: Value of the filtering criteria
            data: Binary data to update with
        """
        # Yritetään avata yhteys tietokantaan ja päivittää tietueita
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään lopullinen SQL-lause, paikkamerkki %s korvautuu binääritiedolla
            sqlClause = f'UPDATE {table} SET  {column} = %s WHERE {criteriaColumn} = {criteriaValue}'

            # Suoritetaan SQL-lause ja lisätään data monikkona
            cursor.execute(sqlClause, (data,))

            # Vahvistetaan tapahtuma (transaction)
            currentConnection.commit()

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys


    # Metodi tietueen poistamiseen
    def deleteRowsFromTable(self, table, criteriaColumn, criteriaValue):
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään lopullinen SQL-lause, paikkamerkki %s korvautuu binääritiedolla
            sqlClause = f'DELETE FROM {table} WHERE {criteriaColumn} = {criteriaValue}'
            
            # Suoritetaan SQL-lause ja lisätään data monikkona
            cursor.execute(sqlClause)

            # Vahvistetaan tapahtuma (transaction)
            currentConnection.commit()

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys


    def getNotReturnedId(self, registernumber):
        """Retrieves a lending id of a vehicle not returned by registernumber

        Args:
            registernumber (str): The registernumber of vehicle to be returned
        """        
        # Yritetään avata yhteys tietokantaan ja hakea tiedot
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään lopullinen SQL-lause
            sqlClause = f"SELECT lainausnumero FROM public.lainaus WHERE rekisterinumero = '{registernumber}' AND palautusaika IS NULL"

            cursor.execute(sqlClause)
            record= cursor.fetchone()
            lendingId = record[0]
            return lendingId

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys
    
    
    
    def getSettingsValue(self, key):
        """Get a setting value from database

        Args:
            key (str): Key for the setting to get

        Returns:
            str: Value for the setting
        """        
        # Yritetään avata yhteys tietokantaan ja hakea tiedot
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään lopullinen SQL-lause
            sqlClause = f"SELECT arvo FROM public.asetus WHERE avain = '{key}'"

            cursor.execute(sqlClause)
            record= cursor.fetchone()
            value = record[0]
            return value

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys
    
    
    def getTimestamps(self, lendingId):
        """Reads starting and ending timestamps for a given lending ID

        Args:
            lendingId (int): ID of lending transaction

        Raises:
            e: Database or OS error

        Returns:
            dict: Dictionary containine start and end times in ISO-format
        """        
        # Yritetään avata yhteys tietokantaan ja päivittää tietueita
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()

            # Määritellään lopullinen SQL-lause
            sqlClause = f"SELECT lainausaika, palautusaika FROM public.lainaus WHERE lainausnumero = '{lendingId}'"

            cursor.execute(sqlClause)
            timeStampsRaw = cursor.fetchone()
            startTime = timeStampsRaw[0].isoformat()[:19] + 'Z'
            endTime = timeStampsRaw[1].isoformat()[:19] + 'Z'
            timeStamps = {'startTime': startTime, 'endTime': endTime}
            return timeStamps

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys


    def setReturnTimestamp(self, lendingId):
        """Set the lend ending timestamp for a returned vehicle

        Args:
            lendingId (int): Id for a lending event
        """  
        sqlClause = f"UPDATE public.lainaus SET palautusaika = CURRENT_TIMESTAMP WHERE lainausnumero = {lendingId}"      
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()
            cursor.execute(sqlClause)

            # Vahvistetaan tapahtuma (transaction)
            currentConnection.commit()

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys


    def addTrip(self, lendingId, tripData):
        """Updates spatial information from trip's JSON data to a table

        Args:
            lendingId (int): Reference to lending transaction
            tripData (dict): Dictionary containing place and odometer data
        """        
        
        
        # Määritellään SQL-lause yksittäisen matkan osan tallentamiseksi
        sqlClause = f"INSERT INTO public.ajon_paikat( lainausnumero, mista, mihin, amml, lmml) VALUES ({lendingId}, '{tripData['fromField']}', '{tripData['toField']}', {tripData['startOdo']}, {tripData['stopOdo']}"


        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()
            cursor.execute(sqlClause)

            # Vahvistetaan tapahtuma (transaction)
            currentConnection.commit()

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

    def getDeviceId(self, registerNumber):
        """Retrieves paikannin.com's device ID from auto-taulu (vehicle)

        Args:
            registerNumber (str): Register number of the vehicle

        Returns:
            int: Device ID for a vehicle
        """        
        sqlClause = f"SELECT deviceid FROM public.auto WHERE rekisterinumero = '{registerNumber}'"

        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()
            cursor.execute(sqlClause)
            result = cursor.fetchone()
            deviceId = result[0]
            return deviceId

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

    # Haetaan osaston vapaat ajoneuvot
    def getVehiclesFree(self, division):
        sqlClause = f"SELECT rekisterinumero, merkki, malli, automaatti, henkilomaara FROM public.vapaana WHERE osasto = '{division}'"
        # Yritetään avata yhteys tietokantaan ja hakea tiedot
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()
         # Suoritetaan SQL-lause ja luetaan tulokset kursorista
            cursor.execute(sqlClause)
            records= cursor.fetchall()
            return records

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys
       
    # Haetaan osaston ajossa olevat ajoneuvot
    def getVehiclesInUse(self, division):
        sqlClause = f"SELECT rekisterinumero, merkki, malli, automaatti, henkilomaara, kuljettaja FROM public.ajossa WHERE osasto = '{division}'"
        # Yritetään avata yhteys tietokantaan ja hakea tiedot
        try:
            # Luodaan yhteys tietokantaan
            currentConnection = psycopg2.connect(self.connectionString)

            # Luodaan kursori suorittamaan tietokantoperaatiota
            cursor = currentConnection.cursor()
         # Suoritetaan SQL-lause ja luetaan tulokset kursorista
            cursor.execute(sqlClause)
            records = cursor.fetchall()
            return records

        # Jos tapahtuu virhe, välitetään se luokkaa käyttävälle ohjelmalle
        except (Exception, psycopg2.Error) as e:
            raise e 
        
        finally:

            # Selvitetään muodostuiko yhteysolio
            if currentConnection:
                cursor.close() # Tuhotaan kursori
                currentConnection.close() # Tuhotaan yhteys

if __name__ == "__main__":

    settingsDictionary = {'server': 'localhost',
                      'port': '5432',
                      'database': 'autolainaus',
                      'userName': 'postgres',
                      'password': 'Q2werty7'}
    dbconnection = DbConnection(settingsDictionary)

    # data = dbconnection.getNotReturnedId('FPB-343')
    # dbconnection.setReturnTimestamp(data)
    # data = dbconnection.getVehiclesFree('Auto')
    # print('Vapaana:', data)
    # data2 = dbconnection.getVehiclesInUse('Auto')
    # print('Ajossa:', data2)
    timeStamps = dbconnection.getTimestamps(20)
    print(timeStamps)
