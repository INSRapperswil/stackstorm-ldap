import ldap
from lib.actions import BaseAction


class SetUserGroupAction(BaseAction):
    def run(self, user_obj):
        user_dn = user_obj.get('distinguishedName')
        group_dn = self._ldap_group_dn

        # Add user to group
        mod_acct = [(ldap.MOD_ADD, 'member', str(user_dn).encode("utf-8"))]

        try:
            self._connection.modify_s(group_dn, mod_acct)
        except ldap.LDAPError as e:
            if 'desc' in e.message:
                self.logger.error(e.message['desc'])
            else:
                self.logger.error(e)
            return False, ""

        return True
