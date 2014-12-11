import logging
import os
import osUtilities
import inspect
import controller.yml.yamlUtilities as yUtils

class TsLoggin(object):

    OPTIONS  = yUtils.YamlUtilities()
    OPTIONS.load(["core.sourcePaths", "logging.loggingProperties"])
    LOG_PATH = OPTIONS.get("loggingPath")
    FORMAT   = '[%(asctime)s][%(levelname)s][%(name)s] : %(message)s'
    LEVELS   = {'isDebug'   : logging.DEBUG,
                'isInfo'    : logging.INFO,
                'isWarning' : logging.WARNING,
                'isError'   : logging.ERROR,
                'isCritical': logging.CRITICAL
               }

    def __init__(self, logFile, loggerName):
        formatter    = logging.Formatter(self.FORMAT)
        self.logFile = os.path.join(self.LOG_PATH, logFile)
        self.logger  = logging.getLogger(loggerName)
        self.ch      = logging.StreamHandler()
        self.ch.setFormatter(formatter)
        self.logger.addHandler(self.ch)
        self._level  = logging.INFO
        logging.basicConfig(filename=self.logFile,
                            format  =self.FORMAT)

    def log(self, message,
                  isDebug   =False,
                  isInfo    =False,
                  isWarning =False,
                  isError   =False,
                  isCritical=False):
        message += self.traceCall(inspect.currentframe())
        self.level = locals()
        self.logger.log(msg=message, level=self.level)

    def traceCall(self, frame):
        # (frame, filename, line_number,
        #  function_name, lines, index)
        format = '\n--------\n' \
                 'file: %(file)s \n' \
                 'line: %(line)s \n' \
                 'Method Called: %(caller)s\n' \
                 'Called From: %(funcName)s'
        callTree = []
        callList = inspect.getouterframes(frame)[1:]
        for call in callList:
            (frame, file, line,
             funcName, caller, index) = call
            caller   = ', '.join([x.replace('\n', '').strip() for x in caller])
            root, ext = os.path.splitext(file)
            name = os.path.basename(root)
            funcName = name if funcName == '<module>' else funcName
            callTree.append(format % locals())
        return ''.join(callTree)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        level = [self.LEVELS[k] for k, v
                 in level.items()
                 if v and self.LEVELS.get(k, None)][0]
        self._level = level
        self.logger.setLevel(level)
        self.ch.setLevel(level)