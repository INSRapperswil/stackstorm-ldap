from lib.actions import BaseAction
import ldap


class SetUserPasswordAction(BaseAction):
    def run(self, user_obj, password):

        unicode_pass = str('\"' + str(password) + '\"')
        password_value = unicode_pass.encode('utf-16-le')

        add_pass = [(ldap.MOD_REPLACE, 'unicodePwd', [password_value])]

        try:
            self._connection.modify_s(user_obj.get('distinguishedName'), add_pass)
        except ldap.LDAPError as e:
            if 'desc' in e.message:
                self.logger.error(e.message['desc'])
            else:
                self.logger.error(e)
            return False, ""

        return True
