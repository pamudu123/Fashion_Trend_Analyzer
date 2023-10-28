# Arguments For Application

###### MODEL PATHS ######
# YOLO MODEL PATH
YOLO_MODEL_PATH = r'YOLO_seg/yolov8s-seg.pt'

# AGE GENDER MODEL PATH
AGE_CONFIG = r'model_files/age_deploy.prototxt'
AGE_MODEL  = r'model_files/age_net.caffemodel'
GENDER_CONFIG = r'model_files/gender_deploy.prototxt'
GENDER_MODEL = r'model_files/gender_net.caffemodel'


###### VIDEO DIRECTORIES ######
VIDEO_PATH = r'recorded_videos/recorded_video.mp4'
SAVE_PROCESSED_VIDEO = r'records/processed_videos'
SAVE_PERSON_DATA_FOLDER = r'save_person_data'
SAVE_EXCEL_RECORDS = r'records/detction_results.xlsx'

###### Video Settings ######
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
IMAGE_SIZE = (IMAGE_WIDTH,IMAGE_HEIGHT)

SAVE_FPS = 30

### BODY RATIOS
HEAD_RATIO       = 0.2
UPPER_BODY_RATIO = 0.5
LOWER_BODY_RATIO = 0.9

#### DETECTION PARAMETERS ####
CORNER_MARGIN = 5

DISPLAY_COLUMN_WIDTH = 240

CENTER_CIRCLE_COLOUR = (0,0,255)

IN_RECT_COORDINATES = (580, 420, 40, 40) 
OUT_RECT_COORDINATES = (580, 60, 40, 40)

DETECTION_POINT_1 = (0,200)
DETECTION_POINT_2 = (640,200)
Y_TRACKED_LINE = 200

AGE_CATEGORIES    = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_CATEGORIES = ['Male', 'Female']


YOUNG_AGE_CATEGORIES = ['(0-2)', '(4-6)', '(8-12)', '(15-20)']
MIDDLE_AGE_CATEGORIES = ['(25-32)', '(38-43)', '(48-53)']
OLD_AGE_CATEGORIES = ['(60-100)']


#### COLOUR RANGES ####
## HSV
HSV_COLOUR_RANGES = {
    "Red": ((0, 50, 50), (10, 100, 100)),
    "Blue": ((200, 0, 0), (260, 100, 100)), 
    "Green": ((60, 50, 50), (150, 100, 100)),
    "White": ((0, 0, 0), (360, 50, 100)),     # S is up to 12% for white
    "Black": ((200, 0, 0), (360, 100, 20)),     # V is up to 12% for black
    "Yellow": ((45, 50, 50), (75, 100, 100)),
    "Orange": ((15, 50, 50), (45, 100, 100)),
    "Purple": ((210, 20, 20), (290, 80, 80)),
    "Pink": ((300, 50, 50), (340, 100, 100)),
    "Cyan": ((180, 60, 50), (220, 100, 100)),
    "Brown": ((15, 60, 20), (45, 80, 60))    # Brown can overlap with other colors
}


## RGB
RGB_COLOUR_RANGE = {
    "Red": [(150, 255), (0, 100), (0, 100)],
    "Blue": [(0, 100), (0, 100), (150, 255)],
    "Green": [(0, 100), (200, 255), (0, 100)],
    "Green": [(0, 70), (0, 70), (0, 70)],  # Dark Green
    "White": [(150, 255), (150, 255), (150, 255)],
    "Black": [(0, 50), (0, 50), (0, 50)],
    "Yellow": [(200, 255), (200, 255), (0, 100)],
    "Orange": [(200, 255), (100, 200), (0, 100)],
    "Purple": [(100, 200), (0, 100), (100, 200)],
    "Pink": [(200, 255), (100, 200), (200, 255)],
    "Cyan": [(0, 100), (200, 255), (200, 255)],
    "Brown": [(100, 150), (100, 150), (100, 150)]
    }


# Dictionary to map color names to BGR values
BGR_EXTRACT_COLOUR_MAP = {
    'Red': (0, 0, 255),        
    'Blue': (255, 0, 0),       
    'Green': (0, 255, 0),      
    'White': (255, 255, 255),
    'Black': (0, 0, 0),        
    'Yellow': (0, 255, 255),   
    'Orange': (0, 165, 255),   
    'Purple': (128, 0, 128),   
    'Pink': (255, 192, 203),   
    'Cyan': (0, 255, 255),     
    'Brown': (165, 42, 42)
}


N_COLOURS = 5  # KMeans gets most common colours

#### Display Images Dir ####
IMAGE_LIBRARY = r'settings/age_gender_icons'


##### SQL Parameters #####
HOST         = "localhost"
SQL_USERNAME = "admin"
SQL_PASSWORD = "password"
SQL_DATABASE_NAME = "shop2"







