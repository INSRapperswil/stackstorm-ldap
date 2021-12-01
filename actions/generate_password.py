from lib.actions import BaseAction
from secrets import token_urlsafe


class GeneratePasswordAction(BaseAction):

    def run(self, nbytes):
        return token_urlsafe(nbytes)
