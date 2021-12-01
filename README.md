# LDAP (Microsoft AD) pack

This pack consists of Microsoft Active Directory LDAP actions.
Based on [python-ldap](https://www.python-ldap.org/) lib.

## Installation

### Dependencies

- `sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev`

## Configuration

### Interactive wizard

`st2 pack config ldap`

#### _Manual configuration_

Copy the example configuration in [ldap.yaml.example](./ldap.yaml.example)
to `/opt/stackstorm/configs/ldap.yaml` and edit as required.

- `ldap_address` - IP Address or FQDN of your LDAP server (e.g. `example.ad.local`)
- `ldap_domain` - Domainname (e.g. `example.ad.local`)
- `ldap_admin_username` - Admin User with CRUD rights
- `ldap_admin_password` - Admin User secret
- `ldap_base_dn` - OU where a user is created and searched
- `ldap_group_dn` - Group to which a user gets assigned
- `mail_sender_address` - Sender mail address
- `mail_text` - Mail content text as jinja syntax with username and password variable
- `mail_subject` - Mail Subject
- `mail_server` - FQDN or IP of the SMTP mail server


You can also use dynamic values from the datastore. See the
[docs](https://docs.stackstorm.com/reference/pack_configs.html) for more info.

## Workflows

### Orquesta

#### orquesta_add_user

Adds a LDAP user to the active directory.

**_Input:_**

- `mail` - _required_
- `password` - _optional_
  - if not set a random password will be generated
- `expires_in` - _optional_
  - default: never
- `expires_in_dimension` - _optional_
  - has to be used if expires_in is set
- `username` - _optional_

#### orquesta_delete_user

Deletes a LDAP user from the active directory.

**_Input:_**

- `username` - _required_
  - sAMAccountName is required
  - Regex values are allowed
- `only_expired_users` - _optional_
  - boolean: deletes only expired users if set to true
  - default: false

## Actions

- `get_user` - Action which retrieves details for a particular user.
- `create_user` - Action which creates a new LDAP user.
- `delete_user` - Action which deletes a particular user.
- `enable_user` - Action which enables a particular user.
- `disable_user` - Action which disables a particular user.
- `generate_password` - Action which creates a XKCD like password.
- `set_user_password` - Action which sets the password for a particular user.
- `set_user_group` - Action which adds a given user to the group defined in the `ldap_group_dn` config.
- `send_mail` - Action to send a mail with a given jinja template as content

## Aliases

- `orquesta_add_user` - only useful in combination with Slack
- `orquesta_delete_user` - only useful in combination with Slack

## Policies

None

## Rules

- `notify_on_user_deletion` - Makes a notification to your ChatOps-Bot if user deletion workflow is executed
- `remove_expired_users_daily` - Cronjob which removes all expired users

## Sensors

None
