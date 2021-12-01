import ldap
from lib.actions import BaseAction


class DisableUserAction(BaseAction):
    def run(self, user_obj):

        # 514 disable user account
        mod_acct = [(ldap.MOD_REPLACE, 'userAccountControl', b'514')]

        try:
            self._connection.modify_s(user_obj.get('distinguishedName'), mod_acct)
        except ldap.LDAPError as e:
            if 'desc' in e.message:
                self.logger.error(e.message['desc'])
            else:
                self.logger.error(e)
            return False, ""

        return True
