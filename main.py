import npyscreen
import psutil

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
        
        

class MainForm(npyscreen.Form):
    def create(self):
        ThisPc = PerformanceInformation()
        self.CpuField = self.add(npyscreen.TitleText, name="CPU Count:\t", value = ThisPc.CPUCount, editable=False)
        self.VmField = self.add(npyscreen.TitleText, name="Virtual Memory %:\t", value = ThisPc.VirtualMemory.percent, editable=False)
        if(ThisPc.sensor == None):
            self.SensorField = self.add(npyscreen.TitleText, name="Sensors:", value = 'Cannot read sensors', editable=False)
        else:
            self.SensorField = self.add(npyscreen.TitleText, name="Sensors:", value = ThisPc.sensor, editable=False)
        if(ThisPc.fans == None):
            self.FanField = self.add(npyscreen.TitleText, name="Fans:", value = 'Cannot read fans', editable=False)
        else:
            self.FanField = self.add(npyscreen.TitleText, name="Fans:", value = ThisPc.fans, editable=False)
    def afterEditing(self):
        self.parentApp.setNextForm(None)
        
        

class MainApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainForm, name = 'Main')
        


if __name__ == "__main__":
    App = MainApp()
    App.run()
