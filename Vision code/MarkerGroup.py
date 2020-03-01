class MarkerGroup:
    # List of all registered markers
    markerList = []

    # Color tolerance
    ctol = 10

    # Time that last activatation can have before deletion
    maxTime = 10

    # Alpha numerical of marker
    aphaNum = ''

    # Time in frames, since the markergroup was activated
    lastActivation = 0

    def __init__(self, m, alphaNum):
        self.markerList = [ m ]   
        self.alphaNum = alphaNum 

    def addMarker(self, m, alphaNum):
        # TODO Add red support
        #print(m.dhue, alphaNum)
        if self.inRange(m.dhue, self.markerList[0].dhue, self.ctol) and self.alphaNum == alphaNum:
            self.markerList.append(m)
            self.lastActivation = 0
            return True
        return False

    # Run every frame
    # This will automatically return a marker when it has left the frame
    def tick(self):
        if self.lastActivation > self.maxTime:
            return False
        self.lastActivation += 1
        return True

    # Check if a is in range of b
    def inRange(self, a, b, range):
        return b - range <= a <= b + range
        
