RoboCoop
========
An ansible role to automate a Raspberry Pi running ArchLinuxARM. Will establish timers for opening the door in the morning, closing it at the night, and weekly updates of the door timers.

Requirements
------------
- wunderground.com API key
- Pushbullet API key

Installation
------------
- Establish basic ssh with rpi, and add the host to an inventory file in the 'robocoop' group
- Create a a vault file with the two api keys
- Run the bootstrap playbook

```sh
$ echo $'[robocoop]\nhost_name' > inventory
$ cp group_vars\robocoop\vault.example group_vars\robocoop\vault # edit me too
$ ansible-vault encrypt group_vars\robocoop\vault
$ ansible-playbook -i inventory bootstrap.yml --ask-vault-pass
```
