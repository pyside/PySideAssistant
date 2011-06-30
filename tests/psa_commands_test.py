'''Unit tests for pyside-assistant commands'''

import unittest
import shutil, os, subprocess

class PySideAssistantCommandsTest(unittest.TestCase):

    def setUp(self):
        self.path = '/tmp/psa-unittests'
        shutil.rmtree(self.path, ignore_errors=True)
        os.makedirs(self.path)
        command = ' '.join(['cd', self.path, ';', 'psa init testproject > /dev/null'])
        self.runShellCommand(command)

    def tearDown(self):
        shutil.rmtree(self.path)

    def runShellCommand(self, command, verbose=False):
        returnCode = subprocess.call(command, shell=True)
        if returnCode:
            raise Exception("Error running command: " + command)

    def testInitCommand(self):

        #assert all files are in place
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'testproject.aegis')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'testproject')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'MANIFEST.in')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'setup.py')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'testproject.longdesc')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'stdeb.cfg')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'testproject.desktop')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'qml')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'qml/MainPage.qml')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'qml/main.qml')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'testproject.png')))
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'README.assistant')))

    def testBuildDebCommand(self):
        command = ' '.join(['cd', os.path.join(self.path,'testproject'), ';', 'psa build-deb > /dev/null 2>&1'])
        self.runShellCommand(command)
        self.assert_(os.path.exists(os.path.join(self.path, 'testproject', 'deb_dist', 'testproject_0.1.0-1_all.deb')))

    def testUpdateCommand(self):
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


    def testInitCommandParameters(self):
        #test long commands
        command = ' '.join(['cd', self.path, ';', 'psa init testproject1 --section="games" --app-name="test app1" --category="Game" --description="a description1" > /dev/null'])
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
        command = ' '.join(['cd', self.path, ';', 'psa init testproject2 -s "network" -a "test app2" -c "Video" -d "a description2" > /dev/null'])
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

if __name__ == "__main__":
    unittest.main()
