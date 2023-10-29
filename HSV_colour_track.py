import args
import cv2
import numpy as np
import cv2
import os
import colorsys


def convert_to_hsv(r, g, b):
    # Convert RGB values to the range [0, 1]
    r /= 255.0
    g /= 255.0
    b /= 255.0

    # Convert RGB to HSV using colorsys
    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # Convert h to [0, 360] and s, v to [0, 100] for common HSV representation
    h = int(h * 360)
    s = int(s * 100)
    v = int(v * 100)

    return h, s, v


def HSV_classify_color(input_color): 
    hsv_color = convert_to_hsv(*input_color)
    hsv_color_ranges = args.HSV_COLOUR_RANGES

    # Convert the input HSV color to integer values
    hsv_color = tuple(int(x) for x in hsv_color)
    
    # Compare the input color to predefined color ranges
    for color_name, (lower_range, upper_range) in hsv_color_ranges.items():
        if all(lower <= value <= upper for value, (lower, upper) in zip(hsv_color, zip(lower_range, upper_range))):
            return color_name
    
    return "Unknown"


def get_mean_bgr(bgr_image, color_to_exclude=(0, 0, 0)):
    extracted_image = bgr_image

    # Create a binary mask for the color to exclude (e.g., black)
    color_mask = np.all(extracted_image != color_to_exclude, axis=-1)
    
    # Calculate the mean BGR values for the extracted region excluding the specified color
    mean_bgr = cv2.mean(extracted_image, mask=color_mask.astype(np.uint8))

    return mean_bgr[:3]  # Extract only the BGR values



if __name__ == '__main__':

    folder_path = r'save_person_data'
    file_names = os.listdir(folder_path)

    face_images  = [os.path.join(folder_path, file_name) for file_name in file_names if file_name.startswith("face")]
    upper_part_images  = [os.path.join(folder_path, file_name) for file_name in file_names if file_name.startswith("upper")]
    lower_part_images  = [os.path.join(folder_path, file_name) for file_name in file_names if file_name.startswith("low")]

    idx = 0
    img = cv2.imread(upper_part_images[idx])
    cv2.imshow("IMG",img)
    cv2.waitKey(0)

    color_name = get_mean_bgr(img)
    print(f"The color is: {color_name}")
