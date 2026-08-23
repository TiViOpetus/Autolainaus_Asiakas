# RASEKO:N AUTOLAINAUSJRÄJESTELMÄN ASIAKASSOVELLUS 2026
# =====================================================

# KIRJASTOJEN JA MODUULIEN LATAUKSET
# ----------------------------------
import os # Polkumääritykset
import sys # Käynnistysargumentit
import json # JSON-tiedostojen käsittely

from PySide6 import QtWidgets # Qt-vimpaimet
from PySide6.QtCore import QThreadPool, Slot, Qt, QByteArray # Säikeistys, slot-dekoraattori, Qt ja QByteArray tietokantaan tallennetun kuvadatan käsittelyyn
from PySide6.QtGui import QPixmap, QCursor # Kuvan luku ja kursorin muutokset

from lendingModules import sound # Äänitoiminnot
from lendingModules import dbOperations # Tietokantatoiminnot
from lendingModules import cipher # Salausmoduuli
from lendingModules import spatialdata # Paikannin.com API-kutsut

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
   
        # Rutiini, joka lukee asetukset, jos ne ovat olemassa
        try:
            # Avataan asetustiedosto ja muutetaan se Python sanakirjaksi
            with open('settings.json', 'rt') as settingsFile: # With sulkee tiedoston automaattisesti
                
                jsonData = settingsFile.read()
                self.currentSettings = json.loads(jsonData)
            
            # Puretaan salasana tietokantaoperaatioita varten  
            self.plainTextPassword = cipher.decryptString(self.currentSettings['password'])

            # Tallennetaan osastotieto autojen suodattamista varten
            self.division = self.currentSettings['division']
            
        # Jos asetusten luku ei onnistu, näytetään virhedialogi
        except Exception as error:
            title = 'Tietokanta-asetusten luku ei onnistunut'
            text = 'Tietokanta-asetuksien avaaminen ja salasanan purku ei onnistunut'
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
    def playSoundInThread(self, soundFileName):
        self.threadPool.start(lambda: self.playSoundFile(soundFileName))

    # Palauta käyttöliittymä alkutilanteeseen ja päivittää vapaiden ja ajossa olevien autojen katalogit
    @Slot()
    def setInitialElements(self):

        # Piilotetaan alkutilanteessa lainauksen ja palautuksen elementit
        self.ui.bottomFrame.hide()
        self.ui.okPushButton.hide()
        self.ui.reasonFrame.hide()
        self.ui.lenderInfoFrame.hide()
        self.ui.carRegisterFrame.hide()
        self.ui.timeFrame.hide()
        self.ui.carInfoFrame.hide()

        # Tyhjennetään syöttökentät
        self.ui.keyBarcodeLineEdit.clear()
        self.ui.keyReturnBarcodeLineEdit.clear()
        self.ui.lenderNameLabel.clear()
        self.ui.ssnLineEdit.clear()
        self.ui.availablePlainTextEdit.clear()
        self.ui.inUsePlainTextEdit.clear()

        # Aktivoidaan tarvittavat painikkeet
        self.ui.okPushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor)) # Tämä koodi ei ole tarpeellinen, omalla laitteellani toimi normaalisti.
        self.ui.okPushButton.setEnabled(True)

        # Palautetaan auton oletuskuva
        self.ui.vehiclePictureLabel.setPixmap(self.defaultVehiclePicture)
        
        # Luetaan tietokanta-asetukset paikallisiin muuttujiin
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaihdetaan selväkieliseksi

        try:
            # Luodaan tietokantayhteys-olio
            dbConnection = dbOperations.DbConnection(dbSettings)

            # Luetaan ajossa näkymästä lista, jonka jäsenet ovat monikoita (tuple)
            inUseVehicles = dbConnection.getVehiclesInUse(self.division)

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
            # Luodaan tietokantayhteys-olio
            # TODO: pelkästään oman osaston autot
            dbConnection = dbOperations.DbConnection(dbSettings)
            freeVehicles = dbConnection.getVehiclesFree(self.division)
            
            # Muodostetaan luettelo vapaista autoista createCatalog-metodilla
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

    # Näyttää ajon tarkoitus -yhdistelmäruudun
    @Slot()
    def activateReason(self):

        # Avataan sivu index #1 (lendPage)
        self.ui.stackedWidget.setCurrentIndex(1)

        # Asetetaan elementtien näkyvyydet
        self.ui.bottomFrame.show()
        self.ui.statusLabel.setText('Auton lainaus')
        self.ui.goBackPushButton.show()
        self.ui.reasonFrame.show()
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

        self.ui.lenderNameLabel.hide()
        self.ui.lenderInfoFrame.show()
        self.ui.ssnLineEdit.show()
        self.ui.ssnLineEdit.setFocus()
        
        self.ui.statusbar.showMessage('Syötä ajokortti koneeseen')
        if self.ui.soundCheckBox.isChecked():
            self.playSoundInThread('drivingLicence.wav')

    # Näyttää avaimen kuvakkeen, rekisterikentän ja lainaajan tiedot
    @Slot()
    def activateKey(self):

        # Piilotetaan ja näytetään lainaajaan liittyvät kentät
        self.ui.ssnLineEdit.hide()
        self.ui.lenderNameLabel.show()

        # Näytetään lainauksee tarvittavat ketät ja asetetaan syöttökenttä aktiiviseksi
        self.ui.carRegisterFrame.show()
        self.ui.keyPictureLabel.show()
        self.ui.registerPlateBGLabel.show()
        self.ui.keyBarcodeLineEdit.show()
        self.ui.keyBarcodeLineEdit.setFocus()
        
        self.ui.statusbar.showMessage('Syötä avaimenperä koneeseen')
        if self.ui.soundCheckBox.isChecked():
            self.playSoundInThread('readKey.wav')

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

        # Piiloteaa tarpeettomat kehykset
        self.ui.carRegisterFrame.hide()

        # Näytetään lainaukseen liittyvät kehykset ja tiedot
        self.ui.timeFrame.show()
        self.ui.carInfoFrame.show()
        self.ui.okPushButton.show()
        self.ui.statusbar.showMessage('Jos tiedot ovat oikein paina OK')

        if self.ui.soundCheckBox.isChecked():
            self.playSoundInThread('saveData.wav')

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
        dbSettings['password'] = plainTextPassword # Vaihdetaan selväkieliseksi

        # Avataan sivu index #0 (mainPage)
        self.ui.stackedWidget.setCurrentIndex(0)

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
                self.playSoundInThread('lendingOk.wav')   
        
        except Exception as e:
            title = 'Lainaustietojen tallentaminen ei onnistu'
            text = 'Ajokorttin tai auton tiedot virheelliset, ota yhteys henkilökuntaan!'
            detailedText = str(e)
            self.openWarning(title, text, detailedText)

            self.setInitialElements()

        self.setInitialElements()
        # Avataan sivu index #0 (mainPage)
        self.ui.stackedWidget.setCurrentIndex(0)

    # Näytetään palautukseen liittyvät kentät ja kuvat
    @Slot()
    def activateReturnCar(self):

        # Avataan sivu index #2 (returnPage)
        self.ui.stackedWidget.setCurrentIndex(2)

        # Näytetään palautkseen liityvä kehys ja sen sisältö
        self.ui.bottomFrame.show()
        self.ui.statusLabel.setText('Auton palautus')
        self.ui.keyPictureReturnLabel.show()
        self.ui.registerPlateBGReturnLabel.show()
        self.ui.goBackPushButton.show()
        self.ui.keyReturnBarcodeLineEdit.show()
        self.ui.keyReturnBarcodeLineEdit.setFocus()
        self.ui.statusbar.showMessage('Lue avaimen viivakoodi')

        if self.ui.soundCheckBox.isChecked():
            self.playSoundInThread('readKey.wav')

    # Tallennetaan palautuksen tiedot tietokantaan ja palautetaan UI alkutilaan
    # TODO: Tarkista tämän toimivuus vielä lisäämällä print()-komennot
    @Slot()
    def saveReturnData(self):
        
        # Luetaan tietokanta-asetukset asetustiedostosta ja puretaan salasanan salaus
        dbSettings = self.currentSettings
        plainTextPassword = self.plainTextPassword
        dbSettings['password'] = plainTextPassword # Vaihdetaan selväkieliseksi

        # Haetaan tiedot tietokannasta ja paikannin.com-palvelusta
        try:
            # Asetetetaan tilarivin teksti kaikilta osin onnistuneesta palautuksesta
            statusMessage = 'Auto palautettu'
            statusSound = 'returnOk.wav'

            # 1. Haetaan API-avain tietokannasta getSettingsValue(self, key)-metodilla
            dbConnection1 = dbOperations.DbConnection(dbSettings)
            apiKey = dbConnection1.getSettingsValue('paikkatietoAPI')
            print('API-key:', apiKey)

            # 2. Haetaan auton deviceID auto-taulusta getDeviceId(registerNumber)-metodilla
            registerNumber = f"{self.ui.keyReturnBarcodeLineEdit.text()}"
            dbConnection2 = dbOperations.DbConnection(dbSettings)
            deviceId = dbConnection2.getDeviceId(registerNumber)
            print('Device ID:', deviceId)

            # 3. Haetaan lainauksen numero rekisterinumeron perusteella
            dbConnection3 = dbOperations.DbConnection(dbSettings)
            lendingId = dbConnection3.getNotReturnedId(registerNumber)
            print('Lainausnumero:', lendingId)

            # 4. Asetetaan auton palautusaika
            dbConnection4 = dbOperations.DbConnection(dbSettings)
            dbConnection4.setReturnTimestamp(lendingId)

            # 5. Haetaan auton lainauksen alkamis- ja päättymisajat tietokannasta
            dbConnection5 = dbOperations.DbConnection(dbSettings)
            timeStamps = dbConnection5.getTimestamps(lendingId)
            startTime = timeStamps['startTime']
            endTime = timeStamps['endTime']
            print('Aloitus ja päättymisajat:', startTime, endTime)

            # 6. Kutsutaan getNoPointsRoutes(self, deviceId, startTime, endTime)-metodia spatialdata-moduulista
            baseUrl = 'https://app.paikannin.com/public/api'
            paikanninDotCom = spatialdata.PaikanninDotCom(apiKey, baseUrl)
            tripData = paikanninDotCom.getNoPointsRoutes(deviceId, startTime, endTime)

            # 7. Tallennetaan paikkatiedot

            # Jos paikkatietoja ei ole saatu, merkitään ne puuttuviksi manuaalista korjausta varten
            if tripData == []:
                dataToSave = {'fromField': 'PUUTTUU', 'toField': 'PUUTTUU', 'startOdo': 0, 'stopOdo': 0}
                statusMessage = 'AJON PAIKKATIETOJA EI SAATU'
            else:
                dataToSave = tripData

            dbConnection6 = dbOperations.DbConnection(dbSettings)
            dbConnection6.addTrip(lendingId,dataToSave)
            print('Paikkatiedot:', tripData)

        # Määritellään virhedialogin ja tilarivin tekstit virhetilanteessa
        except Exception as e:
            title = 'Auton palautustietojen tallentaminen ei onnistunut'
            text = 'Auton palauttamisessa tapahtui virhe: syynä voi olla ongelmat verkkoyhteydessä, tietokatapalvelimassa tai paikannuspalvelussa. Ota yhteys henkilökuntaan.'
            statusMessage = 'AUTON PALAUTTAMISESSA TAPAHTUI VIRHE'
            statusSound = 'keyreadFailed.WAV'
            detailedText = str(e)
            self.openWarning(title, text, detailedText)
        
        finally:

            # Ilmoitetaan tilarivillä auton palautuksen tilatieto
            self.ui.statusbar.showMessage(statusMessage)
            self.setInitialElements()

            # Avataan sivu index #0 (mainPage)
            self.ui.stackedWidget.setCurrentIndex(0)

            if self.ui.soundCheckBox.isChecked():
                self.playSoundInThread(statusSound)

    @Slot()
    def goBack(self):

        # Palauta käyttöliittymä alkutilanteeseen ja päivittää vapaiden ja ajossa olevien autojen katalogit
        self.setInitialElements()

        # Avataan sivu index #0 (mainPage)
        self.ui.stackedWidget.setCurrentIndex(0)

        # Näytetään viesti
        self.ui.statusbar.showMessage('Toiminto peruutettiin', 5000)

    # Metodi monirivisen luettelon muodostamiseen taulun tai näkymän datasta
    def createCatalog(self, tupleList: list, suffix='') -> str:
        """Creates a catalog like text for plainText edits from list of tuples.
        Typically list comes from a database table or view.

        Args:
            tupleList (list): list of tuples containing table data
            suffix (str, optional): a phrase to add to the end of the line. Defaults to ''.

        Returns:
            str: Plain text for the catalog
        """
        # Määritellään vapaana oleliven autojen tiedot
        # availablePlainTextEdit-elementtiin
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