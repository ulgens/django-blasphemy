# Pass args if command is `manage`
ifeq (manage, $(firstword $(MAKECMDGOALS)))
   MANAGE_ARGS := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
   $(eval $(MANAGE_ARGS):;@:)
endif

build:
	docker-compose build --progress plain
up:
	docker-compose up
down:
	docker-compose down
# calling like this: make -- manage migrate
# About "--": https://stackoverflow.com/questions/2214575/passing-arguments-to-make-run#comment29441378_14061796
manage:
	docker-compose run --rm django python manage.py $(MANAGE_ARGS)
shell:
	docker-compose run --rm django python manage.py shell_plus
bash:
	docker-compose run --rm django bash
test:
	docker-compose run --rm django python -Wd manage.py test --parallel
test_fast:
	docker-compose run --rm django python -Wd manage.py test --keepdb --failfast --parallel
