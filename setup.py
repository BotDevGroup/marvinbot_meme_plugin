from distutils.core import setup
from setuptools import find_packages

# apt-get install libtiff5-dev libjpeg-dev zlib1g-dev libfreetype6-dev

REQUIREMENTS = [
    'marvinbot','pillow'
]

setup(name='marvinbot-meme-plugin',
      version='0.1',
      description='Meme Generator',
      author='Conrado Reyes',
      author_email='coreyes@gmail.com',
      url='',
      packages=[
        'marvinbot_meme_plugin',
      ],
      package_dir={
        'marvinbot_meme_plugin':'marvinbot_meme_plugin'
      },
      zip_safe=False,
      include_package_data=True,
      package_data={'': ['*.ini']},
      install_requires=REQUIREMENTS,
      dependency_links=[
          'git+ssh://git@github.com:BotDevGroup/marvin.git#egg=marvinbot',
      ],
)
