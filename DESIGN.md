# Project Design

## Overview

Bartender assigns versions to versionless packages in the dependency file, based on the timestamp of the last modification to that file.

## Task

To restore versions for an outdated project that relies on wildcard versions of packages.

### Selected Approach

A package is considered suitable if its version is the latest version available on pypi.org at the time of the last modification to the dependency file ([why?](#timestamp-of-dependency-file-as-a-point-of-reference)).

## Architecture Overview

The program’s operation is divided into 3 stages, which will be discussed below.

### Retrieving Information from the Repository

The logic for this stage is handled by [git](bartender/git.py), which finds the last commit in which the dependency file was modified. The date and time of this commit are then used as parameters when making requests to pypi.org, thereby filtering out all versions that were released after that time.

### Retrieving Information from Configuration Files

Depending on the type of file, either [pyproject interactor](bartender/interactor/pyproject/__init__.py) or [requirements interactor](bartender/interactor/requirements/__init__.py) handles the file ([why?](#output-to-file)). These interactors read the dependencies and convert them into a format that’s easy to process.

### Making Requests to pypi.org

The main processing takes place in [pypi](bartender/pypi/client.py), which sends requests to `https://pypi.org/pypi/{package_name}/json` ([why PyPI?](#pypi-as-a-source-of-truth)). Using asyncio, requests for each package are processed in parallel.

### Saving Results to a File or Displaying Them on the Screen

If the --dry-run flag is used, results are displayed in the console instead of being saved to a file. Otherwise, saving to a file is handled by the appropriate interactor, depending on the file type.

#### Displaying Results in the Console

The interactor outputs a string in the format of the input file—either a list of dependencies for requirements.txt or the dependencies section from pyproject.toml.

Example for a .toml file:
```
dependencies = [
    "dep1",
    "dep2"
]
```

#### Saving Results to a File

The interactor updates the file with the new dependencies. It should be noted that the .toml format is difficult to handle consistently programmatically. Therefore, in the current version, saving to a file is only possible for requirements.txt. For .toml files, it’s recommended to use --dry-run and manually edit the file.

## Solutions

### Timestamp of Dependency File as a Point of Reference

1) When a package isn’t specified with a version, it refers to the latest version.
2) Bartender assumes that no changes have been made to the latest version between when the project was used and when the file was last modified.
3) Therefore, by knowing the timestamp of the commit, we can likely find a working version of the package for the project.

### PyPI as a Source of Truth

PyPI is the main repository that most users rely on. Given Bartender’s goal of “reviving” old repositories, this is a reasonable compromise between complexity and usefulness.

### Interactors Are Exposed in the Interface

Although, in most cases, there will still be two formats: pyproject.toml and requirements.txt, there are two reasons for this:

1) Their creation is handled by a function that returns an interface; otherwise, we would have to give up on typing.
2) It’s possible to introduce a third format for internal use. Bartender won’t get in the way of such changes.