from dronekit import connect, VehicleMode
from time import sleep, time
import platform 
import cv2 as cv

if platform.machine()[:3] == "arm":
    from picamera.array import PiRGBArray
    from picamera import PiCamera

class fligtController:
    def __init__(self,port='/dev/ttyACM0',baud=57600):
        self.vehicle = connect(port, wait_ready=True, baud=baud)
        self.vehicle.add_message_listener("GLOBAL_POSITION_INT",self.pancake)
        if platform.machine()[:3] == "arm":
            self.camera = PiCamera()
            self.rawCapture = PiRGBArray(self.camera)
        else:
            self.camera = cv.VideoCapture(0)



    def _del_(self):
        self.vehicle.close()

    def pancake(self,vehicle, name, message):
        self.lat = message.lat
        self.lon = message.lon
        self.alt = message.alt
        self.angle = message.hdg/100
        pass
    
    def getGPScords(self):
        return [self.lat, self.lon, self.alt, self.angle]

    if platform.machine()[:3] == "arm":
        def getphotoWithCords(self):
            self.camera.capture(self.rawCapture, format="bgr")
            image = self.rawCapture.array
            return [image,self.lat, self.lon, self.alt, self.angle]
    else:
        def getphotoWithCords(self):
            _, image = self.camera.read()
            return [image,self.lat, self.lon, self.alt, self.angle]

        



if __name__ == '__main__':
    print(platform.machine())
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    fc = fligtController(port=sitl.connection_string())
    sleep(1)
    image,lat,lon,alt,angle = fc.getphotoWithCords()
    print("lat: %i"%(lat))
    print("lon: %i"%(lon))
    print("alt: %i"%(alt))
    print("angle: %i"%(angle))
    cv.imshow("test",image)
    while True:
        image,lat,lon,alt,angle = fc.getphotoWithCords()
        cv.imshow("test",image)
        cv.waitKey(1)
    sleep(10)
        
