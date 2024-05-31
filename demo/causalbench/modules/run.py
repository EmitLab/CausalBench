from causalbench.modules.module import Module
from causalbench.services.requests import save_run


class Run(Module):

    def __init__(self, module_id: int = None):
        super().__init__(module_id, None, 'run')

    def validate(self):
        # TODO: To be implemented
        pass

    def fetch(self, module_id: int) -> str:
        # TODO: To be implemented
        pass

    def save(self, state: dict) -> bool:
        return save_run(self)
