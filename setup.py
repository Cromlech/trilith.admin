from setuptools import setup, find_packages
import os

version = '0.1'

install_requires = [
    'barrel',
    'crom',
    'cromlech.browser',
    'cromlech.configuration',
    'cromlech.dawnlight',
    'cromlech.grok',
    'cromlech.i18n',
    'cromlech.location',
    'cromlech.webob',
    'dolmen.forms.base',
    'dolmen.forms.ztk',
    'dolmen.message',
    'dolmen.tales',
    'dolmen.view',
    'dolmen.viewlet',
    'setuptools',
    'zope.interface',
    'zope.location',
    ]

tests_require = [
    ]

setup(name='trilith.admin',
      version=version,
      description="Trilith UI based on the Cromlech Framework",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='Admin Trilith',
      author='Dolmen Team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['trilith', ],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
