class response:
    def __init__(self):
        self.status = ''
        self.data = ''
        self.error = ''
    def setStatus(self, status):
        self.status = status
    def getStatus(self):
        return self.status
    def setData(self, data):
        self.data = data
    def getData(self):
        return self.data
    def setError(self, error):
        self.error = error
    def getError(self):
        return self.error