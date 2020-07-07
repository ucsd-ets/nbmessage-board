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
    version='0.0.0',
    url="https://github.com/ucsd-ets/nbmessage-board",
    author="Wesley Uykimpang",
    description="Post messages in a jupyter notebook to other users",
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: Education"
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        "pyyaml",
        "beautifulsoup4",
        "oo-tools==0.2.0",
        "markdown"
    ],
    setup_requires = ['pytest-runner'],
    tests_require = [
        'pytest',
        'selenium'
    ],
    include_package_data=True,
    data_files=[('/var/lib/nbmessage-board/test2', [])],
    package_data={
        'nbmessage_board': extension_files,
        'nbmessage_board.extensions.message': static_files,
        '/var/lib/nbmessage-board/test2': static_files
    },
)
