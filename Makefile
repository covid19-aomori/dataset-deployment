.DEFAULT_GOAL := help
ProductId := ${ProductId}
Env := ${Env}
Stackname := $(ProductId)-$(Env)

## sam build
build:
	sam build --use-container

## Deploy
deploy: build
	sam deploy \
		--stack-name $(Stackname) \
		--s3-prefix $(Stackname) \
		--no-fail-on-empty-changeset \
		--parameter-overrides "ProductId=$(ProductId)" "Env=$(Env)"

## Deploy confirm-changeset
deploy_confirm_changeset: build
	sam deploy \
		--stack-name $(Stackname) \
		--s3-prefix $(Stackname) \
		--no-fail-on-empty-changeset \
		--parameter-overrides "ProductId=$(ProductId)" "Env=$(Env)" \
		--confirm-changeset

## Show help
help:
	@make2help $(MAKEFILE_LIST)

.PHONY: help
.SILENT:
