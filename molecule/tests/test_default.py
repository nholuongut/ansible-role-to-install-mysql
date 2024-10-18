import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def get_mysql_version():
    return os.getenv('MYSQL_VERSION', '8.0.13')


def get_mysql_root_password():
    return os.getenv('MYSQL_ROOT_PASSWORD', 'root')


def get_mysql_exec_path(host):
    os = host.system_info.distribution
    if os == 'Mac OS X':
        return '/usr/local/mysql/bin/mysql'
    else:
        return 'mysql'


def get_mysql_installer_filename(host):
    os = host.system_info.distribution
    mysql_version = get_mysql_version()
    if os.lower() in ['ubuntu', 'debian']:
        mysql_installer_filename = 'mysql-apt-config_0.8.10-1_all.deb'
    elif os.lower() in ['centos', 'rhel', 'red hat enterprise linux server']:
        release = host.system_info.release
        if release.startswith('7'):
            mysql_installer_filename = 'mysql80-community-release-el7-1.noarch.rpm'
        else:
            mysql_installer_filename = 'mysql80-community-release-el6-1.noarch.rpm'
    elif os == 'Mac OS X':
        mysql_installer_filename = 'mysql-' + mysql_version + '-macos10.'
    else:
        mysql_installer_filename = 'unknown-' + os
    return mysql_installer_filename


def get_path_separator():
    return '/'


def get_temp_dir():
    return '/tmp'


@pytest.fixture(scope='module')
def test_vars(host):
    test_vars = {
        'mysql_version': get_mysql_version(),
        'mysql_installer_filename': get_mysql_installer_filename(host),
        'mysql_root_password': get_mysql_root_password(),
        'path_separator': get_path_separator(),
        'temp_dir': get_temp_dir(),
        'mysql_database': 'moleculetestdb',
        'mysql_user': 'moleculetestuser'
    }
    return test_vars


def test_mysql_version_installed(host, test_vars):
    mysql_exec_path = get_mysql_exec_path(host)
    result = host.run(mysql_exec_path + " --version")
    assert test_vars['mysql_version'] in result.stdout


def test_root_mysql_user(host, test_vars):
    mysql_exec_path = get_mysql_exec_path(host)
    result = host.run(mysql_exec_path + " -u root -p" +
                      test_vars['mysql_root_password'] + " -e \"SELECT VERSION();\"")
    assert test_vars['mysql_version'] in result.stdout


def test_mysql_database(host, test_vars):
    mysql_exec_path = get_mysql_exec_path(host)
    result = host.run(mysql_exec_path + " -u root -p" +
                      test_vars['mysql_root_password'] + " -e \"SHOW DATABASES;\"")
    assert test_vars['mysql_database'] in result.stdout


def test_mysql_user(host, test_vars):
    mysql_exec_path = get_mysql_exec_path(host)
    result = host.run(mysql_exec_path + " -u root -p" +
                      test_vars['mysql_root_password'] + " -e \"SELECT User FROM mysql.user;\"")
    assert test_vars['mysql_user'] in result.stdout
