from setuptools import setup

setup(name='tweetpy',
      version='0.1.0',
      packages=['tweetpy'],
      entry_points={
          'console_scripts': [
              'tweetpy = tweetpy.__main__:main'
          ]
      },
      )