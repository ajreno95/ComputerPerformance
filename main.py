import npyscreen
import psutil
import platform


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

    def GetNewInfo(self):
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
        self.keypress_timeout = 10
        self.PlatName = self.add(npyscreen.TitleText, name='OS:\t', value = platform.system() + " " + platform.release() , editable=False)
        self.CpuField = self.add(npyscreen.TitleText, name="CPU COUNT:\t", value = MainForm.ThisPc.CPUCount , editable=False)
        self.VmField = self.add(npyscreen.TitleText, name="VIRTUALMEM%:\t", value = None, editable=False)
        self.SensorField = self.add(npyscreen.TitleText, name="SENSORS:", value = None, editable=False)
        self.FanField = self.add(npyscreen.TitleText, name="FANS:", value = None, editable=False)
    
    def afterEditing(self):
        self.parentApp.setNextForm(None)
    
    def while_waiting(self):
        UpdatedPcInfo = MainForm.ThisPc.GetNewInfo()
        self.VmField.value = UpdatedPcInfo.VirtualMemory.percent
        self.VmField.display()
        if(UpdatedPcInfo.sensor == None):
            self.SensorField.value = 'CANNOT READ SENSORS'
        else:
            self.SensorField.value = UpdatedPcInfo.sensor
        if(UpdatedPcInfo.fans == None):
            self.FanField.value = 'CANNOT READ FANS'
        else:
            self.FanField.value = UpdatedPcInfo.fans
        self.FanField.display()
        self.SensorField.display()
        
        

class MainApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainForm, name = 'Main')
        


if __name__ == "__main__":
    App = MainApp()
    App.run()
