# This file is part of the PySide project.
#
# Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: PySide team <contact@pyside.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

import os
import sys
from distutils.core import setup
from distutils import sysconfig
from distutils import log
import shutil
import glob

setup(name="pyside-assistant",
            scripts=['psa'],
            data_files=[
                ('share/psa', ['README']),
                ('share/psa/templates/harmattan',
                        glob.glob('templates/harmattan/*.template') +
                        ['templates/harmattan/template.cfg']),
                ('share/psa/templates/harmattan/qml',
                        glob.glob('templates/harmattan/qml/*.template')),
                ('share/psa/templates/fremantle',
                        glob.glob('templates/fremantle/*.template') +
                        ['templates/fremantle/template.cfg']),
                ('share/psa/templates/fremantle/qml',
                        glob.glob('templates/fremantle/qml/*.template')),
                ('share/psa/templates/ubuntu-qml',
                        glob.glob('templates/ubuntu-qml/*.template') +
                        ['templates/ubuntu-qml/template.cfg']),
                ('share/psa/templates/ubuntu-qml/qml',
                        glob.glob('templates/ubuntu-qml/qml/*.template')),
                ('share/psa/templates/ubuntu-qtgui',
                        glob.glob('templates/ubuntu-qtgui/*.template') +
                        ['templates/ubuntu-qtgui/template.cfg']),
                ('share/psa/scripts', ['scripts/refhashmake.py', 'scripts/deb_add.py']),
            ],
            version='0.1.0',
            maintainer="Bruno Araujo",
            maintainer_email="bruno.araujo@indt.org.br",
            description="Helper scripts for creating PySide-based applications",
            long_description="""
            pyside-assistant is a set of helper scripts which aids the developer to create
            all needed files to successfully create a application using PySide, which can be
            easily built and deployed without additional tools.
            """,)
