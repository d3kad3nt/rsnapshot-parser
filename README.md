# Rsnapshot-Parser

This tool parses the output of Rsnapshot and outputs it through different modules.

## Usage

This tool is intended to be used with rsnapshot. It can be used in a pipe, where the output of rsnapshot is piped 
directly into rsnapshot-parser. The Option "verbose" in the snapshot config has to be set to "5".

The program takes one required argument, the used output modules. They can be given via the option "-m" or "--modules" and 
are a space seperated list.
A complete call can look something like this:  
/usr/local/bin/rsnapshot beta | /opt/rsnapshot_parser/rsnapshot_parser -m text gotify

## Installation

Every release contains a .deb package that can be installed.  
If you don't use a system that can install deb packages or don't want it you can also install it manually.  
These are the steps for the manual installation:

```bash
cd /opt
git clone https://github.com/d3kad3nt/rsnapshot-parser.git
cp rsnapshot-parser/config/rsnapshot_parser.conf /etc/
```

## Config

This program has a config file at /etc/rsnapshot_parser.conf.  
That file is in ini Format and divided into multiple sections.  
The first section is called "parser". This section contains settings that are relevant when the rsnapshot output is 
parsed.  
The other sections are from the modules, where each section has the same name as the module.

The following settings exist in the "parser" section:
**rsnapshot_config**: This is the path of the rsnapshot config file that is used by rsnapshot.
**start_XXXXX**: This Setting sets the start times for each used retain type in the format "hh:mm". 
The "XXXXX" in the setting name have to be exchanged with the name of the retain type, for example "start_alpha=01:00" 

## Modules

There are currently 4 output modules and it is easy to add more.
The modules are: Email, File, Stdout and Gotify

### Email
This module can send emails to defined address. 
It can communicate per SSL/TLS and StartTLS with the email server
The E-Mail can contain content from all Text Providers

#### Config
The settings for the Email Module are in the "email" Section of the config file. 
These are the settings that exist:  
**host**: The Hostname of the used email Server  
**encryption**: The Used Encryption. This accepts the values "SSL" and "StartTLS".  
**port**: The Port of the Mail Server that receives the mail.  
**sender_address**: The EMail Address that should be used to send the mails.
**sender_name**: The Name that should be shown as sender in the mail.  
**password**: The Password of the used Email address.  
**receiver_address**: The Address that this program should send the mails to.  
**providers**: A sorted List of all used text Providers that should be used.

### File
This module outputs plain text to a file that is defined in the config.
The File can contain content from all Text Providers

#### Config
The settings for the File Module are in the "text" Section of the config file.
These are the settings that exist:  
**filepath**: The path of the file that should be created.  
**providers**: A sorted List of all used text Providers that should be used.

### Stdout
This module outputs plain text to stdout. 
This is the only output to stdout by this script.  
The Output can contain content from all Text Providers

#### Config
The settings for the Stdout Module are in the "stdout" Section of the config file.
These are the settings that exist:  
**providers**: A sorted List of all used text Providers that should be used.

### Gotify
This module outputs a short message to a gotify server if the backup was successful or not.

#### Config
The settings for the Gotify Module are in the "gotify" Section of the config file.
These are the settings that exist:  
**url**: The URL of the used gotify instance.  
**api_token**: The api_token from gotify that was created for the application.  

### Text Provider
Text Provider are used to deliver text to the modules and can be used in multiple modules.
If a module supports them they can be configured with the "providers" setting. 
The output ot the providers is the same for every module. 
The following providers exist:
- **Summary**: This provider creates a short (6 lines) summary
- **Error**: This provider outputs any errors that might have occurred in a helpful format.
- **Statistics**: This provider outputs some statistics about the backup like the slowest backupPoints ore the points with the most changed files.
- **BackupPointList**: This provider outputs a list of all backupPoints that ran and some data for every Point.
