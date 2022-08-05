import cv2
from cv2 import mean
import numpy as np

import camera_param_intrinsic

'''
TODO:
    - Change centre point identifier to choose mean, rather than simply highest value.
    - Get rotation information
    - If image get resized, the focal length in pixels should be adjusted.
'''


class Value_Point:
    def __init__(self, _x, _y, _value):
        self.x = _x
        self.y = _y
        self.value = _value
        
    def distance_to(self, point):
        return np.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)


class Marker:
    def __init__(self, _point):
        
        self.id_point = _point
        self.points = [_point]
        
    def average(self, _):
        pass
        
    def weighted_mean(self):

        # Calculate mean of coordinates
        sum = [0, 0]
        for point in self.points:
            sum[0] += point.x
            sum[1] += point.y
        mean_spartial = (sum[0] / len(self.points), sum[1] / len(self.points))

        # Normalise coordinates
        points_demeaned = []
        for point in self.points:
            points_demeaned.append(Value_Point(point.x - mean_spartial[0], point.y - mean_spartial[1], point.value))
        
        # Calculate weighted mean of normalised coordinates
        sum = [0, 0]
        for point in points_demeaned:
            sum[0] += point.x * point.value
            sum[1] += point.y * point.value
        mean_normalised_weighted = (sum[0] / len(self.points), sum[1] / len(self.points))
        
        # Final weighted mean  
        mean_weighted = (mean_spartial[0] + mean_normalised_weighted[0], mean_spartial[1] + mean_normalised_weighted[1])
        return mean_weighted

        '''
        Get mean of coordinates
        Subtract mean from all point coordinates (demean)
        Calculate mean of new points weighed with value (normalised)
        Centre = new_mean + old_mean                
        '''





# Expected marker size in image.
def marker_image_size(marker_world_size, altitude, focal_length):
    ratio = altitude / marker_world_size
    marker_image_size = focal_length * ratio    # TODO: Ratio is inverted, WHY does THIS WORK??
    # marker_image_size = (marker_world_size * focal_length) / altitude
    return marker_image_size


# Define area as two points for cv to draw (upper left corner, lower right corner)
def get_area_points(centre_point):
    
    marker_size = marker_image_size(50, 5, camera_param_intrinsic.FOCAL_LENGTH_PX)
    
    i = centre_point[0]
    j = centre_point[1]
    
    ulc = (int(i - marker_size/2), int(j - marker_size/2))
    lrc = (int(i + marker_size/2), int(j + marker_size/2))
    
    return ulc, lrc


# Define areas arond markers for identification and location.
def mark_markers(img, response, debug=False):
    
    img_marked = img.copy()
    
    DISTANCE_THRESHOLD = 200 + 20  # Marker size + margin
    VALUE_THRESHOLD = 40
    
    markers = []
    
    
    for j, row in enumerate(response):
        for i, value in enumerate(row):
            if value > VALUE_THRESHOLD:
                
                point = Value_Point(i, j, value)
                nr_of_markers = len(markers)
                
                if nr_of_markers == 0:
                    markers.append(Marker(point))
                    
                else:
                    no_marker_fit = False
                    for m, marker in enumerate(markers):
                        distance = point.distance_to(marker.id_point)
                        
                        if (distance < DISTANCE_THRESHOLD):
                            marker.points.append(point)
                            break
                        
                        elif ((m + 1) == nr_of_markers):
                            no_marker_fit = True
                    
                    if no_marker_fit:
                        markers.append(Marker(point))





    if (debug == True):
        for marker in markers:
            
            color = np.random.randint(256, size=3)
            color = ( int(color[0]), int(color[1]), int(color[2]))
            
            for point in marker.points:
                cv2.circle(img_marked, (point.x, point.y), 10, color, -1)
            
        mean = markers[0].weighted_mean()
        cv2.circle(img_marked, (int(mean[0]), int(mean[1])), 20, (255,255,255), -1)

        cv2.imwrite("output/mark_markers.png", img_marked)



    # highest_response = 0
    
    # for j, row in enumerate(response):
    #     for i, value in enumerate(row):
    #         if value > highest_response:
                
    #             cv2.circle(img_marked, (i,j), 10, (200,100,255), -1)
                
    #             highest_response = value
    #             start_point, end_point = get_area_points((i, j))
    #             markers = [start_point, end_point, value]  # [ulc, lrc, value]

    
    # cv2.rectangle(img_marked, markers[0], markers[1], (0, 0, 255), 5)

        
    marker_areas = 0
    return marker_areas

