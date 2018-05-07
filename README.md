# kiln-tools
A few command line tools for FogCreek's Kiln

```
./forkrepo.py parent_name fork_name 
./delrepo.py repo_name 
./kilnpaths.py -f ~/.hgpaths
```

## Usage
* Clone this repo.
* Install the required packages:
>`pip install -U -r requirements.txt`
* Create an API key if you don't have one. Log into Kiln, got to My Settings, Create API Token.
* Create a user config file and add your token to it:
>`echo 'token: "<yourtoken>"' > userconfig.yml`
* Add your Kiln URL to the config file: 
>`echo 'kiln_url: "https://ondemandname.kilnhg.com"' >> userconfig.yml` for Kiln On Demand  
>`echo 'kiln_url: "https://mydomain.com/Kiln"' > userconfig.yml` for your own Kiln instance.
* Run the scripts. Use `-h` for help on individual script arguments.
