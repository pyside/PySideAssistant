'''Unit tests for pyside-assistant commands'''

import unittest
import shutil
import os
import subprocess
import sys
import tempfile
from contextlib import contextmanager

import tarfile
import arfile

@contextmanager
def working_directory(path):
    '''Simple context manager to change the working directory'''
    current_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(current_dir)


class PySideAssistantCommandsTest(unittest.TestCase):

    def setUp(self):
        self.path = tempfile.mkdtemp(prefix='psatemp')
        shutil.rmtree(self.path, ignore_errors=True)
        os.makedirs(self.path)

    def tearDown(self):
        shutil.rmtree(self.path)

    def runShellCommand(self, command, verbose=False):
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        if proc.returncode:
            self.fail(stderr)

    def verifyDirectoryStructure(self, root, files):
        for filename in files:
            self.assert_(os.path.exists(os.path.join(root, filename)), msg='File %s not found' % filename)


class InitTest(PySideAssistantCommandsTest):
    def testInitCommandHarmattan(self):
        with working_directory(self.path):
            command = 'psa init testproject-harmattan harmattan> /dev/null'
            self.runShellCommand(command)

        #assert all files are in place
        project_path = os.path.join(self.path, 'testproject-harmattan')

        filenames = [
         'testproject-harmattan.psa',
         'testproject-harmattan.aegis',
         'testproject-harmattan',
         'MANIFEST.in',
         'setup.py',
         'testproject-harmattan.longdesc',
         'stdeb.cfg',
         'testproject-harmattan.desktop',
         'qml',
         'qml/MainPage.qml',
         'qml/main.qml',
         'testproject-harmattan.png',
         'README.assistant',
        ]

        self.verifyDirectoryStructure(project_path, filenames)

    def testInitCommandFremantle(self):
        with working_directory(self.path):
            command = 'psa init testproject-fremantle fremantle > /dev/null'
            self.runShellCommand(command)

        #assert all files are in place
        project_path = os.path.join(self.path, 'testproject-fremantle')

        filenames = [
         'testproject-fremantle.psa',
         'testproject-fremantle',
         'MANIFEST.in',
         'setup.py',
         'testproject-fremantle.longdesc',
         'stdeb.cfg',
         'testproject-fremantle.desktop',
         'qml',
         'qml/main.qml',
         'testproject-fremantle.png',
         'README.assistant',
        ]

        self.verifyDirectoryStructure(project_path, filenames)

    def testInitCommandUbuntu(self):
        with working_directory(self.path):
            command = 'psa init testproject-ubuntu ubuntu-qml > /dev/null'
            self.runShellCommand(command)

        #assert all files are in place
        project_path = os.path.join(self.path, 'testproject-ubuntu')

        filenames = [
         'testproject-ubuntu.psa',
         'testproject-ubuntu',
         'MANIFEST.in',
         'setup.py',
         'testproject-ubuntu.longdesc',
         'stdeb.cfg',
         'testproject-ubuntu.desktop',
         'qml',
         'qml/main.qml',
         'testproject-ubuntu.png',
         'README.assistant',
        ]

        self.verifyDirectoryStructure(project_path, filenames)

    def testInitCommandUbuntu(self):
        with working_directory(self.path):
            command = 'psa init testproject-ubuntu-gui ubuntu-qtgui > /dev/null'
            self.runShellCommand(command)

        #assert all files are in place
        project_path = os.path.join(self.path, 'testproject-ubuntu-gui')

        filenames = [
         'testproject-ubuntu-gui.psa',
         'testproject-ubuntu-gui',
         'MANIFEST.in',
         'setup.py',
         'testproject-ubuntu-gui.longdesc',
         'stdeb.cfg',
         'testproject-ubuntu-gui.desktop',
         'testproject-ubuntu-gui.png',
         'README.assistant',
        ]

        self.verifyDirectoryStructure(project_path, filenames)

    def testInitCommandParameters(self):
        #test long commands
        with working_directory(self.path):
            command = 'psa init testproject1 harmattan --section="games" --app-name="test app1" --category="Game" --description="a description1" > /dev/null'
            self.runShellCommand(command)

        f = open(os.path.join(self.path, 'testproject1', 'stdeb.cfg'))
        contents = f.read()
        f.close()
        self.assert_('Section: user/games' in contents)

        f = open(os.path.join(self.path, 'testproject1', 'testproject1.desktop'))
        contents = f.read()
        f.close()
        self.assert_('Name=test app1' in contents)
        self.assert_('Categories=Game;' in contents)

        f = open(os.path.join(self.path, 'testproject1', 'setup.py'))
        contents = f.read()
        f.close()
        self.assert_('description="a description1"' in contents)

        #test short commands
        command = ' '.join(['cd', self.path, ';', 'psa init testproject2 harmattan -s "network" -a "test app2" -c "Video" -d "a description2" > /dev/null'])
        self.runShellCommand(command)

        f = open(os.path.join(self.path, 'testproject2', 'stdeb.cfg'))
        contents = f.read()
        f.close()
        self.assert_('Section: user/network' in contents)

        f = open(os.path.join(self.path, 'testproject2', 'testproject2.desktop'))
        contents = f.read()
        f.close()
        self.assert_('Name=test app2' in contents)
        self.assert_('Categories=Video;' in contents)

        f = open(os.path.join(self.path, 'testproject2', 'setup.py'))
        contents = f.read()
        f.close()
        self.assert_('description="a description2"' in contents)


