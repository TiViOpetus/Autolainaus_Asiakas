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

        # Yritetään avata yhteys tietokantaan ja lisätä tietue
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

    def addToTableWithNullableValues(self, table: str, data: dict) -> None:
        """Safe insert with NULL support"""
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()

            columns = list(data.keys())
            values = list(data.values())

            columnString = ", ".join(columns)
            placeholderString = ", ".join(["%s"] * len(values))

            sqlClause = f"""
            INSERT INTO {table} ({columnString})
            VALUES ({placeholderString})
            """

            cursor.execute(sqlClause, values)
            currentConnection.commit()

        except (Exception, psycopg2.Error) as e:
            raise e

        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    def _pickFirstPayloadValue(self, payload: dict, *keys):
        """Returns the first non-empty value found from a payload."""
        for key in keys:
            value = payload.get(key)
            if value is not None and value != '':
                return value
        return None

    def _jsonValueForDatabase(self, value):
        """Serializes nested JSON values to text so they can be stored safely."""
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False)
        return value

    def readTableColumns(self, table: str) -> list:
        """Returns table column names in physical order."""
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()

            sqlClause = """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
            """

            cursor.execute(sqlClause, (table,))
            records = cursor.fetchall()
            return [row[0] for row in records]

        except (Exception, psycopg2.Error) as e:
            raise e

        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    def _next_paikkatietoid(self) -> int:
        """Returns next paikkatietoid value by taking max+1 from web_paikkatieto.
        This is a best-effort fallback for schemas that require an explicit
        paikkatietoid and do not provide a sequence/default.
        """
        currentConnection = None
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()
            cursor.execute('SELECT COALESCE(MAX(paikkatietoid), 0) + 1 FROM public.web_paikkatieto;')
            row = cursor.fetchone()
            return int(row[0]) if row and row[0] is not None else 1
        except (Exception, psycopg2.Error) as e:
            raise e
        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    def readTableColumnMetadata(self, table: str) -> dict:
        """Returns a dict of column metadata: is_nullable, data_type, column_default."""
        currentConnection = None
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()
            sqlClause = """
            SELECT column_name, is_nullable, data_type, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            """
            cursor.execute(sqlClause, (table,))
            records = cursor.fetchall()
            return {row[0]: {'is_nullable': row[1], 'data_type': row[2], 'column_default': row[3]} for row in records}
        except (Exception, psycopg2.Error) as e:
            raise e
        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    def getOpenLoanNumberByRegistration(self, registrationNumber: str):
        """Fetches the active loan number for a registration number."""
        currentConnection = None
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()
            sqlClause = """
            SELECT lainausnumero
            FROM lainaus
            WHERE palautusaika IS NULL AND rekisterinumero = %s
            """
            cursor.execute(sqlClause, (registrationNumber,))
            row = cursor.fetchone()
            return None if row is None else row[0]

        except (Exception, psycopg2.Error) as e:
            raise e

        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    def setLoanReturnTimestamp(self, loanNumber):
        """Sets the return timestamp for a loan number."""
        currentConnection = None
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()
            sqlClause = """
            UPDATE public.lainaus
            SET palautusaika = CURRENT_TIMESTAMP
            WHERE lainausnumero = %s
            """
            cursor.execute(sqlClause, (loanNumber,))
            currentConnection.commit()

            if cursor.rowcount == 0:
                raise ValueError('Palautusaikaa ei paivitetty, lainausta ei loytynyt')

        except (Exception, psycopg2.Error) as e:
            raise e

        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    def insertWebPaikkatietoData(
        self,
        loanNumber,
        a_kaupunki,
        a_katu,
        a_katunumero,
        b_kaupunki,
        b_katu,
        b_katunumero,
        alku_km,
        loppu_km,
    ):
        """Inserts route/location data into web_paikkatieto."""
        currentConnection = None
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()
            sqlClause = """
            INSERT INTO public.web_paikkatieto(
                lainausnumero,
                a_kaupunki,
                a_katu,
                a_katunumero,
                b_kaupunki,
                b_katu,
                b_katunumero,
                alku_km,
                loppu_km
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                sqlClause,
                (
                    loanNumber,
                    a_kaupunki,
                    a_katu,
                    a_katunumero,
                    b_kaupunki,
                    b_katu,
                    b_katunumero,
                    alku_km,
                    loppu_km,
                ),
            )
            currentConnection.commit()

        except (Exception, psycopg2.Error) as e:
            raise e

        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    # Compatibility wrappers for older user.py API
    def getNotReturnedId(self, registrationNumber: str):
        """Compatibility wrapper: returns active loan id for registration."""
        return self.getOpenLoanNumberByRegistration(registrationNumber)

    def setReturnTimestamp(self, loanNumber):
        """Compatibility wrapper: sets return timestamp for a loan."""
        return self.setLoanReturnTimestamp(loanNumber)

    def addTrip(self, tripData: dict):
        """Compatibility wrapper: tries to insert a trip dict into web_paikkatieto.

        Uses a safe insert that supports NULLs; falls back to field-by-field
        insert if necessary.
        """
        try:
            self.addToTableWithNullableValues('web_paikkatieto', tripData)
            return
        except Exception:
            # Fallback: try inserting using the more explicit insert method
            loanNumber = tripData.get('lainausnumero')
            self.insertWebPaikkatietoData(
                loanNumber,
                tripData.get('a_kaupunki'),
                tripData.get('a_katu'),
                tripData.get('a_katunumero'),
                tripData.get('b_kaupunki'),
                tripData.get('b_katu'),
                tripData.get('b_katunumero'),
                tripData.get('alku_km'),
                tripData.get('loppu_km'),
            )

    def getActiveLoanNumberForReturn(self, registrationNumber: str):
        """Returns active loan number for a registration number, or None."""
        currentConnection = None
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()
            sqlClause = """
            SELECT lainausnumero
            FROM lainaus
            WHERE rekisterinumero = %s
            AND palautusaika IS NULL
            ORDER BY lainausnumero DESC
            LIMIT 1
            """
            cursor.execute(sqlClause, (registrationNumber,))
            row = cursor.fetchone()
            if row is None:
                return None
            return row[0]

        except (Exception, psycopg2.Error) as e:
            raise e

        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    def getLatestLoanNumberForRegistration(self, registrationNumber: str):
        """Returns the most recent loan number for a registration, regardless of return timestamp."""
        currentConnection = None
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()
            sqlClause = """
            SELECT lainausnumero
            FROM lainaus
            WHERE rekisterinumero = %s
            ORDER BY lainausnumero DESC
            LIMIT 1
            """
            cursor.execute(sqlClause, (registrationNumber,))
            row = cursor.fetchone()
            return None if row is None else row[0]
        except (Exception, psycopg2.Error) as e:
            raise e
        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    def updateReturnTimestampForLoan(self, loanNumber):
        """Sets return timestamp for one active loan row by loan number."""
        currentConnection = None
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()
            sqlClause = """
            UPDATE lainaus
            SET palautusaika = CURRENT_TIMESTAMP
            WHERE lainausnumero = %s
            AND palautusaika IS NULL
            """
            cursor.execute(sqlClause, (loanNumber,))
            currentConnection.commit()

            if cursor.rowcount == 0:
                raise ValueError('Palautusaikaa ei paivitetty, lainausta ei loytynyt tai se on jo palautettu')

        except (Exception, psycopg2.Error) as e:
            raise e

        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

    def saveWebPaikkatietoData(self, registrationNumber: str, loanNumber, locationData) -> bool:
        """Maps and saves location payload into web_paikkatieto when possible."""
        tableColumns = self.readTableColumns('web_paikkatieto')
        if not tableColumns:
            return False

        data = {}

        if 'lainausnumero' in tableColumns:
            data['lainausnumero'] = loanNumber

        if 'rekisterinumero' in tableColumns:
            data['rekisterinumero'] = registrationNumber

        payload = self._extractLatestTripPayload(locationData)

        if isinstance(payload, dict):
            routeStartPosition = self._pickFirstPayloadValue(
                payload,
                'routeStartPosition',
                'route_start_position',
                'startPosition',
                'start_position',
                'routeStart',
            )
            routesStopPosition = self._pickFirstPayloadValue(
                payload,
                'routesStopPosition',
                'routes_stop_position',
                'stopPosition',
                'stop_position',
                'routeStopPosition',
                'route_stop_position',
            )

            if 'mista' in tableColumns:
                data['mista'] = (
                    payload.get('mista')
                    or payload.get('from')
                    or payload.get('origin')
                    or payload.get('startAddress')
                    or payload.get('start_location')
                    or payload.get('originAddress')
                )
            if 'mihin' in tableColumns:
                data['mihin'] = (
                    payload.get('mihin')
                    or payload.get('to')
                    or payload.get('destination')
                    or payload.get('endAddress')
                    or payload.get('end_location')
                )
            if 'routeStartPosition' in tableColumns:
                data['routeStartPosition'] = self._jsonValueForDatabase(routeStartPosition)
            if 'route_start_position' in tableColumns:
                data['route_start_position'] = self._jsonValueForDatabase(routeStartPosition)
            if 'routesStopPosition' in tableColumns:
                data['routesStopPosition'] = self._jsonValueForDatabase(routesStopPosition)
            if 'routes_stop_position' in tableColumns:
                data['routes_stop_position'] = self._jsonValueForDatabase(routesStopPosition)
            if 'mista' in tableColumns and 'mista' not in data:
                data['mista'] = self._jsonValueForDatabase(routeStartPosition)
            if 'mihin' in tableColumns and 'mihin' not in data:
                data['mihin'] = self._jsonValueForDatabase(routesStopPosition)
            # Odometer / distance fields - support both camelCase and snake_case
            drive_start = (
                payload.get('driveStartOdo')
                or payload.get('startOdometer')
                or payload.get('odometerStart')
                or payload.get('alku_km')
                or payload.get('startKm')
            )
            drive_stop = (
                payload.get('driveStopOdo')
                or payload.get('endOdometer')
                or payload.get('odometerEnd')
                or payload.get('loppu_km')
                or payload.get('endKm')
            )
            drive_length = (
                payload.get('driveLenght')
                or payload.get('driveLength')
                or payload.get('distanceKm')
                or payload.get('distance')
                or payload.get('tripDistanceKm')
                or payload.get('matka_km')
            )
            if 'driveStartOdo' in tableColumns:
                data['driveStartOdo'] = drive_start
            if 'drive_start_odo' in tableColumns:
                data['drive_start_odo'] = drive_start
            if 'driveStopOdo' in tableColumns:
                data['driveStopOdo'] = drive_stop
            if 'drive_stop_odo' in tableColumns:
                data['drive_stop_odo'] = drive_stop
            if 'driveLenght' in tableColumns:
                data['driveLenght'] = drive_length
            if 'drive_length' in tableColumns:
                data['drive_length'] = drive_length
            if 'lahtoaika' in tableColumns:
                data['lahtoaika'] = (
                    payload.get('lahtoaika')
                    or payload.get('startTime')
                    or payload.get('fromTime')
                    or payload.get('tripStart')
                    or payload.get('departureTime')
                    or payload.get('startedAt')
                )
            if 'saapumisaika' in tableColumns:
                data['saapumisaika'] = (
                    payload.get('saapumisaika')
                    or payload.get('endTime')
                    or payload.get('toTime')
                    or payload.get('tripEnd')
                    or payload.get('arrivalTime')
                    or payload.get('endedAt')
                )
            if 'matka_km' in tableColumns:
                data['matka_km'] = (
                    payload.get('matka_km')
                    or payload.get('distanceKm')
                    or payload.get('distance')
                    or payload.get('tripDistanceKm')
                )
            if 'matkamittarialussa' in tableColumns:
                data['matkamittarialussa'] = (
                    payload.get('matkamittarialussa')
                    or payload.get('alku_km')
                    or payload.get('startKm')
                    or payload.get('odometerStart')
                    or payload.get('startOdometer')
                )
            if 'matkamittarilopussa' in tableColumns:
                data['matkamittarilopussa'] = (
                    payload.get('matkamittarilopussa')
                    or payload.get('loppu_km')
                    or payload.get('endKm')
                    or payload.get('odometerEnd')
                    or payload.get('endOdometer')
                )
            if 'alku_km' in tableColumns:
                data['alku_km'] = (
                    payload.get('alku_km')
                    or payload.get('startKm')
                    or payload.get('odometerStart')
                    or payload.get('startOdometer')
                )
            if 'loppu_km' in tableColumns:
                data['loppu_km'] = (
                    payload.get('loppu_km')
                    or payload.get('endKm')
                    or payload.get('odometerEnd')
                    or payload.get('endOdometer')
                )
            if 'paikkatietoid' in tableColumns:
                data['paikkatietoid'] = (
                    payload.get('paikkatietoid')
                    or payload.get('id')
                    or payload.get('paikkatieto_id')
                )
            if 'a_kaupunki' in tableColumns:
                data['a_kaupunki'] = payload.get('a_kaupunki') or payload.get('startCity') or payload.get('fromCity')
            if 'a_katu' in tableColumns:
                data['a_katu'] = payload.get('a_katu') or payload.get('startStreet') or payload.get('fromStreet')
            if 'a_katunumero' in tableColumns:
                data['a_katunumero'] = payload.get('a_katunumero') or payload.get('startStreetNumber') or payload.get('fromStreetNumber')
            if 'akaupunki' in tableColumns:
                data['akaupunki'] = (
                    payload.get('akaupunki')
                    or payload.get('a_kaupunki')
                    or payload.get('startCity')
                    or payload.get('fromCity')
                )
            if 'akatu' in tableColumns:
                data['akatu'] = (
                    payload.get('akatu')
                    or payload.get('a_katu')
                    or payload.get('startStreet')
                    or payload.get('fromStreet')
                )
            if 'akatunumero' in tableColumns:
                data['akatunumero'] = (
                    payload.get('akatunumero')
                    or payload.get('a_katunumero')
                    or payload.get('startStreetNumber')
                    or payload.get('fromStreetNumber')
                )
            if 'b_kaupunki' in tableColumns:
                data['b_kaupunki'] = payload.get('b_kaupunki') or payload.get('endCity') or payload.get('toCity')
            if 'b_katu' in tableColumns:
                data['b_katu'] = payload.get('b_katu') or payload.get('endStreet') or payload.get('toStreet')
            if 'b_katunumero' in tableColumns:
                data['b_katunumero'] = payload.get('b_katunumero') or payload.get('endStreetNumber') or payload.get('toStreetNumber')
            if 'bkaupunki' in tableColumns:
                data['bkaupunki'] = (
                    payload.get('bkaupunki')
                    or payload.get('b_kaupunki')
                    or payload.get('endCity')
                    or payload.get('toCity')
                )
            if 'bkatu' in tableColumns:
                data['bkatu'] = (
                    payload.get('bkatu')
                    or payload.get('b_katu')
                    or payload.get('endStreet')
                    or payload.get('toStreet')
                )
            if 'bkatunumero' in tableColumns:
                data['bkatunumero'] = (
                    payload.get('bkatunumero')
                    or payload.get('b_katunumero')
                    or payload.get('endStreetNumber')
                    or payload.get('toStreetNumber')
                )

        if 'raaka_json' in tableColumns:
            data['raaka_json'] = json.dumps(locationData, ensure_ascii=False)
        elif 'raw_json' in tableColumns:
            data['raw_json'] = json.dumps(locationData, ensure_ascii=False)

        # Ensure required paikkatietoid exists for schemas that enforce NOT NULL
        if 'paikkatietoid' in tableColumns and ('paikkatietoid' not in data or data.get('paikkatietoid') is None):
            try:
                data['paikkatietoid'] = self._next_paikkatietoid()
            except Exception:
                # If we cannot generate one, leave it to the DB (may fail)
                pass

        # Read column metadata to supply defaults for NOT NULL columns without defaults
        try:
            metadata = self.readTableColumnMetadata('web_paikkatieto')
        except Exception:
            metadata = {}

        for col in tableColumns:
            colmeta = metadata.get(col)
            if not colmeta:
                continue
            is_nullable = colmeta.get('is_nullable')
            col_default = colmeta.get('column_default')
            data_type = colmeta.get('data_type')

            if is_nullable == 'NO' and col_default is None and (col not in data or data.get(col) is None):
                # Supply a conservative default based on data type
                if data_type in ('integer', 'bigint', 'smallint', 'numeric', 'real', 'double precision'):
                    data[col] = 0
                elif data_type in ('timestamp without time zone', 'timestamp with time zone', 'date', 'time'):
                    try:
                        data[col] = self.getPgTimestamp()
                    except Exception:
                        data[col] = ''
                else:
                    data[col] = ''

        filtered = {key: value for key, value in data.items() if key in tableColumns}
        if not filtered:
            return False

        self.addToTableWithNullableValues('web_paikkatieto', filtered)
        return True

    def _extractLatestTripPayload(self, locationData):
        """Returns the most relevant trip payload from API wrapper structures."""
        payload = locationData

        if isinstance(locationData, str):
            payload = json.loads(locationData)

        if isinstance(payload, list):
            for item in reversed(payload):
                if isinstance(item, dict):
                    return item
            return payload[-1] if payload else payload

        if isinstance(payload, dict):
            candidateKeys = (
                'routes',
                'trips',
                'data',
                'items',
                'results',
                'payload',
                'history',
            )

            for key in candidateKeys:
                nestedValue = payload.get(key)
                if isinstance(nestedValue, list) and nestedValue:
                    for item in reversed(nestedValue):
                        if isinstance(item, dict):
                            return item
                    return nestedValue[-1]
                if isinstance(nestedValue, dict):
                    return nestedValue

        return payload

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
    # TODO: Muokkaa tätä, siten että saadaan toinen ehto, siitä että palautusaika pitää olla tyhjä!
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

    def updateReturnTimeStampByLoanNumber(self, table: str, column: str, criteriaColumn: str, criteriaValue):
        """Updates return timestamp using loan number safely"""
        try:
            currentConnection = psycopg2.connect(self.connectionString)
            cursor = currentConnection.cursor()

            sqlClause = f"""
            UPDATE {table}
            SET {column} = CURRENT_TIMESTAMP
            WHERE {criteriaColumn} = %s
            AND {column} IS NULL
            """

            cursor.execute(sqlClause, (criteriaValue,))
            currentConnection.commit()

        except (Exception, psycopg2.Error) as e:
            raise e

        finally:
            if currentConnection:
                cursor.close()
                currentConnection.close()

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
            registernumber (str) A: registernumber of vehicle to be returned
        """
        return self.getActiveLoanNumberForReturn(registernumber)
        
    def setReturnTimestamp(self, lendingID):
        """Set the timestamp of the returned vehicle

        Args:
            lendingId (int): Id for a lending event
        """
        self.updateReturnTimestampForLoan(lendingID)

    def addTrip(self, tripData):
        """Updates spatial information from JSON data to a table

        Args:
            tripData (json): JSN object containing place and odometer data
        """
        if tripData is None:
            raise ValueError('tripData is missing')

        payload = tripData
        if isinstance(tripData, str):
            payload = json.loads(tripData)

        if isinstance(payload, list):
            if len(payload) == 0:
                raise ValueError('tripData list is empty')
            payload = payload[-1]

        if not isinstance(payload, dict):
            raise ValueError('tripData must be a JSON object or an array containing objects')

        loanNumber = (
            payload.get('lainausnumero')
            or payload.get('loanNumber')
            or payload.get('lendingID')
            or payload.get('lendingId')
        )

        if loanNumber is None:
            raise ValueError('tripData does not contain loan number (lainausnumero)')

        routeValues = [
            payload.get('a_kaupunki'),
            payload.get('a_katu'),
            payload.get('a_katunumero'),
            payload.get('b_kaupunki'),
            payload.get('b_katu'),
            payload.get('b_katunumero'),
            payload.get('alku_km'),
            payload.get('loppu_km'),
        ]

        if all(value is None for value in routeValues):
            raise ValueError('tripData does not contain legacy route fields for web_paikkatieto')

        self.insertWebPaikkatietoData(
            loanNumber,
            payload.get('a_kaupunki'),
            payload.get('a_katu'),
            payload.get('a_katunumero'),
            payload.get('b_kaupunki'),
            payload.get('b_katu'),
            payload.get('b_katunumero'),
            payload.get('alku_km'),
            payload.get('loppu_km'),
        )

    # Haetaan osaston vapaat ajoneuvot
    def getVehiclesFree(self, department):
        sqlClause = f"SELECT rekisterinumero, merkki, malli, automaatti, henkilomaara FROM public.vapaana WHERE osasto = '{department}'"
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
    def getVehiclesInUse(self, department):
        sqlClause = f"SELECT rekisterinumero, merkki, malli, automaatti, henkilomaara, kuljettaja FROM public.ajossa WHERE osasto = '{department}'"
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


if __name__ == "__main__":

    settingsDictionary = {'server': 'localhost',
                      'port': '5433',
                      'database': 'autolainaus',
                      'userName': 'postgres',
                      'password': 'Q2werty'}
    dbconnection = DbConnection(settingsDictionary)

    # data = dbconnection.getNotReturnedID('FPB-343')
    # dbconnetion.setReturnedTimestamp(data)
    data = dbconnection.getVehiclesFree('Auto')
    print('vapaana:', data)
    data2 = dbconnection.getVehiclesInUse('Auto')

