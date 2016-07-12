xblock-cnvideo
--------------

This python package is meant to be used as a Xblock Component for OpenEDX LMS and Studio

It is developped and maintained at Univerisité de Lille by the team of the project [Culture Numérique](https://culturenumerique.univ-lille3.fr/)

# Installation instruction

It depends wether you need to install it in a [DevStack](https://openedx.atlassian.net/wiki/display/OpenOPS/Running+Devstack#RunningDevstack-InstallingtheOpenedXDeveloperStack) or [FullStack](https://openedx.atlassian.net/wiki/display/OpenOPS/Running+Fullstack) OpenEDX instance

## Install on Devstack

## Install on FullStack (production-like environnement)

Several ways of installing a new Xblock on FullStack are documented, but the recommended way is [this one](https://github.com/edx/edx-platform/wiki/Installing-a-new-XBlock), but with the following changes.
 
 ### Allow All Advanced Components (first time only)
 
- Manually edit the custom settings in /edx/app/edxapp/cms.env.json. 
- Look for attribute "FEATURES", instead of "EDXAPP_FEATURES", and add an item to it:
```
"FEATURES":[
    "ALLOW_ALL_ADVANCED_COMPONENTS": true,
    ...
]
```
- then restart the server but with following command:
```
$ sudo /edx/bin/supervisorctl restart edxapp:
```

### Install CNVideoXBlock

Same as [in the documentation](https://github.com/edx/edx-platform/wiki/Installing-a-new-XBlock#install-an-xblock)

    # Move to the folder:
    cd /edx/app/edxapp
    # Download the XBlock
    sudo -u edxapp git clone https://github.com/CultureNumerique/xblock-cnvideo.git
    # Install it
    sudo -u edxapp /edx/bin/pip.edxapp install xblock-cnvideo/
    # Optionnaly : Remove the installation files
    sudo rm -r xblock-cnvideo

### Reboot if something isn't right ###
In some cases, rebooting is necessary to use the XBlock.

    sudo /edx/bin/supervisorctl restart edxapp:

### Activate the CNVideoXBlock in your course ###
Go to `Settings -> Advanced Settings` and set `advanced_modules` to `["cnvideo"]`.

### Use it in a unit ###
Select `Advanced -> cnvideo` in your unit.


