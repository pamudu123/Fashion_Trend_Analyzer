import cv2
import os
import numpy as np

import args


def get_person_category_icon_path(age_range, gender):
    if age_range in args.YOUNG_AGE_CATEGORIES:
        age_group = 'young'
    elif age_range in args.MIDDLE_AGE_CATEGORIES:
        age_group = 'middle_age'
    elif age_range in args.OLD_AGE_CATEGORIES:
        age_group = 'old'
    
    icon_path = f'{args.IMAGE_LIBRARY}/{age_group}_{gender.lower()}.png'
    if not os.path.exists(icon_path):
        raise FileNotFoundError
    else:
        return icon_path


def create_image_icon(icon_path, rect_size, upper_color, bottom_color):
    image = np.ones((rect_size[1], rect_size[0], 3), dtype=np.uint8) * 255

    # Split the rectangle into upper and lower parts
    upper_part = image[:rect_size[1] // 2, :]
    lower_part = image[rect_size[1] // 2:, :]

    # Set colors for upper and lower parts
    upper_part[:] = upper_color
    lower_part[:] = bottom_color

    # Load the icon with transparency
    icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)

    # Resize the icon to fit the rectangle
    icon = cv2.resize(icon, (rect_size[0], rect_size[1]))

    # Position to place the icon in the center of the rectangle
    icon_x = 0
    icon_y = 0

    # Perform alpha compositing to blend the icon with the rectangle
    for c in range(0, 3):
        image[icon_y:icon_y + icon.shape[0], icon_x:icon_x + icon.shape[1], c] = (
            image[icon_y:icon_y + icon.shape[0], icon_x:icon_x + icon.shape[1], c] * (1 - icon[:, :, 3] / 255.0)
            + icon[:, :, c] * (icon[:, :, 3] / 255.0)
        )

    return image


if __name__ == '__main__':
    person_icon_path = get_person_category_icon_path('(15-20)','Male')
    resulting_image = create_image_icon(person_icon_path, rect_size=(200, 200), upper_color=(0, 0, 255), bottom_color=(0, 255, 0))

    cv2.imshow("LIVE",resulting_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()