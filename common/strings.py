"""Module for string constants."""

DB_PATH = 'telefonanalyse.db'
DB_NAME_CALLS = 'Anrufe'

EXPORT_DEFAULT_PATH = 'Anrufliste.csv'
EXPORT_TYPES =  (('Comma Seperated Values','*.csv'),('Alle Dateien','*.*'))

TITLE = 'ADFC Telefonanalyse'
TOPICLIST = (
    'Codierung',
    'Verkehr',
    'Mitgliedschaft',
    'Touren',
    'Versicherung',
    'B2B',
    'Tourismus',
    'Aktive'
)

class ALERT():
    class TITLE():
        ENTRYERROR = 'Eingabefehler'
        FILEERROR = 'Dateifehler'
        MISSINGENTRY = 'Fehlende Eingabe'
        NOENTRIESFOUND = 'Keine Einträge gefunden'
        SQLERROR = 'SQL-Fehler'
        SUCCESS = 'Erfolg'
    COUNT_EXPORT = 'Es wurden {count} Einträge exportiert.'
    ERROR_DB_ACCESS = 'Fehler beim Zugriff auf die Datenbank'
    ERROR_DB_UPDATE = 'Fehler beim Aktualisieren der Datenbank'
    ERROR_FILE_OPEN = 'Fehler beim Öffnen der Datei.'
    ERROR_FILE_SAVE = 'Fehler beim Speichern der Datei.'
    FORMAT_DAYS = 'Gib bitte eine Anzahl an Tagen an.'
    FORMAT_DURATION = 'Gib die Dauer des Anrufes bitte in ganzen Minuten an.'
    FORMAT_TIME = 'Gib bitte eine korrekte Uhrzeit ein.'
    MISSING_DURATION = 'Gib bitte die Dauer des Anrufes an.'
    MISSING_TOPIC = 'Gib bitte den Grund des Anrufes an.'
    SUCCESS_ENTRY = 'Eintrag erstellt.'
    SUCCESS_SAVE = 'Die Datei wurde gespeichert.'
    ZERO_ENTRIES = 'Die Anrufsliste enthält im gewünschten Zeitraum keine Einträge.'

class BUTTON():
    OK = 'OK'
    EXPORT = 'Exportieren…'

class COLUMN():
    class DB():
        # Internal names in database
        DATE = 'Day'
        DURATION = 'Duration'
        ID = 'ID'
        TIME = 'Time'
        TOPIC = 'Topic'
    DATE = 'Datum'
    DATETIME = 'Zeitpunkt'
    DURATION = 'Dauer'
    ID = 'Eintrag'
    TIME = 'Uhrzeit'
    TOPIC = 'Thema'

class LABEL():
    EXPORT_DAYS_LN1 = 'Nur die Einträge der letzten'
    EXPORT_DAYS_LN2 = 'Tage exportieren'
    EXPORT_ENTIRE_LIST = 'Die ganze Liste exportieren'
    MINUTES = 'Minuten'
    TABLE_WITH_HEADER = 'Tabelle mit Überschriftszeile'

class WINDOW():
    ENTRY = 'Ein Telefongespräch eintragen'
    EXPORT = 'Die Anrufliste exportieren'
