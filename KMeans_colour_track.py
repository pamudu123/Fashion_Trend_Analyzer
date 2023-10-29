import numpy as np
import cv2
import os
from sklearn.cluster import KMeans
from collections import defaultdict
import HSV_colour_track

import args


def remove_black_pixels(np_image,thresh=0):
    # mask to identify non-black pixels
    non_black_mask = (np_image[:, :, 0] > thresh) & (np_image[:, :, 1] > thresh) & (np_image[:, :, 2] > thresh)
    return  np_image[non_black_mask]


def RGB_classify_color(rgb_value):
    R_value, G_value, B_value = rgb_value

    color_ranges = args.RGB_COLOUR_RANGE

    for color, color_range in color_ranges.items():
        if (color_range[0][0] <= R_value <= color_range[0][1] and
            color_range[1][0] <= G_value <= color_range[1][1] and
            color_range[2][0] <= B_value <= color_range[2][1]):
            return color
    # else:
    #     if R_value >= G_value and R_value >= B_value:
    #         return "Red" 
    #     elif G_value >= R_value and G_value >= B_value:
    #         return "Green" 
    #     elif B_value >= G_value and B_value >= R_value:
    #         return "Blue" 

        
def KMeans_colour_clustering(np_image, n_colors=args.N_COLOURS):
    
    image = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)  # Convert to RGB color space

    image = remove_black_pixels(image)
    pixels = image.reshape(-1, 3)         # 2D array of pixels
    
    # Apply K-Means clustering to find the most common colors
    kmeans = KMeans(n_clusters=n_colors,random_state=42,n_init=10)
    kmeans.fit(pixels)

    common_colors = kmeans.cluster_centers_.astype(int)

    # Count the number of pixels in each cluster
    cluster_counts = np.bincount(kmeans.labels_)

    # Calculate the percentage of each color in the image
    color_percentages = (cluster_counts / len(pixels)) * 100
    common_colors_with_percentages = list(zip(common_colors, color_percentages))

    return common_colors_with_percentages


def get_comman_clours(colors_and_percentages):
    common_colours_list = []
    for col,per in colors_and_percentages:
        RGB_colour = HSV_colour_track.HSV_classify_color(list(col))

        common_colours_list.append((RGB_colour,int(per)))

    color_sums = defaultdict(int)

    for color, per in common_colours_list:
        if color == 'Unknown':
            continue
        if per > 10:
            color_sums[color] += per
    sorted_common_colors = sorted(color_sums.items(), key=lambda x: x[1], reverse=True)

    return sorted_common_colors


if __name__ == '__main__':

    folder_path = r'save_person_data'
    file_names = os.listdir(folder_path)

    face_images  = sorted([os.path.join(folder_path, file_name) for file_name in file_names if file_name.startswith("face")])
    upper_part_images  = sorted([os.path.join(folder_path, file_name) for file_name in file_names if file_name.startswith("upper")])
    lower_part_images  = sorted([os.path.join(folder_path, file_name) for file_name in file_names if file_name.startswith("low")])

    idx = 1
    image_path = upper_part_images[idx]


    image = cv2.imread(image_path)
    result = KMeans_colour_clustering(image)
    
    print(get_comman_clours(result))

    cv2.imshow("IMG",image)
    cv2.waitKey(0)

