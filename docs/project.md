# `mimir` - `pm` module

`pm` module's main goal is to add and track projects in `mimir`

## actions
| action | descrription |
| :-: | - |
| new <project name> <path> | adds project `project_name` to the registry and created directory for it |
| add <path> <project name> |
| list | lists all projects in the registry |
| delte <project name> | deletes `project_name` from the registry |

### `pm new`
`pm new <project name> <path>` | creates and adds new project to the project registry.

#### Arguments
`project name` name of the project and directory that will be created

`path` path for the project directory to be created
### `pm add`
`pm new <project name> <path>` | adds already existing project to the registry

#### Arguments
`project name` name of the project in the registry

`path` path to already existing project's directory
### `pm list`
`pm list` | lists all the project names and paths of projects in registry
### `pm delete`
`pm delete <project name>` | deletes project from registry and if user chooses from a hard drive too
#### Arguments
`project name` name of the project in a registry to be deleted

