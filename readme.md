## Dragon Quest III Class Challenge
This repository is for a script that helps manage a specific class challenge for Dragon Quest III. 

Refer to https://pastebin.com/2t2wGfzH for basic explanation

This program dynamically creates images in the `current` directory based on the current party's buildout. This was made to be used with OBS and layouts.

If enough people are interested, a proper program/GUI can be built out

## Usage
From command line, run the script:  
`python script.py`  
to be greeted with a command center. Use help function for explanations for each command.

Basic usage would be: 
- `new` - start a new party  
- `promote 1` - promote first party member  
- `promote all` - promote all together  
- `reroll 3` - reroll a character's promotion  

## Configs
The local file `config.yaml` can be edited in a text editor. The following configurations exist:

- autosave: true, false
    - allows autosaving after every input. use save/load commands to interact with current_chars.save
- hero_enabled: true, false
    - forces character in slot 1 to be hero. false setting requires savefile with hero in ruida's tavern
- hero_gender: m, f
- minimum_starting_magical: 0,1,2,3,4
    - minimum number of starting characters that will have magic (either cleric or wizard)
- maximum_starting_jesters: 0,1,2,3,4
    - maximum number of starting characters that will be jesters
- promote_sage_limit: 0,1,2,3,4
    - number of sages allowed in the party. does not necessarily mean how many sages will be in the party, just the limits
- promote_enable_jesters: true, false
    - toggle for allowing jesters as promoted classes
- force_jesters_to_sage: true, false
    - toggle guarantee jesters to promote to sage 