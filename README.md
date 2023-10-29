# Fashion Trend Analyzer

The Fashion Trend Analyzer is designed to identify and record seasonal costume patterns among different age groups and genders.

## 1. People Detection and Tracking

- **Detection Model**: YOLOv8 segmentation model.
- **Tracking Algorithm**: ByteTrack Algorithm.
- **Count**: Records the number of people entering (IN) and leaving (OUT).

**When a person is entering:**
- **Segmentation Mask Retrieval**: The system fetches the segmentation mask.
- **Body Division**:
  - The detected person image is divided into three sections based on predefined ratios:
    1. Head Part
    2. Upper Costume Part
    3. Lower Costume Part

## 2. Age and Gender Prediction (Head Region)

- **Models**:
  - Uses two separate models for age and gender prediction.
  - Due to real-time application needs, a lightweight model ("coffee model") is employed.
  - For enhanced speed, the model is quantized to INT8.
- **Age Categories**:
  - The age model can predict the following age categories: '(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)'.
- **Gender Prediction**:
  - The gender model can predict whether the detected person is Male or Female.

## 3. Costume Color Detection (Upper and Lower Costume Regions)

- **Algorithm**: Uses KMeans algorithm-based method for identify colours.
- **Steps**:
  1. **Image Conversion**: Converts from BGR to RGB using OpenCV.
  2. **Preprocessing**:The black background pixels in the pixel mask are removed.
  3. **K-Means Clustering**: Groups similar pixels (colors) into clusters.
  4. **Cluster Analysis**: Retrieves the cluster centers representing the most common colors.
  5. **Pixel Count**: Calculates the number of pixels in each cluster.
  6. **Percentage Calculation**: Determines the percentage of each color cluster in the image.
  7. **Most Common Color Values**: Generates a list of common RGB color values along with their respective percentages.
  8. **RGB2HSV**: Converts the RGB color values to the HSV color format.
  9. **Determine Respective Color**: Based on the HSV values, the respective color is determined.

## 4. Data Storage

- **Excel**: All the records are saved in an Excel file.
- **Database**: Records are also stored in a MySQL database for reference.

## 5. Display

- The details, including segmentation masks, are displayed in an OpenCV window.


## Demonstration
![DemoVideo](resources/video.gif)