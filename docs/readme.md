# Mimir

`mimir` is cli app for knowledge hoarding and project management.

# Thought Process
If you want to investigate my thought process and whole development process check [`exploration/mimir` log](https://github.com/Huginn18/huginn18/blob/main/exploration/mimir.md)

# Features
## Quicknote
`qn` module is used to make quick, short term notes. `qn` notes can be organized into multiple separate directories. Default directory for `qn` files is `~/.config/.mimir.d/qn/`.
## Log
`log` module is used to keep logs/journals both private and about projects. `log` is can be used in tandem with projects module (projects created with `project` module will be also used inside `log` module). Default directory for `log` files is `~/.config/.mimir.d/log/`.
## ToDo
This one is self-explanatory.
## Documenation
`doc` module is used for wiki like style documentation.
## Estimation
`est` module is used for creation of project's budget/estimation sheet.
## Project Management
`pm` module is used to track and manage projects. Projects manifest is used by the rest of the `mimir` modules.
## CV Generator
	TBU

# Config
`mimir` has really simple config file called `.mimirrc` which is stored in `~/.config/` directory.
## Contents
`.mimirrc` stores two fields for every module.
### Status
This field shouldn't be modified by the user. It is used to determine if module was initialized and if so if it is active.
### Custom paths
This list stores paths to all directories set up by the user.
