# DNS Sinkhole
Use PiHole blocklists with PowerDNS Recursor.
This is a python language port of [Blocklister](https://github.com/thommay/blocklister) ment to reduce system requirements. As python is available on most systems I think it's more fitting for the job.

## How to use
1. Populate your config.toml with blocklists you want to use
2. Run script to create blocklist.lua and permitlist.lua
```python pdns-sinkhole-generator.py config.toml```
3. Copy adblock.lua to your PowerDNS config folder
4. Update your new copy of adblock.lua with correct paths to your blocklist.lua and permitlist.lua
5. Update recursor.conf to sinkhole your DNS requests using your new lists ```lua-dns-script=/etc/powerdns/adblock.lua```
6. Restart PowerDNS Recursor to apply configuration

## Acknowledgments

### Blocklister
This project is a rewrite of [Blocklister](https://github.com/thommay/blocklister) by [Thom May](https://github.com/thommay). The original project was written in [Rust].

This rewrite has been undertaken to port the functionality to Python. All credit for the original implementation and design goes to Thom May.

### Simple adblock powerdns
Just as Blocklister we reuse the [Lua code](https://gist.github.com/ahupowerdns/bb1a043ce453a9f9eeed) by [Bert Hubert](https://gist.github.com/ahupowerdns) for PowerDNS recursor to put the blocklist to work.

### Use of AI tools
This language port was translated with the assistance of ChatGPT (GPT-4 and GPT-4o). Further improvments will likely be assisted by similar tools as I am no developer. 