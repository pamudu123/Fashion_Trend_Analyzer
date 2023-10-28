import cv2
import numpy as np
import args


class DisplayInfoColumn:
    def __init__(self,frame_height,left_margin=2,line_height = 20):
        self.frame_height = frame_height
        self.column_width = args.DISPLAY_COLUMN_WIDTH

        self.left_margin = left_margin
        self.line_height = line_height

        self.age_gender_start = 20
        self.colour_start     = 230


    def update_column_info(self,color_counts,age_gender_distribution):
        # Function to update the black image with text
        black_image = np.zeros((self.frame_height, self.column_width, 3), dtype=np.uint8)

        # Text to be added to the black region
        text = f"""
Age Gender Distribution (IN)
----------------------------------
Age      Male      Women
"""
        for age_range, counts in age_gender_distribution.items():
            text += f"{age_range:<10} {counts['Male']:<12} {counts['Female']:<12}\n"

        # Split the text into lines and add them to the black region
        lines = text.strip().split('\n')
        y = self.age_gender_start                       # Vertical position to start adding text
        for line in lines:
            cv2.putText(black_image, line, (self.left_margin, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y += self.line_height


        text = f"""
Costum Colours
---------------------------------
Colour   Upper     Lower
"""
        for color, counts in color_counts.items():
            text += f"{color:<12} {counts['Upper Body']:<12} {counts['Lower Body']:<12}\n"

        lines = text.strip().split('\n')
        
        y = self.colour_start

        for line in lines:
            cv2.putText(black_image, line, (self.left_margin, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            y += self.line_height
        
        return black_image



if __name__ == '__main__':
    video_path = 0
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    color_counts = {
        'Red': {'Upper Body': 2, 'Lower Body': 1},
        'Blue': {'Upper Body': 0, 'Lower Body': 0},
        'Green': {'Upper Body': 0, 'Lower Body': 0},
        'White': {'Upper Body': 0, 'Lower Body': 0},
        'Black': {'Upper Body': 0, 'Lower Body': 0},
        'Yellow': {'Upper Body': 0, 'Lower Body': 0},
        'Orange': {'Upper Body': 0, 'Lower Body': 0},
        'Purple': {'Upper Body': 0, 'Lower Body': 0},
        'Pink': {'Upper Body': 0, 'Lower Body': 0},
    }

    age_gender_distribution = {
        "(4-6)": {"Male": 2, "Female": 3},
        "(8-12)": {"Male": 0, "Female": 0},
        "(15-20)": {"Male": 0, "Female": 0},
        "(25-32)": {"Male": 0, "Female": 0},
        "(38-43)": {"Male": 0, "Female": 0},
        "(48-53)": {"Male": 0, "Female": 0},
        "(60-100)": {"Male": 0, "Female": 0}
    }

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Update the black image with current text values
        display_column = DisplayInfoColumn(frame_height)
        black_image = display_column.update_column_info(color_counts,age_gender_distribution)

        # Concatenate the frame and black_image horizontally
        combined_frame = np.hstack((frame, black_image))

        cv2.imshow("LIVE",combined_frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break


    cv2.destroyAllWindows()
