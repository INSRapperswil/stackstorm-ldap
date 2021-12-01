import ldap
import ldap.modlist as modlist
from lib.actions import BaseAction
from lib.actions import ActiveDirectoryUser
from lib.formatters import to_dict
from lib.formatters import datetime_to_absolute_adinterval
from lib.formatters import datetime_to_string
from datetime import timedelta
from datetime import datetime
import pytz


class CreateUserAction(BaseAction):
    def run(self, email, expiration, time_dimension, username=None):
        user_obj = ActiveDirectoryUser()
        user_obj.base_dn = "{0}".format(self._ldap_base_dn)
        # cut username after 20 caracters, because of max. field size in AD
        user_obj.username = (username[:20] if username else email.split("@")[0][:20])
        user_obj.distinguishedName = "cn={0},{1}".format(
            user_obj.username, self._ldap_base_dn
        )
        user_obj.domain = "{0}".format(self._ldap_domain)

        if expiration:
            user_obj.accountExpires = datetime.now(tz=pytz.utc) + timedelta(
                **{time_dimension: expiration}
            )

        else:
            user_obj.accountExpires = None

        user_attributes = {
            "objectClass": [b"top", b"person", b"organizationalPerson", b"user"],
            "cn": str(user_obj.username).encode("utf-8"),
            "userPrincipalName": "{0}@{1}".format(user_obj.username, user_obj.domain).encode("utf-8"),
            "sAMAccountName": str(user_obj.username).encode("utf-8"),
            "givenName": b"INS",
            "sn": b"INS",
            "displayName": b"INS",
            "userAccountControl": b"514",
            "mail": "{0}".format(email).encode("utf-8"),
            "accountExpires": "{0}".format(
                datetime_to_absolute_adinterval(user_obj.accountExpires)
            ).encode("utf-8"),
        }

        user_ldif = modlist.addModlist(user_attributes)
        user_obj.accountExpires = datetime_to_string(user_obj.accountExpires)

        try:
            self._connection.add_s(user_obj.distinguishedName, user_ldif)
        except ldap.LDAPError as e:
            if "desc" in e.message:
                self.logger.error(e.message["desc"])
            else:
                self.logger.error(e)
            return False, to_dict(user_obj)

        return True, to_dict(user_obj)
