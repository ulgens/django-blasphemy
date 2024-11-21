# django-blasphemy

Django development playground. It's for when you need to try something but the project in front of you is too complex / big / important to test stuff on it. Can be used as project starter if you have that kind of energy.

* Before first run, cp `env.sample` to `.env` and update it as you like.
* For docker build, [Buildkit](https://docs.docker.com/develop/develop-images/build_enhancements/#to-enable-buildkit-builds) must be enabled. If Buildkit is not enabled system or user wide, docker related commands should be called like
`DOCKER_BUILDKIT=1 make build` or `DOCKER_BUILDKIT=1 docker-compose build`

# Contribution

Install pre-commit hooks by `pre-commit install`
