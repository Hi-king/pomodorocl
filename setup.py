from distutils.core import setup, Command


class PyTest(Command):
    user_options = []
    def initialize_options(self): pass
    def finalize_options(self): pass
    def run(self):
        import sys, subprocess
        errno = subprocess.call([sys.executable, 'runtest.py'])
        raise SystemExit(errno)
setup(
    name='pomodoro',
    version='',
    packages=['test', 'test.timer', 'timer'],
    url='',
    license='',
    author='hiking',
    author_email='hikingko1@gmail.com',
    description='',
    cmdclass={'test': PyTest}
)
