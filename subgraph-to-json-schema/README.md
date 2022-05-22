oclif-hello-world
=================

oclif example Hello World CLI

[![oclif](https://img.shields.io/badge/cli-oclif-brightgreen.svg)](https://oclif.io)
[![Version](https://img.shields.io/npm/v/oclif-hello-world.svg)](https://npmjs.org/package/oclif-hello-world)
[![CircleCI](https://circleci.com/gh/oclif/hello-world/tree/main.svg?style=shield)](https://circleci.com/gh/oclif/hello-world/tree/main)
[![Downloads/week](https://img.shields.io/npm/dw/oclif-hello-world.svg)](https://npmjs.org/package/oclif-hello-world)
[![License](https://img.shields.io/npm/l/oclif-hello-world.svg)](https://github.com/oclif/hello-world/blob/main/package.json)

<!-- toc -->
* [Usage](#usage)
* [Commands](#commands)
<!-- tocstop -->
# Usage
<!-- usage -->
```sh-session
$ npm install -g subgraph-to-json-schema
$ subgraph-to-json-schema COMMAND
running command...
$ subgraph-to-json-schema (--version)
subgraph-to-json-schema/0.0.0 darwin-x64 node-v16.15.0
$ subgraph-to-json-schema --help [COMMAND]
USAGE
  $ subgraph-to-json-schema COMMAND
...
```
<!-- usagestop -->
# Commands
<!-- commands -->
* [`subgraph-to-json-schema hello PERSON`](#subgraph-to-json-schema-hello-person)
* [`subgraph-to-json-schema hello world`](#subgraph-to-json-schema-hello-world)
* [`subgraph-to-json-schema help [COMMAND]`](#subgraph-to-json-schema-help-command)
* [`subgraph-to-json-schema plugins`](#subgraph-to-json-schema-plugins)
* [`subgraph-to-json-schema plugins:install PLUGIN...`](#subgraph-to-json-schema-pluginsinstall-plugin)
* [`subgraph-to-json-schema plugins:inspect PLUGIN...`](#subgraph-to-json-schema-pluginsinspect-plugin)
* [`subgraph-to-json-schema plugins:install PLUGIN...`](#subgraph-to-json-schema-pluginsinstall-plugin-1)
* [`subgraph-to-json-schema plugins:link PLUGIN`](#subgraph-to-json-schema-pluginslink-plugin)
* [`subgraph-to-json-schema plugins:uninstall PLUGIN...`](#subgraph-to-json-schema-pluginsuninstall-plugin)
* [`subgraph-to-json-schema plugins:uninstall PLUGIN...`](#subgraph-to-json-schema-pluginsuninstall-plugin-1)
* [`subgraph-to-json-schema plugins:uninstall PLUGIN...`](#subgraph-to-json-schema-pluginsuninstall-plugin-2)
* [`subgraph-to-json-schema plugins update`](#subgraph-to-json-schema-plugins-update)

## `subgraph-to-json-schema hello PERSON`

Say hello

```
USAGE
  $ subgraph-to-json-schema hello [PERSON] -f <value>

ARGUMENTS
  PERSON  Person to say hello to

FLAGS
  -f, --from=<value>  (required) Whom is saying hello

DESCRIPTION
  Say hello

EXAMPLES
  $ oex hello friend --from oclif
  hello friend from oclif! (./src/commands/hello/index.ts)
```

_See code: [dist/commands/hello/index.ts](https://github.com/mattevenson/hello-world/blob/v0.0.0/dist/commands/hello/index.ts)_

## `subgraph-to-json-schema hello world`

Say hello world

```
USAGE
  $ subgraph-to-json-schema hello world

DESCRIPTION
  Say hello world

EXAMPLES
  $ oex hello world
  hello world! (./src/commands/hello/world.ts)
```

## `subgraph-to-json-schema help [COMMAND]`

Display help for subgraph-to-json-schema.

```
USAGE
  $ subgraph-to-json-schema help [COMMAND] [-n]

ARGUMENTS
  COMMAND  Command to show help for.

FLAGS
  -n, --nested-commands  Include all nested commands in the output.

DESCRIPTION
  Display help for subgraph-to-json-schema.
```

_See code: [@oclif/plugin-help](https://github.com/oclif/plugin-help/blob/v5.1.10/src/commands/help.ts)_

## `subgraph-to-json-schema plugins`

List installed plugins.

```
USAGE
  $ subgraph-to-json-schema plugins [--core]

FLAGS
  --core  Show core plugins.

DESCRIPTION
  List installed plugins.

EXAMPLES
  $ subgraph-to-json-schema plugins
```

_See code: [@oclif/plugin-plugins](https://github.com/oclif/plugin-plugins/blob/v2.0.11/src/commands/plugins/index.ts)_

## `subgraph-to-json-schema plugins:install PLUGIN...`

Installs a plugin into the CLI.

```
USAGE
  $ subgraph-to-json-schema plugins:install PLUGIN...

ARGUMENTS
  PLUGIN  Plugin to install.

FLAGS
  -f, --force    Run yarn install with force flag.
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Installs a plugin into the CLI.

  Can be installed from npm or a git url.

  Installation of a user-installed plugin will override a core plugin.

  e.g. If you have a core plugin that has a 'hello' command, installing a user-installed plugin with a 'hello' command
  will override the core plugin implementation. This is useful if a user needs to update core plugin functionality in
  the CLI without the need to patch and update the whole CLI.

ALIASES
  $ subgraph-to-json-schema plugins add

EXAMPLES
  $ subgraph-to-json-schema plugins:install myplugin 

  $ subgraph-to-json-schema plugins:install https://github.com/someuser/someplugin

  $ subgraph-to-json-schema plugins:install someuser/someplugin
```

## `subgraph-to-json-schema plugins:inspect PLUGIN...`

Displays installation properties of a plugin.

```
USAGE
  $ subgraph-to-json-schema plugins:inspect PLUGIN...

ARGUMENTS
  PLUGIN  [default: .] Plugin to inspect.

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Displays installation properties of a plugin.

EXAMPLES
  $ subgraph-to-json-schema plugins:inspect myplugin
```

## `subgraph-to-json-schema plugins:install PLUGIN...`

Installs a plugin into the CLI.

```
USAGE
  $ subgraph-to-json-schema plugins:install PLUGIN...

ARGUMENTS
  PLUGIN  Plugin to install.

FLAGS
  -f, --force    Run yarn install with force flag.
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Installs a plugin into the CLI.

  Can be installed from npm or a git url.

  Installation of a user-installed plugin will override a core plugin.

  e.g. If you have a core plugin that has a 'hello' command, installing a user-installed plugin with a 'hello' command
  will override the core plugin implementation. This is useful if a user needs to update core plugin functionality in
  the CLI without the need to patch and update the whole CLI.

ALIASES
  $ subgraph-to-json-schema plugins add

EXAMPLES
  $ subgraph-to-json-schema plugins:install myplugin 

  $ subgraph-to-json-schema plugins:install https://github.com/someuser/someplugin

  $ subgraph-to-json-schema plugins:install someuser/someplugin
```

## `subgraph-to-json-schema plugins:link PLUGIN`

Links a plugin into the CLI for development.

```
USAGE
  $ subgraph-to-json-schema plugins:link PLUGIN

ARGUMENTS
  PATH  [default: .] path to plugin

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Links a plugin into the CLI for development.

  Installation of a linked plugin will override a user-installed or core plugin.

  e.g. If you have a user-installed or core plugin that has a 'hello' command, installing a linked plugin with a 'hello'
  command will override the user-installed or core plugin implementation. This is useful for development work.

EXAMPLES
  $ subgraph-to-json-schema plugins:link myplugin
```

## `subgraph-to-json-schema plugins:uninstall PLUGIN...`

Removes a plugin from the CLI.

```
USAGE
  $ subgraph-to-json-schema plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Removes a plugin from the CLI.

ALIASES
  $ subgraph-to-json-schema plugins unlink
  $ subgraph-to-json-schema plugins remove
```

## `subgraph-to-json-schema plugins:uninstall PLUGIN...`

Removes a plugin from the CLI.

```
USAGE
  $ subgraph-to-json-schema plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Removes a plugin from the CLI.

ALIASES
  $ subgraph-to-json-schema plugins unlink
  $ subgraph-to-json-schema plugins remove
```

## `subgraph-to-json-schema plugins:uninstall PLUGIN...`

Removes a plugin from the CLI.

```
USAGE
  $ subgraph-to-json-schema plugins:uninstall PLUGIN...

ARGUMENTS
  PLUGIN  plugin to uninstall

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Removes a plugin from the CLI.

ALIASES
  $ subgraph-to-json-schema plugins unlink
  $ subgraph-to-json-schema plugins remove
```

## `subgraph-to-json-schema plugins update`

Update installed plugins.

```
USAGE
  $ subgraph-to-json-schema plugins update [-h] [-v]

FLAGS
  -h, --help     Show CLI help.
  -v, --verbose

DESCRIPTION
  Update installed plugins.
```
<!-- commandsstop -->
