import cv2
import numpy as np
import os
from ultralytics import YOLO


from tracked_person import TrackedPerson
from track_records import TrackRecords
from display_info_column import DisplayInfoColumn

from text_rectangle import draw_rectangle_with_text
import args

# Load the YOLOv8 model
model = YOLO(args.YOLO_MODEL_PATH)


# Open the video file
video_path = args.VIDEO_PATH
cap = cv2.VideoCapture(video_path)


# Initialization
tracked_objects = {}
total_in_count = 0
total_out_count = 0
frame_count = 0

track_records = TrackRecords()
display_infor_column = DisplayInfoColumn(args.IMAGE_HEIGHT)


# save processed video
# Codec and create a VideoWriter object to save the video in MP4 format
save_video_path = f'{args.SAVE_PROCESSED_VIDEO}/rec_{len(os.listdir(args.SAVE_PROCESSED_VIDEO))+1}.avi'
print(save_video_path)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(save_video_path, fourcc, args.SAVE_FPS, (args.IMAGE_WIDTH + args.DISPLAY_COLUMN_WIDTH, 
                                                                  args.IMAGE_HEIGHT))

start_frame = -1
stop_frame = -1

out_track_ids = []

while cap.isOpened():
    success, frame = cap.read()

    if success:
        frame = cv2.resize(frame,dsize = args.IMAGE_SIZE)
        display_frame = frame.copy()

        # For process part of the video
        frame_count +=1        
        if (frame_count < start_frame) and (start_frame != -1):
            continue

        if (frame_count > stop_frame) and (stop_frame != -1):
            break

        # Run YOLOv8 tracking
        results = model.track(frame, persist=True, classes=0,verbose=False)  # filter class = 0 (person)

        # Get the boxes and track IDs
        boxes = results[0].boxes.xyxy.cpu().numpy()
        track_ids = results[0].boxes.id
        if track_ids is not None:
            track_ids = track_ids.int().cpu().tolist()
        else:
            track_ids = []
        
        masks = results[0].masks
        if masks is not None:
            masks = masks.data.numpy()
        else:
            masks = []

        # Visualize the results on the frame
        display_frame = results[0].plot()

        for i,(mask,box, track_id) in enumerate(zip(masks,boxes, track_ids)):
            if track_id in tracked_objects.keys():
                x1,y1,x2,y2 = int(box[0]),int(box[1]),int(box[2]),int(box[3])
                bbox_width = int(x2-x1)
                bbox_height = int(y2-y1)

                tracked_person = tracked_objects[track_id]
                
                # Display the tracked ID and "person" label on top of the rectangle
                text = f'person id: {track_id}'
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]

                # Draw a horizontal line under the text
                line_start = (x1, y1 - 5)
                line_end = (x1 + text_size[0]+10, y1 - 5)
      
                cx,cy = tracked_person.calculate_bbox_center(box)
                is_entered = tracked_person.check_person_in_out(box)[1]

                if is_entered == "IN":
                    if (x1 > 0 + args.CORNER_MARGIN) and (x2 < args.IMAGE_WIDTH - args.CORNER_MARGIN) and (y1 > 0 + args.CORNER_MARGIN) and (y2 < args.IMAGE_HEIGHT - args.CORNER_MARGIN):
                        capture_signal = tracked_person.check_save_info()

                        if capture_signal==False:
                            total_in_count +=1
                            dupliacte_frame = frame.copy()
    
                            dupliacte_frame[mask == 0] = (0,0,0)
                            extarct_person = dupliacte_frame[y1:y2,x1:x2]

                            # seperate image for head,upper_body and lower_body
                            head,upper_body,lower_body = tracked_person.seperate_image(extarct_person)
                            
                            # get Colours
                            upper_colour, bottom_colour = tracked_person.detect_costum_colours(upper_body,lower_body)
                            # Age Gender predictions
                            age , gender = tracked_person.detect_age_gender(head)
                            
                            print(f'{track_id} : {upper_colour} : {bottom_colour} : {age} : {gender}')
                            
                            tracked_person.save_record()
                            track_records.add_record(tracked_person.get_predictions())

                            # save tracked images
                            save_image_name = f'{args.SAVE_PERSON_DATA_FOLDER}/{track_id}.jpg'
                            if not os.path.exists(save_image_name):
                                cv2.imwrite(save_image_name,extarct_person)
                                cv2.imwrite(f'{args.SAVE_PERSON_DATA_FOLDER}/face_{track_id}.jpg' , head)
                                cv2.imwrite(f'{args.SAVE_PERSON_DATA_FOLDER}/low_{track_id}.jpg' , lower_body)
                                cv2.imwrite(f'{args.SAVE_PERSON_DATA_FOLDER}/upper_{track_id}.jpg' , upper_body)

                    icon_colour = tracked_person.detection_result_image(bbox_width)
                    try:
                        display_frame[y1: y1+icon_colour.shape[0],x1-icon_colour.shape[1]: x1] = icon_colour
                    except Exception as e:
                        print(f'display icon image is out of frmae : {e}')


                if is_entered == "OUT":
                    if track_id not in out_track_ids:
                        total_out_count +=1
                        out_track_ids.append(track_id)

                cv2.circle(display_frame, (cx, cy), 5, args.CENTER_CIRCLE_COLOUR, -1)

            else:
                # New tracking id                
                tracked_objects[track_id] = TrackedPerson(track_id, box)  # Detected for first time
        

        cv2.line(display_frame, args.DETECTION_POINT_1, args.DETECTION_POINT_2, (0,255,0), 3) 

        display_frame = draw_rectangle_with_text(display_frame, args.IN_RECT_COORDINATES, str(total_in_count), "In", text_color=(0,0,0), rectangle_color=(255,0,0))
        display_frame = draw_rectangle_with_text(display_frame, args.OUT_RECT_COORDINATES, str(total_out_count), "Out", text_color=(0,0,0), rectangle_color=(255,0,0))


        color_counts, age_gender_distribution = track_records.get_count_dicts()

        # info column
        info_column_image = display_infor_column.update_column_info(color_counts,age_gender_distribution)

        combined_frame = np.hstack((display_frame, info_column_image)) 

        # save current frame
        out.write(combined_frame)

        # cv2.imshow("YOLOv8 Tracking", display_frame)
        cv2.imshow("LIVE FRAME", combined_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video
        break

out.release()
cap.release()
cv2.destroyAllWindows()