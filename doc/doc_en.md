# io_artiste (en)

### Node List

- **operator** : primary and/or essential nodes for launching the test(s)
- **mode** : launches the different existing game modes
- **debug** : debug and additional options

---
|Node|Category|Image|Description|
|:---:|:---:|:---:|:---:|
|Init|operator|![](./IMG/init_01.jpeg)|is the starting point of the node tree|
|CLI|operator|![](./IMG/CLI_01.jpeg)|is a node that works like a terminal|
|Go Run Test|operator|![](./IMG/running_01.jpeg)|is the node that executes the node tree (terminal command)|
|Preview CMD|debug|![](./IMG/preview_01.jpeg)|is a command preview node|
---

## Init Node
- **SuperUser** : allows running a command as administrator (not available on Windows; open directly in administrator mode for similar behavior)
- **Password (if SuperUser checked)** : your personal password.

![](./IMG/init_sudo_02.jpeg)
- **Custom Executable** : enables the choice of a custom executable.
- **Game (file) path (if Custom Executable checked)** : use an STK executable other than the one installed on the system.

![](./IMG/init_git_custom_02.jpeg)
- **Track (folder) path** : load your own "Track/Battle/Soccers" folder.
- **Kart (folder) path** : load your own "Kart" folder.
- **Disable addon tracks** : if enabled, does not load the "Tracks/Battle/Soccers" addons downloaded from the game.
- **Disable addon karts** : if enabled, does not load the "Karts" addons downloaded from the game.
- **v(2.x or 1.x)** : Allows you to adjust the command depending on whether you want to use SupertuxKart 1.x or SuperTuxKart Evolution (2.x) 
- **Difficulty** : choose a difficulty level (Novice/Intermediate/Expert/SuperTux) if v(2.x or 1.x) is true a new additional difficulty is available.

When used, it is always at the start of the node tree.

![](./IMG/init_04.jpeg)

## CLI Nodes

Should be treated as a terminal.

![](./IMG/CLI_02.jpeg)

Can be chained together for a cleaner visual layout.

![](./IMG/CLI_03.jpeg)

## Go Run Test Nodes

Is the only truly mandatory node since it launches the execution of the command built with the node tree.
- **Run** : launches the command from Blender (blocks the Blender user interface).
- **Popen** : launches the command independently of Blender (does not block the Blender user interface).

![](./IMG/running_02.jpeg)

It is always placed at the end of the node tree.

## Preview CMD Nodes

This node allows you to preview the command(s) built in the node tree, which can be useful to ensure the correct command is launched by checking the selected options.

It can display long commands over multiple lines.

![](./IMG/preview_02.jpeg)
![](./IMG/preview_03.jpeg)
![](./IMG/preview_04.jpeg)

### Nodes can be linked to each other without issue

![](./IMG/tree_01.jpeg)
![](./IMG/tree_02.jpeg)
![](./IMG/tree_03.jpeg)

---
### [back to home](./../doc_io_artiste.md)
