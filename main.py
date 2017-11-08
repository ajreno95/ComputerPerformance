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

    def getVMInfo():
        return psutil.virtual_memory()
        
        

class MainForm(npyscreen.Form):
    ThisPc = PerformanceInformation()
    def create(self):
        self.keypress_timeout = 10
        self.CpuField = self.add(npyscreen.TitleText, name="CPU Count:\t", value = MainForm.ThisPc.CPUCount, editable=False)
        self.VmField = self.add(npyscreen.TitleText, name="Virtual Memory %:\t", value = MainForm.ThisPc.VirtualMemory.percent, editable=False)
        if(MainForm.ThisPc.sensor == None):
            self.SensorField = self.add(npyscreen.TitleText, name="Sensors:", value = 'Cannot read sensors', editable=False)
        else:
            self.SensorField = self.add(npyscreen.TitleText, name="Sensors:", value = MainForm.ThisPc.sensor, editable=False)
        if(MainForm.ThisPc.fans == None):
            self.FanField = self.add(npyscreen.TitleText, name="Fans:", value = 'Cannot read fans', editable=False)
        else:
            self.FanField = self.add(npyscreen.TitleText, name="Fans:", value = MainForm.ThisPc.fans, editable=False)
    
    

    def afterEditing(self):
        self.parentApp.setNextForm(None)
    
    def while_waiting(self, ):
        self.VmField = MainForm.ThisPc.getVMInfo
        self.VmField.display()
        
        

class MainApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainForm, name = 'Main')
        


if __name__ == "__main__":
    App = MainApp()
    App.run()