class BuildTest(PySideAssistantCommandsTest):


    def init_project(self, project, templatename):
        with working_directory(self.path):
            command = 'psa init %s %s > /dev/null' % (project, templatename)
            self.runShellCommand(command)

        return os.path.join(self.path, project)

    def build_deb(self, project, path):
        expected_deb = os.path.join(path, 'deb_dist', ('%s_0.1.0-1_all.deb' % project))
        with working_directory(os.path.join(self.path, project)):
            command = 'psa build-deb > /dev/null'
            self.runShellCommand(command)
        self.assert_(os.path.exists(expected_deb), msg="Debian file %s does not exist" % expected_deb)

        return expected_deb

    def check_deb_contents(self, deb, deb_contents):
        path = tempfile.mkdtemp(prefix='psa_deb')

        try:
            arfile.extract(deb, targetdir=path)

            rootfiles = deb_contents['root']
            for filename in rootfiles:
                self.assertTrue(os.path.exists(os.path.join(path, filename)))

            # control.tar.gz
            files = deb_contents['control']
            tar = tarfile.open(os.path.join(path, 'control.tar.gz'), 'r')

            try:
                for filename in files:
                    self.assertTrue(tar.getmember(filename))
            finally:
                tar.close()

            # data.tar.gz
            files = deb_contents['data']
            tar = tarfile.open(os.path.join(path, 'data.tar.gz'), 'r')

            try:
                for filename in files:
                    self.assertTrue(tar.getmember(filename))
            finally:
                tar.close()
        finally:
            shutil.rmtree(path)

    def base_debian_components(self):
        '''Base debian components common to all packages'''

        return {
                'root': ['debian-binary'],
                'control': [
                        './control',
                        './md5sums',
                        './postinst',
                ],
                'data': [
                ]
        }

    def testBuildHarmattan(self):

        project = 'foobar'

        path = self.init_project(project, 'harmattan')

        with open(os.path.join(path, project+'.aegis'), 'w') as handle:
            handle.write('The quick brown fox jumps over the lazy dog')

        deb = self.build_deb(project, path)

        deb_contents = self.base_debian_components()

        deb_contents['root'].append('./_aegis')
        deb_contents['control'].append('./digsigsums')
        deb_contents['data'].append('./usr/bin/%s' % project)
        deb_contents['data'].append('./usr/share/applications/%s.desktop' % project)
        deb_contents['data'].append('./usr/share/icons/hicolor/64x64/apps/%s.png' % project)
        deb_contents['data'].append('./usr/share/%s/qml/main.qml' % project)
        deb_contents['data'].append('./usr/share/%s/qml/MainPage.qml' % project)

        self.check_deb_contents(deb, deb_contents)

    def testBuildFremantle(self):
        project = 'foobar'

        path = self.init_project(project, 'fremantle')

        deb = self.build_deb(project, path)

        deb_contents = self.base_debian_components()

        deb_contents['data'].append('./usr/bin/%s' % project)
        deb_contents['data'].append('./usr/share/applications/hildon/%s.desktop' % project)
        deb_contents['data'].append('./usr/share/icons/%s.png' % project)
        deb_contents['data'].append('./opt/usr/share/%s/qml/main.qml' % project)

        self.check_deb_contents(deb, deb_contents)

    def testBuildUbuntu(self):
        project = 'foobar'

        path = self.init_project(project, 'ubuntu-qml')

        deb = self.build_deb(project, path)

        deb_contents = self.base_debian_components()

        deb_contents['data'].append('./usr/bin/%s' % project)
        deb_contents['data'].append('./usr/share/applications/%s.desktop' % project)
        deb_contents['data'].append('./usr/share/pixmaps/%s.png' % project)
        deb_contents['data'].append('./usr/share/%s/qml/main.qml' % project)

        self.check_deb_contents(deb, deb_contents)

    def testBuildUbuntuGui(self):
        project = 'foobar'

        path = self.init_project(project, 'ubuntu-qtgui')

        deb = self.build_deb(project, path)

        deb_contents = self.base_debian_components()

        deb_contents['data'].append('./usr/bin/%s' % project)
        deb_contents['data'].append('./usr/share/applications/%s.desktop' % project)
        deb_contents['data'].append('./usr/share/pixmaps/%s.png' % project)

        self.check_deb_contents(deb, deb_contents)

