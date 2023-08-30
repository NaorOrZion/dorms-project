from enum import Enum

# General
VALID_GENDER_RADIO_VALUE = ["זכר", "נקבה", "אחר"]
UPLOAD_FOLDER = "./files/upload/"
DOWNLOAD_FOLDER = "./files/download/"
DOWNLOAD_TEMPLATE_XLSX = "./files/download/residents-template.xlsx"
ALLOWED_EXTENSIONS = {"xlsx"}
RESIDENTS_CHART_HEADERS = [
    "שם מלא",
    "מסגרת",
    "מגדר",
    "סוג שירות",
    "גר/ה בבאר שבע",
    "תעודת זהות",
]
EMPTY_BED_TEXT = "מיטה פנויה"

## DB Consts
# Building table columns
BUILDING_TABLE = "buildings"
BUILDING_ID_BUILDING_TABLE = "building_id"
APT_COUNT_BUILDING_TABLE = "apt_count"

# Apartment table columns
APARTMENTS_TABLE = "apartments"
APT_ID_APT_TABLE = "apt_id"
ROOMS_IN_APT_TABLE = "rooms_in_apt"
GENDER_APT_TABLE = "gender"
BUILDING_ID_APT_TABLE = "building_id"

# Room table columns
ROOMS_TABLE = "rooms"
APT_ID_ROOM_TABLE = "apt_id"
ROOM_ID_ROOM_TABLE = "room_id"
AMINACH_BED_ROOM_TABLE = "aminach_beds"
BUNK_BED_ROOM_TABLE = "bunk_beds"

# Aminach bed table cloumns
AMINACH_BED_TABLE = "aminach_bed"
APT_ID_AMINACH_TABLE = "apt_id"
BED_ID_AMINACH_TABLE = "bed_id"
MATTRESS_COUNT_AMINACH_TABLE = "mattress_count"
PERSON1_AMINACH_TABLE = "person1"
ROOM_ID_AMINACH_TABLE = "room_id"

# Bunk bed table cloumns
BUNK_BED_TABLE = "bunk_bed"
APT_ID_BUNK_TABLE = "apt_id"
BED_ID_BUNK_TABLE = "bed_id"
MATTRESS_COUNT_BUNK_TABLE = "mattress_count"
PERSON1_BUNK_TABLE = "person1"
PERSON2_BUNK_TABLE = "person2"
ROOM_ID_BUNK_TABLE = "room_id"

# Residents table columns
RESIDENTS_TABLE = "residents"
ID_RESIDENTS_TABLE = "id"
FULL_NAME_RESIDENTS_TABLE = "full_name"
ASSOCIATION_RESIDENTS_TABLE = "association"
GENDER_RESIDENTS_TABLE = "gender"
SERVICE_RESIDENTS_TABLE = "service"
BEERSHEVA_RESIDENTS_TABLE = "beersheva"
TAZ_RESIDENTS_TABLE = "taz"
APT_RESIDENTS_TABLE = "apartment"


## PostgreSQL consts
# db connection consts
DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "Naor55060606!"
DB_PORT = 5432


class TextConsts(Enum):
    TEXT_BUILDING_FIELD = "Building Number"
    TEXT_APARTMENT_FIELD = "Apartment Number"
    TEXT_FULL_NAME_FIELD = "Full Name"
    TEXT_SERVICE_FIELD = "Service type"
    TEXT_IS_BEERSHEVA_RESIDENT_FIELD = "Live in Beer-Sheva?"
    TEXT_GENDER_FIELD = "Gender Field"
    TEXT_INPUT_REQUIRED = "Input is required!"
    TEXT_DATA_REQUIRED = "Data is required!"
    TEXT_BUILDING_DATA_INVALID = "Building number is not valid!"
    TEXT_APARTMENT_DATA_INVALID = "Apartment number is not valid!"
    TEXT_STRING_DATA_INVALID = "Length must be between 2 and 25 characters long"
    TEXT_SAVE_CHANGES = "שמירת שינויים"


class ChoiceFrameConsts(Enum):
    CHOICE_MEA = "צוות מאה"
    CHOICE_LIBA = "צוות ליבה"
    CHOICE_MITKAN = "מתקן"
    CHOICE_LAMDA = "למדא"
    CHOICE_MASHAN = "משאן"
    CHOICE_HEADQUARTERS = "מפקדה"
    CHOICE_LOGISTICS = "לוגיסטיקה"
    CHOICE_RED_PROG = "תכנות אדום"
    CHOICE_BLUE_PROG = "תכנות כחול"
    CHOICE_GREEN_PROG = "תכנות ירוק"
    CHOICE_YELLOW_PROG = "תכנות צהוב"
    CHOICE_CYBER_A = "מגן סייבר א"
    CHOICE_CYBER_B = "מגן סייבר ב"
    CHOICE_MAPAL = "מפל"
    CHOICE_DATA = "דאטה"
    CHOICE_MAGEN_KEVA = "מגן קבע"
    CHOICE_SRE = "SRE"
    CHOICE_ERP = "ERP"
    CHOICE_DEVOPS_A = "DevOps A"
    CHOICE_DEVOPS_B = "DevOps B"
    CHOICE_QA_A = "QA A"
    CHOICE_QA_B = "QA B"
    CHOICE_PSI = "PSI"
    CHOICE_DC = "DC"
    CHOICE_BI = "BI"
    CHOICE_ELSE = "אחר"


class ChoiceGenderConsts(Enum):
    CHOICE_GENDER_MALE = "זכר"
    CHOICE_GENDER_FEMALE = "נקבה"
    CHOICE_GENDER_UNKNOWN = "אחר"


class ChoiceServicesConsts(Enum):
    CHOICE_HOVA = "חובה"
    CHOICE_KEVA = "קבע"
    CHOICE_HANICH = "חניך/ה"


class ChoiceIsBeershevaResidentConsts(Enum):
    CHOICE_BEERSHEVA_FALSE = "לא"
    CHOICE_BEERSHEVA_TRUE = "כן"
