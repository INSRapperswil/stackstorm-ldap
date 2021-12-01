import ldap
import pytz
from lib.actions import BaseAction
from lib.formatters import tuple_list_to_list_of_dicts
from lib.formatters import datetime_to_absolute_adinterval
from lib.formatters import absolute_adinterval_to_datetime
from lib.formatters import datetime_to_string
from datetime import datetime


class GetUserAction(BaseAction):
    def run(self, username, only_expired_users):
        date_time = None

        if only_expired_users:
            date_time = datetime.now(tz=pytz.utc)

        userlist = self._connection.search_s(
            self._ldap_base_dn,
            ldap.SCOPE_SUBTREE,
            '(&(sAMAccountName={0})(objectClass=person)(accountExpires<={1}))'.format(username, datetime_to_absolute_adinterval(date_time)),
            [
                'name',
                'sAMAccountName',
                'accountExpires',
                'userAccountControl',
                'mail',
                'distinguishedName'
            ]
        )

        userlist = tuple_list_to_list_of_dicts(userlist)

        for user in userlist:
            user['accountExpires'] = datetime_to_string(absolute_adinterval_to_datetime(int(user.get('accountExpires'))))

        return userlist
