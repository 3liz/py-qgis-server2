
SDIST=dist

configure::
	@echo "Configuring $(PYTHON_PKG)"
	@sed -e 's/$${PIN_VERSION}/$(VERSION)/g' pyproject.toml.in > pyproject.toml

dist::
	mkdir -p $(SDIST)
	rm -rf *.egg-info
	$(PYTHON) setup.py sdist --dist-dir=$(SDIST)

clean::
	rm -rf $(SDIST) *.egg-info

deliver::
	twine upload -r storage $(SDIST)/*

lint::
	@ruff check $(PYTHON_PKG) $(TESTDIR)

lint-preview::
	@ruff check --preview $(PYTHON_PKG) $(TESTDIR)


install::
	pip install -U --upgrade-strategy=eager -e .

install-tests::
	pip install  -r $(topsrcdir)/tests/requirements.txt

autopep8::
	@ruff check --preview --fix $(PYTHON_PKG) $(TESTDIR)

typecheck::
	@mypy --config-file=$(topsrcdir)/config/mypy.ini -p $(PYTHON_PKG)

security::
	@bandit -r $(PYTHON_PKG)


.PHONY: $(REQUIREMENTS)

# Output frozen requirements
requirements: $(REQUIREMENTS)
	@echo "Optional dependencies: $(OPTIONAL_DEPENDENCIES)"
	@pipdeptree -p "$$($(DEPTH)/requirements.sh $(OPTIONAL_DEPENDENCIES))" -f \
		| sed "s/^[ \t]*//" | sed "/^\-e .*/d" \
		| sort | uniq > $<
	@echo "Requirements written in $<"


ifndef TESTDIR
test::
else
test:: lint-preview typecheck security
	cd $(TESTDIR) && pytest -v $(PYTEST_ARGS)
endif
