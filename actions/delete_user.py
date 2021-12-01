import ldap
from lib.actions import BaseAction


class DeleteUserAction(BaseAction):
    def run(self, user_obj):
        try:
            self._connection.delete_s(user_obj.get('distinguishedName'))
        except ldap.LDAPError as e:
            if 'desc' in e.message:
                self.logger.error(e.message['desc'])
            else:
                self.logger.error(e)
            return False, user_obj

        return True, user_obj
