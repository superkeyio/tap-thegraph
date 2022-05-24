# tap-thegraph

`tap-thegraph` is a [Singer](https://www.singer.io/) tap for [The Graph](https://thegraph.com/en/) built with the [Meltano Tap SDK](https://sdk.meltano.com).

## Quickstart

```bash
# 1. Install our packages for extracting subgraph data.
npm install -g graphql-api-to-json-schema
pipx install tap-thegraph

# 2. Install a Singer target for loading the data to a destination (for example, CSV).
pipx install target-csv

# 3. Configure which subgraphs and entities to extract (for example, all markets on Compound V2).
echo "{\"subgraphs\":[{\"url\":\"https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2\",\"entities\":[{\"name\":\"Market\"}]}]}" >> config.json

# 4. Run the pipeline!
tap-thegraph --config config.json | target-csv
```



## Installation


```bash
npm install -g graphql-api-to-json-schema # Needed for converting the GraphQL API schema for a subgraph to JSON schema
pipx install tap-thegraph
```

## Configuration

You must pass in a JSON file following this format:
```json
{
  "subgraphs": [
    {
      "url": "<SUBGRAPH_URL>",
      "entities": [
        { "name": "<ENTITY_NAME>" }, 
        { "name": "<ENTITY_NAME>", "created_at": "<TIMESTAMP_OR_BLOCK_NUMBER_FIELD>" }, 
        ...
      ]
    },
    ...
  ]
}
```

For each entity that you want to extract, you must specify the `name` (ex: `Market`) and, optionally, `created_at`, which is the name of a timestamp / block number field corresponding to when the entity was created. 

Specifying `created_at` for an entity enables "incremental" replication, which means that we can re-run the tap and resume where we left off instead of replicating everything again ("full table" replication).

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-thegraph --about
```

## Usage


### Executing the Tap Directly

```bash
tap-thegraph --version
tap-thegraph --help
tap-thegraph --config CONFIG --discover > ./catalog.json
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_thegraph/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-thegraph` CLI interface directly using `poetry run`:

```bash
poetry run tap-thegraph --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-thegraph
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-thegraph --version
# OR run a test `elt` pipeline:
meltano elt tap-thegraph target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
