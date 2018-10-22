class webBot(object):
    def __init__(self):
        self.readLocalVariables()
        self.printVariables()

    def readLocalVariables(self):
        self.localVariables = {}
        with open('/home/jjc62351/work/PythonPrograms/myDict.txt') as file:
            for line in file:
                (key,val) = line.split(',')
                self.localVariables[int(key)] = val

    def printVariables(self):
        print self.localVariables[2]


def main():
    webBot()

if __name__ == "__main__":
    main()



 
