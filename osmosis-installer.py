import subprocess
import os
import platform
import time
import readline
import random
import argparse
import sys
from sys import argv
from os import remove

# self-destruct file after first call
#remove(argv[0])

class CustomHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        return ', '.join(action.option_strings)
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)

fmt = lambda prog: CustomHelpFormatter(prog,max_help_position=30)

osmo_home = subprocess.run(["echo $HOME/.osmosisd"], capture_output=True, shell=True, text=True).stdout.strip()

parser = argparse.ArgumentParser(description="Osmosis Installer",formatter_class=fmt)

# automated commands ("auto" group)
auto = parser.add_argument_group('Automated')

auto.add_argument(
    '-m',
    '--mainnet-default',
    action='store_true',
    help='R|Use all default settings with no input for mainnet\n ',
    dest="mainnetDefault")

auto.add_argument(
    '-t',
    '--testnet-default',
    action='store_true',
    help='R|Use all default settings with no input for testnet\n ',
    dest="testnetDefault")

# mainnet and testnet commands ("both" group)
both = parser.add_argument_group('Mainnet and Testnet')

both.add_argument(
    '-s',
    '--swap',
    type = bool,
    default=True,
    help='R|Use swap if less than 32Gb RAM are detected \nDefault (bool): True\n ',
    dest="swapOn")

both.add_argument(
    '-i',
    '--install-home',
    type = str,
    default=osmo_home,
    help='R|Osmosis installation location \nDefault: "'+osmo_home+'"\n ',
    dest="installHome")

both.add_argument(
    '-na',
    '--name',
    type = str,
    default="defaultNode",
    help='R|Node name \nDefault: "defaultNode"\n ',
    dest="nodeName")

portDefault = 'tcp://0.0.0.0:1317;0.0.0.0:9090;0.0.0.0:9091;tcp://127.0.0.1:26658;tcp://127.0.0.1:26657;tcp://0.0.0.0:26656;localhost:6060'
both.add_argument(
    '-p',
    '--ports',
    type=lambda s: [str(item) for item in s.split(';')],
    default=portDefault,
    help='R|Single string seperated by semicolons of ports. Order must be api, grpc server, grpc web, abci app addr, rpc laddr, p2p laddr, and pprof laddr \nDefault: \"'+portDefault+'\"\n ',
    dest="ports")

nodeTypeChoices = ['full', 'client', 'local']
both.add_argument(
    '-ty',
    '--type',
    type = str,
    choices=nodeTypeChoices,
    default='full',
    help='R|Node type \nDefault: "full" '+str(nodeTypeChoices)+'\n ',
    dest="nodeType")

networkChoices = ['osmosis-1', 'osmo-test-4']
both.add_argument(
    '-n',
    '--network',
    type = str,
    choices=networkChoices,
    default='osmosis-1',
    help='R|Network to join \nDefault: "osmosis-1" '+str(networkChoices)+'\n ',
    dest="network")

pruningChoices = ['default', 'nothing', 'everything']
both.add_argument(
    '-pr',
    '--prune',
    type = str,
    choices=pruningChoices,
    default='everything',
    help='R|Pruning settings \nDefault: "everything" '+str(pruningChoices)+'\n ',
    dest="pruning")

cosmovisorServiceChoices = ['cosmoservice', 'osmoservice', 'noservice']
both.add_argument(
    '-cvs',
    '--cosmovisor-service',
    type = str,
    choices=cosmovisorServiceChoices,
    default='osmoservice',
    help='R|Start with cosmovisor systemctl service, osmosisd systemctl service, or exit without creating or starting a service \nDefault: "osmoservice" '+str(cosmovisorServiceChoices),
    dest="cosmovisorService")

# testnet only commands ("testnet" group)
testnet = parser.add_argument_group('Testnet only')

dataSyncTestnetChoices = ['snapshot', 'exit']
testnet.add_argument(
    '-dst',
    '--data-sync-test',
    type = str,
    choices=dataSyncTestnetChoices,
    default='snapshot',
    help='R|Data sync options \nDefault: "snapshot" '+str(dataSyncTestnetChoices)+'\n ',
    dest="dataSyncTestnet")

snapshotTypeTestnetChoices = ['pruned', 'archive']
testnet.add_argument(
    '-stt',
    '--snapshot-type-test',
    type = str,
    choices=snapshotTypeTestnetChoices,
    default='pruned',
    help='R|Snapshot type \nDefault: "pruned" '+str(snapshotTypeTestnetChoices)+'\n ',
    dest="snapshotTypeTestnet")

# mainnet only commands ("mainnet" group)
mainnet = parser.add_argument_group('Mainnet only')

dataSyncTypeChoices = ['snapshot', 'genesis', 'exit']
mainnet.add_argument(
    '-ds',
    '--data-sync',
    type = str,
    choices=dataSyncTypeChoices,
    default='snapshot',
    help='R|Data sync options \nDefault: "snapshot" '+str(dataSyncTypeChoices)+'\n ',
    dest="dataSync")

snapshotTypeChoices = ['pruned', 'default', 'archive']
mainnet.add_argument(
    '-st',
    '--snapshot-type',
    type = str,
    choices=snapshotTypeChoices,
    default='pruned',
    help='R|Snapshot type \nDefault: "pruned" '+str(snapshotTypeChoices)+'\n ',
    dest="snapshotType")

snapshotLocationChoices = ['netherlands', 'singapore', 'sanfrancisco']
mainnet.add_argument(
    '-sl',
    '--snapshot-location',
    type = str,
    choices=snapshotLocationChoices,
    default='netherlands',
    help='R|Snapshot location \nDefault: "netherlands" '+str(snapshotLocationChoices)+'\n ',
    dest="snapshotLocation")

replayDbBackendChoices = ['goleveldb', 'rocksdb']
mainnet.add_argument(
    '-rdb',
    '--replay-db-backend',
    type = str,
    choices=replayDbBackendChoices,
    default='goleveldb',
    help='R|Database backend when replaying from genesis\nDefault: "goleveldb" '+str(replayDbBackendChoices)+'\n ',
    dest="replayDbBackend")

mainnet.add_argument(
    '-es',
    '--extra-swap',
    type = bool,
    default=True,
    help='R|Use extra swap if less than 64Gb RAM are detected when syncing from genesis\nDefault (bool): True\n ',
    dest="extraSwap")

mainnet.add_argument(
    '-sr',
    '--start-replay',
    type = bool,
    default=True,
    help='R|Immediately start replay on completion\nDefault (bool): True\n ',
    dest="startReplay")

parser._optionals.title = 'Optional Arguments'

if not len(sys.argv) > 1:
    parser.set_defaults(mainnetDefault=False, testnetDefault=False, swapOn=None, installHome=None, nodeName=None, ports=None, nodeType=None, network=None, pruning=None, cosmovisorService=None, dataSyncTestnet=None, snapshotTypeTestnet=None, dataSync=None, snapshotType=None, snapshotLocation=None, replayDbBackend=None, extraSwap=None, startReplay=None)

args = parser.parse_args()

if args.testnetDefault == True:
    args.network = 'osmo-test-4'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)
   finally:
      readline.set_startup_hook()


