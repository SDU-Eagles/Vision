from cmath import pi
import cv2
import numpy as np


'''
TODO:
    - Get rotation information
    - Filter markers with few response points
    - Fix world-marker-size to image-marker-size (resizing world marker causes inverted behaviour, but inverting ration din't work earlier)
'''


class Value_Point:
    def __init__(self, _x, _y, _value):
        self.x = _x
        self.y = _y
        self.value = _value
        
    def distance_to(self, point):
        return np.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)


class Marker:
    def __init__(self, _point, marker_size):
        
        self.id_point = _point
        self.points = [_point]
        self.location = [0,0]
        self.rotation = 0
        self.size = int(marker_size)
        
                
    def weighted_mean(self):
        # https://physics.stackexchange.com/questions/685186/weighted-center-of-mass-of-an-image-using-the-correct-weights             

        # Calculate mean of coordinates
        sum = [0, 0]
        for point in self.points:
            sum[0] += point.x
            sum[1] += point.y
        mean_spartial = (sum[0] / len(self.points), sum[1] / len(self.points))
        # return mean_spartial

        # Normalise coordinates
        points_demeaned = []
        for point in self.points:
            points_demeaned.append(Value_Point(point.x - mean_spartial[0], point.y - mean_spartial[1], point.value))
        
        # Calculate weighted mean of normalised coordinates
        sum = [0, 0]
        valsum = 0 # Total sum of pixel values
        for point in points_demeaned:
            sum[0] += point.x * point.value
            sum[1] += point.y * point.value
            valsum += point.value
        mean_normalised_weighted = (sum[0] / valsum, sum[1] / valsum)
        # mean_normalised_weighted = (sum[0] / len(self.points), sum[1] / len(self.points))
        
        # Final weighted mean  
        mean_weighted = (mean_spartial[0] + mean_normalised_weighted[0], mean_spartial[1] + mean_normalised_weighted[1])
        mean_weighted = (int(mean_weighted[0]), int(mean_weighted[1]))
        return mean_weighted
    

    def average_angle(self, angle_grid):
        
        size = int(self.size)
        ulc, _ = get_area_points(self.location, size)
        sum = 0
        for i in range(size):
            for j in range(size):
                sum += angle_grid[ulc[0] + i, ulc[1] + j]
        
        return sum / size**2


# Define area as two points for cv to draw (upper left corner, lower right corner)
def get_area_points(centre_point, marker_size):
    
    i = centre_point[0]
    j = centre_point[1]
    
    ulc = (int(i - marker_size/2), int(j - marker_size/2))
    lrc = (int(i + marker_size/2), int(j + marker_size/2))
    
    return ulc, lrc


# Define areas arond markers for identification and location.
def mark_markers(img, response, gradient_angles, marker_image_size, scale_factor = 1, debug=False):

    img_marked = img.copy()
    
    DISTANCE_THRESHOLD = marker_image_size + 20  # Marker size + margin
    VALUE_THRESHOLD = 20

    markers = []
    
    # Divide response points into marker areas
    for j, row in enumerate(response):
        for i, value in enumerate(row):
            if value > VALUE_THRESHOLD:
                
                point = Value_Point(i, j, value)
                nr_of_markers = len(markers)
                
                
                if nr_of_markers == 0:
                    markers.append(Marker(point, marker_image_size))
                    
                # Allocate points into marker areas depending on distance to existing markers
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
                        markers.append(Marker(point, marker_image_size))
     
                        
    # Get middle point and angle of markers     
    marker_locations = []
    marker_rotations = []
    
    for marker in markers:
        mean = marker.weighted_mean()
        marker_locations.append(mean)
        marker.location = mean
                
        # angle = gradient_angles[mean[0], mean[1]]
        angle = (marker.average_angle(gradient_angles) % (pi/2))
        marker_rotations.append(angle)     
        marker.rotation = angle
        
                
        
    


    # Write images for visual purposes
    if (debug == True):
        for marker in markers:
            
            color = np.random.randint(256, size=3)
            color = (int(color[0]), int(color[1]), int(color[2]))
            
            # for point in marker.points:
            #     cv2.circle(img_marked, (point.x, point.y), int(2*scale_factor), color, -1)
            
            location = marker.location
            # angle = marker.rotation + pi/4
            angle = marker.rotation
            # Middle point
            cv2.circle(img_marked, location, int(20*scale_factor), (200,200,255), -1)
            # Rectangle around marker
            rot_rectangle = (location, (marker_image_size, marker_image_size), np.rad2deg(angle))
            box = cv2.boxPoints(rot_rectangle) 
            box = np.int0(box) #Convert into integer values
            img_marked = cv2.drawContours(img_marked, [box], 0, color, int(np.ceil(5*scale_factor)))
            # Angle of marker
            cv2.line(img_marked, location, (int(np.cos(angle)*200*scale_factor)+location[0], int(np.sin(angle)*200*scale_factor)+location[1]), color, int(np.ceil(5*scale_factor)))
            

        cv2.imwrite("output/mark_markers.png", img_marked)
        print("Wrote image to path: 'output/mark_markers.png'")


    return marker_locations, marker_rotations

