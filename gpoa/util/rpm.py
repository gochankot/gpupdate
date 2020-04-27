#
# GPOA - GPO Applier for Linux
#
# Copyright (C) 2019-2020 BaseALT Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import subprocess
import rpm


def is_rpm_installed(rpm_name):
    '''
    Check if the package named 'rpm_name' is installed
    '''
    ts = rpm.TransactionSet()
    pm = ts.dbMatch('name', rpm_name)

    if pm.count() > 0:
        return True

    return False

class Package:
    __install_command = ['/usr/bin/apt-get', '-y', 'install']
    __remove_command = ['/usr/bin/apt-get', '-y', 'remove']
    __reinstall_command = ['/usr/bin/apt-get', '-y', 'reinstall']

    def __init__(self, package_name):
        self.package_name = package_name
        self.for_install = True

        if package_name.endswith('-'):
            self.package_name = package_name[:-1]
            self.for_install = False

        self.installed = is_rpm_installed(self.package_name)

    def mark_for_install(self):
        self.for_install = True

    def mark_for_removal(self):
        self.for_install = False

    def is_installed(self):
        return self.installed

    def is_for_install(self):
        return self.for_install

    def is_for_removal(self):
        return (not self.for_install)

    def action(self):
        if self.for_install:
            if not self.is_installed():
                return self.install()
        else:
            if self.is_installed():
                return self.remove()

    def install(self):
        fullcmd = self.__install_command
        fullcmd.append(self.package_name)
        return subprocess.check_call(fullcmd)

    def reinstall(self):
        fullcmd = self.__reinstall_command
        fullcmd.append(self.package_name)
        return subprocess.check_call(fullcmd)

    def remove(self):
        fullcmd = self.__remove_command
        fullcmd.append(self.package_name)
        return subprocess.check_call(fullcmd)

    def __repr__(self):
        return self.package_name

    def __str__(self):
        return self.package_name


def update():
    '''
    Update APT-RPM database.
    '''
    subprocess.check_call(['/usr/bin/apt-get', 'update'])

def install_rpm(rpm_names, force=True, single_call=True):
    '''
    Install RPM from APT-RPM sources.

    :param rpm_names: List of names of RPM packages to install
    :param force: Check if RPM is installed
    '''
    install_command = ['/usr/bin/apt-get', '-y', 'install']

    package_list = [Package(rpm_name) for rpm_name in rpm_names]

    update()

    filtered_package_list = list()
    if not force:
        for package in package_list:
            if (not package.is_installed()) and package.is_for_install():
                filtered_package_list.append(package)

            if package.is_installed() and package.is_for_removal():
                filtered_package_list.append(package)
    else:
        filtered_package_list = package_list()

    if len(filtered_package_list) > 0:
        if single_call:
            string_filtered_list = [str(x) for x in filtered_package_list]
            install_command.extend(string_filtered_list)
            subprocess.check_call(install_command)
        else:
            for package in filtered_package_list:
                package.action()

def remove_rpm(rpm_names, force=True, single_call=True):
    '''
    Remove RPM from file system.

    :param rpm_names: List of names of RPM packages to install
    :param force: Don't check if rpm is installed
    '''
    remove_command = ['/usr/bin/apt-get', '-y', 'remove']

    package_list = [Package(rpm_name) for rpm_name in rpm_names]

    filtered_package_list = list()
    if not force:
        for package in package_list:
            if package.is_installed() and package.is_for_removal():
                filtered_package_list.append(package)
    else:
        filtered_package_list = package_list

    if len(filtered_package_list) > 0:
        if single_call:
            string_filtered_list = [str(x) for x in filtered_package_list]
            remove_command.extend(string_filtered_list)
            subprocess.check_call(remove_command)
        else:
            for package in filtered_package_list:
                package.action()

