import cv2
import numpy as np

# from marker_patterns import marker_patterns



def identify_marker(img_marker, grid_size, scale_factor, debug=False):
    
    img_marked = img_marker.copy()
    
    
    img_grey = cv2.cvtColor(img_marker, cv2.COLOR_BGR2GRAY)
    img_binary = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, int(np.ceil(250*scale_factor)), 2)
    
    img_size, _ = img_binary.shape
    tile_size = int(np.round(img_size / grid_size))
    print(np.round(img_size / grid_size))
    
    marker_values = np.zeros((grid_size, grid_size))
    
    for img_y in range(0, img_size, tile_size):
        for img_x in range(0, img_size, tile_size):
            
            # for tile_y in range(tile_size):
            #     for tile_x in range(tile_size):
            
            # Middle point
            cv2.circle(img_marked, (img_x, img_y), int(10*scale_factor), (0,233,255), -1)
            
            
            
            
            
            
            
            # tile_x = int((i * tile_size) + tile_size/2)
            # tile_y = int((j * tile_size) + tile_size/2)
            # value = 1 if img_binary[tile_x, tile_y] < 150 else 0
            # marker_values[i, j] = value
    
    print(marker_values)
    

    markerID = None
    patterns = marker_patterns()
    for ID, pattern in enumerate(patterns):
        isEqual = np.array_equal(marker_values, pattern)
        if isEqual:
            markerID = ID
            
            
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

