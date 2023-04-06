SHELL := /bin/bash
APP_NAME = ragnarok-disguise

.PHONY: set_heroku_env
set_heroku_env:
	@echo "Setting Heroku environment variables from .env..."
	@( \
		while IFS='=' read -r key value; do \
			heroku config:set --app $(APP_NAME) $$key=$$value; \
		done < .env; \
	)
	@echo "Heroku environment variables set successfully."