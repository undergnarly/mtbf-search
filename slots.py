
from datetime import datetime
from design import Ui_Form


class MainWindowSlots(Ui_Form):
    
    def set_time(self):
        str_time = datetime.now().strftime('%H:%M:%S')
        self.pushButton.setText(str_time)
        return None
	