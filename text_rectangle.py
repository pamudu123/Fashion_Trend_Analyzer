import cv2
import numpy as np

def draw_rectangle_with_text(image, rect_coords, text_inside, text_outside, font_scale=1.0, font_thickness=3, text_color=(255, 255, 255), rectangle_color=(0, 0, 255)):

    x, y, width, height = rect_coords

    # Draw the rectangle
    cv2.rectangle(image, (x, y), (x + width, y + height), rectangle_color, -1)

    # Calculate the position to place the text inside the rectangle
    text_size_inside = cv2.getTextSize(text_inside, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
    text_x_inside = x + (width - text_size_inside[0]) // 2
    text_y_inside = y + (height + text_size_inside[1]) // 2

    # Draw the text inside the rectangle
    cv2.putText(image, text_inside, (text_x_inside, text_y_inside), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness)

    # Calculate the position to place the text outside the rectangle
    text_size_outside = cv2.getTextSize(text_outside, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
    text_x_outside = x + (width - text_size_outside[0]) // 2
    text_y_outside = y - 10  # Adjust the Y position to be above the rectangle

    # Draw the text outside the rectangle
    cv2.putText(image, text_outside, (text_x_outside, text_y_outside), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness)

    return image

if __name__ == "__main__":
    width, height = 400, 200
    image = 255 * np.ones((height, width, 3), dtype=np.uint8)

    # Define rectangle coordinates, text inside, and text outside, and colors
    rect_coords = (50, 50, 300, 100)
    text_inside = "Inside"
    text_outside = "Outside"
    text_color = (0, 0, 0)  # Black
    rectangle_color = (0, 255, 0)  # Green

    # Draw the rectangle with text inside and outside
    result_image = draw_rectangle_with_text(image, rect_coords, text_inside, text_outside, text_color=text_color, rectangle_color=rectangle_color)

    # Display the result image
    cv2.imshow("Rectangle with Text", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
