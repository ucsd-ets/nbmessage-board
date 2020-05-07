import setuptools, os

# get paths to all the extension files
extension_files = []
for (dirname, dirnames, filenames) in os.walk("nbmessage_board/nbextensions"):
    root = os.path.relpath(dirname, "nbmessage_board")
    for filename in filenames:
        if filename.endswith(".pyc"):
            continue
        extension_files.append(os.path.join(root, filename))

# get paths to all the static files and templates
static_files = []
for (dirname, dirnames, filenames) in os.walk("nbmessage_board/extensions/message"):
    root = os.path.relpath(dirname, "nbmessage_board/extensions/message")
    for filename in filenames:
        static_files.append(os.path.join(root, filename))

setuptools.setup(
    name="nbmessage_board",
    version='0.1.0',
    url="",
    author="Wesley Uykimpang",
    description="Discuss what's happening in a jupyter notebook",
    packages=setuptools.find_packages(),
    install_requires=[
        "markdown2",
        "pyyaml"
    ],
    setup_requires = ['pytest-runner'],
    tests_require = ['pytest'],
    package_data={'nbmessage_board': extension_files,
                  'nbmessage_board.extensions.message': static_files
                },
)
