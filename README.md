# Nagios-plugins-storage-storage

This is Nagios probe to monitor Storage endpoints free space.

It's based on the information retrieved by the Operations portal which is aggregating the information published by the storages via the BDII.
A valid token to access the Opeerations portal API  is needed to execute the probe

## Usage

```shell
usage: storage_monitor_probe.py [-h] [--version] [-H HOSTNAME] [-w WARNING]
                                [-c CRITICAL] [-d] [--print-all] [-p PREFIX]
                                [-s SUFFIX] [-t TIMEOUT] [-C COMMAND]
                                [--dry-run] [-o OUTPUT] [-F FILE] [-T TOKEN]
                                [-V VO] [-m MIN_FREE_SPACE]
                                [-O OPS_PORTAL_URL]

NAGIOS Storage Free Space probe

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Host name, IP Address, or unix socket (must be an
                        absolute path)
  -w WARNING, --warning WARNING
                        Offset to result in warning status
  -c CRITICAL, --critical CRITICAL
                        Offset to result in critical status
  -d, --debug           Specify debugging mode
  --print-all           Print output from all metrics to stdout
  -p PREFIX, --prefix PREFIX
                        Text to prepend to ever metric name
  -s SUFFIX, --suffix SUFFIX
                        Text to append to every metric name
  -t TIMEOUT, --timeout TIMEOUT
                        Global timeout for plugin execution
  -C COMMAND, --command COMMAND
                        Nagios command pipe for submitting passive results
  --dry-run             Dry run, will not execute commands and submit passive
                        results
  -o OUTPUT, --output OUTPUT
                        Plugin output format; valid options are nagios,
                        check_mk or passive (via command pipe); defaults to
                        nagios)
  -F FILE, --file FILE  input json file with storage info
  -T TOKEN, --token TOKEN
                        token needed to access Operations portal API
  -V VO, --VO VO        The VO to test
  -m MIN_FREE_SPACE, --min_free_space MIN_FREE_SPACE
                        The min free space in GB
  -O OPS_PORTAL_URL, --ops_portal_url OPS_PORTAL_URL
                        OPS Portal url

```
## Example

```shell
/plugins/storage_monitor_probe.py --token=xxxxxxxxx --dry-run -H srm.ciemat.es -m 400  -d
Sep 26 21:42:04 DEBUG core[379]: Call sequence: [(<function metricCheckFreeSpace at 0x7f85136c69d8>, 'CheckFreeSpace', False)]
Sep 26 21:42:04 DEBUG core[379]:    Function call: metricCheckFreeSpace
OK - Free space is above the threshold: 3848 GB

mkdir build
cd build
make rpm -f ../Makefile 
```

