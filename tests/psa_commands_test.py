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


class InitTest(PySideAssistantCommandsTest):
    def testInitCommandHarmattan(self):
        with working_directory(self.path):
            command = 'psa init testproject-harmattan harmattan> /dev/null'
            self.runShellCommand(command)

        #assert all files are in place
        project_path = os.path.join(self.path, 'testproject-harmattan')

        self.assert_(os.path.isdir(project_path))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'testproject-harmattan.psa')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'testproject-harmattan.aegis')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'testproject-harmattan')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'MANIFEST.in')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'setup.py')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'testproject-harmattan.longdesc')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'stdeb.cfg')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'testproject-harmattan.desktop')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'qml')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'qml/MainPage.qml')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'qml/main.qml')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'testproject-harmattan.png')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-harmattan', 'README.assistant')))


    def testInitCommandFremantle(self):
        with working_directory(self.path):
            command = 'psa init testproject-fremantle fremantle > /dev/null'
            self.runShellCommand(command)

        #assert all files are in place
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'testproject-fremantle')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'testproject-fremantle.psa')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'MANIFEST.in')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'setup.py')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'testproject-fremantle.longdesc')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'stdeb.cfg')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'testproject-fremantle.desktop')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'qml')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'qml/main.qml')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'testproject-fremantle.png')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject-fremantle', 'README.assistant')))

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
