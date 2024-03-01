from .setup_model import SetupCheckBase
class CheckTestFail(SetupCheckBase):

    def _check_setup(self):
        return False, "TEST FAIL"

    def __init__(self):
        self.check_name = "intentionally failing"
        self.instructions = ""
        self.success, self.error_reason = self._check_setup()

