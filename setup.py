from distutils.core import setup
import os


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

app_name = 'vodkamartiniquiz'
app_name_len = len(app_name) + 1

for dirpath, dirnames, filenames in os.walk(app_name):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[app_name_len:] # Strip "app_name/" or "app_name\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(name='vodkamartiniquiz',
      version = __import__(app_name).get_version().replace(' ', '-'),
      description='The quiz files and directory structure for VodkaMartini',
      author='Alexis Bellido',
      author_email='alexis@ventanazul.com',
      url='https://github.com/alexisbellido/django-vodkamartini-quiz',
      download_url='https://github.com/alexisbellido/django-vodkamartini-quiz/tarball/master',
      package_dir={'vodkamartiniquiz': 'vodkamartiniquiz'},
      packages=packages,
      package_data={'vodkamartiniquiz': data_files},

      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities'],
      )
