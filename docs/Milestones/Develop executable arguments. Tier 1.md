# This Milestone is reached once the following arguments are implemented

# Arguments:
## Split:
### Option to print a projects results in it's own file)
#### Includes:
---
## Help:
### Display Arguments and usage information
#### includes:
1. Usages
2. List other Arguments
3. List shorthands

---

## Debug:
### Option to controll level of output for debugging.
#### Includes:
Will need to be updated to control # of sensors scanned, and options to avoid sending requests entirely.
|Level |Effect     | Syntax       |
|----| ------------ | ------------|
|0   | Silent run with output to file.      | --debug=0 |
|1   | Split run with file/console logging. | --debug=1 |
|2   | Test run. Only logs to console.      | --debug=2 |
|3   | Test run. No output.                 | --debug=3 |

---

## Verbose:
### Option to control how much run data is printed. Useful information for debugging
#### Includes:
'diff' date diffrences
Statements after function completions
Timestamps
Urls
May add levels
---

## Headless:
### Option to toggle rendering of the browser
#### Includes:
true/false
---

## Project:
### Option to run only a specific project
#### Includes:
Check project list for name values
Prompting if given value is missing

options:
Description
Usage
Shorthand
Defaults
Prompt missing values