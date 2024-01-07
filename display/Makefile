# get repo path from ../config.yml
REPO_PATH := $(shell grep 'repo_path:' ../config.yml | awk '{ print $$2 }')

Markdown_Docs_folder := $(shell grep 'Markdown_Docs_folder:' ../config.yml | awk '{ print $$2 }')

# get book name from REPO_PATH
BOOK_NAME := $(notdir $(REPO_PATH))
$(info BOOK_NAME is $(BOOK_NAME))
MARKDOWN_DOCS_FOLDER := $(Markdown_Docs_folder)
$(info MARKDOWN_DOCS_FOLDER is $(MARKDOWN_DOCS_FOLDER))
GITBOOK_PORT := 4000
GITBOOK_LRPORT := 30000

# info colors
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)


.PHONY: help
.PHONY: init_env env_install
.PHONY: init npm_install clear_book copy_book_json install
.PHONY: generate generate_repo_agent_books generate_summary


################################################################################
# We need nodejs 10.x to run gitbook, this target will install nodejs 10.x
################################################################################
env_install:
	chmod +x ./scripts/install-nodejs.sh
	./scripts/install-nodejs.sh

## init nodejs 10.x env
init_env: env_install
	echo "You have prepared nodejs 10.x  environment."



################################################################################
# The following targets are used to init the gitbook environment
################################################################################
### Install gitbook-cli
npm_install:
	npm install gitbook-cli -g

## clear repo generated book
clear_book:
	-rm -rf ./books/$(BOOK_NAME)

### copy book.json
copy_book_json: clear_book
	mkdir -p ./books/$(BOOK_NAME)
	cp ./book_template/book.json ./books/$(BOOK_NAME)/book.json

### gitbook install plugins
install:
	echo "You need to make sure you have installed nodejs 10.x."
	cd ./books/$(BOOK_NAME) && gitbook install

## gitbook init to install plugins
init: npm_install clear_book copy_book_json install
	@echo Compelete init docs book


################################################################################
# The following targets are used to generate the book and book.json for the gitbook
################################################################################
clear_src:
	-rm -rf ./books/$(BOOK_NAME)/src

generate_repo_agent_books:
	@echo "Generating Repo Agent books..."
	@python ./book_tools/generate_repoagent_books.py $(MARKDOWN_DOCS_FOLDER) $(BOOK_NAME) $(REPO_PATH)

generate_summary:
	@echo "Generating summary..."
	@python ./book_tools/generate_summary_from_book.py $(BOOK_NAME)

## generate repo book
generate: clear_src generate_repo_agent_books generate_summary
	@echo complete repo book: $(BOOK_NAME) generate

## serve gitbook
serve:  generate
	gitbook --port $(GITBOOK_PORT) --lrport $(GITBOOK_LRPORT) serve ./books/$(BOOK_NAME)


TASK_MAX_CHAR_NUM=30
## make help info
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<task>${RESET}'
	@echo ''
	@echo 'Tasks:'
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpInfo = match(lastLine, /^## (.*)/); \
		if (helpInfo) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpInfo = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TASK_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpInfo; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)