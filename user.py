# PYSIDE6-MALLINE SOVELLUKSEN PÄÄIKKUNAN LUOMISEEN
# KÄÄNNETYSTÄ KÄYTTÖLIITTYMÄTIEDOSTOSTA (mainWindow_ui.py)
# =====================================================

# KIRJASTOJEN JA MODUULIEN LATAUKSET
# ----------------------------------
import os # Polkumääritykset
import sys # Käynnistysargumentit
import json # JSON-tiedostojen käsittely
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from PySide6 import QtWidgets # Qt-vimpaimet
from PySide6.QtCore import QThreadPool, Slot, Qt, QByteArray # Säikeistys, slot-dekoraattori ja Qt
from PySide6.QtGui import QPixmap, QCursor # Kuvan luku ja kursorin muutokset

from lendingModules import sound # Äänitoiminnot
from lendingModules import dbOperations # Tietokantatoiminnot

# mainWindow_ui:n tilalle käännetyn pääikkunan tiedoston nimi
# ilman .py-tiedostopäätettä
from user_ui import Ui_MainWindow # Käännetyn käyttöliittymän luokka

# Määritellään luokka, joka perii QMainWindow- ja Ui_MainWindow-luokan
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """A class for creating a main window for the application"""
    
    # Määritellään olionmuodostin ja kutsutaan yliluokkien muodostimia
    def __init__(self):
        super().__init__()

        # Luodaan säikeistystä varten uusi säievaranto
        self.threadPool = QThreadPool().globalInstance()

        # Luodaan käyttöliittymä konvertoidun tiedoston perusteella MainWindow:n ui-ominaisuudeksi. Tämä suojaa lopun MainWindow-olion ylikirjoitukselta, kun ui-tiedostoa päivitetään
        self.ui = Ui_MainWindow()

        # Kutsutaan käyttöliittymän muodostusmetodia setupUi
        self.ui.setupUi(self)
   
        # Load database settings from environment variables instead of settings.json
        try:
            self.currentSettings = {
                'server': os.getenv('DB_HOST', 'localhost'),
                'port': os.getenv('DB_PORT', '5432'),
                'database': os.getenv('DB', 'autolainaus'),
                'userName': os.getenv('DB_USER', 'autolainaus'),
                'password': os.getenv('DB_PLAIN_PASSWORD', ''),  # Using plain text from .env
                # Optional department filter (set by administrative settings)
                'department': os.getenv('DEPARTMENT') or os.getenv('OSASTO') or None,
                'paikanninApiUrl': os.getenv('PAIKANNIN_API_URL', 'https://app.paikannin.com'),
                'paikanninDeviceId': os.getenv('PAIKANNIN_DEVICE_ID', ''),
                'paikanninApiKey': os.getenv('PAIKANNIN_API_KEY', ''),
                'paikanninApiKeyHeader': os.getenv('PAIKANNIN_API_KEY_HEADER', 'Authorization'),
                'paikanninApiKeyPrefix': os.getenv('PAIKANNIN_API_KEY_PREFIX', 'Bearer '),
                'paikanninTimeoutSeconds': int(os.getenv('PAIKANNIN_TIMEOUT_SECONDS', '10')),
            }
            self.plainTextPassword = self.currentSettings['password']
            # Also accept department set in settings.json (admin UI may write here)
            try:
                settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
                if os.path.exists(settings_path):
                    with open(settings_path, 'r', encoding='utf-8') as sf:
                        file_settings = json.load(sf)
                        dept = file_settings.get('department') or file_settings.get('osasto')
                        if dept:
                            self.currentSettings['department'] = dept
            except Exception:
                # Ignore failures reading admin settings file; fallback to env
                pass
        
        except Exception as error:
            title = 'Ympäristömuuttujien luku ei onnistunut'
            text = 'Tietokanta-asetuksien avaaminen .env-tiedostosta ei onnistunut'
            detailedText = str(error)
            self.openWarning(title, text, detailedText)      

        self.defaultVehiclePicture = QPixmap('uiPictures\\defaultVehicles.png')

        # Ohjelman käynnistyksessä piilotetaan tarpeettomat elementit
        self.setInitialElements()


        # OHJELMOIDUT SIGNAALIT
        # ---------------------
        
        # Kun Lainaa-painiketta painetaan, kutsutaan activateReason-metodia
        self.ui.takeCarPushButton.clicked.connect(self.activateReason)

        # Kun ajon syy on valittu, kutsutaan activateLender-metodi
        self.ui.reasonComboBox.currentIndexChanged.connect(self.activateLender)

        # Kun ajokortin viivakoodi on luettu, kutsutaan activateKey-metodia
        self.ui.ssnLineEdit.returnPressed.connect(self.activateKey)
        
        # Kun avaimenperä on luettu, kutsutaan setLendingData-metodia
        self.ui.keyBarcodeLineEdit.returnPressed.connect(self.setLendingData)

        # Kun OK-painiketta on painettu, tallenna tiedot 
        # ja palauta käyttöliittymä alkutilaan
        self.ui.okPushButton.clicked.connect(self.saveLendingData)

        # Kun palauta-painiketta on painettu, kutsutaan activateReturnCar-metodia
        self.ui.returnCarPushButton.clicked.connect(self.activateReturnCar)

        # Kun avaimenperä on luettu palutettaessa, kutsutaan saveReturnData-metodia
        self.ui.keyReturnBarcodeLineEdit.returnPressed.connect(self.saveReturnData)
    
        # Kun mykistä painiketta painetaan, kutsutaan mute-metodia
        
        #self.ui.soundOffPushButton.clicked.connect(self.mute)

        # Kun äänipäiniketta painetaan, kutsutaan unmute-metodia
        #self.ui.soundOnPushButton.clicked.connect(self.unmute)

        # Kun kumoa painiketta painetaan palautetaan UI-alkutilaan
        self.ui.goBackPushButton.clicked.connect(self.goBack)
    
    # OHJELMOIDUT SLOTIT
    # ------------------
   
    # Soita parametrina annettu äänistiedosto (työfunktio)
    @Slot(str)
    def playSoundFile(self, soundFileName):
        fileAndPath = 'sounds\\' + soundFileName
        sound.playWav(fileAndPath)
    
    # Säikeen käynnistävä funktio 
    @Slot(str)
    def playSoundInTread(self, soundFileName):
        self.threadPool.start(lambda: self.playSoundFile(soundFileName))

    # Palauta käyttöliittymä alkutilanteeseen ja päivittää vapaiden ja 
    # ajossa olevien autojen katalogit
    @Slot()
    def setInitialElements(self):

        # Piilotetaan alkutilanteessa lainauksen ja palautuksen elementit
        self.ui.reasonComboBox.hide()
        self.ui.registerPlateBGLabel.hide()
        self.ui.registerPlateBGReturnLabel.hide()
        self.ui.okPushButton.hide()
        self.ui.calendarLabel.hide()
        self.ui.clockLabel.hide()
        self.ui.dateLabel.hide()
        self.ui.goBackPushButton.hide()
        self.ui.keyBarcodeLineEdit.hide()
        self.ui.keyReturnBarcodeLineEdit.hide()
        self.ui.keyPictureLabel.hide()
        self.ui.keyPictureReturnLabel.hide()
        self.ui.lenderPictureLabel.hide()
        self.ui.ssnLineEdit.hide()
        self.ui.statusLabel.hide()
        self.ui.timeLabel.hide()
        self.ui.lenderNameLabel.hide()
        self.ui.carInfoLabel.hide()

        # Näytetään alkutilanteen elementit
        self.ui.returnCarPushButton.show()
        self.ui.takeCarPushButton.show()
        self.ui.statusFrame.show()

        # Tyhjennetään syöttökentät
        self.ui.keyBarcodeLineEdit.clear()
        self.ui.keyReturnBarcodeLineEdit.clear()
        self.ui.ssnLineEdit.clear()
        self.ui.availablePlainTextEdit.clear()
        self.ui.inUsePlainTextEdit.clear()

        # Aktivoidaan tarvittavat painikkeet
        self.ui.okPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.ui.okPushButton.setEnabled(True)

        # Palautetaan auton oletuskuva
        self.ui.vehiclePictureLabel.setPixmap(self.defaultVehiclePicture)
        
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        try:
            # Luodaan tietokantayhteys-olio
            dbConnection = dbOperations.DbConnection(dbSettings)

            # Prefer DB-side helper if available (more robust SQL filtering)
            dept = self.currentSettings.get('department') or os.getenv('DEPARTMENT') or os.getenv('OSASTO')
            inUseVehicles = []
            if dept:
                try:
                    inUseVehicles = dbConnection.getVehiclesInUse(dept)
                except Exception:
                    inUseVehicles = self._readTableWithOptionalDepartmentFilter(dbConnection, 'ajossa')
            else:
                inUseVehicles = self._readTableWithOptionalDepartmentFilter(dbConnection, 'ajossa')

            # Alustetaan tyhjä lista muokattuja autotietoja varten
            modifiedInUseVehiclesList = []

            # Alustetaan tyhjä lista, jotta monikkoon voi tehdä muutoksia
            

            # Käydään lista läpi ja lisätään monikon alkiot listaan
            for vehicleTuple in inUseVehicles:
                modifiedInUseVehicles = []
                modifiedInUseVehicles.append(vehicleTuple[0])
                modifiedInUseVehicles.append(vehicleTuple[1])
                modifiedInUseVehicles.append(vehicleTuple[2])
                modifiedInUseVehicles.append(vehicleTuple[3])
                modifiedInUseVehicles.append(vehicleTuple[4])

                # Lisätään sana paikkaa
                modifiedInUseVehicles.append('paikkaa')
                modifiedInUseVehicles.append(vehicleTuple[5])

                # Muutetaan lista takaisin monikoksi
                modifiedInsUseVehicleTuple = tuple(modifiedInUseVehicles)

                # Lisätään monikko lopulliseen listaan
                modifiedInUseVehiclesList.append(modifiedInsUseVehicleTuple)   
                
            # Muodostetaan luettelo vapaista autoista createCatalog-metodilla
            catalogData = self.createCatalog(modifiedInUseVehiclesList)
            self.ui.inUsePlainTextEdit.setPlainText(catalogData)

        except Exception as e:
            title = 'Autotietojen lukeminen ei onnistunut'
            text = 'Ajossa olevien autojen tiedot eivät ole saatavissa'
            detailedText = str(e)
            self.openWarning(title, text, detailedText) 
        try:
            # Luodaan tietokantayhteys-olio ja luetaan vapaat autot
            dbConnection = dbOperations.DbConnection(dbSettings)
            dept = self.currentSettings.get('department') or os.getenv('DEPARTMENT') or os.getenv('OSASTO')
            if dept:
                try:
                    freeVehicles = dbConnection.getVehiclesFree(dept)
                except Exception:
                    freeVehicles = self._readTableWithOptionalDepartmentFilter(dbConnection, 'vapaana')
            else:
                freeVehicles = self._readTableWithOptionalDepartmentFilter(dbConnection, 'vapaana')
            catalogData = self.createCatalog(freeVehicles, 'paikkaa')
            self.ui.availablePlainTextEdit.setPlainText(catalogData)

        except Exception as e:
            title = 'Autotietojen lukeminen ei onnistunut'
            text = 'Vapaana olevien autojen tiedot eivät ole saatavissa'
            detailedText = str(e)
            self.openWarning(title, text, detailedText)

        # Aktivoidaan lainaus- ja palautuspainikkeet, jos lainattavia tai palautettaiva autoja
        if self.ui.availablePlainTextEdit.toPlainText() == '':
            self.ui.takeCarPushButton.setEnabled(False)
        else:
            self.ui.takeCarPushButton.setEnabled(True)

        if self.ui.inUsePlainTextEdit.toPlainText() == '':
            self.ui.returnCarPushButton.setEnabled(False)
        else:
            self.ui.returnCarPushButton.setEnabled(True)

    def _readTableWithOptionalDepartmentFilter(self, dbConnection, table: str):
        """Reads all rows from a table, applying a department filter if configured.

        Returns full table when no department is configured or when table has no
        recognizable department column.
        """
        dept = self.currentSettings.get('department') or os.getenv('DEPARTMENT') or os.getenv('OSASTO')
        if not dept:
            return dbConnection.readAllColumnsFromTable(table)

        try:
            cols = dbConnection.readTableColumns(table)
        except Exception:
            return dbConnection.readAllColumnsFromTable(table)

        possible_names = ['osasto', 'department', 'osastokoodi', 'osastonimi', 'osastotunnus', 'dept']
        for name in possible_names:
            if name in cols:
                try:
                    # Read all rows once and filter in Python to avoid exact-string mismatches.
                    rows = dbConnection.readAllColumnsFromTable(table)
                    dept_index = cols.index(name)
                    normalized_department = str(dept).strip().casefold()
                    filtered_rows = []
                    for row in rows:
                        if len(row) <= dept_index:
                            continue
                        row_department = str(row[dept_index]).strip().casefold()
                        if row_department == normalized_department:
                            filtered_rows.append(row)
                    return filtered_rows
                except Exception:
                    return dbConnection.readAllColumnsFromTable(table)

        return dbConnection.readAllColumnsFromTable(table)

    # Näyttää ajon tarkoitus -yhdistelmäruudun
    @Slot()
    def activateReason(self):

        # Asetetaan elementtien näkyvyydet
        self.ui.statusFrame.hide()
        self.ui.statusLabel.setText('Auton lainaus')
        self.ui.goBackPushButton.show()
        self.ui.reasonComboBox.show()
        self.ui.returnCarPushButton.hide()
        self.ui.takeCarPushButton.hide()
        self.ui.statusLabel.show()
        self.ui.statusbar.showMessage('Valitse ajon tarkoitus')

        # Päivitetään ajon tarkoitus -yhdistelmäruudun arvot
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi
    

        # Tehdään lista ajon tarkoituksista
        dbConnection = dbOperations.DbConnection(dbSettings) # Luodaan tietokantayhteys-olio

        
        reasonList = dbConnection.readColumsFromTable('tarkoitus', ['tarkoitus'])
        reasonStringList = []
        for item in reasonList:
            stringValue = str(item[0])
            reasonStringList.append(stringValue)
        
        self.ui.reasonComboBox.clear()
        self.ui.reasonComboBox.addItems(reasonStringList)

    # Näyttää lainaajan kuvakkeen ja henkilötunnuksen kentän
    @Slot()
    def activateLender(self):
        
        self.ui.lenderPictureLabel.show()
        self.ui.ssnLineEdit.show()
        self.ui.ssnLineEdit.setFocus()
        
        
        self.ui.statusbar.showMessage('Syötä ajokortti koneeseen')
        if self.ui.soundCheckBox.isChecked():
            self.playSoundInTread('drivingLicence.wav')
            
        

    # Näyttää avaimen kuvakkeen, rekisterikentän ja lainaajan tiedot
    @Slot()
    def activateKey(self):
        self.ui.ssnLineEdit.hide()
        self.ui.keyPictureLabel.show()
        self.ui.registerPlateBGLabel.show()
        self.ui.keyBarcodeLineEdit.show()
        self.ui.keyBarcodeLineEdit.setFocus()
        self.ui.lenderNameLabel.show()
        self.ui.statusbar.showMessage('Syötä avaimenperä koneeseen')
        if self.ui.soundCheckBox.isChecked():
            self.playSoundInTread('readKey.wav')

        # Luetaan tietokannasta lainaajan nimi
        # Tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi
        
        # luetaan lainaajan tiedoista etunimi ja sukunimi
        try:
            # Luodaan tietokantayhteys-olio
            dbConnection = dbOperations.DbConnection(dbSettings)
            criteria = f"hetu = '{self.ui.ssnLineEdit.text()}'"
            resultSet = dbConnection.filterColumsFromTable('lainaaja',['etunimi', 'sukunimi'], criteria)
            row = resultSet[0]
            lenderName = f'{row[0]} {row[1]}'
            self.ui.lenderNameLabel.setText(lenderName)

        except Exception as e:
            title = 'Ajokortin lukeminen ei onnistunut'
            text = 'Ajokortin tietoja ei löytynyt, ota yhteys henkilökuntaan'
            detailedText = str(e)
            self.openWarning(title, text, detailedText)

    # Näyttää lainauksen loput tiedot
    @Slot()
    def setLendingData(self):
        self.ui.carInfoLabel.show()
        self.ui.dateLabel.show()
        self.ui.calendarLabel.show()
        self.ui.timeLabel.show()
        self.ui.clockLabel.show()
        self.ui.okPushButton.show()
        self.ui.statusbar.showMessage('Jos tiedot ovat oikein paina OK')
        if self.ui.soundCheckBox.isChecked():
            self.playSoundInTread('saveData.wav')

        # Päivitetään auton tiedot 
        
        # Tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        # luetaan auton tiedoista merkki, malli ja henkilömäärä
        try:
            # Luodaan tietokantayhteys-olio
            dbConnection = dbOperations.DbConnection(dbSettings)
            criteria = f"rekisterinumero = '{self.ui.keyBarcodeLineEdit.text()}'"
            resultSet = dbConnection.filterColumsFromTable('vapaana',['merkki', 'malli', 'henkilomaara'], criteria)
            row = resultSet[0]
            carData = f'{row[0]} {row[1]} \n {row[2]}-paikkainen'
            self.ui.carInfoLabel.setText(carData)

        except Exception as e:
            title = 'Auton lainaaminen ei ole mahdollista'
            text = 'Auton palautus edellisestä ajosta on tekemättä, ota yhteys henkilökuntaan'
            detailedText = str(e)

            
            # Muuta kursorin muoto
            self.ui.okPushButton.setCursor(QCursor(Qt.CursorShape.ForbiddenCursor))

            # Otetaan painike pois käytöstä, muuttaa kursorin oletuskursoriksi
            self.ui.okPushButton.setDisabled(True)
            self.openWarning(title, text, detailedText)

            # Muutetaan tilarivin teksti
            self.ui.statusbar.showMessage(title)
        
        try:
            dbConnection = dbOperations.DbConnection(dbSettings)
            timeStamp = dbConnection.getPgTimestamp()
            date = timeStamp[0:10]
            # Merkit 12-17 ovat kellonaika minuuttien tarkkuudella
            time = timeStamp[11:16]

            # Näytetään aikaleima käyttöliittymässä
            self.ui.dateLabel.setText(date)
            self.ui.timeLabel.setText(time)

        except Exception as e:
            title = 'Aikaleiman lukeminen ei onnistunut'
            text = 'Yhteys palvelimeen on katkennut, tee lainaus uudelleen'
            detailedText = str(e)
            self.openWarning(title, text, detailedText)

        try:
            # Luodaan tietokantayhteys-olio
            dbConnection = dbOperations.DbConnection(dbSettings)
            criteria = f"rekisterinumero = '{self.ui.keyBarcodeLineEdit.text()}'"

            # Haetaan auton kuva auto-taulusta
            resultSet = dbConnection.filterColumsFromTable('auto', ['kuva'], criteria)
            row = resultSet[0]
            picture = row[0] # PNG tai JPG kuva tietokannasta

            # Create a pixmap by reading the file and set label    
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(bytearray(row[0])))
            self.ui.vehiclePictureLabel.setPixmap(pixmap)

        except Exception as e:
            title = 'Auton kuvan lataaminen ei onnistunut'
            text = 'Jos mitään tietoja ei tullut näkyviin, ota yhteys henkilökuntaan'
            detailedText = str(e)
            self.openWarning(title, text, detailedText)

    # Tallennetaan lainauksen tiedot ja palautetaan käyttöliittymä alkutilaan
    @Slot()
    def saveLendingData(self):
        # Save data to the database
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaidetaan selväkieliseksi

        try:
            # Luodaan tietokantayhteys-olio
            dbConnection = dbOperations.DbConnection(dbSettings)
            reason = self.ui.reasonComboBox.currentText()
            ssn = self.ui.ssnLineEdit.text() # Henkilötunnus ajopäiväkirjaan
            key = self.ui.keyBarcodeLineEdit.text() # Rekisterinumero ajopäiväkirjaan
            dataDictionary = {'tarkoitus': reason,
                            'hetu': ssn,
                            'rekisterinumero': key}
            dbConnection.addToTable('lainaus', dataDictionary)

            self.setInitialElements()
            self.ui.statusbar.showMessage('Auton lainaustiedot tallennettiin', 5000)
            if self.ui.soundCheckBox.isChecked():
                self.playSoundInTread('lendingOk.wav')   
        
        except Exception as e:
            title = 'Lainaustietojen tallentaminen ei onnistu'
            text = 'Ajokorttin tai auton tiedot virheelliset, ota yhteys henkilökuntaan!'
            detailedText = str(e)
            self.openWarning(title, text, detailedText)

    
        

    # Näytetään palautukseen liittyvät kentät ja kuvat
    @Slot()
    def activateReturnCar(self):
        self.ui.statusFrame.hide()
        self.ui.takeCarPushButton.hide()
        self.ui.returnCarPushButton.hide()
        self.ui.statusLabel.setText('Auton palautus')
        self.ui.keyPictureReturnLabel.show()
        self.ui.registerPlateBGReturnLabel.show()
        self.ui.keyReturnBarcodeLineEdit.show()
        self.ui.goBackPushButton.show()
        self.ui.keyReturnBarcodeLineEdit.setFocus()
        self.ui.statusbar.showMessage('Lue avaimen viivakoodi')
        if self.ui.soundCheckBox.isChecked():
            self.playSoundInTread('readKey.wav')

    # Tallennetaan palautuksen tiedot tietokantaan ja palautetaan UI alkutilaan
    @Slot()
    def saveReturnData(self):
        # Save data to the database
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        # Luetaan tietokanta-asetukset
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword

        dbConnection = dbOperations.DbConnection(dbSettings)
        registrationNumber = self.ui.keyReturnBarcodeLineEdit.text().strip()
        loanNumber = None
        tripWarningMessage = None

        # 1) Haetaan aktiivinen lainausnumero rekisterinumerolla.
        try:
            loanNumber = dbConnection.getNotReturnedId(registrationNumber)
            # Fallback: jos avoimea lainausta ei löydy, käytä viimeisintä lainaa
            if loanNumber is None:
                loanNumber = dbConnection.getLatestLoanNumberForRegistration(registrationNumber)
            if loanNumber is None:
                raise ValueError("Palautettavaa lainausta ei löytynyt")

        except Exception as e:
            self.openWarning(
                'Auton palautus ei onnistunut',
                'Palautettavaa lainausta ei loytynyt',
                str(e)
            )
            return

        # 2) Paivitetaan palautusaika loydetylle lainausnumerolle.
        try:
            print(f'DEBUG: Attempting to set return timestamp for loanNumber={loanNumber}')
            dbConnection.setReturnTimestamp(loanNumber)
            print(f'DEBUG: Return timestamp set successfully')

        except Exception as e:
            print(f'DEBUG: Error setting return timestamp: {type(e).__name__}: {str(e)}')
            self.openWarning(
                'Auton palautus ei onnistunut',
                'Palautusajan paivitys epaonnistui',
                str(e)
            )
            return

        # 3) Haetaan paikannindata ja tallennetaan web_paikkatieto-tauluun.
        # Vaihe ei estä itse palautusta.
        try:
            locationData = self.fetchPaikanninData(registrationNumber, loanNumber)
            if not locationData:
                tripWarningMessage = 'Paikannin ei palauttanut paikkatietoja'
            else:
                # Try modern mapping first
                try:
                    saved = dbConnection.saveWebPaikkatietoData(
                        registrationNumber,
                        loanNumber,
                        locationData,
                    )
                except Exception as e:
                    saved = False
                    tripWarningMessage = f'Paikkatietojen tallennus epäonnistui: {str(e)}'

                if not saved:
                    # Vanha reittimuoto on edelleen tuettu, jos API palauttaa legacy-rakenteen.
                    tripData = locationData
                    if isinstance(locationData, dict):
                        tripData = dict(locationData)
                        tripData.setdefault('lainausnumero', loanNumber)
                        tripData.setdefault('rekisterinumero', registrationNumber)
                    elif isinstance(locationData, list) and locationData and isinstance(locationData[-1], dict):
                        tripData = dict(locationData[-1])
                        tripData.setdefault('lainausnumero', loanNumber)
                        tripData.setdefault('rekisterinumero', registrationNumber)

                    try:
                        dbConnection.addTrip(tripData)
                        # clear any previous warning since addTrip succeeded
                        tripWarningMessage = None
                    except Exception as e:
                        tripWarningMessage = f'Paikkatiedon tallennus ohitettiin: {str(e)}'

        except Exception as e:
            tripWarningMessage = f'Paikkatietojen haku/tallennus ei onnistunut: {str(e)}'

        # UI reset
        self.setInitialElements()
        if tripWarningMessage:
            self.ui.statusbar.showMessage(f'Auto palautettu, mutta {tripWarningMessage}', 9000)
        else:
            self.ui.statusbar.showMessage('Auto palautettu')

        if self.ui.soundCheckBox.isChecked():
            self.playSoundInTread('returnOk.wav')

    def fetchPaikanninData(self, registrationNumber: str, loanNumber):
        """Fetches location data from a configured paikannin endpoint.

        The exact API endpoint is configuration-dependent, so this method uses
        a URL from the application settings when available.
        """

        # Load from .env file or environment variables
        paikanninUrl = os.getenv('PAIKANNIN_API_URL')
        apiKey = os.getenv('PAIKANNIN_API_KEY')

        if not paikanninUrl or not apiKey:
            return None

        apiKeyHeaderName = os.getenv('PAIKANNIN_API_KEY_HEADER', 'Authorization')
        apiKeyPrefix = os.getenv('PAIKANNIN_API_KEY_PREFIX', 'Bearer ')
        timeoutSeconds = int(os.getenv('PAIKANNIN_TIMEOUT_SECONDS', '10'))

        headers = {apiKeyHeaderName: f'{apiKeyPrefix}{apiKey}' if apiKeyPrefix else apiKey}

        requestUrl = paikanninUrl
        if '{' in paikanninUrl and '}' in paikanninUrl:
            endTime = self.currentSettings.get('paikanninEndTime')
            startTime = self.currentSettings.get('paikanninStartTime')

            # Jos aikaa ei ole asetettu, kaytetaan oletuksena viimeiset 24 h UTC-aikana.
            if not endTime:
                endTime = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
            if not startTime:
                startTime = (datetime.now(timezone.utc).replace(microsecond=0) - timedelta(hours=24)).isoformat().replace('+00:00', 'Z')

            deviceId = os.getenv('PAIKANNIN_DEVICE_ID') or registrationNumber
            templateValues = {
                'registrationNumber': registrationNumber,
                'rekisterinumero': registrationNumber,
                'loanNumber': loanNumber,
                'lainausnumero': loanNumber,
                'deviceId': deviceId,
                'startTime': startTime,
                'endTime': endTime,
            }

            for key, value in templateValues.items():
                if value is not None:
                    requestUrl = requestUrl.replace('{' + key + '}', str(value))

            if '{' in requestUrl and '}' in requestUrl:
                raise ValueError(f'Paikannin URL:ssa on korvaamattomia paikkamerkkeja: {requestUrl}')

        try:
            response = requests.get(
                requestUrl,
                headers=headers,
                timeout=timeoutSeconds,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Paikannin API-kutsu epäonnistui: {str(e)}') from e
        except ValueError as e:
            raise ValueError(f'Paikannin API ei palauttanut JSON-dataa osoitteesta: {requestUrl}') from e

    
    @Slot()
    def goBack(self):
        self.setInitialElements()
        self.ui.statusbar.showMessage('Toiminto peruutettiin', 5000)
    
    # Metodi monirivisen luettelon muodostamiseen taulun tai näkymän datasta
    def createCatalog(self, tupleList: list, suffix='') -> str:
        """Creates a catalog like text for plainText edits from list of tuples.
        Typically list comes from a database table or view.
        """
        catalogData = ''
        rowText = ''
            
        for vehiclTtuple in tupleList:
            rowData = ''
            for vehicleData in vehiclTtuple:
                vehicleDataAsStr = str(vehicleData)
                if vehicleDataAsStr == 'True':
                    replacedVehicleData = 'automaatti'
                elif vehicleDataAsStr == 'False':
                    replacedVehicleData = 'manuaali'
                else:
                    replacedVehicleData = vehicleDataAsStr
                # replacedVehicleData = vehicleDataAsStr.replace('False', '')
                rowData = rowData + f'{replacedVehicleData} '
                
            rowText = rowData + f'{suffix}\n'
            catalogData = catalogData + rowText
        return catalogData
    
    # Avataan MessageBox
    # Malli mahdollista virheilmoitusta varten
    def openWarning(self, title: str, text:str, detailedText:str) -> None: 
        """Opens a message box for errors

        Args:
            title (str): The title of the message box
            text (str): Error message
            detailedText (str): Detailed error message typically from source
        """
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setWindowTitle(title)
        msgBox.setText(text)
        msgBox.setDetailedText(detailedText)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()


# LUODAAN VARSINAINEN SOVELLUS
# ============================
app = QtWidgets.QApplication(sys.argv)

# Asetetaan sovelluksen tyyliksi Fusion, ilman asetusta käyttöjärjestelmän oletustyyli tulee käyttöön
app.setStyle('fusion')

# Luodaan objekti pääikkunalle ja tehdään siitä näkyvä
window = MainWindow()
window.show()

# Käynnistetään sovellus ja tapahtumienkäsittelijä (event loop)
app.exec()


    

