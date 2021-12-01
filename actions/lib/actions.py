from st2actions.runners.pythonrunner import Action
import ldap


class BaseAction(Action):
    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self._ldap_address = self.config.get('ldap_address')
        self._ldap_username = self.config.get('ldap_admin_username')
        self._ldap_password = self.config.get('ldap_admin_password')
        self._ldap_domain = self.config.get('ldap_domain')
        self._ldap_base_dn = self.config.get('ldap_base_dn')
        self._ldap_group_dn = self.config.get('ldap_group_dn')
        self._connection = self._authenticate()

    def _authenticate(self):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        ldap_connection = ldap.initialize('ldaps://' + self._ldap_address + ':636')
        ldap_connection.protocol_version = 3
        ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
        ldap_connection.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
        ldap_connection.set_option(ldap.OPT_X_TLS_DEMAND, True)
        ldap_connection.set_option(ldap.OPT_DEBUG_LEVEL, 255)

        ldap_connection.simple_bind_s(self._ldap_username, self._ldap_password)

        return ldap_connection


class ActiveDirectoryUser:
    pass
