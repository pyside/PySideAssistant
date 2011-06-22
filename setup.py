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

from distutils.core import setup
import glob

setup(name="pyside-assistant",
      scripts=['psa'],
      version='0.1.0',
      maintainer="Bruno Araujo",
      maintainer_email="bruno.araujo@indt.org.br",
      description="Helper scripts for creating PySide-based applications",
      long_description="""
       pyside-assistant is a set of helper scripts which aids the developer to create
       all needed files to successfully create a application using PySide, which can be
       easily built and deployed without additional tools.
      """,
      data_files=[('share/pyside-assistant/templates', glob.glob('templates/*')),
                  ('share/pyside-assistant/templates', ['README.assistant']),
                  ('share/pyside-assistant/scripts', glob.glob('scripts/*')), ],)
