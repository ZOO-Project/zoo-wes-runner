# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Added GitHub Issue and Pull Request templates to standardise contributions

### Changed
- Included `hatch` environment configuration and test runner setup in `pyproject.toml`
- Reformatted source files for consistency with `black` and `isort` coding standards


## [v0.2.1] - 2026-06-16
### Fixed
- Fixed inheritance from `ZooWESRunner` to properly initialize instance properties

## [v0.2.0] - 2026-01-23
### Added
- Package is now officially available on PyPI: `pip install zoo-wes-runner`
- Added `zoo-runner-common` as an official dependency for shared runner functionality
- Added `zoo-template-common` as a dependency for reusable template utilities
- Added version bump script for automating release versioning
- Automated PyPI publish workflow triggered on new releases

### Changed
- Refactored `ZooWESRunner` constructor to accept only keyword arguments for improved API clarity
- Modularized the codebase by extracting shared logic into `zoo-runner-common` and `zoo-template-common`
- Updated package to support `zoo-runner-common` v0.1.2 and its new import paths (`from zoo_runner_common import ...`)
- Reuse of `ZooStub` aligned with updated `zoo-runner-common` integration
- Switched build backend to `hatchling`; version is now managed via `zoo_wes_runner/__about__.py`
- Removed GitHub version reference from package versioning

### Fixed
- Fixed inheritance: `ZooCalrissianRunner` now correctly inherits from `ZooWESRunner`

## [v0.1.0] - 2023-01-01
### Added
- Initial release of `zoo-wes-runner`
- `ZooWESRunner`: core runner class for submitting CWL Application Package jobs to a Workflow Execution Service (WES) endpoint, with support for TOIL on SLURM HPC clusters
- `ExecutionHandler` interface with pre/post-execution hooks, secrets management, pod environment variable and node selector configuration, output handling, and additional parameter support
- Support for connecting the ZOO-Project ADES to an HPC environment via the GA4GH WES API
- Core dependencies: `httpx>=0.24.1`, `cwl-utils`, `zoo-runner-common`
- MkDocs Material documentation site
- Python 3.8+ support (tested on 3.10, 3.11, 3.12)

[Unreleased]: https://github.com/ZOO-Project/zoo-wes-runner/compare/v0.2.1...HEAD
[v0.2.1]: https://github.com/ZOO-Project/zoo-wes-runner/compare/v0.2.0...v0.2.1
[v0.2.0]: https://github.com/ZOO-Project/zoo-wes-runner/compare/v0.1.0...v0.2.0
[v0.1.0]: https://github.com/ZOO-Project/zoo-wes-runner/releases/tag/v0.1.0