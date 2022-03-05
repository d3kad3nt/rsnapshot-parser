#Rsnapshot-Parser

This tool parses the output of Rsnapshot and outputs it through different modules.

##Usage

This tool is intended to be used with rsnapshot. It can be used in a pipe, where the output of rsnapshot is piped 
directly into rsnapshot-parser. The outputlevel in 

##Config

This programm has a config file at /etc/rsnapshot_parser.conf.  
That file is in ini Format and divided into multiple sections.  
The first section is called "parser". This section contains settings that are relevant when the rsnapshot output is 
parsed.  
The other sections are from the modules, where each section has the same name as the module.

##Modules

Currently, only 2 modules exist, but it is easy to add new modules.

###Text
This module outputs plain text either to a file or the terminal.

The text contains different infos about the backup like the number of files that were changed, or the time
of the backup (if configured)

###Gotify
This module outputs a short message to a gotify server if the backup was successful or not.
