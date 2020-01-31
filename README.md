# EUMETSAT OSX wallpaper

Python script to create an awesome wallpaper of our earth, as seen by EUMETSAT sattelites above Europe.

## Prerequisites

### Anaconda installation
conda or miniconda installed
```zsh
brew install miniconda
conda init zsh
```

### Conda environment created
install the environment:
```zsh
conda env create -f environment.yml
```
it will create a new conda environment, named `eumetsat`

## Script installation

### Test the script

```
zsh generate_earth.zsh
```

### Create cron job

Open you crontab file:
```
crontab -e
```

And add this line to your crontab file (don't forget to replace `PATH_TO_YOUR_FOLDER`):
```
* * * * * cd PATH_TO_YOUR_FOLDER/eumetsat-osx-wallpaper && zsh generate_earth.zsh  >/tmp/stdout.log 2>/tmp/stderr.log
```

You'll be able to check the logs using:
```
cat /tmp/std*.log
```

## To be improved

- [ ] download more sample images from EUMETSAT to generate a proper mask programmatically
