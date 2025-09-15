# django-blasphemy

Django development playground. It's for when you need to try something but the project in front of you is too complex / big / important to test stuff on it. Can be used as project starter if you have that kind of energy.

## Prerequisites
- A terminal emulator.
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [just](https://just.systems/man/en/)
- [prek](https://github.com/j178/prek?tab=readme-ov-file#installation)
- [git-lfs](https://git-lfs.github.com/)
- A modern web browser.

## Setup
> Make sure that you have an up to date version of Docker and [just](https://just.systems/man/en/) is installed.

* Copy `.env.dist` to `.env` and update it as you need.
* Run `just build` to build docker compose services.
* Run `just init_data` to initialize the database and create a superuser.
* Run `just up` to start the project.

The project homepage can be accessed at `http://localhost:8000/`.

## Troubleshooting

### Git LFS
* Installation: Follow the installation steps for your OS/tooling: https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage.
* If you are having issues with LFS files, like missing file content, ensure that:
  * LFS is installed and working fine, by using `git lfs -v`.
  * Hooks are installed, by using `git lfs install`.
  * Files are pulled successfully, by using `git lfs pull`.

# Contribution
Install git hooks by `prek install`
