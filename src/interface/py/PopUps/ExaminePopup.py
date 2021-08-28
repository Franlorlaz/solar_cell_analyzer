"""" Popup to examine the save path."""

from pathlib import Path
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class ExaminePopup(Popup):
    """Examination popup class."""
    id_examine_popup = ObjectProperty(None)
    save_init_path = StringProperty('')

    def __init__(self, **kwargs):
        """Initialize examine popup."""
        super(ExaminePopup, self).__init__(**kwargs)
        examine_path = Path(__file__ + '/../../../../measures').resolve()
        examine_path = examine_path.joinpath('../../../').resolve()
        self.save_init_path = str(examine_path)
