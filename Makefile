include ../deploy/Makefile.vars

SITE_FLAG=../var/core.site-packages

all: ${SITE_FLAG} help

help:
	@echo To run
	@echo make actor.service
	@echo make radius.service
	@echo make rpc.service

${SITE_FLAG}: requrements.txt ${PYTHON}
	${PYTHON} -m pip install -r requrements.txt
	touch ${SITE_FLAG}

%.service: ${PYTHON} ${SITE_FLAG} ${RABBIT}
	${PYTHON} -m $@
