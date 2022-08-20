import cv2
import numpy as np

# from marker_patterns import marker_patterns


'''
TODO: 
    - Change looping tile method. Perhaps only locally in the middle of each tile, rather than all of it.
    - Robustness!
    - Handle if multiple markers are over EQUAL_THRESHOLD (20 as of now) -> Use highest value
'''


def identify_marker(img_marker, grid_size, scale_factor, debug=False):
    
    img_marked = img_marker.copy()
    
    img_grey = cv2.cvtColor(img_marker, cv2.COLOR_BGR2GRAY)
    kernel_size = int(np.ceil(250*scale_factor))
    try:
        img_binary = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, kernel_size, 2)
    except:  
        kernel_size += 1  
        img_binary = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, kernel_size, 2)
    
    
    img_size, _ = img_binary.shape
    tile_size = int(np.ceil(img_size / grid_size))
    marker_values = np.zeros((grid_size, grid_size))
    
    # Loop indicies
    i = 0; j = 0
    
    for img_y in range(0, img_size, tile_size):
        i = 0
        for img_x in range(0, img_size, tile_size):
            
            # Ulc point (debug)
            cv2.circle(img_marked, (img_x, img_y), int(10*scale_factor), (0,233,255), -1)
            
            # color = np.random.randint(256, size=3)
            # color = (int(color[0]), int(color[1]), int(color[2]))
            
            value_sum = 0
            value_avg = 0
            
            for tile_y in range(tile_size):
                for tile_x in range(tile_size):
                    x = img_x + tile_x
                    y = img_y + tile_y
                    # cv2.circle(img_marked, (x, y), int(1*scale_factor), color, -1)
                    if (x >= img_size or y >= img_size):
                        continue
                    else:
                        value_sum += 1 if img_binary[x, y] < 150 else 0
                        # v = 1 if img_binary[x, y] < 150 else 0
                        # cv2.circle(img_marked, (x, y), int(1*scale_factor), (255*v,255*v,255*v), -1)
                        
            value_avg = value_sum / (tile_x * tile_y)
            
            if (value_avg < 0.5):
                marker_values[i, j] = 0
            else:
                marker_values[i, j] = 1
            
            
            # Loop indicies increments
            i += 1    
        j += 1


    markerID = None
    patterns = marker_patterns()
    EQUAL_THRESHOLD = 20
    for ID, pattern in enumerate(patterns):
        isEqual = np.sum(marker_values == pattern)
        if isEqual > EQUAL_THRESHOLD:
            markerID = ID + 1
            
            
    if debug:
        cv2.imwrite("output/identify_marker.png", img_marked)
        print("Wrote image to path: 'output/identify_marker.png'")
        
        print(f"Marker has ID: {markerID}")


    return markerID



# Known patterns of markers
def marker_patterns():
    patterns = np.array(
        [
            [[1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1]],
            
            [[0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]],
            
            [[0, 1, 1, 1, 0],
            [1, 0, 1, 0, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 1, 0, 1],
            [0, 1, 1, 1, 0]],

            [[1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1]],
            
            [[1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]],
        ]
    )
    return patterns



if __name__ == "__main__":
    path = "Markers/Marker2.png"
    img = cv2.imread(path)
    img = img[0:1050, 0:1050]
    markerID = identify_marker(img, 5, 1, debug = True)
    
