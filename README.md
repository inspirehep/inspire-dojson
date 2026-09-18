<!--
This file is part of INSPIRE.
Copyright (C) 2014-2017 CERN.

INSPIRE is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

In applying this license, CERN does not waive the privileges and immunities
granted to it by virtue of its status as an Intergovernmental Organization or
submit itself to any jurisdiction.
-->

# INSPIRE-DoJSON

INSPIRE-specific rules to transform from MARCXML to JSON and back.

## Installation

INSPIRE-DoJSON requires Python 3.11 or newer and Poetry 2.

```shell
poetry install
```

## Local development

```shell
poetry install --with test,dev
poetry run pytest
```

## Building the package

```shell
poetry build
```
