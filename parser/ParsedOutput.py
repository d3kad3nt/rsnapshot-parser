class LogOutput:
    def __init__(self, config, input):
        self.config = config
        self.log = self.readInput(input)
        self.backupPoints = self.parseBackupPoints()

    def parseBackupPoints(self):
        backupPoints = self.config.getBackupPoints()
        currentBackupPoint = -1
        currentBackupPointLog = []
        for line in self.log:
            if (currentBackupPoint + 1) < len(backupPoints) and backupPoints[currentBackupPoint + 1].backupStartLine() in line:
                if currentBackupPoint >= 0:
                    backupPoints[currentBackupPoint].addLog(currentBackupPointLog)
                currentBackupPoint += 1
                currentBackupPointLog = []
            currentBackupPointLog.append(line)
        backupPoints[currentBackupPoint].addLog(currentBackupPointLog)
        return backupPoints

    def readInput(self, filename: str):
        with open(filename, "r", encoding="utf8") as logfile:
            lines = logfile.readlines()
        linestart = ""
        reallines = []
        for line in lines:
            # Rsnapshot cuts long lines into multiple lines seperated by "\"
            if linestart:
                line = linestart + line[4:]
            if line.endswith("\\\n"):
                linestart = line.strip()[:-1]
            else:
                linestart = ""
                reallines.append(line)
        return reallines

    def commandsWithStatusCount(self, status):
        return len(self.commandsWithStatus(status))

    def commandsWithStatus(self, status):
        result = []
        for backupPoint in self.backupPoints:
            if isinstance(backupPoint.getState(), status):
                result.append(backupPoint)
        return result

    def commandsNotWithStatusCount(self, status):
        return len(self.commandsNotWithStatus(status))

    def commandsNotWithStatus(self, status):
        result = []
        for backupPoint in self.backupPoints:
            if not isinstance(backupPoint.getState(), status):
                result.append(backupPoint)
        return result
