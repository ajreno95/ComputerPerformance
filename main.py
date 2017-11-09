import npyscreen
import psutil
import platform
import multiprocessing
from tqdm import tqdm


def ProgBar(status, length):
    prog = int(status/length)
    bar = '['
    for i in range(1,prog):
        bar += '|'
    for i in range(len(bar), 100//length):
        bar += ' ' 
    bar += '] ' + str(status) + '%'    
    return bar


'''
class NetworkInformation:
    def __init__(self):
'''        


class PerformanceInformation:
    def __init__(self):
        self.CPUCount = psutil.cpu_count()
        self.VirtualMemory = psutil.virtual_memory()
        self.NetworkInfo = psutil.net_io_counters()
        if hasattr(psutil, 'sensors_temperatures'):
            self.sensor = psutil.sensors_temperatures()
        else:
            self.sensor = None
        if hasattr(psutil, 'sensors_fans'):
            self.fans = psutil.sensors_fans()
        else:
            self.fans = None

    def GetNewPerformanceInfo(self):
        #Call psutil methods to get current performance values
        #and return updated performance object
        self.VirtualMemory = psutil.virtual_memory()
        self.NetworkInfo = psutil.net_io_counters()
        if hasattr(psutil, 'sensors_temperatures'):
            self.sensor = psutil.sensors_temperatures()
        else:
            self.sensor = None
        if hasattr(psutil, 'sensors_fans'):
            self.fans = psutil.sensors_fans()
        else:
            self.fans = None
        return self


class MainForm(npyscreen.Form):    
    ThisPc = PerformanceInformation()

    def create(self):
        #Set refresh time
        self.keypress_timeout = 1
    
        #Create Box to display PC performance data
        self.PerformanceBox = self.add(npyscreen.BoxTitle, name='System Information', max_width = 45, rely=2, max_height = 9, editable=False)
        self.PerformanceBox.values =  ['OS:\t'+platform.system()+' '+platform.release(),
                                'CPU COUNT:\t'+str(MainForm.ThisPc.CPUCount),
                                'VirtualMEM%:\t',
                                'SENSORS:\t',
                                'FANS:\t'
                                ]

        self.CpuBox = self.add(npyscreen.BoxTitle, name='TestBox', max_width = 55, rely=2, relx = 47, max_height = 9, editable=False)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
    
    def while_waiting(self):
        UpdatedPcInfo = MainForm.ThisPc.GetNewPerformanceInfo()
        SensorInfo = None
        FanInfo = None

        #Check to see if Sensor and Fans are working, if not output error
        if(UpdatedPcInfo.sensor == None):
            SensorInfo = 'CANNOT READ SENSORS'
        else:
            SensorInfo = UpdatedPcInfo.sensor
        if(UpdatedPcInfo.fans == None):
            FanInfo = 'CANNOT READ FANS'
        else:
            FanInfo = UpdatedPcInfo.fans

        #insert PerformanceBox values
        self.PerformanceBox.values =  ['OS:\t'+platform.system()+' '+platform.release(),
                                'CPU COUNT:\t'+str(MainForm.ThisPc.CPUCount),
                                'VirtualMEM%:\t'+ProgBar(UpdatedPcInfo.VirtualMemory.percent, 5),
                                'SENSORS:\t'+SensorInfo,
                                'FANS:\t'+FanInfo
                                ]

        #insert CpuBox values
        self.CpuBox.values = []
        for counter, cpu in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
            self.CpuBox.values += 'CPU'+str(counter)+': '+ProgBar(cpu, 3),

        self.PerformanceBox.display()
        self.CpuBox.display()

        

class MainApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainForm, name = 'Main')
 
        


if __name__ == "__main__":
    App = MainApp()
    App.run()
