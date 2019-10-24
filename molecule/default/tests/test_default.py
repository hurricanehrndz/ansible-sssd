import os

import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_sssd_conf(host):
    conf = host.file('/etc/sssd/sssd.conf')

    assert conf.exists
    assert conf.user == 'root'
    assert conf.group == 'root'


def test_sssd_conf_content(host):
    conf = host.file('/etc/sssd/sssd.conf')
    conf_content = conf.content

    expected = [
        b'config_file_version = 2',
        b'services = nss, pam, ssh, sudo',
        b'domains = contoso.com',
        b'default_domain_suffix = contoso.com',
        b'filter_groups = root',
        b'filter_users = root',
        b'reconnection_retries = 3',
        b'[domain/contoso.com]',
        b'ad_domain = contoso.com',
        b'krb5_realm = contoso.com'
    ]

    for line in expected:
        assert line in conf_content


def test_apparmor_home_tunable(host):
    conf = host.file('/etc/apparmor.d/tunables/home.d/ansible')

    assert conf.exists
    assert conf.user == 'root'
    assert conf.group == 'root'
    assert conf.mode == 0o644

    conf_content = conf.content
    expected_line = b'@{HOMEDIRS}+=/home/contoso.com/'
    assert expected_line in conf_content


def test_smb_conf(host):
    conf = host.file('/etc/samba/smb.conf')

    assert conf.exists
    assert conf.user == 'root'
    assert conf.group == 'root'
    assert conf.mode == 0o644


@pytest.mark.parametrize("expected_line", [
    b'realm = CONTOSO.COM',
    b'workgroup = CONTOSO',
    b'idmap config CONTOSO:backend = ad',
    b'idmap config CONTOSO:schema_mode = rfc2307',
    b'idmap config CONTOSO:range = 10000-999999',
    b'idmap config CONTOSO:unix_nss_info = yes',
    b'kerberos method = secrets and keytab',
    b'security = ads'
])
def test_smb_conf_contents(host, expected_line):
    conf = host.file('/etc/samba/smb.conf')
    conf_content = conf.content

    assert expected_line in conf_content


@pytest.mark.parametrize("expected_line", [
    b'PasswordAuthentication no',
    b'AuthorizedKeysCommand /usr/bin/sss_ssh_authorizedkeys',
    b'AuthorizedKeysCommandUser nobody'
])
def test_sshd_config(host, expected_line):
    config = host.file('/etc/ssh/sshd_config')
    config_contents = config.content

    assert expected_line in config_contents