class UpdateTest(PySideAssistantCommandsTest):

    def testUpdateCommand(self):
        command = ' '.join(['cd', self.path, ';', 'psa init testproject harmattan > /dev/null'])
        self.runShellCommand(command)

        #test long commands
        command = ' '.join(['cd', os.path.join(self.path,'testproject'), ';', 'psa update --section="games" --app-name="test app1" --category="Game" --description="a description1" > /dev/null'])
        self.runShellCommand(command)
        f = open(os.path.join(self.path, 'testproject', 'stdeb.cfg'))
        contents = f.read()
        f.close()
        self.assert_('Section: user/games' in contents)

        f = open(os.path.join(self.path, 'testproject', 'testproject.desktop'))
        contents = f.read()
        f.close()
        self.assert_('Name=test app1' in contents)
        self.assert_('Categories=Game;' in contents)

        f = open(os.path.join(self.path, 'testproject', 'setup.py'))
        contents = f.read()
        f.close()
        self.assert_('description="a description1"' in contents)

        #test short commands
        command = ' '.join(['cd', os.path.join(self.path,'testproject'), ';', 'psa update -s "network" -a "test app2" -c "Video" -d "a description2" > /dev/null'])
        self.runShellCommand(command)

        f = open(os.path.join(self.path, 'testproject', 'stdeb.cfg'))
        contents = f.read()
        f.close()
        self.assert_('Section: user/network' in contents)

        f = open(os.path.join(self.path, 'testproject', 'testproject.desktop'))
        contents = f.read()
        f.close()
        self.assert_('Name=test app2' in contents)
        self.assert_('Categories=Video;' in contents)

        f = open(os.path.join(self.path, 'testproject', 'setup.py'))
        contents = f.read()
        f.close()
        self.assert_('description="a description2"' in contents)


if __name__ == "__main__":
    unittest.main()
