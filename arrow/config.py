from __future__ import print_function

import logging as std_logging
import os

from oslo_config import cfg

from oslo_log import log as logging


# (cfg.CONF) instance with a local instance (cfg.ConfigOpts()) once
# the cli tests move to the clients.  The cli tests rely on oslo
# incubator modules that use the global cfg.CONF.
_CONF = cfg.CONF

selenium_group = cfg.OptGroup(name='selenium',
                              title="Selenium Configuration Options")
SeleniumGroup = [
    cfg.StrOpt('hub_ip',
               help="Hub node ip address of the selenium-grid."),
    cfg.StrOpt('browser',
               help="The Docker Selenium node with browser installed for testing."),
]

identity_group = cfg.OptGroup(name='identity',
                              title="FMS Configuration Options")
IdentityGroup = [
    cfg.StrOpt('uri',
               help="IP address of FMS server."),
    cfg.StrOpt('username',
               help="Username of FMS server."),
    cfg.StrOpt('tenant_name',
               help="Tenant name to use for Nova API requests."),
    cfg.StrOpt('admin_role',
               default='admin',
               help="Role required to administrate keystone."),
    cfg.StrOpt('password',
               help="Password of FMS server.",
               secret=True),
    cfg.StrOpt('domain_name',
               help="Domain name for authentication (Keystone V3)."
                    "The same domain applies to user and project"),
]

fss_group = cfg.OptGroup(name='fss',
                              title="FSS server Configuration Options")

FSSGroup = [
    cfg.StrOpt('ip',
               help="IP address of the FSS server."),
    cfg.StrOpt('user',
               help="user name of the FSS server."),
    cfg.StrOpt('password',
               help="password of the FSS server."),
    cfg.StrOpt('pool_name',
               help="Default Storage Pool name of the FSS server."),
]

vdev_group = cfg.OptGroup(name='vdev',
                            title='Block Storage Options')

VdevGroup = [
    #cfg.StrOpt('disk_format',
    #           default='raw',
    #           help='Disk format to use when copying a vdev to image'),
    cfg.IntOpt('vdev_size',
               default=1,
               help='Default size in GB for vdevs created by vdevs tests'),
]

_opts = [
    (selenium_group, SeleniumGroup),
    (identity_group, IdentityGroup),
    (fss_group, FSSGroup),
    (vdev_group, VdevGroup)
]

def register_opts():
    for g, o in _opts:
        register_opt_group(_CONF, g, o)

def register_opt_group(conf, opt_group, options):
    conf.register_group(opt_group)
    for opt in options:
        conf.register_opt(opt, group=opt_group.name)

class ArrowConfigPrivate(object):
    """Provides FreeStor-Arrow configuration information."""

    DEFAULT_CONFIG_DIR = os.path.join(
        os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
        "etc")
    #DEFAULT_CONFIG_DIR = /usr/share/openstack-arrow-kilo/etc/

    DEFAULT_CONFIG_FILE = "arrow.conf"

    def __getattr__(self, attr):
        # Handles config options from the default group
        return getattr(_CONF, attr)
    
    def __init__(self, parse_conf=True, config_path=None):
        """Initialize a configuration from a conf directory and conf file."""
        super(ArrowConfigPrivate, self).__init__()
        config_files = []
        failsafe_path = "/etc/arrow/" + self.DEFAULT_CONFIG_FILE

        if config_path:
            path = config_path
        else:
            # Environment variables override defaults...
            conf_dir = os.environ.get('ARROW_CONFIG_DIR',
                                      self.DEFAULT_CONFIG_DIR)
            conf_file = os.environ.get('ARROW_CONFIG',
                                       self.DEFAULT_CONFIG_FILE)

            path = os.path.join(conf_dir, conf_file)

        if not os.path.isfile(path):
            path = failsafe_path

        # only parse the config file if we expect one to exist. This is needed
        # to remove an issue with the config file up to date checker.
        if parse_conf:
            config_files.append(path)
        logging.register_options(_CONF)
        if os.path.isfile(path):
            _CONF([], project='arrow', default_config_files=config_files)
        else:
            _CONF([], project='arrow')
        logging.setup(_CONF, 'arrow')
        LOG = logging.getLogger('arrow')
        LOG.info("Using arrow config file %s" % path)
        register_opts()
        self._set_attrs()
        if parse_conf:
            _CONF.log_opt_values(LOG, std_logging.DEBUG)

    def _set_attrs(self):
        #It will get the configs of arrow.conf 
        #self.auth = _CONF.auth
        self.identity = _CONF.identity
        #_CONF.set_default('domain_name', self.identity.admin_domain_name,
         #                 group='identity')
        #_CONF.set_default('alt_domain_name', self.identity.admin_domain_name,
         #                 group='identity')


class ArrowConfigProxy(object):
    _config = None
    _path = None

    _extra_log_defaults = [
        ('paramiko.transport', std_logging.INFO),
        ('requests.packages.urllib3.connectionpool', std_logging.WARN),
    ]

    def _fix_log_levels(self):
        """Tweak the oslo log defaults."""
        for name, level in self._extra_log_defaults:
            std_logging.getLogger(name).setLevel(level)

    def __getattr__(self, attr):
        if not self._config:
            self._fix_log_levels()
            self._config = ArrowConfigPrivate(config_path=self._path)

        return getattr(self._config, attr)

    def set_config_path(self, path):
        self._path = path


CONF = ArrowConfigProxy()
