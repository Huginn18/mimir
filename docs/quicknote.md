# `mimir` - `qn` module

`qn` module's main goal is to handle creation, editing and managing notes in `mimir`.

## actions
| action | description |
| :-: | - |
| new <note name> <-s> | creates new note and opens note in vim. If -s argument is used vim won't be opened. |
| edit <note name> | opens note in vim |
| list <-u> | lists all notes in manifest. If `-u` argument is used manifest will be updated before printing the list. |
| delete <note name> | deletes note |
| save | commits all changes and pushes them to the repo. Available only if `git` support is turned on. |
| rename <note name> <new note name> | renames note from <note name> to <new note name> |
| find <keyword> | prints list of all the notes containing <keyword> in their name |
### `qn new`
`qn new <note name> <-s>` | creates file for `note name` and opens it in vim. If `-s` argument is used note won't be opened in the editor.
#### Arguments
`note name` | name for the `.md` file that will be created. It is also used as the name of the note in the `qn` module.

`-s` | this argument is used to stop `qn` module from opening note in `vim`

### `qn edit`
`qn edit <note name>` | opens `.md` file associated with the `note name` in `vim`
#### Arguments
`note name` | name for the note to be opened in editor

### `qn list`
`qn list <-u>` | lists all the notes that are registered in the system.
#### Arguments
`-u` | this argument forces `qn` module to update manifest (based on the files in the directory) before printing the list

### `qn delete`
`qn delete <note name>` | deletes `<note name>.md` file and removes note from the manifest
#### Arguments
`note name` | name of the note to be delted

### `qn save`
`qn save` | adds, commits and pushes all changes to the notes

### `qn rename`
`qn rename <note name> <new note name>` | renames note from `note name` to `new note name`
#### Arguments
`note name` | name of the note to be renamed

`new note name` | this will be used as new name for the note