def completeCosmovisor():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN + "The cosmovisor service is currently running in the background")
    print(bcolors.OKGREEN + "To see the status of cosmovisor, run the following command: 'sudo systemctl status cosmovisor'")
    print(bcolors.OKGREEN + "To see the live logs from cosmovisor, run the following command: 'journalctl -u cosmovisor -f'")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'"+ bcolors.ENDC)
    quit()


def completeOsmosisd():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN + "The osmosisd service is currently running in the background")
    print(bcolors.OKGREEN + "To see the status of the osmosis daemon, run the following command: 'sudo systemctl status osmosisd'")
    print(bcolors.OKGREEN + "To see the live logs from the osmosis daemon, run the following command: 'journalctl -u osmosisd -f'")
    print(bcolors.OKGREEN + "In order to use cosmovisor/osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'"+ bcolors.ENDC)
    quit()


def complete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis full node!")
    print(bcolors.OKGREEN + "The osmosisd service is NOT running in the background")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'")
    print(bcolors.OKGREEN + "After reloading your terminal and/or profile, you can start osmosisd with: 'osmosisd start'"+ bcolors.ENDC)
    quit()


def partComplete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up the Osmosis daemon!")
    print(bcolors.OKGREEN + "The osmosisd service is NOT running in the background, and your data directory is empty")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'")
    print(bcolors.OKGREEN + "If you intend to use osmosisd without syncing, you must include the '--node' flag after cli commands with the address of a public RPC node"+ bcolors.ENDC)
    quit()


def clientComplete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Osmosis client node!")
    print(bcolors.OKGREEN + "DO NOT start the osmosis daemon. You can query directly from the command line without starting the daemon!")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'"+ bcolors.ENDC)
    quit()


def replayComplete():
    print(bcolors.OKGREEN + "Congratulations! You are currently replaying from genesis in a background service!")
    print(bcolors.OKGREEN + "To see the status of cosmovisor, run the following command: 'sudo systemctl status cosmovisor'")
    print(bcolors.OKGREEN + "To see the live logs from cosmovisor, run the following command: 'journalctl -u cosmovisor -f'")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'"+ bcolors.ENDC)
    quit()


def replayDelay():
    print(bcolors.OKGREEN + "Congratulations! Osmosis is ready to replay from genesis on your command!")
    print(bcolors.OKGREEN + "YOU MUST MANUALLY INCREASE ULIMIT FILE SIZE BEFORE STARTING WITH `ulimit -n 200000`")
    print(bcolors.OKGREEN + "In order to use osmosisd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'")
    print(bcolors.OKGREEN + "Once reloaded, use the command `cosmosvisor start` to start the replay from genesis process")
    print(bcolors.OKGREEN + "It is recommended to run this in a tmux session if not running in a background service")
    print(bcolors.OKGREEN + "You must use `cosmosvisor start` and not `osmosisd start` in order to upgrade automatically"+ bcolors.ENDC)
    quit()


def localOsmosisComplete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up a LocalOsmosis node!")
    print(bcolors.OKGREEN + "To start the local network")
    print(bcolors.OKGREEN + "Run 'source ~/.profile'")
    print(bcolors.OKGREEN + "Ensure docker is running in the background if on linux or start the Docker application if on Mac")
    print(bcolors.OKGREEN + "Find the installed LocalOsmosis folder and cd into it")
    print(bcolors.OKGREEN + "Run 'docker-compose up'")
    print(bcolors.OKGREEN + "Run 'osmosisd status' to check that you are now creating blocks"+ bcolors.ENDC)
    quit()


def cosmovisorService ():
    print(bcolors.OKGREEN + "Creating Cosmovisor Service" + bcolors.ENDC)
    subprocess.run(["echo '# Setup Cosmovisor' >> "+HOME+"/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export DAEMON_NAME=osmosisd' >> "+HOME+"/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export DAEMON_HOME="+osmo_home+"' >> "+HOME+"/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export DAEMON_ALLOW_DOWNLOAD_BINARIES=false' >> "+HOME+"/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export DAEMON_LOG_BUFFER_SIZE=512' >> "+HOME+"/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export DAEMON_RESTART_AFTER_UPGRADE=true' >> "+HOME+"/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export UNSAFE_SKIP_BACKUP=true' >> "+HOME+"/.profile"], shell=True, env=my_env)
    subprocess.run(["""echo '[Unit]
Description=Cosmovisor daemon
After=network-online.target
[Service]
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_HOME="""+ osmo_home+"""\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
Environment=\"UNSAFE_SKIP_BACKUP=true\"
User="""+ USER+"""
ExecStart="""+HOME+"""/go/bin/cosmovisor start --home """+osmo_home+"""
Restart=always
RestartSec=3
LimitNOFILE=infinity
LimitNPROC=infinity
[Install]
WantedBy=multi-user.target
' >cosmovisor.service
    """], shell=True, env=my_env)
    subprocess.run(["sudo mv cosmovisor.service /lib/systemd/system/cosmovisor.service"], shell=True, env=my_env)
    subprocess.run(["sudo systemctl daemon-reload"], shell=True, env=my_env)
    subprocess.run(["systemctl restart systemd-journald"], shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)


def osmosisdService ():
    print(bcolors.OKGREEN + "Creating Osmosisd Service..." + bcolors.ENDC)
    subprocess.run(["""echo '[Unit]
Description=Osmosis Daemon
After=network-online.target
[Service]
User="""+ USER+"""
ExecStart="""+HOME+"""/go/bin/osmosisd start --home """+osmo_home+"""
Restart=always
RestartSec=3
LimitNOFILE=infinity
LimitNPROC=infinity
Environment=\"DAEMON_HOME="""+osmo_home+"""\"
Environment=\"DAEMON_NAME=osmosisd\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
[Install]
WantedBy=multi-user.target
' >osmosisd.service
    """], shell=True, env=my_env)
    subprocess.run(["sudo mv osmosisd.service /lib/systemd/system/osmosisd.service"], shell=True, env=my_env)
    subprocess.run(["sudo systemctl daemon-reload"], shell=True, env=my_env)
    subprocess.run(["systemctl restart systemd-journald"], shell=True, env=my_env)


