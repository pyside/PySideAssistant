'''Unit tests for pyside-assistant commands'''

import unittest
import shutil
import os
import subprocess
import sys
import tempfile
from contextlib import contextmanager

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
    def testBuildDebCommand(self):
        with working_directory(self.path):
            command = 'psa init testproject harmattan > /dev/null'
            self.runShellCommand(command)
            with working_directory(os.path.join(self.path, 'testproject')):
                command = 'psa build-deb > /dev/null'
                self.runShellCommand(command)
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'deb_dist', 'testproject_0.1.0-1_all.deb')))

        #TODO test if icon was added.


    def testBuildDebCommandFremantle(self):
        with working_directory(self.path):
            command = 'psa init testproject fremantle > /dev/null'
            self.runShellCommand(command)
            with working_directory(os.path.join(self.path, 'testproject')):
                command = 'psa build-deb > /dev/null'
                self.runShellCommand(command)
                self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'deb_dist', 'testproject_0.1.0-1_all.deb')))


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
