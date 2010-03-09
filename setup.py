from setuptools import setup, find_packages

readme = open("chimpy/README.txt").read()

setup(name='chimpy',
      version='1.2',
      description='Python wrapper for the MailChimp API',
      long_description=readme,
      classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords = 'email mail mailinglist newsletter',
      author='James Casbon, Anton Stonor, Andrew Ingram',
      author_email='andy@andrewingram.net,
      url = 'http://code.google.com/p/chimpy/',
      license = 'New BSD License',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
        'simplejson', ]
      )
