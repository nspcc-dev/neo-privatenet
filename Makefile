B=\033[0;1m
G=\033[0;92m
R=\033[0m

ECHO="echo -e"

.PHONY: help up down privnet logs

# Show this help prompt
help:
	@echo '  Usage:'
	@echo ''
	@echo '    make <target>'
	@echo ''
	@echo '  Targets:'
	@echo ''
	@awk '/^#/{ comment = substr($$0,3) } comment && /^[a-zA-Z][a-zA-Z0-9_-]+ ?:/{ print "   ", $$1, comment }' $(MAKEFILE_LIST) | column -t -s ':' | grep -v 'IGNORE' | sort | uniq

# Follow containers logs
logs:
	@docker-compose logs -f

# Up private-net full environment
up: down
	@docker-compose up -d

# Stop private-net environment
down:
	@docker-compose down

# Kill private-net environment
kill:
	# kill containers
	@docker-compose kill
	# remove containers
	@docker-compose down

# Run only private-net without neo-scanner and postgresql
privnet: down
	@docker-compose up -d neo-privnet