develop: install-requirements setup-git

upgrade: install-requirements

setup-git:
	pre-commit install
	git config branch.autosetuprebase always
	git config --bool flake8.strict true

install-requirements:
	pdm install
