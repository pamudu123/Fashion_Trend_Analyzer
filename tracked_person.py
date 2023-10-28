import datetime

from KMeans_colour_track import *
from age_gender_classification import AgeGenderPredictor
from add_detection_icon import create_image_icon,get_person_category_icon_path
import record_excel
from SQL_save import SQLManager
import args


age_gender_classifier = AgeGenderPredictor()

class TrackedPerson:
    def __init__(self, track_id, initial_bbox):
        self.track_id = track_id

        # Location
        self.bboxes = [initial_bbox]        # store a list of bounding boxes
        self.center_coordinates = [self.calculate_bbox_center(initial_bbox)]
                
        # Detected Time
        current_datetime = datetime.datetime.now()
        self.detected_date = current_datetime.date()
        self.detected_time = current_datetime.time()

        # SQL setup
        self.sql_manager = SQLManager()
        self.sql_manager.create_table_if_not_exists()


        # Age , Gender
        self.predicted_age = None
        self.predicted_gender = None

        # Costum colours
        self.upper_costum_colour = None
        self.bottom_costum_colour = None

        # Costum type
        # -- Implementing --

    def check_save_info(self):
        if (self.upper_costum_colour) and (self.bottom_costum_colour):
            return True
        else:
            return False
        
    def seperate_image(self,person_croped_image):
        person_height = person_croped_image.shape[0]
        person_width = person_croped_image.shape[1]
        print(person_width,person_height)

        # Calculate the y-coordinate for each region based on the ratios
        head_y = int(person_height * args.HEAD_RATIO)
        upper_body_y = int(person_height * args.UPPER_BODY_RATIO)
        lower_body_y = int(person_height * args.LOWER_BODY_RATIO)

        # Crop the head, upper body, and lower body regions
        head = person_croped_image[0:head_y, :]
        upper_body = person_croped_image[head_y:upper_body_y, :]
        lower_body = person_croped_image[upper_body_y:lower_body_y, :]

        return head,upper_body,lower_body

    def detect_costum_colours(self,upper_body_image,lower_body_image):
        self.upper_costum_colour = get_comman_clours(KMeans_colour_clustering(upper_body_image))[0]
        self.bottom_costum_colour = get_comman_clours(KMeans_colour_clustering(lower_body_image))[0]

        return self.upper_costum_colour, self.bottom_costum_colour
    
    def detect_age_gender(self,face_image):
        self.predicted_age , self.predicted_gender = age_gender_classifier.predict_age_gender(face_image)
        return self.predicted_age , self.predicted_gender

    def save_record(self):
        # save record in Excel
        record_excel.add_record_to_excel( 
            self.track_id, 
            self.detected_date,
            self.detected_time, 
            self.predicted_age, 
            self.predicted_gender, 
            self.upper_costum_colour, 
            self.bottom_costum_colour)
        
        # save record in SQL
        self.sql_manager.insert_record(self.track_id, self.detected_date, self.detected_time, 
                                  self.predicted_age, self.predicted_gender, 
                                  self.upper_costum_colour, self.bottom_costum_colour)

        
    def get_predictions(self):
        return  self.track_id, self.detected_date,self. detected_time, self.predicted_age, self.predicted_gender, self.upper_costum_colour, self.bottom_costum_colour

    def calculate_bbox_center(self,bbox_coor):
        x1,y1,x2,y2 = bbox_coor[0],bbox_coor[1],bbox_coor[2],bbox_coor[3]
        # x2,y2 = x1+w , y1+h
        # bbox_center = (int(x1 + w/2) , int(y1 + h/2))
        bbox_center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        return (bbox_center)

    def update_bbox(self, new_bbox):
        self.current_bbox = new_bbox
        self.bboxes.append(new_bbox)
        self.center_coordinates.append(self.calculate_bbox_center(new_bbox))

    def check_person_in_out(self,new_bbox):
        # is_in = False 
        self.update_bbox(new_bbox)
        self.Cy = [coord[1] for coord in self.center_coordinates]

       
        if min(self.Cy) < args.Y_TRACKED_LINE and max(self.Cy) > args.Y_TRACKED_LINE:
            is_entering = self.is_entering()
            if is_entering:
                return (True,"OUT")  ### IN
            else:
                return (True,"IN") ##  OUT
        else:
            return (False,"")
            
    
    # Function to check if a list is descending
    def is_entering(self):
        if self.Cy[0] > args.Y_TRACKED_LINE:
            return True
        else:
            return False
        

    def detection_result_image(self,bbox_width):
        person_icon = get_person_category_icon_path(self.predicted_age, self.predicted_gender)

        icon_coloured_image = create_image_icon(person_icon, rect_size=(bbox_width, bbox_width), 
                                                upper_color= args.BGR_EXTRACT_COLOUR_MAP[self.upper_costum_colour[0]], 
                                                bottom_color= args.BGR_EXTRACT_COLOUR_MAP[self.bottom_costum_colour[0]])
        return icon_coloured_image

    def __str__(self):
        return f'{self.track_id} {self.center_coordinates}'