def cosmovisorInit ():
    print(bcolors.OKGREEN + """Do you want to use Cosmovisor to automate future upgrades?
1) Yes, install cosmovisor and set up background service
2) No, just set up an osmosisd background service (recommended)
3) Don't install cosmovisor and don't set up a background service
    """+ bcolors.ENDC)
    if args.cosmovisorService == "cosmoservice" :
        useCosmovisor = '1'
    elif args.cosmovisorService == "osmoservice" :
        useCosmovisor = '2'
    elif args.cosmovisorService == "noservice" :
        useCosmovisor = '3'
    else:
        useCosmovisor = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if useCosmovisor == "1":
        subprocess.run(["clear"], shell=True)
        print(bcolors.OKGREEN + "Setting Up Cosmovisor..." + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME))
        subprocess.run(["go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor"], shell=True, env=my_env)
        subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/genesis"], shell=True, env=my_env)
        subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/genesis/bin"], shell=True, env=my_env)
        subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades"], shell=True, env=my_env)
        subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades/v7/bin"], shell=True, env=my_env)
        os.chdir(os.path.expanduser(HOME+'/osmosis'))
        subprocess.run(["git checkout v7.3.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["cp build/osmosisd "+osmo_home+"/cosmovisor/upgrades/v7/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run([". "+HOME+"/.profile"], shell=True, env=my_env)
        subprocess.run(["cp "+ GOPATH +"/bin/osmosisd "+osmo_home+"/cosmovisor/genesis/bin"], shell=True, env=my_env)
        cosmovisorService()
        subprocess.run(["sudo systemctl start cosmovisor"], shell=True, env=my_env)
        subprocess.run(["clear"], shell=True)
        completeCosmovisor()
    elif useCosmovisor == "2":
        osmosisdService()
        subprocess.run(["sudo systemctl start osmosisd"], shell=True, env=my_env)
        subprocess.run(["clear"], shell=True)
        completeOsmosisd()
    elif useCosmovisor == "3":
        subprocess.run(["clear"], shell=True)
        complete()
    else:
        subprocess.run(["clear"], shell=True)
        cosmovisorInit()


def startReplayNow():
    print(bcolors.OKGREEN + """Do you want to start cosmovisor as a background service?
1) Yes, start cosmovisor as a background service and begin replay
2) No, exit and start on my own (will still auto update at upgrade heights)
    """+ bcolors.ENDC)
    if args.startReplay == True :
        startNow = '1'
    elif args.startReplay == False :
        startNow = '2'
    else:
        startNow = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if startNow == "1":
        subprocess.run(["clear"], shell=True)
        cosmovisorService()
        subprocess.run(["sudo systemctl start cosmovisor"], shell=True, env=my_env)
        replayComplete()
    if startNow == "2":
        subprocess.run(["clear"], shell=True)
        replayDelay()
    else:
        subprocess.run(["clear"], shell=True)
        startReplayNow()


def replayFromGenesisLevelDb ():
    print(bcolors.OKGREEN + "Setting Up Cosmovisor..." + bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME))
    subprocess.run(["go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/genesis"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/genesis/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades/v4/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades/v5/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades/v7/bin"], shell=True, env=my_env)
    os.chdir(os.path.expanduser(HOME+'/osmosis'))
    print(bcolors.OKGREEN + "Preparing v4 Upgrade..." + bcolors.ENDC)
    subprocess.run(["git checkout v4.2.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["cp build/osmosisd "+osmo_home+"/cosmovisor/upgrades/v4/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Preparing v5/v6 Upgrade..." + bcolors.ENDC)
    subprocess.run(["git checkout v6.4.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["cp build/osmosisd "+osmo_home+"/cosmovisor/upgrades/v5/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Preparing v7 Upgrade..." + bcolors.ENDC)
    subprocess.run(["git checkout v7.3.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["cp build/osmosisd "+osmo_home+"/cosmovisor/upgrades/v7/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["git checkout v3.1.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run([". "+HOME+"/.profile"], shell=True, env=my_env)
    subprocess.run(["cp "+ GOPATH +"/bin/osmosisd "+osmo_home+"/cosmovisor/genesis/bin"], shell=True, env=my_env)
    print(bcolors.OKGREEN + "Adding Persistent Peers For Replay..." + bcolors.ENDC)
    peers = "2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.66.52.160:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.82.89.95:26656"
    subprocess.run(["sed -i -E 's/persistent_peers = \"\"/persistent_peers = \""+peers+"\"/g' "+osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["clear"], shell=True)
    startReplayNow()


def replayFromGenesisRocksDb ():
    print(bcolors.OKGREEN + "Changing db_backend to rocksdb..." + bcolors.ENDC)
    subprocess.run(["sed -i -E 's/db_backend = \"goleveldb\"/db_backend = \"rocksdb\"/g' "+osmo_home+"/config/config.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    print(bcolors.OKGREEN + "Installing rocksdb..." + bcolors.ENDC)
    print(bcolors.OKGREEN + "This process may take 15 minutes or more" + bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME))
    subprocess.run(["sudo apt-get install -y libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["git clone https://github.com/facebook/rocksdb.git"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    os.chdir(os.path.expanduser(HOME+"/rocksdb"))
    subprocess.run(["git checkout v6.29.3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["export CXXFLAGS='-Wno-error=deprecated-copy -Wno-error=pessimizing-move -Wno-error=class-memaccess'"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["sudo make shared_lib"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["sudo make install-shared INSTALL_PATH=/usr"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["sudo echo 'export LD_LIBRARY_PATH=/usr/local/lib' >> $HOME/.bashrc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    my_env["LD_LIBRARY_PATH"] = "/usr/local/lib"
    print(bcolors.OKGREEN + "Setting Up Cosmovisor..." + bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME))
    subprocess.run(["go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/genesis"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/genesis/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades/v4/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades/v5/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p "+osmo_home+"/cosmovisor/upgrades/v7/bin"], shell=True, env=my_env)
    os.chdir(os.path.expanduser(HOME+'/osmosis'))
    print(bcolors.OKGREEN + "Preparing v4 Upgrade..." + bcolors.ENDC)
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["git checkout v4.2.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["sed '/gorocksdb.*/d' ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["echo \" \" >> ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["echo 'replace github.com/tecbot/gorocksdb => github.com/cosmos/gorocksdb v1.2.0' >> ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["go mod tidy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["cp build/osmosisd "+osmo_home+"/cosmovisor/upgrades/v4/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Preparing v5/v6 Upgrade..." + bcolors.ENDC)
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["git checkout v6.4.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["cp build/osmosisd "+osmo_home+"/cosmovisor/upgrades/v5/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Preparing v7 Upgrade..." + bcolors.ENDC)
    subprocess.run(["git checkout v7.3.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["cp build/osmosisd "+osmo_home+"/cosmovisor/upgrades/v7/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["git checkout v3.1.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["sed '/gorocksdb.*/d' ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["echo \" \" >> ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["echo 'require github.com/tecbot/gorocksdb v0.0.0-20191217155057-f0fad39f321c // indirect' >> ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["echo 'replace github.com/tecbot/gorocksdb => github.com/cosmos/gorocksdb v1.2.0' >> ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["go mod tidy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run([". "+HOME+"/.profile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["cp build/osmosisd "+osmo_home+"/cosmovisor/genesis/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["sudo /sbin/ldconfig -v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Adding Persistent Peers For Replay..." + bcolors.ENDC)
    peers = "2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.66.52.160:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.82.89.95:26656"
    subprocess.run(["sed -i -E 's/persistent_peers = \"\"/persistent_peers = \""+peers+"\"/g' "+osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["clear"], shell=True)
    startReplayNow()


def replayFromGenesisDb ():
    print(bcolors.OKGREEN + """Please choose which database you want to use:
1) goleveldb (Default)
2) rocksdb (faster but less support)
    """+ bcolors.ENDC)
    if args.replayDbBackend == "goleveldb":
        databaseType = '1'
    elif args.replayDbBackend == "rocksdb":
        databaseType = '2'
    else:
        databaseType = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if databaseType == "1":
        subprocess.run(["clear"], shell=True)
        replayFromGenesisLevelDb()
    elif databaseType == "2":
        subprocess.run(["clear"], shell=True)
        replayFromGenesisRocksDb()
    else:
        subprocess.run(["clear"], shell=True)
        replayFromGenesisDb()


def extraSwap():
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    mem_gib = mem_bytes/(1024.**3)
    print(bcolors.OKGREEN +"RAM Detected: "+str(round(mem_gib))+"GB"+ bcolors.ENDC)
    swapNeeded = 64 - round(mem_gib)
    if round(mem_gib) < 64:
        print(bcolors.OKGREEN +"""
There have been reports of replay from genesis needing extra swap (up to 64GB) to prevent OOM errors.
Would you like to overwrite any previous swap file and instead set a """+str(swapNeeded)+"""GB swap file?
1) Yes, set up extra swap (recommended)
2) No, do not set up extra swap
        """+ bcolors.ENDC)
        if args.extraSwap == True :
            swapAns = '1'
        elif args.extraSwap == False :
            swapAns = '2'
        else:
            swapAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

        if swapAns == "1":
            print(bcolors.OKGREEN +"Setting up "+ str(swapNeeded)+ "GB swap file..."+ bcolors.ENDC)
            subprocess.run(["sudo swapoff -a"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo fallocate -l " +str(swapNeeded)+"G /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo chmod 600 /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo mkswap /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo swapon /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo cp /etc/fstab /etc/fstab.bak"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["clear"], shell=True)
            print(bcolors.OKGREEN +str(swapNeeded)+"GB swap file set"+ bcolors.ENDC)
            replayFromGenesisDb()
        elif swapAns == "2":
            subprocess.run(["clear"], shell=True)
            replayFromGenesisDb()
        else:
            subprocess.run(["clear"], shell=True)
            extraSwap()
    else:
        print(bcolors.OKGREEN +"You have enough RAM to meet the 64GB minimum requirement, moving on to system setup..."+ bcolors.ENDC)
        time.sleep(3)
        subprocess.run(["clear"], shell=True)
        replayFromGenesisDb()


# def stateSyncInit ():
#     print(bcolors.OKGREEN + "Replacing trust height, trust hash, and RPCs in config.toml" + bcolors.ENDC)
#     LATEST_HEIGHT= subprocess.run(["curl -s http://osmo-sync.blockpane.com:26657/block | jq -r .result.block.header.height"], capture_output=True, shell=True, text=True, env=my_env)
#     TRUST_HEIGHT= str(int(LATEST_HEIGHT.stdout.strip()) - 2000)
#     TRUST_HASH= subprocess.run(["curl -s \"http://osmo-sync.blockpane.com:26657/block?height="+str(TRUST_HEIGHT)+"\" | jq -r .result.block_id.hash"], capture_output=True, shell=True, text=True, env=my_env)
#     RPCs = "osmo-sync.blockpane.com:26657,osmo-sync.blockpane.com:26657"
#     subprocess.run(["sed -i -E 's/enable = false/enable = true/g' "+osmo_home+"/config/config.toml"], shell=True)
#     subprocess.run(["sed -i -E 's/rpc_servers = \"\"/rpc_servers = \""+RPCs+"\"/g' "+osmo_home+"/config/config.toml"], shell=True)
#     subprocess.run(["sed -i -E 's/trust_height = 0/trust_height = "+TRUST_HEIGHT+"/g' "+osmo_home+"/config/config.toml"], shell=True)
#     subprocess.run(["sed -i -E 's/trust_hash = \"\"/trust_hash = \""+TRUST_HASH.stdout.strip()+"\"/g' "+osmo_home+"/config/config.toml"], shell=True)
#     print(bcolors.OKGREEN + """
# Osmosis is about to statesync. This process can take anywhere from 5-30 minutes.
# During this process, you will see many logs (to include many errors)
# As long as it continues to find/apply snapshot chunks, it is working.
# If it stops finding/applying snapshot chunks, you may cancel and try a different method.

# Continue?:
# 1) Yes
# 2) No
#     """+ bcolors.ENDC)
#     stateSyncAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
#     if stateSyncAns == "1":
#         subprocess.run(["osmosisd start"], shell=True, env=my_env)
#         print(bcolors.OKGREEN + "Statesync finished. Installing required patches for state sync fix" + bcolors.ENDC)
#         os.chdir(os.path.expanduser(HOME))
#         subprocess.run(["git clone https://github.com/tendermint/tendermint"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
#         os.chdir(os.path.expanduser(HOME+'/tendermint/'))
#         subprocess.run(["git checkout callum/app-version"], shell=True, env=my_env)
#         subprocess.run(["make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
#         subprocess.run(["tendermint set-app-version 1 --home "+osmo_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
#         subprocess.run(["clear"], shell=True)
#         if os_name == "Linux":
#             cosmovisorInit()
#         else:
#             complete()
#     elif stateSyncAns == "2":
#         dataSyncSelection()
#     else:
#         subprocess.run(["clear"], shell=True)
#         stateSyncInit()

#def testnetStateSyncInit ():
    #print(bcolors.OKGREEN + "Replacing trust height, trust hash, and RPCs in config.toml" + bcolors.ENDC)
    #LATEST_HEIGHT= subprocess.run(["curl -s http://143.198.139.33:26657/block | jq -r .result.block.header.height"], capture_output=True, shell=True, text=True, env=my_env)
    #TRUST_HEIGHT= str(int(LATEST_HEIGHT.stdout.strip()) - 2000)
    #TRUST_HASH= subprocess.run(["curl -s \"http://143.198.139.33:26657/block?height="+str(TRUST_HEIGHT)+"\" | jq -r .result.block_id.hash"], capture_output=True, shell=True, text=True, env=my_env)
    #RPCs = "143.198.139.33:26657,143.198.139.33:26657"
    #subprocess.run(["sed -i -E 's/enable = false/enable = true/g' "+osmo_home+"/config/config.toml"], shell=True)
    #subprocess.run(["sed -i -E 's/rpc_servers = \"\"/rpc_servers = \""+RPCs+"\"/g' "+osmo_home+"/config/config.toml"], shell=True)
    #subprocess.run(["sed -i -E 's/trust_height = 0/trust_height = "+TRUST_HEIGHT+"/g' "+osmo_home+"/config/config.toml"], shell=True)
    #subprocess.run(["sed -i -E 's/trust_hash = \"\"/trust_hash = \""+TRUST_HASH.stdout.strip()+"\"/g' "+osmo_home+"/config/config.toml"], shell=True)
    #if os_name == "Linux":
        #subprocess.run(["clear"], shell=True)
        #cosmovisorInit()
    #else:
        #subprocess.run(["clear"], shell=True)
        #complete()


def snapshotInstall ():
    print(bcolors.OKGREEN + "Downloading Decompression Packages..." + bcolors.ENDC)
    if os_name == "Linux":
        subprocess.run(["sudo apt-get install wget liblz4-tool aria2 -y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    else:
        subprocess.run(["brew install aria2"], shell=True, env=my_env)
        subprocess.run(["brew install lz4"], shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading Snapshot..." + bcolors.ENDC)
    proc = subprocess.run(["curl https://quicksync.io/osmosis.json|jq -r '.[] |select(.file==\""+ fileName +"\")|select (.mirror==\""+ location +"\")|.url'"], capture_output=True, shell=True, text=True)
    os.chdir(os.path.expanduser(osmo_home))
    subprocess.run(["wget -O - "+proc.stdout.strip()+" | lz4 -d | tar -xvf -"], shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)
    if os_name == "Linux":
        cosmovisorInit()
    else:
        complete()


def mainNetLocation ():
    global location
    print(bcolors.OKGREEN + """Please choose the location nearest to your node:
1) Netherlands
2) Singapore
3) SanFrancisco (WARNING: Location usually slow)
    """+ bcolors.ENDC)
    if args.snapshotLocation == "netherlands":
        nodeLocationAns = "1"
    elif args.snapshotLocation == "singapore":
        nodeLocationAns = "2"
    elif args.snapshotLocation == "sanfrancisco":
        nodeLocationAns = "3"
    else:
        nodeLocationAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if nodeLocationAns == "1":
        subprocess.run(["clear"], shell=True)
        location = "Netherlands"
        snapshotInstall()
    elif nodeLocationAns == "2":
        subprocess.run(["clear"], shell=True)
        location = "Singapore"
        snapshotInstall()
    elif nodeLocationAns == "3":
        subprocess.run(["clear"], shell=True)
        location = "SanFrancisco"
        snapshotInstall()
    else:
        subprocess.run(["clear"], shell=True)
        mainNetLocation()


def testNetType ():
    global fileName
    global location
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned (recommended)
2) Archive
    """+ bcolors.ENDC)
    if args.snapshotTypeTestnet == "pruned":
        nodeTypeAns = "1"
    elif args.snapshotTypeTestnet == "archive":
        nodeTypeAns = "2"
    else:
        nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if nodeTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        fileName = "osmotestnet-4-pruned"
        location = "Netherlands"
        snapshotInstall()
    elif nodeTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        fileName = "osmotestnet-4-archive"
        location = "Netherlands"
        snapshotInstall()
    else:
        subprocess.run(["clear"], shell=True)
        testNetType()


def mainNetType ():
    global fileName
    global location
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned (recommended)
2) Default
3) Archive
    """+ bcolors.ENDC)
    if args.snapshotType == "pruned":
        nodeTypeAns = "1"
    elif args.snapshotType == "default":
        nodeTypeAns = "2"
    elif args.snapshotType == "archive":
        nodeTypeAns = "3"
    else:
        nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if nodeTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        fileName = "osmosis-1-pruned"
        mainNetLocation()
    elif nodeTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        fileName = "osmosis-1-default"
        mainNetLocation()
    elif nodeTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        fileName = "osmosis-1-archive"
        location = "Netherlands"
        snapshotInstall()
    else:
        subprocess.run(["clear"], shell=True)
        mainNetType()


def dataSyncSelection ():
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) Start at block 1 and automatically upgrade at upgrade heights (replay from genesis, can also select rocksdb here)
3) Exit now, I only wanted to install the daemon
    """+ bcolors.ENDC)
    if args.dataSync == "snapshot":
        dataTypeAns = "1"
    elif args.dataSync == "genesis":
        dataTypeAns = "2"
    elif args.dataSync == "exit":
        dataTypeAns = "3"
    else:
        dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        mainNetType()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        extraSwap()
    #elif dataTypeAns == "2":
        #subprocess.run(["clear"], shell=True)
        #stateSyncInit ()
    elif dataTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        partComplete()
    else:
        subprocess.run(["clear"], shell=True)
        dataSyncSelection()


def dataSyncSelectionTest ():
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) Exit now, I only wanted to install the daemon
    """+ bcolors.ENDC)
    if args.dataSyncTestnet == "snapshot":
        dataTypeAns = "1"
    elif args.dataSyncTestnet == "exit":
        dataTypeAns = "2"
    else:
        dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        testNetType()
    #elif dataTypeAns == "2":
        #subprocess.run(["clear"], shell=True)
        #testnetStateSyncInit()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        partComplete()
    else:
        subprocess.run(["clear"], shell=True)
        dataSyncSelectionTest()


def pruningSettings ():
    print(bcolors.OKGREEN + """Please choose your desired pruning settings:
1) Default: (keep last 100,000 states to query the last week worth of data and prune at 100 block intervals)
2) Nothing: (keep everything, select this if running an archive node)
3) Everything: (modified prune everything due to bug, keep last 10,000 states and prune at a random prime block interval)
    """+ bcolors.ENDC)
    if args.pruning == "default":
        pruneAns = '1'
    elif args.pruning == "nothing":
        pruneAns = '2'
    elif args.pruning == "everything":
        pruneAns = '3'
    else:
        pruneAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if pruneAns == "1" and networkAns == "1":
        subprocess.run(["clear"], shell=True)
        dataSyncSelection()
    elif pruneAns == "1" and networkAns == "2":
        subprocess.run(["clear"], shell=True)
        dataSyncSelectionTest()
    elif pruneAns == "2" and networkAns == "1":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"nothing\"/g' "+osmo_home+"/config/app.toml"], shell=True)
        dataSyncSelection()
    elif pruneAns == "2" and networkAns == "2":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"nothing\"/g' "+osmo_home+"/config/app.toml"], shell=True)
        dataSyncSelectionTest()
    elif pruneAns == "3" and networkAns == "1":
        primeNum = random.choice([x for x in range(11, 97) if not [t for t in range(2, x) if not x % t]])
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"custom\"/g' "+osmo_home+"/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-keep-recent = \"0\"/pruning-keep-recent = \"10000\"/g' "+osmo_home+"/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-interval = \"0\"/pruning-interval = \""+str(primeNum)+"\"/g' "+osmo_home+"/config/app.toml"], shell=True)
        dataSyncSelection()
    elif pruneAns == "3" and networkAns == "2":
        primeNum = random.choice([x for x in range(11, 97) if not [t for t in range(2, x) if not x % t]])
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"custom\"/g' "+osmo_home+"/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-keep-recent = \"0\"/pruning-keep-recent = \"10000\"/g' "+osmo_home+"/config/app.toml"], shell=True)
        subprocess.run(["sed -i -E 's/pruning-interval = \"0\"/pruning-interval = \""+str(primeNum)+"\"/g' "+osmo_home+"/config/app.toml"], shell=True)
        dataSyncSelectionTest()
    else:
        subprocess.run(["clear"], shell=True)
        pruningSettings()


def customPortSelection ():
    print(bcolors.OKGREEN + """Do you want to run Osmosis on default ports?:
1) Yes, use default ports (recommended)
2) No, specify custom ports
    """+ bcolors.ENDC)
    if args.ports:
        api_server = args.ports[0]
        grpc_server = args.ports[1]
        grpc_web = args.ports[2]
        abci_app_addr = args.ports[3]
        rpc_laddr = args.ports[4]
        p2p_laddr = args.ports[5]
        pprof_laddr = args.ports[6]
    else:
        portChoice = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

        if portChoice == "1":
            subprocess.run(["clear"], shell=True)
            pruningSettings()
        elif portChoice == "2":
            subprocess.run(["clear"], shell=True)
            print(bcolors.OKGREEN + "Input desired values. Press enter for default values" + bcolors.ENDC)
            #app.toml
            api_server_def = "tcp://0.0.0.0:1317"
            grpc_server_def = "0.0.0.0:9090"
            grpc_web_def = "0.0.0.0:9091"
            #config.toml
            abci_app_addr_def = "tcp://127.0.0.1:26658"
            rpc_laddr_def = "tcp://127.0.0.1:26657"
            p2p_laddr_def = "tcp://0.0.0.0:26656"
            pprof_laddr_def = "localhost:6060"
            #user input
            api_server = rlinput(bcolors.OKGREEN +"(1/7) API Server: "+ bcolors.ENDC, api_server_def)
            grpc_server = rlinput(bcolors.OKGREEN +"(2/7) gRPC Server: "+ bcolors.ENDC, grpc_server_def)
            grpc_web = rlinput(bcolors.OKGREEN +"(3/7) gRPC Web: "+ bcolors.ENDC, grpc_web_def)
            abci_app_addr = rlinput(bcolors.OKGREEN +"(4/7) ABCI Application Address: "+ bcolors.ENDC, abci_app_addr_def)
            rpc_laddr = rlinput(bcolors.OKGREEN +"(5/7) RPC Listening Address: "+ bcolors.ENDC, rpc_laddr_def)
            p2p_laddr = rlinput(bcolors.OKGREEN +"(6/7) P2P Listening Address: "+ bcolors.ENDC, p2p_laddr_def)
            pprof_laddr = rlinput(bcolors.OKGREEN +"(7/7) pprof Listening Address: "+ bcolors.ENDC, pprof_laddr_def)
        elif portChoice and portChoice != "1" or portChoice != "2":
            subprocess.run(["clear"], shell=True)
            customPortSelection()
    #change app.toml values
    subprocess.run(["sed -i -E 's|tcp://0.0.0.0:1317|"+api_server+"|g' "+osmo_home+"/config/app.toml"], shell=True)
    subprocess.run(["sed -i -E 's|0.0.0.0:9090|"+grpc_server+"|g' "+osmo_home+"/config/app.toml"], shell=True)
    subprocess.run(["sed -i -E 's|0.0.0.0:9091|"+grpc_web+"|g' "+osmo_home+"/config/app.toml"], shell=True)
    #change config.toml values
    subprocess.run(["sed -i -E 's|tcp://127.0.0.1:26658|"+abci_app_addr+"|g' "+osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["sed -i -E 's|tcp://127.0.0.1:26657|"+rpc_laddr+"|g' "+osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["sed -i -E 's|tcp://0.0.0.0:26656|"+p2p_laddr+"|g' "+osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["sed -i -E 's|localhost:6060|"+pprof_laddr+"|g' "+osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["clear"], shell=True)
    pruningSettings()

def setupLocalnet ():
    print(bcolors.OKGREEN + "Initializing LocalOsmosis " + nodeName + bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME))
    subprocess.run(["git clone https://github.com/osmosis-labs/LocalOsmosis.git"], shell=True)
    localOsmosisComplete()

def setupMainnet ():
    print(bcolors.OKGREEN + "Initializing Osmosis Node " + nodeName + bcolors.ENDC)
    #subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+osmo_home+"/config/app.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+osmo_home+"/config/config.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+osmo_home+"/config/addrbook.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["osmosisd init " + nodeName + " --chain-id=osmo-1 -o --home "+osmo_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL ,shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Genesis..." + bcolors.ENDC)
    subprocess.run(["wget -O "+osmo_home+"/config/genesis.json https://github.com/osmosis-labs/networks/raw/main/osmosis-1/genesis.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Addressbook..." + bcolors.ENDC)
    subprocess.run(["wget -O "+osmo_home+"/config/addrbook.json https://quicksync.io/addrbook.osmosis.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)
    customPortSelection()


def setupTestnet ():
    print(bcolors.OKGREEN + "Initializing Osmosis Node " + nodeName + bcolors.ENDC)
    #subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+osmo_home+"/config/config.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+osmo_home+"/config/app.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm "+osmo_home+"/config/addrbook.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["osmosisd init " + nodeName + " --chain-id=osmo-test-4 -o --home "+osmo_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Genesis..." + bcolors.ENDC)
    subprocess.run(["wget -O "+osmo_home+"/config/genesis.tar.bz2 wget https://github.com/osmosis-labs/networks/raw/main/osmo-test-4/genesis.tar.bz2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Finding and Replacing Seeds..." + bcolors.ENDC)
    peers = "4ab030b7fd75ed895c48bcc899b99c17a396736b@137.184.190.127:26656,3dbffa30baab16cc8597df02945dcee0aa0a4581@143.198.139.33:26656"
    subprocess.run(["sed -i -E 's/persistent_peers = \"\"/persistent_peers = \""+peers+"\"/g' "+osmo_home+"/config/config.toml"], shell=True)
    subprocess.run(["tar -xjf "+osmo_home+"/config/genesis.tar.bz2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["rm "+osmo_home+"/config/genesis.tar.bz2"], shell=True)
    subprocess.run(["sed -i -E 's/seeds = \"21d7539792ee2e0d650b199bf742c56ae0cf499e@162.55.132.230:2000,295b417f995073d09ff4c6c141bd138a7f7b5922@65.21.141.212:2000,ec4d3571bf709ab78df61716e47b5ac03d077a1a@65.108.43.26:2000,4cb8e1e089bdf44741b32638591944dc15b7cce3@65.108.73.18:2000,f515a8599b40f0e84dfad935ba414674ab11a668@osmosis.blockpane.com:26656,6bcdbcfd5d2c6ba58460f10dbcfde58278212833@osmosis.artifact-staking.io:26656\"/seeds = \"0f9a9c694c46bd28ad9ad6126e923993fc6c56b1@137.184.181.105:26656\"/g' "+osmo_home+"/config/config.toml"], shell=True)
    print(bcolors.OKGREEN + "Downloading and Replacing Addressbook..." + bcolors.ENDC)
    subprocess.run(["wget -O "+osmo_home+"/config/addrbook.json https://quicksync.io/addrbook.osmotestnet.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)
    customPortSelection()


def clientSettings ():
    if networkAns == "1":
        print(bcolors.OKGREEN + "Initializing Osmosis Client Node " + nodeName + bcolors.ENDC)
        #subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm "+osmo_home+"/config/client.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["osmosisd init " + nodeName + " --chain-id=osmosis-1 -o --home "+osmo_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        print(bcolors.OKGREEN + "Changing Client Settings..." + bcolors.ENDC)
        subprocess.run(["sed -i -E 's/chain-id = \"\"/chain-id = \"osmosis-1\"/g' "+osmo_home+"/config/client.toml"], shell=True)
        #subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"https://rpc-osmosis.blockapsis.com:443\"|g' "+osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"http://osmosis.artifact-staking.io:26657\"|g' "+osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["clear"], shell=True)
        clientComplete()
    elif networkAns == "2":
        print(bcolors.OKGREEN + "Initializing Osmosis Client Node " + nodeName + bcolors.ENDC)
        #subprocess.run(["osmosisd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm "+osmo_home+"/config/client.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["osmosisd init " + nodeName + " --chain-id=osmo-test-4 -o --home "+osmo_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        print(bcolors.OKGREEN + "Changing Client Settings..." + bcolors.ENDC)
        subprocess.run(["sed -i -E 's/chain-id = \"\"/chain-id = \"osmo-test-4\"/g' "+osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"https://testnet-rpc.osmosis.zone:443\"|g' "+osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["clear"], shell=True)
        clientComplete()
    elif networkAns == "3":
        print(bcolors.OKGREEN + "Initializing LocalOsmosis Node " + nodeName + bcolors.ENDC)
        subprocess.run(["rm "+osmo_home+"/config/client.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["osmosisd init " + nodeName + " --chain-id=localosmosis -o --home "+osmo_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        print(bcolors.OKGREEN + "Changing Client Settings..." + bcolors.ENDC)
        subprocess.run(["sed -i -E 's/chain-id = \"\"/chain-id = \"localosmosis\"/g' "+osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"tcp://127.0.0.1:26657\"|g' "+osmo_home+"/config/client.toml"], shell=True)
        subprocess.run(["clear"], shell=True)
        setupLocalnet()


def initNodeName ():
    global nodeName
    print(bcolors.OKGREEN + "AFTER INPUTING NODE NAME, ALL PREVIOUS OSMOSIS DATA WILL BE RESET" + bcolors.ENDC)
    if args.nodeName:
        nodeName = args.nodeName
    else:
        nodeName= input(bcolors.OKGREEN + "Input desired node name (no quotes, cant be blank): "+ bcolors.ENDC)

    if nodeName and networkAns == "1" and node == "1":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["rm -r "+osmo_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm -r "+HOME+"/.osmosisd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        setupMainnet()
    elif nodeName and networkAns == "2" and node == "1":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["rm -r "+osmo_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm -r "+HOME+"/.osmosisd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        setupTestnet()
    elif nodeName and node == "2" or node == "3":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["rm -r "+osmo_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm -r "+HOME+"/.osmosisd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        clientSettings()
    else:
        subprocess.run(["clear"], shell=True)
        print(bcolors.OKGREEN + "Please insert a non-blank node name" + bcolors.ENDC)
        initNodeName()


def installLocationHandler ():
    global osmo_home
    print(bcolors.OKGREEN + "Input desired installation location. Press enter for default location" + bcolors.ENDC)
    location_def = subprocess.run(["echo $HOME/.osmosisd"], capture_output=True, shell=True, text=True).stdout.strip()
    if args.installHome:
        osmo_home = args.installHome
    else:
        osmo_home = rlinput(bcolors.OKGREEN +"Installation Location: "+ bcolors.ENDC, location_def)

    if osmo_home.endswith("/"):
        print(bcolors.FAIL + "Please ensure your path does not end with `/`" + bcolors.FAIL)
        installLocationHandler()
    elif not osmo_home.startswith("/") and not osmo_home.startswith("$"):
        print(bcolors.FAIL + "Please ensure your path begin with a `/`" + bcolors.FAIL)
        installLocationHandler()
    elif osmo_home == "":
        print(bcolors.FAIL + "Please ensure your path is not blank" + bcolors.FAIL)
        installLocationHandler()
    else:
        osmo_home = subprocess.run(["echo "+osmo_home], capture_output=True, shell=True, text=True).stdout.strip()
        subprocess.run(["clear"], shell=True)
        initNodeName()


def installLocation ():
    global osmo_home
    print(bcolors.OKGREEN + """Do you want to install Osmosis in the default location?:
1) Yes, use default location (recommended)
2) No, specify custom location
    """+ bcolors.ENDC)
    if args.installHome:
        locationChoice = '2'
    else:
        locationChoice = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if locationChoice == "1":
        subprocess.run(["clear"], shell=True)
        osmo_home = subprocess.run(["echo $HOME/.osmosisd"], capture_output=True, shell=True, text=True).stdout.strip()
        initNodeName()
    elif locationChoice == "2":
        subprocess.run(["clear"], shell=True)
        installLocationHandler()
    else:
        subprocess.run(["clear"], shell=True)
        installLocation()



def initSetup ():
    global my_env
    if os_name == "Linux":
        print(bcolors.OKGREEN + "Please wait while the following processes run:" + bcolors.ENDC)
        print(bcolors.OKGREEN + "(1/5) Updating Packages..." + bcolors.ENDC)
        subprocess.run(["sudo apt-get update"], stdout=subprocess.DEVNULL, shell=True)
        subprocess.run(["DEBIAN_FRONTEND=noninteractive apt-get -y upgrade"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(2/5) Installing make and GCC..." + bcolors.ENDC)
        subprocess.run(["sudo apt install git build-essential ufw curl jq snapd --yes"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(3/5) Installing Go..." + bcolors.ENDC)
        subprocess.run(["wget -q -O - https://git.io/vQhTU | bash -s -- --remove"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["wget -q -O - https://git.io/vQhTU | bash -s -- --version 1.18"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(4/5) Reloading Profile..." + bcolors.ENDC)
        subprocess.run([". "+HOME+"/.profile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        os.chdir(os.path.expanduser(HOME))
        subprocess.run(["git clone https://github.com/osmosis-labs/osmosis"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        os.chdir(os.path.expanduser(HOME+'/osmosis'))
        if networkAns == "1":
            print(bcolors.OKGREEN + "(5/5) Installing Osmosis v7.3.0 Binary..." + bcolors.ENDC)
            subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["git pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["git checkout v7.3.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        if networkAns == "2":
            print(bcolors.OKGREEN + "(5/5) Installing Osmosis v7.3.0 Binary..." + bcolors.ENDC)
            subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["git pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["git checkout v7.3.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        my_env = os.environ.copy()
        my_env["PATH"] = "/"+HOME+"/go/bin:/"+HOME+"/go/bin:/"+HOME+"/.go/bin:" + my_env["PATH"]
        subprocess.run(["make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        if node == "3":
            print(bcolors.OKGREEN + "Installing Docker..." + bcolors.ENDC)
            subprocess.run(["sudo apt-get remove docker docker-engine docker.io"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo apt-get update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo apt install docker.io -y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            print(bcolors.OKGREEN + "Installing Docker-Compose..." + bcolors.ENDC)
            subprocess.run(["sudo apt install docker-compose -y"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["clear"], shell=True)
    else:
        print(bcolors.OKGREEN + "Please wait while the following processes run:" + bcolors.ENDC)
        print(bcolors.OKGREEN + "(1/4) Installing brew and wget..." + bcolors.ENDC)
        subprocess.run(["sudo chown -R $(whoami) /usr/local/var/homebrew"], shell=True)
        subprocess.run(["echo | /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)\""], shell=True)
        #subprocess.run(["sudo chown -R $(whoami) /usr/local/share/zsh /usr/local/share/zsh/site-functions"], shell=True)
        subprocess.run(["echo 'eval \"$(/opt/homebrew/bin/brew shellenv)\"' >> "+HOME+"/.zprofile"], shell=True)
        subprocess.run(["eval \"$(/opt/homebrew/bin/brew shellenv)\""], shell=True)
        my_env = os.environ.copy()
        my_env["PATH"] = "/opt/homebrew/bin:/opt/homebrew/bin/brew:" + my_env["PATH"]
        subprocess.run(["brew install wget"], shell=True, env=my_env)
        print(bcolors.OKGREEN + "(2/4) Installing jq..." + bcolors.ENDC)
        subprocess.run(["brew install jq"], shell=True, env=my_env)
        print(bcolors.OKGREEN + "(3/4) Installing Go..." + bcolors.ENDC)
        subprocess.run(["brew install go@1.18"], shell=True, env=my_env)
        print(bcolors.OKGREEN + "(4/4) Installing Osmosis V7.3.0 Binary..." + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME))
        subprocess.run(["git clone https://github.com/osmosis-labs/osmosis"], shell=True)
        os.chdir(os.path.expanduser(HOME+'/osmosis'))
        subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["git pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["git checkout v7.3.0"], shell=True)
        my_env["PATH"] = "/"+HOME+"/go/bin:/"+HOME+"/go/bin:/"+HOME+"/.go/bin:" + my_env["PATH"]
        subprocess.run(["make install"], shell=True, env=my_env)
        if node == "3":
            print(bcolors.OKGREEN + "Installing Docker..." + bcolors.ENDC)
            subprocess.run(["brew install docker"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            print(bcolors.OKGREEN + "Installing Docker-Compose..." + bcolors.ENDC)
            subprocess.run(["brew install docker-compose"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["clear"], shell=True)
    installLocation()


def initEnvironment():
    if os_name == "Linux":
        print(bcolors.OKGREEN +"System Detected: Linux"+ bcolors.ENDC)
        mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        mem_gib = mem_bytes/(1024.**3)
        print(bcolors.OKGREEN +"RAM Detected: "+str(round(mem_gib))+"GB"+ bcolors.ENDC)
        if round(mem_gib) < 32:
            print(bcolors.OKGREEN +"""
You have less than the recommended 32GB of RAM. Would you like to set up a swap file?
1) Yes, set up swap file
2) No, do not set up swap file
            """+ bcolors.ENDC)
            if args.swapOn == True :
                swapAns = '1'
            elif args.swapOn == False :
                swapAns = '2'
            else:
                swapAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

            if swapAns == "1":
                swapNeeded = 32 - round(mem_gib)
                print(bcolors.OKGREEN +"Setting up "+ str(swapNeeded)+ "GB swap file..."+ bcolors.ENDC)
                subprocess.run(["sudo swapoff -a"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["sudo fallocate -l " +str(swapNeeded)+"G /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["sudo chmod 600 /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["sudo mkswap /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["sudo swapon /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["sudo cp /etc/fstab /etc/fstab.bak"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["clear"], shell=True)
                print(bcolors.OKGREEN +str(swapNeeded)+"GB swap file set"+ bcolors.ENDC)
                initSetup()
            elif swapAns == "2":
                subprocess.run(["clear"], shell=True)
                initSetup()
            else:
                subprocess.run(["clear"], shell=True)
                initEnvironment()
        else:
            print(bcolors.OKGREEN +"You have enough RAM to meet the 32GB minimum requirement, moving on to system setup..."+ bcolors.ENDC)
            time.sleep(3)
            subprocess.run(["clear"], shell=True)
            initSetup()

    elif os_name == "Darwin":
        print(bcolors.OKGREEN +"System Detected: Mac"+ bcolors.ENDC)
        mem_bytes = subprocess.run(["sysctl hw.memsize"], capture_output=True, shell=True, text=True)
        mem_bytes = str(mem_bytes.stdout.strip())
        mem_bytes = mem_bytes[11:]
        mem_gib = int(mem_bytes)/(1024.**3)
        print(bcolors.OKGREEN +"RAM Detected: "+str(round(mem_gib))+"GB"+ bcolors.ENDC)
        if round(mem_gib) < 32:
            print(bcolors.OKGREEN +"""
You have less than the recommended 32GB of RAM. Would you still like to continue?
1) Yes, continue
2) No, quit
            """+ bcolors.ENDC)
            if args.swapOn == True :
                warnAns = '1'
            elif args.swapOn == False :
                warnAns = '1'
            else:
                warnAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

            if warnAns == "1":
                subprocess.run(["clear"], shell=True)
                initSetup()
            elif warnAns == "2":
                subprocess.run(["clear"], shell=True)
                quit()
            else:
                subprocess.run(["clear"], shell=True)
                initEnvironment()
        else:
            print(bcolors.OKGREEN +"You have enough RAM to meet the 32GB minimum requirement, moving on to system setup..."+ bcolors.ENDC)
            time.sleep(3)
            subprocess.run(["clear"], shell=True)
            initSetup()
    else:
        print(bcolors.OKGREEN +"System OS not detected...Will continue with Linux environment assumption..."+ bcolors.ENDC)
        time.sleep(3)
        initSetup()


def networkSelect ():
    global networkAns
    print(bcolors.OKGREEN + """Please choose a network to join:
1) Mainnet (osmosis-1)
2) Testnet (osmo-test-4)
    """+ bcolors.ENDC)
    if args.network == "osmosis-1":
        networkAns = '1'
    elif args.network == "osmo-test-4":
        networkAns = '2'
    else:
        networkAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

    if networkAns == '1' and node == '1':
        subprocess.run(["clear"], shell=True)
        initEnvironment()
    elif networkAns == '1' and node == '2':
        subprocess.run(["clear"], shell=True)
        initSetup()
    elif networkAns == '2' and node == '1':
        subprocess.run(["clear"], shell=True)
        initEnvironment()
    elif networkAns == '2' and node == '2':
        subprocess.run(["clear"], shell=True)
        initSetup()
    else:
        subprocess.run(["clear"], shell=True)
        networkSelect()


def start ():
    subprocess.run(["clear"], shell=True)
    def restart ():
        global HOME
        global USER
        global GOPATH
        global machine
        global os_name
        global node
        os_name = platform.system()
        machine =  platform.machine()
        HOME = subprocess.run(["echo $HOME"], capture_output=True, shell=True, text=True).stdout.strip()
        USER = subprocess.run(["echo $USER"], capture_output=True, shell=True, text=True).stdout.strip()
        GOPATH = HOME+"/go"
        print(bcolors.OKGREEN + """
 ██████╗ ███████╗███╗   ███╗ ██████╗ ███████╗██╗███████╗
██╔═══██╗██╔════╝████╗ ████║██╔═══██╗██╔════╝██║██╔════╝
██║   ██║███████╗██╔████╔██║██║   ██║███████╗██║███████╗
██║   ██║╚════██║██║╚██╔╝██║██║   ██║╚════██║██║╚════██║
╚██████╔╝███████║██║ ╚═╝ ██║╚██████╔╝███████║██║███████║
 ╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝╚══════╝


Welcome to the Osmosis node installer V2.0.0!
For more information, please visit docs.osmosis.zone
Ensure no osmosis services are running in the background
If running over an old osmosis installation, back up
any important osmosis data before proceeding

Please choose a node type:
1) Full Node (download chain data and run locally)
2) Client Node (setup a daemon and query a public RPC)
3) LocalOsmosis Node (setup a daemon and query a localOsmosis development RPC)
        """+ bcolors.ENDC)
        if args.nodeType == 'full':
            node = '1'
        elif args.nodeType == 'client':
            node = '2'
        elif args.nodeType == 'local':
            node = '3'
        else:
            node = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)

        if node == '1':
            subprocess.run(["clear"], shell=True)
            networkSelect()
        elif node == '2':
            subprocess.run(["clear"], shell=True)
            networkSelect()
        elif node == '3':
            subprocess.run(["clear"], shell=True)
            initSetup()
        else:
            subprocess.run(["clear"], shell=True)
            restart()
    restart()

start()
