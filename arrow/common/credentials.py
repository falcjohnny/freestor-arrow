import os

from tempest.common import accounts
from tempest.common import cred_provider
from tempest.common import isolated_creds
from tempest import config
from tempest import exceptions

CONF = config.CONF
#CONF should be the "/var/lib/jenkins/jobs/Python_Unittest_Selenium/workspace/freestor-arrow/etc/arrow.conf"
#Account not used, ignore it now
def get_isolated_credentials(name):
    # If a test requires a new account to work, it can have it via forcing
    # tenant isolation. A new account will be produced only for that test.
    # In case admin credentials are not available for the account creation,
    # the test should be skipped else it would fail.
    #if CONF.auth.allow_tenant_isolation or force_tenant_isolation:
    #    return isolated_creds.IsolatedCreds(
    #        name=name,
    #        network_resources=network_resources,
    #        identity_version=identity_version)
    #else:
        #CONF.auth.test_accounts_file means arrow.conf->[auth]->test_accounts_file
        #test_accounts_file = /usr/share/openstack-tempest-kilo/etc/accounts.yaml
        #We can use two kinds of configuration files : arrow.conf or account.yaml
        if (CONF.auth.test_accounts_file and
                os.path.isfile(CONF.auth.test_accounts_file)):
            # Most params are not relevant for pre-created accounts
            return accounts.Accounts(name=name,
                                     identity_version=identity_version)
        else:
            return accounts.NotLockingAccounts(
                name=name, identity_version=identity_version)



