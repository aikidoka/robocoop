RoboCoop
========
An ansible role to automate a Raspberry Pi running Raspbian GNU/Linux. Will establish timers for opening the door in the morning, closing it at the night, and weekly updates of the door timers.

Requirements
------------
- wunderground.com API key
- Pushbullet API key

Installation
------------
- Establish basic ssh with rpi (ansible is set to run locally)
- Create a a vault file with the two api keys
- Run the bootstrap playbook

```sh
$ cp group_vars\robocoop\vault.example group_vars\robocoop\vault # edit me too
$ ansible-vault encrypt group_vars\robocoop\vault
$ ansible-playbook -i inventory bootstrap.yml --ask-vault-pass
```
