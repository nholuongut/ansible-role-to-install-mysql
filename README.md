# Ansible role for Install MySQL

![](https://i.imgur.com/waxVImv.png)
### [View all Roadmaps](https://github.com/nholuongut/all-roadmaps) &nbsp;&middot;&nbsp; [Best Practices](https://github.com/nholuongut/all-roadmaps/blob/main/public/best-practices/) &nbsp;&middot;&nbsp; [Questions](https://www.linkedin.com/in/nholuong/)
<br/>

This role is designed to install MySQL Community Edition versions 8.0.x and
5.7.x.

## Goal

The initial goal for this role is to provide a method to provision macOS,
Ubuntu, RedHat and Windows with MySQL using the same role, so that
a single playbook may be used to provision all of these platforms for
software testing.

Important considerations before using this role:

- no attempt to provide the security that would be necessary for a production
  installation has been included
- an attempt to download the necessary installer directly from the vendor
  has been included (_Note: if you are trying to install a version different_
  _from the latest version--as defined in `defaults.yml`--you will need to_
  _provide the `mysql_installer_filename` value)_
- the role is designed to be able to specify particular versions to be
  installed, rather than simply "the latest" (Note: it may not be possible
  to install a specific version on RedHat or Ubuntu while this role is using
  the respective package managers)

## Requirements

This role is currently designed to be used with a MySQL installer downloaded
from the [MySQL web site](https://www.mysql.com) and placed locally on your
"controller" (the machine from which you are running the Ansible playbook). If
it cannot be found in any of the specified locations, the role will attempt to
download the installer directly to the target from the vendor's site.

If you are running Ansible 2.4 or above on macOS High Sierra or above, you may
want to learn more about an issue with "changes made in High Sierra that are
breaking lots of Python things that use fork()."
See Ansible issue [32499](https://github.com/ansible/ansible/issues/32499) for
more information.

Because of the above issue, you may want to include this line in your
`Vagrantfile` if you are using vagrant:

    ENV["VAGRANT_OLD_ENV_OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"

Or, export this information before executing the role:

    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

_Note: The provisioning of a Windows VM seems to be particularly sensitive to_
_this._

## Environment Variables

Variables that are particular to the environment from which you are running
the playbook can be supplied as environment variables so that they can be
"sourced" from a file in the environment.  This provides an easy way to
supply different paths to resources if you are using the roles on different
computers.

| Option                                | Default | Example                                  |
| :------------------------------------ | :------ | :--------------------------------------- |
| `MYSQL_VERSION`                       | none    | `8.0.15` or `5.7.25    `                 |
| `MYSQL_LINUX_LOCAL_INSTALLERS_PATH`   | none    | `/Users/Shared/Installers/Linux/MySQL`   |
| `MYSQL_MAC_LOCAL_INSTALLERS_PATH`     | none    | `/Users/Shared/Installers/macOS/MySQL`   |
| `MYSQL_WINDOWS_LOCAL_INSTALLERS_PATH` | none    | `/Users/Shared/Installers/Windows/MySQL` |
| `LINUX_LOCAL_INSTALLERS_PATH`         | none    | `/Users/Shared/Installers/Linux`         |
| `MAC_LOCAL_INSTALLERS_PATH`           | none    | `/Users/Shared/Installers/macOS`         |
| `WINDOWS_LOCAL_INSTALLERS_PATH`       | none    | `/Users/Shared/Installers/Windows`       |
| `MYSQL_LOCAL_INSTALLERS_PATH`         | none    | `/Users/Shared/Installers/MySQL`         |
| `LOCAL_INSTALLERS_PATH`               | none    | `/Users/Shared/Installers`               |

_Note: One or more of the `INSTALLERS_PATH` environment variables may be_
_defined and the role will search the paths in the above order until it_
_finds an installer._

## Role Variables

Variables that are targeted toward options to use during the execution of the
roles are left to be specified as role variables and can be specified in the
playbook itself or on the command line when running the playbook.

| Option                        | Default                       | Example                                                                                     |
| :---------------------------- | :---------------------------- | :------------------------------------------------------------------------------------------ |
| `mysql_version`               | `8.0.15`                      | `5.7.25`                                                                                    |
| `mysql_installers_path_list`  | [`/Users/Shared/Installers`]  | [`/Users/Shared/Installers/MySQL`,`/Users/myaccount/Desktop`]                               |
| `mysql_installer_filename`    | latest platform-specific file | `mysql-8.0.12-macos10.13-x86_64.dmg`                                                        |
| `mysql_root_password`         | `rootP@ssw0rd`                | `eYyYQ@J3>b+2XycnUu6`                                                                       |
| `mysql_authentication_plugin` | MySQL version dependent       | `mysql_native_password` or `caching_sha2_password`                                          |
| `mysql_databases`             | none                          | `testdb`                                                                                    |
| `mysql_users`                 | none                          | `- { name: 'testuser', host: 'localhost', password: 'testpass' }`                           |
| `mysql_user_access`           | none                          | `- { name: 'testuser', host: 'localhost', access: 'ALL', database: 'testdb', tables: '*' }` |

_Note: Using `myql_installers_path_list` might not be considered_
_"normal usage", but is supported for use in playbooks or other scenarios in_
_which it makes sense._

_Note: Using `mysql_installers_path` is still supported, but is deprecated_
_and will be removed with the next breaking change._

## Dependencies

Installation of MySQL on Windows requires the appropriate Visual C++
Redistributable for Visual Studio.  MySQL 5.7 requires 2013, while MySQL 8
requires 2015.  This role does not attempt to install these nor include a
dependency that will install these.

## Role Use

Use of this role consists of the following:

- Create a playbook
- Obtain and have the desired installer available locally on the ansible
  controller
- Provide the location of the installer on the controller as an environment
  variable, in the playbook or as an extra-var
- Provide the version of MySQL (must match the installer) as an environment
  variable, in the playbook or as an extra-var
- Run the playbook

### Example Playbooks

``` yaml
- name: Install default MySQL
    hosts: servers
    roles:
        - { role: kaos2oak.mysql }
```

_Note: See the `defaults.yml` file for the "default" MySQL version that will_
_be installed by the above playbook._

``` yaml
- name: Install MySQL 5.7.25
    hosts: servers
    vars:
        mysql_version: '5.7.25'
    roles:
        - { role: kaos2oak.mysql }
```

``` yaml
- name: Install MySQL 5.7.25 and create mydb
    hosts: servers
    vars:
        mysql_version: '5.7.25'
        mysql_authentication_plugin: mysql_native_password
        mysql_root_password: W7HgBBja*ELuiGRrnuJ
        mysql_databases:
            - mydb
        mysql_users:
            - { name: 'myuser', host: 'localhost', password: 'TGhXAgWTK*yGHd2' }
        mysql_user_access:
            - { name: 'myuser', host: 'localhost', access: 'ALL', database: 'mydb', tables: '*' }
    roles:
        - { role: kaos2oak.mysql }
```

``` yaml
- name: Install MySQL 8.0.15, create mydb and use the mysql_native_password auth plugin
    hosts: servers
    vars:
        mysql_version: '8.0.15'
        mysql_authentication_plugin: mysql_native_password
        mysql_root_password: W7HgBBja*ELuiGRrnuJ
        mysql_databases:
            - mydb
        mysql_users:
            - { name: 'myuser', host: 'localhost', password: 'TGhXAgWTK*yGHd2' }
        mysql_user_access:
            - { name: 'myuser', host: 'localhost', access: 'ALL', database: 'mydb', tables: '*' }
    roles:
        - { role: kaos2oak.mysql }
```

### Example Installer Locations

If you really want it to be quick and easy:

    export MYSQL_LOCAL_INSTALLERS_PATH="$HOME/Downloads"

Or, you could always move the installers to a more permanent default location
after downloading them and then point to that location:

    /Users/Shared/Installers/MySQL

If you like to keep things neat and organized, you might organize the installers
into folders, create a file named something like `setup` in a directory named
`my` in this repository (most contents of the `my` directory are part of the
.gitignore ignored files, so it will not be part of any commit) and then
`source` the file:

``` shell
# File: setup
export MYSQL_MAC_LOCAL_INSTALLERS_PATH="$HOME/Installers/Mac/MySQL"
export MYSQL_LINUX_LOCAL_INSTALLERS_PATH="$HOME/Installers/Linux/MySQL"
export MYSQL_WINDOWS_LOCAL_INSTALLERS_PATH="$HOME/Installers/Windows/MySQL"
```

    source my/setup

### Example MySQL Version

Since the MySQL version may be something that you want to change on the fly,
you probably don't want to include it in the `setup` file, but you can always
provide it on the command line before the ansible-playbook run:

    export MYSQL_VERSION=5.7.25

Or, provide it as an "extra-vars" role variable for the ansible-playbook run:

    -e "mysql_version=8.0.15"

And maybe the installer name, if you want the role to try to download an
installer that is not the latest:

    -e "mysql_version=8.0.12 mysql_installer_filename=mysql-8.0.12-macos10.13-x86_64.dmg"

### Example Playbook Runs

Assuming you have created a playbook named `k2o-mysql.yml`:

    ansible-playbook k2o-mysql.yml

    MYSQL_VERSION=5.7.25 ansible-playbook k2o-mysql.yml

    ansible-playbook k2o-mysql.yml -e "mysql_version=5.7.25"

If the playbook itself contains the version of MySQL, it might look like:

    ansible-playbook k2o-mysql-5.7.25.yml

## Role Testing

### Pre-requisites

[Molecule](https://molecule.readthedocs.io/en/latest/) is being used for
testing this role.

_Note: Windows testing with Molecule is not actively supported, so these tests_
_may not work._

You will need to install molecule and python support modules before running
the role tests:

    pip install molecule
    pip install docker-py

You also need to install the following before running the vagrant role tests:

    pip install python-vagrant

You may also need to run the following command prior to executing molecule
tests with vagrant (see [Requirements](#requirements)):

    export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

The 'verifier' for Windows is disabled as I have not yet been able to get the
testinfra verfication to work for Windows. If you have any experience or advice
in this area, please let me know.

### MySQL Versions in Molecule tests

To run the molecule tests for a particular MySQL version, you will need to
provide the `MYSQL_VERSION` as an environment variable and ensure the installer
is located locally in the appropriate ...`INSTALLERS_PATH` location. See
examples, below.

It is also possible to edit the `molecule.yml` file for a scenario and
specify the mysql_version like this:

    provisioner:
      name: ansible
      env:
        MYSQL_VERSION: 5.7.25

### Default Tests

No default tests are currently implemented.

### Ubuntu Tests

Ubuntu 18 & 16 via vagrant:

    molecule test --scenario-name ubuntu-vagrant

or

    MYSQL_VERSION=5.7.25 molecule test --scenario-name ubuntu-vagrant

### RedHat Tests

RedHat 7 & 6 via vagrant:

    molecule test --scenario-name redhat-vagrant

### macOS Tests

macOS 10.13, 10.12, 10.11 via vagrant:

    molecule test --scenario-name macos-vagrant

### Windows Tests

Window 2012r2 via vagrant (may not work):

    molecule test --scenario-name windows-vagrant

# 🚀 I'm are always open to your feedback.  Please contact as bellow information:
### [Contact ]
* [Name: nho Luong]
* [Skype](luongutnho_skype)
* [Github](https://github.com/nholuongut/)
* [Linkedin](https://www.linkedin.com/in/nholuong/)
* [Email Address](luongutnho@hotmail.com)

![](https://i.imgur.com/waxVImv.png)
![](Donate.png)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/nholuong)

# License
* Nho Luong (c). All Rights Reserved.🌟
