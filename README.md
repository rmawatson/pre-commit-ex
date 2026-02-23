[![build status](https://github.com/pre-commit/pre-commit/actions/workflows/main.yml/badge.svg)](https://github.com/pre-commit/pre-commit/actions/workflows/main.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/pre-commit/pre-commit/main.svg)](https://results.pre-commit.ci/latest/github/pre-commit/pre-commit/main)

## This fork adds extensions to allow invocation of hooks as tools from the command line.

[[Original PR]](https://github.com/pre-commit/pre-commit/pull/3618)

## Installation

```bash
pip install pre-commit-ex
```

This package is a drop-in replacement for `pre-commit`. It follows the upstream version number with a post-release suffix for changes applied on top — e.g. `4.5.1.post1`, `4.5.1.post2` — so the base version always indicates which upstream release the fork is tracking.

## Upstream sync

This fork tries to stay in sync with [pre-commit/pre-commit](https://github.com/pre-commit/pre-commit), rebasing on top of new upstream releases where possible. All additions are intended to be backward compatible, with only additonal functionality.

## Extensions in this fork

### Using pre-commit hooks as terminal tools

By default, pre-commit only allows invoking a hook with the arguments that have been preconfigured in the `.pre-commit-config.yaml` `args: [...]` field for that hook:
```bash
pre-commit run example-hook
```

Passing different arguments to different invocations requires defining each permutation as a separate entry in `.pre-commit-config.yaml` with specific `args: [...]`. This doesn't support using hooks as general-purpose tools with dynamic arguments.

#### The `--tool` flag

When `--tool` is used:

- `allow_all_files=true` is implied
- The hook must be exposed with `stages: ["manual"]`
- Arbitrary arguments can be passed after `--`
- Output is streamed live to the terminal

**Usage:**
```bash
pre-commit run <hook-id> --tool -- [arguments...]
```

**Example:**
```bash
pre-commit run example-hook --tool -- --arg1 --arg2=4
```

This invokes `example-hook` with `--arg1` and `--arg2=4` passed directly to the underlying tool, without needing a predefined entry for each argument combination.

#### The `--no-tool-status-message` flag

Suppresses the `hook-name.....Success/Failed` status line that is printed after a `--tool` or `stream_output` hook completes. Useful when capturing or piping the hook's output.

```bash
pre-commit run example-hook --tool --no-tool-status-message -- --arg1
```

### `--log-level` option

All subcommands now accept a `--log-level` option to control the verbosity of pre-commit's own status messages. This is independent of the hook's output, and is useful for suppressing `[INFO]` logging from pre-commit. For example when tracking a branch `rev` and wanting to suppress the messages notifying you of an update.

```
--log-level {DEBUG,INFO,WARNING,ERROR}
```

The default is `INFO`. Use `WARNING` or `ERROR` to suppress informational messages:

```bash
pre-commit run example-hook --log-level WARNING
```

### `stream_output` hook field

Hooks can opt in to live streaming of their output by setting `stream_output: true` in `.pre-commit-hooks.yaml`. Unlike buffered output, streamed output is written to the terminal as the hook runs rather than after it completes. Previously output would only be shown once the tool has completed.

```yaml
- id: example-hook
  name: Example Hook
  entry: example-hook
  language: python
  stream_output: true
```

### `subdirectory` hook field

A single repository can now contain multiple independent hooks, each with its own `pyproject.toml` (or equivalent package definition) located in a subdirectory. Set `subdirectory` in `.pre-commit-hooks.yaml` to point to the subdirectory that should be used as the package root for that hook.

```yaml
- id: tool-a
  name: Tool A
  entry: tool-a
  language: python
  subdirectory: tool_a

- id: tool-b
  name: Tool B
  entry: tool-b
  language: python
  subdirectory: tool_b
```

Each subdirectory should contain its own `pyproject.toml` defining the hook's dependencies and entry point. This allows for the same isolated environment for each tool, but the flexibility to keep multiple tools in the same repository — previously all tools in a repository installed into a single environment per language.

### Automatic mutable ref resolution

A `rev` is classified as immutable (and therefore not subject to auto-resolution) if it is a hex commit hash (7+ characters) or a valid [PEP 440](https://peps.python.org/pep-0440/) version string (e.g. `4.5.1`, `1.0.0`). Anything else — branch names, short aliases, non-PEP-440 tags — is treated as a mutable ref.

When a `rev` in `.pre-commit-config.yaml` is a mutable ref, this fork automatically resolves it to the corresponding commit hash at install time and re-resolves it on subsequent runs if the upstream ref has moved. A log message is printed when the resolved hash changes:

```
Updating 'main': abc1234 -> def5678
```

This removes the need to run `pre-commit autoupdate` for repositories that you want to track by branch. `pre-commit autoupdate` can still be used to lock the `rev` to the current latest commit hash, but doing so will replace the branch name with a static hash, after which automatic tracking will no longer apply.

## pre-commit

A framework for managing and maintaining multi-language pre-commit hooks.

For more information see: https://pre-commit.com/
