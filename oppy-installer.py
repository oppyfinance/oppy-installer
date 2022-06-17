import subprocess
import os
import platform
import sys
import time
import readline
import random
import argparse
from mnemonic import Mnemonic

parser = argparse.ArgumentParser(description="Use default settings")
parser.add_argument('-m', action='store_true', help='use default settings with no input for mainnet')
parser.add_argument('-t', action='store_true', help='use default settings with no input for mainnet')

args = parser.parse_args()


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
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Oppysis full node!")
    print(bcolors.OKGREEN + "The cosmovisor service is currently running in the background")
    print(
        bcolors.OKGREEN + "To see the status of cosmovisor, run the following command: 'sudo systemctl status cosmovisor'")
    print(
        bcolors.OKGREEN + "To see the live logs from cosmovisor, run the following command: 'journalctl -u cosmovisor -f'")
    print(
        bcolors.OKGREEN + "In order to use oppyd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'" + bcolors.ENDC)
    quit()


def completeOppysisd():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Oppysis full node!")
    print(bcolors.OKGREEN + "The oppyd service is currently running in the background")
    print(
        bcolors.OKGREEN + "To see the status of the oppy daemon, run the following command: 'sudo systemctl status oppyd'")
    print(
        bcolors.OKGREEN + "To see the live logs from the oppy daemon, run the following command: 'journalctl -u oppyd -f'")
    print(
        bcolors.OKGREEN + "In order to use cosmovisor/oppyd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'" + bcolors.ENDC)
    quit()


def complete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Oppysis full node!")
    print(bcolors.OKGREEN + "The oppyd service is NOT running in the background")
    print(
        bcolors.OKGREEN + "In order to use oppyd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'")
    print(
        bcolors.OKGREEN + "After reloading your terminal and/or profile, you can start oppyd with: 'oppyd start'" + bcolors.ENDC)
    quit()


def partComplete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up the Oppysis daemon!")
    print(bcolors.OKGREEN + "The oppyd service is NOT running in the background, and your data directory is empty")
    print(
        bcolors.OKGREEN + "In order to use oppyd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'")
    print(
        bcolors.OKGREEN + "If you intend to use oppyd without syncing, you must include the '--node' flag after cli commands with the address of a public RPC node" + bcolors.ENDC)
    quit()


def clientComplete():
    print(bcolors.OKGREEN + "Congratulations! You have successfully completed setting up an Oppysis client node!")
    print(
        bcolors.OKGREEN + "DO NOT start the oppy daemon. You can query directly from the command line without starting the daemon!")
    print(
        bcolors.OKGREEN + "In order to use oppyd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'" + bcolors.ENDC)
    quit()


def replayComplete():
    print(bcolors.OKGREEN + "Congratulations! You are currently replaying from genesis in a background service!")
    print(
        bcolors.OKGREEN + "To see the status of cosmovisor, run the following command: 'sudo systemctl status cosmovisor'")
    print(
        bcolors.OKGREEN + "To see the live logs from cosmovisor, run the following command: 'journalctl -u cosmovisor -f'")
    print(
        bcolors.OKGREEN + "In order to use oppyd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'" + bcolors.ENDC)
    quit()


def replayDelay():
    print(bcolors.OKGREEN + "Congratulations! Oppysis is ready to replay from genesis on your command!")
    print(bcolors.OKGREEN + "YOU MUST MANUALLY INCREASE ULIMIT FILE SIZE BEFORE STARTING WITH `ulimit -n 200000`")
    print(
        bcolors.OKGREEN + "In order to use oppyd from the cli, either reload your terminal or refresh your profile with: 'source ~/.profile'")
    print(
        bcolors.OKGREEN + "Once reloaded, use the command `cosmosvisor start` to start the replay from genesis process")
    print(bcolors.OKGREEN + "It is recommended to run this in a tmux session if not running in a background service")
    print(
        bcolors.OKGREEN + "You must use `cosmosvisor start` and not `oppyd start` in order to upgrade automatically" + bcolors.ENDC)
    quit()


def cosmovisorService():
    print(bcolors.OKGREEN + "Creating Cosmovisor Service" + bcolors.ENDC)
    subprocess.run(["echo '# Setup Cosmovisor' >> " + HOME + "/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export DAEMON_NAME=oppyd' >> " + HOME + "/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export DAEMON_HOME=" + oppy_home + "' >> " + HOME + "/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export DAEMON_ALLOW_DOWNLOAD_BINARIES=false' >> " + HOME + "/.profile"], shell=True,
                   env=my_env)
    subprocess.run(["echo 'export DAEMON_LOG_BUFFER_SIZE=512' >> " + HOME + "/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export DAEMON_RESTART_AFTER_UPGRADE=true' >> " + HOME + "/.profile"], shell=True, env=my_env)
    subprocess.run(["echo 'export UNSAFE_SKIP_BACKUP=true' >> " + HOME + "/.profile"], shell=True, env=my_env)
    subprocess.run(["""echo '[Unit]
Description=Cosmovisor daemon
After=network-online.target
[Service]
Environment=\"DAEMON_NAME=oppyd\"
Environment=\"DAEMON_HOME=""" + oppy_home + """\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
Environment=\"UNSAFE_SKIP_BACKUP=true\"
User=""" + USER + """
ExecStart=""" + HOME + """/go/bin/cosmovisor start --home """ + oppy_home + """
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


def oppydService():
    print(bcolors.OKGREEN + "Creating Oppysisd Service..." + bcolors.ENDC)
    subprocess.run(["""echo '[Unit]
Description=Oppysis Daemon
After=network-online.target
[Service]
User=""" + USER + """
ExecStart=""" + HOME + """/go/bin/oppyd start --home """ + oppy_home + """
Restart=always
RestartSec=3
LimitNOFILE=infinity
LimitNPROC=infinity
Environment=\"DAEMON_HOME=""" + oppy_home + """\"
Environment=\"DAEMON_NAME=oppyd\"
Environment=\"DAEMON_ALLOW_DOWNLOAD_BINARIES=false\"
Environment=\"DAEMON_RESTART_AFTER_UPGRADE=true\"
Environment=\"DAEMON_LOG_BUFFER_SIZE=512\"
[Install]
WantedBy=multi-user.target
' >oppyd.service
    """], shell=True, env=my_env)
    subprocess.run(["sudo mv oppyd.service /lib/systemd/system/oppyd.service"], shell=True, env=my_env)
    subprocess.run(["sudo systemctl daemon-reload"], shell=True, env=my_env)
    subprocess.run(["systemctl restart systemd-journald"], shell=True, env=my_env)


def cosmovisorInit():
    print(bcolors.OKGREEN + """Do you want to use Cosmovisor to automate future upgrades?
1) Yes, install cosmovisor and set up background service
2) No, just set up an oppyd background service (recommended)
3) Don't install cosmovisor and don't set up a background service
    """ + bcolors.ENDC)
    if args.m == True:
        useCosmovisor = '2'
    else:
        useCosmovisor = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if useCosmovisor == "1":
        subprocess.run(["clear"], shell=True)
        print(bcolors.OKGREEN + "Setting Up Cosmovisor..." + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME))
        subprocess.run(["go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor"], shell=True, env=my_env)
        subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/genesis"], shell=True, env=my_env)
        subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/genesis/bin"], shell=True, env=my_env)
        subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades"], shell=True, env=my_env)
        subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades/v7/bin"], shell=True, env=my_env)
        os.chdir(os.path.expanduser(HOME + '/oppy'))
        subprocess.run(["git checkout v7.2.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                       env=my_env)
        subprocess.run(["make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["cp build/oppyd " + oppy_home + "/cosmovisor/upgrades/v7/bin"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run([". " + HOME + "/.profile"], shell=True, env=my_env)
        subprocess.run(["cp " + GOPATH + "/bin/oppyd " + oppy_home + "/cosmovisor/genesis/bin"], shell=True,
                       env=my_env)
        cosmovisorService()
        subprocess.run(["sudo systemctl start cosmovisor"], shell=True, env=my_env)
        subprocess.run(["clear"], shell=True)
        completeCosmovisor()
    elif useCosmovisor == "2":
        oppydService()
        subprocess.run(["sudo systemctl start oppyd"], shell=True, env=my_env)
        subprocess.run(["clear"], shell=True)
        completeOppysisd()
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
    """ + bcolors.ENDC)
    startNow = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)
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


def replayFromGenesisLevelDb():
    print(bcolors.OKGREEN + "Setting Up Cosmovisor..." + bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME))
    subprocess.run(["go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/genesis"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/genesis/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades/v4/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades/v5/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades/v7/bin"], shell=True, env=my_env)
    os.chdir(os.path.expanduser(HOME + '/oppychain'))

    subprocess.run(["make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["cp oppyChaind " + oppy_home + "/cosmovisor/genesis/bin"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=my_env)


    # subprocess.run(["git checkout v3.1.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
    #                env=my_env)
    # subprocess.run(["make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run([". " + HOME + "/.profile"], shell=True, env=my_env)
    # subprocess.run(["cp " + GOPATH + "/bin/oppyd " + oppy_home + "/cosmovisor/genesis/bin"], shell=True, env=my_env)
    print(bcolors.OKGREEN + "Adding Persistent Peers For Replay..." + bcolors.ENDC)
    peers = "9fd886cd0dd656e01aaedf61db63af1bf79b701e@164.92.138.207:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.66.52.160:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.82.89.95:26656"
    subprocess.run([
                       "sed -i -E 's/persistent_peers = \"\"/persistent_peers = \"" + peers + "\"/g' " + oppy_home + "/config/config.toml"],
                   shell=True)
    subprocess.run(["clear"], shell=True)
    startReplayNow()


def replayFromGenesisRocksDb():
    print(bcolors.OKGREEN + "Changing db_backend to rocksdb..." + bcolors.ENDC)
    subprocess.run(
        ["sed -i -E 's/db_backend = \"goleveldb\"/db_backend = \"rocksdb\"/g' " + oppy_home + "/config/config.toml"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    print(bcolors.OKGREEN + "Installing rocksdb..." + bcolors.ENDC)
    print(bcolors.OKGREEN + "This process may take 15 minutes or more" + bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME))
    subprocess.run(["sudo apt-get install -y libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["git clone https://github.com/facebook/rocksdb.git"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)
    os.chdir(os.path.expanduser(HOME + "/rocksdb"))
    subprocess.run(["git checkout v6.29.3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(
        ["export CXXFLAGS='-Wno-error=deprecated-copy -Wno-error=pessimizing-move -Wno-error=class-memaccess'"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["sudo make shared_lib"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["sudo make install-shared INSTALL_PATH=/usr"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   shell=True)
    subprocess.run(["sudo echo 'export LD_LIBRARY_PATH=/usr/local/lib' >> $HOME/.bashrc"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)
    my_env["LD_LIBRARY_PATH"] = "/usr/local/lib"
    print(bcolors.OKGREEN + "Setting Up Cosmovisor..." + bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME))
    subprocess.run(["go install github.com/cosmos/cosmos-sdk/cosmovisor/cmd/cosmovisor@v1.0.0"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/genesis"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/genesis/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades/v4/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades/v5/bin"], shell=True, env=my_env)
    subprocess.run(["mkdir -p " + oppy_home + "/cosmovisor/upgrades/v7/bin"], shell=True, env=my_env)
    os.chdir(os.path.expanduser(HOME + '/oppy'))
    print(bcolors.OKGREEN + "Preparing v4 Upgrade..." + bcolors.ENDC)
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["git checkout v4.2.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["sed '/gorocksdb.*/d' ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["echo \" \" >> ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["echo 'replace github.com/tecbot/gorocksdb => github.com/cosmos/gorocksdb v1.2.0' >> ./go.mod"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["go mod tidy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["cp build/oppyd " + oppy_home + "/cosmovisor/upgrades/v4/bin"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Preparing v5/v6 Upgrade..." + bcolors.ENDC)
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["git checkout v6.4.1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["cp build/oppyd " + oppy_home + "/cosmovisor/upgrades/v5/bin"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Preparing v7 Upgrade..." + bcolors.ENDC)
    subprocess.run(["git checkout v7.2.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["cp build/oppyd " + oppy_home + "/cosmovisor/upgrades/v7/bin"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["git checkout v3.1.0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["sed '/gorocksdb.*/d' ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["echo \" \" >> ./go.mod"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(
        ["echo 'require github.com/tecbot/gorocksdb v0.0.0-20191217155057-f0fad39f321c // indirect' >> ./go.mod"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["echo 'replace github.com/tecbot/gorocksdb => github.com/cosmos/gorocksdb v1.2.0' >> ./go.mod"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["go mod tidy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make build"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run([". " + HOME + "/.profile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    subprocess.run(["cp build/oppyd " + oppy_home + "/cosmovisor/genesis/bin"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["BUILD_TAGS=rocksdb make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   shell=True, env=my_env)
    subprocess.run(["sudo /sbin/ldconfig -v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                   env=my_env)
    print(bcolors.OKGREEN + "Adding Persistent Peers For Replay..." + bcolors.ENDC)
    peers = "9fd886cd0dd656e01aaedf61db63af1bf79b701e@164.92.138.207:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.66.52.160:26656,2dd86ed01eae5673df4452ce5b0dddb549f46a38@34.82.89.95:26656"
    subprocess.run([
                       "sed -i -E 's/persistent_peers = \"\"/persistent_peers = \"" + peers + "\"/g' " + oppy_home + "/config/config.toml"],
                   shell=True)
    subprocess.run(["clear"], shell=True)
    startReplayNow()


def replayFromGenesisDb():
    print(bcolors.OKGREEN + """Please choose which database you want to use:
1) goleveldb (Default)
2) rocksdb (faster but less support)
    """ + bcolors.ENDC)
    databaseType = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)
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
    mem_gib = mem_bytes / (1024. ** 3)
    print(bcolors.OKGREEN + "RAM Detected: " + str(round(mem_gib)) + "GB" + bcolors.ENDC)
    swapNeeded = 64 - round(mem_gib)
    if round(mem_gib) < 64:
        print(bcolors.OKGREEN + """
There have been reports of replay from genesis needing extra swap (up to 64GB) to prevent OOM errors.
Would you like to overwrite any previous swap file and instead set a """ + str(swapNeeded) + """GB swap file?
1) Yes, set up extra swap (recommended)
2) No, do not set up extra swap
        """ + bcolors.ENDC)
        swapAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)
        if swapAns == "1":
            print(bcolors.OKGREEN + "Setting up " + str(swapNeeded) + "GB swap file..." + bcolors.ENDC)
            subprocess.run(["sudo swapoff -a"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo fallocate -l " + str(swapNeeded) + "G /swapfile"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo chmod 600 /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           shell=True)
            subprocess.run(["sudo mkswap /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo swapon /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["sudo cp /etc/fstab /etc/fstab.bak"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           shell=True)
            subprocess.run(["echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab"], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["clear"], shell=True)
            print(bcolors.OKGREEN + str(swapNeeded) + "GB swap file set" + bcolors.ENDC)
            replayFromGenesisDb()
        elif swapAns == "2":
            subprocess.run(["clear"], shell=True)
            replayFromGenesisDb()
        else:
            subprocess.run(["clear"], shell=True)
            extraSwap()
    else:
        print(
            bcolors.OKGREEN + "You have enough RAM to meet the 64GB minimum requirement, moving on to system setup..." + bcolors.ENDC)
        time.sleep(3)
        subprocess.run(["clear"], shell=True)
        replayFromGenesisDb()


# def stateSyncInit ():
#     print(bcolors.OKGREEN + "Replacing trust height, trust hash, and RPCs in config.toml" + bcolors.ENDC)
#     LATEST_HEIGHT= subprocess.run(["curl -s http://osmo-sync.blockpane.com:26657/block | jq -r .result.block.header.height"], capture_output=True, shell=True, text=True, env=my_env)
#     TRUST_HEIGHT= str(int(LATEST_HEIGHT.stdout.strip()) - 2000)
#     TRUST_HASH= subprocess.run(["curl -s \"http://osmo-sync.blockpane.com:26657/block?height="+str(TRUST_HEIGHT)+"\" | jq -r .result.block_id.hash"], capture_output=True, shell=True, text=True, env=my_env)
#     RPCs = "osmo-sync.blockpane.com:26657,osmo-sync.blockpane.com:26657"
#     subprocess.run(["sed -i -E 's/enable = false/enable = true/g' "+oppy_home+"/config/config.toml"], shell=True)
#     subprocess.run(["sed -i -E 's/rpc_servers = \"\"/rpc_servers = \""+RPCs+"\"/g' "+oppy_home+"/config/config.toml"], shell=True)
#     subprocess.run(["sed -i -E 's/trust_height = 0/trust_height = "+TRUST_HEIGHT+"/g' "+oppy_home+"/config/config.toml"], shell=True)
#     subprocess.run(["sed -i -E 's/trust_hash = \"\"/trust_hash = \""+TRUST_HASH.stdout.strip()+"\"/g' "+oppy_home+"/config/config.toml"], shell=True)
#     print(bcolors.OKGREEN + """
# Oppysis is about to statesync. This process can take anywhere from 5-30 minutes.
# During this process, you will see many logs (to include many errors)
# As long as it continues to find/apply snapshot chunks, it is working.
# If it stops finding/applying snapshot chunks, you may cancel and try a different method.

# Continue?:
# 1) Yes
# 2) No
#     """+ bcolors.ENDC)
#     stateSyncAns = input(bcolors.OKGREEN + 'Enter Choice: '+ bcolors.ENDC)
#     if stateSyncAns == "1":
#         subprocess.run(["oppyd start"], shell=True, env=my_env)
#         print(bcolors.OKGREEN + "Statesync finished. Installing required patches for state sync fix" + bcolors.ENDC)
#         os.chdir(os.path.expanduser(HOME))
#         subprocess.run(["git clone https://github.com/tendermint/tendermint"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
#         os.chdir(os.path.expanduser(HOME+'/tendermint/'))
#         subprocess.run(["git checkout callum/app-version"], shell=True, env=my_env)
#         subprocess.run(["make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
#         subprocess.run(["tendermint set-app-version 1 --home "+oppy_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
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

# def testnetStateSyncInit ():
# print(bcolors.OKGREEN + "Replacing trust height, trust hash, and RPCs in config.toml" + bcolors.ENDC)
# LATEST_HEIGHT= subprocess.run(["curl -s http://143.198.139.33:26657/block | jq -r .result.block.header.height"], capture_output=True, shell=True, text=True, env=my_env)
# TRUST_HEIGHT= str(int(LATEST_HEIGHT.stdout.strip()) - 2000)
# TRUST_HASH= subprocess.run(["curl -s \"http://143.198.139.33:26657/block?height="+str(TRUST_HEIGHT)+"\" | jq -r .result.block_id.hash"], capture_output=True, shell=True, text=True, env=my_env)
# RPCs = "143.198.139.33:26657,143.198.139.33:26657"
# subprocess.run(["sed -i -E 's/enable = false/enable = true/g' "+oppy_home+"/config/config.toml"], shell=True)
# subprocess.run(["sed -i -E 's/rpc_servers = \"\"/rpc_servers = \""+RPCs+"\"/g' "+oppy_home+"/config/config.toml"], shell=True)
# subprocess.run(["sed -i -E 's/trust_height = 0/trust_height = "+TRUST_HEIGHT+"/g' "+oppy_home+"/config/config.toml"], shell=True)
# subprocess.run(["sed -i -E 's/trust_hash = \"\"/trust_hash = \""+TRUST_HASH.stdout.strip()+"\"/g' "+oppy_home+"/config/config.toml"], shell=True)
# if os_name == "Linux":
# subprocess.run(["clear"], shell=True)
# cosmovisorInit()
# else:
# subprocess.run(["clear"], shell=True)
# complete()


def snapshotInstall():
    print(bcolors.OKGREEN + "Downloading Decompression Packages..." + bcolors.ENDC)
    if os_name == "Linux":
        subprocess.run(["sudo apt-get install wget liblz4-tool aria2 -y"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)
    else:
        subprocess.run(["brew install aria2"], shell=True, env=my_env)
        subprocess.run(["brew install lz4"], shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading Snapshot..." + bcolors.ENDC)
    proc = subprocess.run([
                              "curl https://quicksync.io/oppy.json|jq -r '.[] |select(.file==\"" + fileName + "\")|select (.mirror==\"" + location + "\")|.url'"],
                          capture_output=True, shell=True, text=True)
    os.chdir(os.path.expanduser(oppy_home))
    subprocess.run(["wget -O - " + proc.stdout.strip() + " | lz4 -d | tar -xvf -"], shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)
    if os_name == "Linux":
        cosmovisorInit()
    else:
        complete()


def mainNetLocation():
    global location
    print(bcolors.OKGREEN + """Please choose the location nearest to your node:
1) Netherlands
2) Singapore
3) SanFrancisco (WARNING: Location usually slow)
    """ + bcolors.ENDC)
    nodeLocationAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)
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


def testNetType():
    global fileName
    global location
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned (recommended)
2) Archive
    """ + bcolors.ENDC)
    nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)
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


def mainNetType():
    global fileName
    global location
    print(bcolors.OKGREEN + """Please choose the node snapshot type:
1) Pruned (recommended)
2) Default
3) Archive
    """ + bcolors.ENDC)
    nodeTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)
    if nodeTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        fileName = "oppy-1-pruned"
        mainNetLocation()
    elif nodeTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        fileName = "oppy-1-default"
        mainNetLocation()
    elif nodeTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        fileName = "oppy-1-archive"
        location = "Netherlands"
        snapshotInstall()
    else:
        subprocess.run(["clear"], shell=True)
        mainNetType()


def dataSyncSelection():
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) Start at block 1 and automatically upgrade at upgrade heights (replay from genesis, can also select rocksdb here)
3) Exit now, I only wanted to install the daemon
    """ + bcolors.ENDC)
    if args.m == True:
        global location;
        location = "Netherlands"
        global fileName;
        fileName = "oppy-1-pruned"
        snapshotInstall()
    else:
        dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        mainNetType()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        extraSwap()
    # elif dataTypeAns == "2":
    # subprocess.run(["clear"], shell=True)
    # stateSyncInit ()
    elif dataTypeAns == "3":
        subprocess.run(["clear"], shell=True)
        partComplete()
    else:
        subprocess.run(["clear"], shell=True)
        dataSyncSelection()


def dataSyncSelectionTest():
    print(bcolors.OKGREEN + """Please choose from the following options:
1) Download a snapshot from ChainLayer (recommended)
2) Exit now, I only wanted to install the daemon
    """ + bcolors.ENDC)
    if args.t == True:
        global fileName;
        fileName = "osmotestnet-4-pruned"
        global location;
        location = "Netherlands"
        snapshotInstall()
    else:
        dataTypeAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if dataTypeAns == "1":
        subprocess.run(["clear"], shell=True)
        testNetType()
    # elif dataTypeAns == "2":
    # subprocess.run(["clear"], shell=True)
    # testnetStateSyncInit()
    elif dataTypeAns == "2":
        subprocess.run(["clear"], shell=True)
        installBridge()
    else:
        subprocess.run(["clear"], shell=True)
        dataSyncSelectionTest()


def installBridge():
    print(bcolors.OKGREEN + "Now we install the bridge"+bcolors.ENDC)
    os.chdir(os.path.expanduser(HOME))
    subprocess.run(["git clone https://github.com/oppyfinance/oppy-bridge.git"], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, shell=True)

    os.chdir(os.path.expanduser(HOME+"/oppy-bridge"))
    print(bcolors.OKGREEN + "(5/5) Installing Oppy bridge Binary..." + bcolors.ENDC)
    subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["git pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    subprocess.run(["git checkout dev"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

    my_env = os.environ.copy()
    my_env["PATH"] = "/" + HOME + "/go/bin:/" + HOME + "/go/bin:/" + HOME + "/.go/bin:" + my_env["PATH"]
    subprocess.run(["make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)

    subprocess.run(["clear"], shell=True)





    partComplete()


def pruningSettings():
    print(bcolors.OKGREEN + """Please choose your desired pruning settings:
1) Default: (keep last 100,000 states to query the last week worth of data and prune at 100 block intervals)
2) Nothing: (keep everything, select this if running an archive node)
3) Everything: (modified prune everything due to bug, keep last 10,000 states and prune at a random prime block interval)
    """ + bcolors.ENDC)
    if args.m == True:
        pruneAns = '3'
    else:
        pruneAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if pruneAns == "1" and networkAns == "1":
        subprocess.run(["clear"], shell=True)
        dataSyncSelection()
    elif pruneAns == "1" and networkAns == "2":
        subprocess.run(["clear"], shell=True)
        dataSyncSelectionTest()
    elif pruneAns == "2" and networkAns == "1":
        subprocess.run(["clear"], shell=True)
        subprocess.run(
            ["sed -i -E 's/pruning = \"default\"/pruning = \"nothing\"/g' " + oppy_home + "/config/app.toml"],
            shell=True)
        dataSyncSelection()
    elif pruneAns == "2" and networkAns == "2":
        subprocess.run(["clear"], shell=True)
        subprocess.run(
            ["sed -i -E 's/pruning = \"default\"/pruning = \"nothing\"/g' " + oppy_home + "/config/app.toml"],
            shell=True)
        dataSyncSelectionTest()
    elif pruneAns == "3" and networkAns == "1":
        primeNum = random.choice([x for x in range(11, 97) if not [t for t in range(2, x) if not x % t]])
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"custom\"/g' " + oppy_home + "/config/app.toml"],
                       shell=True)
        subprocess.run([
                           "sed -i -E 's/pruning-keep-recent = \"0\"/pruning-keep-recent = \"10000\"/g' " + oppy_home + "/config/app.toml"],
                       shell=True)
        subprocess.run(["sed -i -E 's/pruning-interval = \"0\"/pruning-interval = \"" + str(
            primeNum) + "\"/g' " + oppy_home + "/config/app.toml"], shell=True)
        dataSyncSelection()
    elif pruneAns == "3" and networkAns == "2":
        primeNum = random.choice([x for x in range(11, 97) if not [t for t in range(2, x) if not x % t]])
        subprocess.run(["clear"], shell=True)
        subprocess.run(["sed -i -E 's/pruning = \"default\"/pruning = \"custom\"/g' " + oppy_home + "/config/app.toml"],
                       shell=True)
        subprocess.run([
                           "sed -i -E 's/pruning-keep-recent = \"0\"/pruning-keep-recent = \"10000\"/g' " + oppy_home + "/config/app.toml"],
                       shell=True)
        subprocess.run(["sed -i -E 's/pruning-interval = \"0\"/pruning-interval = \"" + str(
            primeNum) + "\"/g' " + oppy_home + "/config/app.toml"], shell=True)
        dataSyncSelectionTest()
    else:
        subprocess.run(["clear"], shell=True)
        pruningSettings()


def customPortSelection():
    print(bcolors.OKGREEN + """Do you want to run Oppychain on default ports?:
1) Yes, use default ports (recommended)
2) No, specify custom ports
    """ + bcolors.ENDC)
    portChoice = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)
    if portChoice == "1":
        subprocess.run(["clear"], shell=True)
        pruningSettings()
    elif portChoice == "2":
        subprocess.run(["clear"], shell=True)
        print(bcolors.OKGREEN + "Input desired values. Press enter for default values" + bcolors.ENDC)
        # app.toml
        api_server_def = "tcp://0.0.0.0:1317"
        grpc_server_def = "0.0.0.0:9090"
        grpc_web_def = "0.0.0.0:9091"
        # config.toml
        abci_app_addr_def = "tcp://127.0.0.1:26658"
        rpc_laddr_def = "tcp://127.0.0.1:26657"
        p2p_laddr_def = "tcp://0.0.0.0:26656"
        pprof_laddr_def = "localhost:6060"
        # user input
        api_server = rlinput(bcolors.OKGREEN + "(1/7) API Server: " + bcolors.ENDC, api_server_def)
        grpc_server = rlinput(bcolors.OKGREEN + "(2/7) gRPC Server: " + bcolors.ENDC, grpc_server_def)
        grpc_web = rlinput(bcolors.OKGREEN + "(3/7) gRPC Web: " + bcolors.ENDC, grpc_web_def)
        abci_app_addr = rlinput(bcolors.OKGREEN + "(4/7) ABCI Application Address: " + bcolors.ENDC, abci_app_addr_def)
        rpc_laddr = rlinput(bcolors.OKGREEN + "(5/7) RPC Listening Address: " + bcolors.ENDC, rpc_laddr_def)
        p2p_laddr = rlinput(bcolors.OKGREEN + "(6/7) P2P Listening Address: " + bcolors.ENDC, p2p_laddr_def)
        pprof_laddr = rlinput(bcolors.OKGREEN + "(7/7) pprof Listening Address: " + bcolors.ENDC, pprof_laddr_def)
        # change app.toml values
        subprocess.run(["sed -i -E 's|tcp://0.0.0.0:1317|" + api_server + "|g' " + oppy_home + "/config/app.toml"],
                       shell=True)
        subprocess.run(["sed -i -E 's|0.0.0.0:9090|" + grpc_server + "|g' " + oppy_home + "/config/app.toml"],
                       shell=True)
        subprocess.run(["sed -i -E 's|0.0.0.0:9091|" + grpc_web + "|g' " + oppy_home + "/config/app.toml"], shell=True)
        # change config.toml values
        subprocess.run(
            ["sed -i -E 's|tcp://127.0.0.1:26658|" + abci_app_addr + "|g' " + oppy_home + "/config/config.toml"],
            shell=True)
        subprocess.run(["sed -i -E 's|tcp://127.0.0.1:26657|" + rpc_laddr + "|g' " + oppy_home + "/config/config.toml"],
                       shell=True)
        subprocess.run(["sed -i -E 's|tcp://0.0.0.0:26656|" + p2p_laddr + "|g' " + oppy_home + "/config/config.toml"],
                       shell=True)
        subprocess.run(["sed -i -E 's|localhost:6060|" + pprof_laddr + "|g' " + oppy_home + "/config/config.toml"],
                       shell=True)
        subprocess.run(["clear"], shell=True)
        pruningSettings()
    else:
        subprocess.run(["clear"], shell=True)
        customPortSelection()


def setupMainnet():
    print(bcolors.OKGREEN + "Initializing Oppysis Node " + nodeName + bcolors.ENDC)
    # subprocess.run(["oppyd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["rm " + oppy_home + "/config/app.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   shell=True, env=my_env)
    subprocess.run(["rm " + oppy_home + "/config/config.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   shell=True, env=my_env)
    subprocess.run(["rm " + oppy_home + "/config/addrbook.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                   shell=True, env=my_env)
    subprocess.run(["oppyChaind init " + nodeName + " --chain-id=oppyChain-1 -o --home " + oppy_home],
                   stdout=sys.stdout, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Genesis..." + bcolors.ENDC)
    subprocess.run([
                       "wget -O " + oppy_home + "/config/genesis.json https://github.com/oppy-labs/networks/raw/main/oppy-1/genesis.json"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Addressbook..." + bcolors.ENDC)
    subprocess.run(["wget -O " + oppy_home + "/config/addrbook.json https://quicksync.io/addrbook.oppy.json"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)

    if args.m == True:
        pruningSettings()
    else:
        customPortSelection()


def setupTestnet(nodeName):

    print(bcolors.OKGREEN + "Initializing Oppy Node " + nodeName + bcolors.ENDC)
    # subprocess.run(["oppyd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    # subprocess.run(["rm " + oppy_home + "/config/config.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    #                shell=True, env=my_env)
    # subprocess.run(["rm " + oppy_home + "/config/app.toml"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    #                shell=True, env=my_env)
    # subprocess.run(["rm " + oppy_home + "/config/addrbook.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    #                shell=True, env=my_env)

    ## we need users to write down the mnemonic files
    mnemo = Mnemonic("english")
    words = mnemo.generate(strength=256)
    print(bcolors.OKGREEN + """Please write down the mnemonic in a safe please and it is the only way to recover your node!!!"""+ bcolors.ENDC)
    print(bcolors.FAIL + "\n\n"+words +"\n\n"+bcolors.ENDC)

    input(bcolors.OKGREEN + "PLEASE CONFIRM YOU HAVE WRITE DOWN THE MNEMONIC(1) " + bcolors.ENDC)
    input(bcolors.OKGREEN + "PLEASE CONFIRM YOU HAVE WRITE DOWN THE MNEMONIC(2) " + bcolors.ENDC)
    input(bcolors.OKGREEN + "PLEASE CONFIRM YOU HAVE WRITE DOWN THE MNEMONIC(3) " + bcolors.ENDC)

    subprocess.run(["echo "+ words + "|oppyChaind init " + nodeName + " --chain-id=oppychain-1 -o --home " + oppy_home + "--recover"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    print(bcolors.OKGREEN + "Downloading and Replacing Genesis..." + bcolors.ENDC)
    subprocess.run(["wget -O " + oppy_home + "/config/genesis.json wget https://rpc.test.oppy.zone/genesis"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)

    subprocess.run(["curl https://rpc.test.oppy.zone/genesis |jq '.result''.genesis'>" + oppy_home + "/config/genesis.json"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)


    print(bcolors.OKGREEN + "Finding and Replacing Seeds..." + bcolors.ENDC)
    peers = "b7aef07e409a37a36edb73d17d6fc8b4ada85169@67.219.100.37:26656"
    subprocess.run([
                       "sed -i -E 's/persistent_peers = \"\"/persistent_peers = \"" + peers + "\"/g' " + oppy_home + "/config/config.toml"],
                   shell=True)
    #we avoid the seed node here
    # subprocess.run([
    #                    "sed -i -E 's/seeds = \"seeds = \"0f9a9c694c46bd28ad9ad6126e923993fc6c56b1@137.184.181.105:26656\"/g' " + oppy_home + "/config/config.toml"],
    #                shell=True)
    # print(bcolors.OKGREEN + "Downloading and Replacing Addressbook..." + bcolors.ENDC)
    # subprocess.run(["wget -O " + oppy_home + "/config/addrbook.json https://quicksync.io/addrbook.osmotestnet.json"],
    #                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
    subprocess.run(["clear"], shell=True)
    if args.m == True:
        pruningSettings()
    else:
        customPortSelection()


def clientSettings():
    if networkAns == "1":
        print(bcolors.OKGREEN + "Initializing Oppysis Client Node " + nodeName + bcolors.ENDC)
        # subprocess.run(["oppyd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm " + oppy_home + "/config/client.toml"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["oppyd init " + nodeName + " --chain-id=oppy-1 -o --home " + oppy_home],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        print(bcolors.OKGREEN + "Changing Client Settings..." + bcolors.ENDC)
        subprocess.run(
            ["sed -i -E 's/chain-id = \"\"/chain-id = \"oppy-1\"/g' " + oppy_home + "/config/client.toml"],
            shell=True)
        # subprocess.run(["sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"https://rpc-oppy.blockapsis.com:443\"|g' "+oppy_home+"/config/client.toml"], shell=True)
        subprocess.run([
                           "sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"http://oppy.artifact-staking.io:26657\"|g' " + oppy_home + "/config/client.toml"],
                       shell=True)
        subprocess.run(["clear"], shell=True)
        clientComplete()
    elif networkAns == "2":
        print(bcolors.OKGREEN + "Initializing Oppysis Client Node " + nodeName + bcolors.ENDC)
        # subprocess.run(["oppyd unsafe-reset-all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["rm " + oppy_home + "/config/client.toml"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["oppyd init " + nodeName + " --chain-id=osmo-test-4 -o --home " + oppy_home],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        print(bcolors.OKGREEN + "Changing Client Settings..." + bcolors.ENDC)
        subprocess.run(
            ["sed -i -E 's/chain-id = \"\"/chain-id = \"osmo-test-4\"/g' " + oppy_home + "/config/client.toml"],
            shell=True)
        subprocess.run([
                           "sed -i -E 's|node = \"tcp://localhost:26657\"|node = \"https://testnet-rpc.oppy.zone:443\"|g' " + oppy_home + "/config/client.toml"],
                       shell=True)
        subprocess.run(["clear"], shell=True)
        clientComplete()


def initNodeName():
    global nodeName
    print(bcolors.OKGREEN + "AFTER INPUTING NODE NAME, ALL PREVIOUS OPPY DATA WILL BE RESET" + bcolors.ENDC)
    if args.m == True:
        nodeName = 'defaultNode'
    else:
        nodeName = input(bcolors.OKGREEN + "Input desired node name (no quotes, cant be blank): " + bcolors.ENDC)

    if nodeName and networkAns == "1" and node == "1":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["rm -r " + oppy_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                       env=my_env)
        subprocess.run(["rm -r " + HOME + "/.oppyChain"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       shell=True, env=my_env)
        setupMainnet()
    elif nodeName and networkAns == "2" and node == "1":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["rm -r " + oppy_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                       env=my_env)
        subprocess.run(["rm -r " + HOME + "/.oppyChain"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       shell=True, env=my_env)
        setupTestnet(nodeName)
    elif nodeName and node == "2":
        subprocess.run(["clear"], shell=True)
        subprocess.run(["rm -r " + oppy_home], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                       env=my_env)
        subprocess.run(["rm -r " + HOME + "/.oppyd"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                       shell=True, env=my_env)
        clientSettings()
    else:
        subprocess.run(["clear"], shell=True)
        print(bcolors.OKGREEN + "Please insert a non-blank node name" + bcolors.ENDC)
        initNodeName()


def installLocationHandler():
    global oppy_home
    print(bcolors.OKGREEN + "Input desired installation location. Press enter for default location" + bcolors.ENDC)
    # app.toml
    location_def = subprocess.run(["echo $HOME/.oppychain"], capture_output=True, shell=True, text=True).stdout.strip()
    # user input
    oppy_home = rlinput(bcolors.OKGREEN + "Installation Location: " + bcolors.ENDC, location_def)
    if oppy_home.endswith("/"):
        print(bcolors.FAIL + "Please ensure your path does not end with `/`" + bcolors.FAIL)
        installLocationHandler()
    elif not oppy_home.startswith("/") and not oppy_home.startswith("$"):
        print(bcolors.FAIL + "Please ensure your path begin with a `/`" + bcolors.FAIL)
        installLocationHandler()
    elif oppy_home == "":
        print(bcolors.FAIL + "Please ensure your path is not blank" + bcolors.FAIL)
        installLocationHandler()
    else:
        oppy_home = subprocess.run(["echo " + oppy_home], capture_output=True, shell=True, text=True).stdout.strip()
        subprocess.run(["clear"], shell=True)
        initNodeName()


def installLocation():
    global oppy_home
    print(bcolors.OKGREEN + """Do you want to install Oppysis in the default location?:
1) Yes, use default location (recommended)
2) No, specify custom location
    """ + bcolors.ENDC)
    if args.m == True:
        locationChoice = '1'
    else:
        locationChoice = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    if locationChoice == "1":
        subprocess.run(["clear"], shell=True)
        oppy_home = subprocess.run(["echo $HOME/.oppyChain"], capture_output=True, shell=True, text=True).stdout.strip()
        initNodeName()
    elif locationChoice == "2":
        subprocess.run(["clear"], shell=True)
        installLocationHandler()
    else:
        subprocess.run(["clear"], shell=True)
        installLocation()


def initSetup():
    global my_env
    if os_name == "Linux":
        print(bcolors.OKGREEN + "Please wait while the following processes run:" + bcolors.ENDC)
        print(bcolors.OKGREEN + "(1/5) Updating Packages..." + bcolors.ENDC)
        subprocess.run(["sudo apt-get update"], stdout=subprocess.DEVNULL, shell=True)
        subprocess.run(["DEBIAN_FRONTEND=noninteractive apt-get -y upgrade"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(2/5) Installing make and GCC..." + bcolors.ENDC)
        subprocess.run(["sudo apt install git build-essential ufw curl jq snapd --yes"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(3/5) Installing Go..." + bcolors.ENDC)
        subprocess.run(["wget -q -O - https://git.io/vQhTU | bash -s -- --version 1.17.2"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)
        print(bcolors.OKGREEN + "(4/5) Reloading Profile..." + bcolors.ENDC)
        subprocess.run([". " + HOME + "/.profile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        os.chdir(os.path.expanduser(HOME))
        subprocess.run(["git clone https://github.com/oppyfinance/oppychain.git"], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, shell=True)
        os.chdir(os.path.expanduser(HOME + '/oppychain'))
        # fixme we checkout the dev at the moment
        if networkAns == "1":
            print(bcolors.OKGREEN + "(5/5) Installing Oppychain Binary..." + bcolors.ENDC)
            subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["git pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["git checkout  dev"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        if networkAns == "2":
            print(bcolors.OKGREEN + "(5/5) Installing Oppychain Binary..." + bcolors.ENDC)
            subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["git pull"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            subprocess.run(["git checkout dev"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        my_env = os.environ.copy()
        my_env["PATH"] = "/" + HOME + "/go/bin:/" + HOME + "/go/bin:/" + HOME + "/.go/bin:" + my_env["PATH"]
        subprocess.run(["make install"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["cp /root/oppychain/oppyChaind "+HOME+"/go/bin/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["clear"], shell=True)
    else:
        print(bcolors.OKGREEN + "Please wait while the following processes run:" + bcolors.ENDC)
        print(bcolors.OKGREEN + "(1/4) Installing brew and wget..." + bcolors.ENDC)
        subprocess.run(["sudo chown -R $(whoami) /usr/local/var/homebrew"], shell=True)
        subprocess.run([
                           "echo | /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)\""],
                       shell=True)
        # subprocess.run(["sudo chown -R $(whoami) /usr/local/share/zsh /usr/local/share/zsh/site-functions"], shell=True)
        subprocess.run(["echo 'eval \"$(/opt/homebrew/bin/brew shellenv)\"' >> " + HOME + "/.zprofile"], shell=True)
        subprocess.run(["eval \"$(/opt/homebrew/bin/brew shellenv)\""], shell=True)
        my_env = os.environ.copy()
        my_env["PATH"] = "/opt/homebrew/bin:/opt/homebrew/bin/brew:" + my_env["PATH"]
        subprocess.run(["brew install wget"], shell=True, env=my_env)
        print(bcolors.OKGREEN + "(2/4) Installing jq..." + bcolors.ENDC)
        subprocess.run(["brew install jq"], shell=True, env=my_env)
        print(bcolors.OKGREEN + "(3/4) Installing Go..." + bcolors.ENDC)
        subprocess.run(["brew install go@1.17"], shell=True, env=my_env)
        print(bcolors.OKGREEN + "(4/4) Installing Oppysis V7.2.0 Binary..." + bcolors.ENDC)
        os.chdir(os.path.expanduser(HOME))
        subprocess.run(["git clone https://github.com/oppy-labs/oppy"], shell=True)
        os.chdir(os.path.expanduser(HOME + '/oppy'))
        subprocess.run(["git stash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        subprocess.run(["git checkout v7.2.0"], shell=True)
        my_env["PATH"] = "/" + HOME + "/go/bin:/" + HOME + "/go/bin:/" + HOME + "/.go/bin:" + my_env["PATH"]
        subprocess.run(["make install"], shell=True, env=my_env)
        subprocess.run(["cp /root/oppychain/oppyChaind "+HOME+"/go/bin/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, env=my_env)
        subprocess.run(["clear"], shell=True)
    installLocation()


def initEnvironment():
    if os_name == "Linux":
        print(bcolors.OKGREEN + "System Detected: Linux" + bcolors.ENDC)
        mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        mem_gib = mem_bytes / (1024. ** 3)
        print(bcolors.OKGREEN + "RAM Detected: " + str(round(mem_gib)) + "GB" + bcolors.ENDC)
        if round(mem_gib) < 32:
            print(bcolors.OKGREEN + """
You have less than the recommended 32GB of RAM. Would you like to set up a swap file?
1) Yes, set up swap file
2) No, do not set up swap file
            """ + bcolors.ENDC)
            if args.m == True:
                swapAns = '1'
            else:
                swapAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

            if swapAns == "1":
                swapNeeded = 32 - round(mem_gib)
                print(bcolors.OKGREEN + "Setting up " + str(swapNeeded) + "GB swap file..." + bcolors.ENDC)
                subprocess.run(["sudo swapoff -a"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["sudo fallocate -l " + str(swapNeeded) + "G /swapfile"], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["sudo chmod 600 /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               shell=True)
                subprocess.run(["sudo mkswap /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               shell=True)
                subprocess.run(["sudo swapon /swapfile"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               shell=True)
                subprocess.run(["sudo cp /etc/fstab /etc/fstab.bak"], stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
                subprocess.run(["clear"], shell=True)
                print(bcolors.OKGREEN + str(swapNeeded) + "GB swap file set" + bcolors.ENDC)
                initSetup()
            elif swapAns == "2":
                subprocess.run(["clear"], shell=True)
                initSetup()
            else:
                subprocess.run(["clear"], shell=True)
                initEnvironment()
        else:
            print(
                bcolors.OKGREEN + "You have enough RAM to meet the 32GB minimum requirement, moving on to system setup..." + bcolors.ENDC)
            time.sleep(3)
            subprocess.run(["clear"], shell=True)
            initSetup()

    elif os_name == "Darwin":
        print(bcolors.OKGREEN + "System Detected: Mac" + bcolors.ENDC)
        mem_bytes = subprocess.run(["sysctl hw.memsize"], capture_output=True, shell=True, text=True)
        mem_bytes = str(mem_bytes.stdout.strip())
        mem_bytes = mem_bytes[11:]
        mem_gib = int(mem_bytes) / (1024. ** 3)
        print(bcolors.OKGREEN + "RAM Detected: " + str(round(mem_gib)) + "GB" + bcolors.ENDC)
        if round(mem_gib) < 32:
            print(bcolors.OKGREEN + """
You have less than the recommended 32GB of RAM. Would you still like to continue?
1) Yes, continue
2) No, quit
            """ + bcolors.ENDC)
            warnAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)
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
            print(
                bcolors.OKGREEN + "You have enough RAM to meet the 32GB minimum requirement, moving on to system setup..." + bcolors.ENDC)
            time.sleep(3)
            subprocess.run(["clear"], shell=True)
            initSetup()
    else:
        print(
            bcolors.OKGREEN + "System OS not detected...Will continue with Linux environment assumption..." + bcolors.ENDC)
        time.sleep(3)
        initSetup()


def networkSelect():
    global networkAns
    print(bcolors.OKGREEN + """Please choose a network to join:
1) Mainnet (oppyChain-1)
2) Testnet (oppydev-1)
    """ + bcolors.ENDC)
    if args.m == True and args.t != True:
        networkAns = '1'
    elif args.t == True:
        networkAns = '2'
    else:
        networkAns = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

    # this is full node and main net
    if networkAns == '1' and node == '1':
        subprocess.run(["clear"], shell=True)
        initEnvironment()
    # this is full node test net
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


def start():
    subprocess.run(["clear"], shell=True)

    def restart():
        global HOME
        global USER
        global GOPATH
        global machine
        global os_name
        global node
        os_name = platform.system()
        machine = platform.machine()
        HOME = subprocess.run(["echo $HOME"], capture_output=True, shell=True, text=True).stdout.strip()
        USER = subprocess.run(["echo $USER"], capture_output=True, shell=True, text=True).stdout.strip()
        GOPATH = HOME + "/go"
        print(bcolors.OKGREEN + """
                         ___                       ____ _           _       
                        / _ \ _ __  _ __  _   _   / ___| |__   __ _(_)_ __  
                       | | | | '_ \| '_ \| | | | | |   | '_ \ / _` | | '_ \ 
                       | |_| | |_) | |_) | |_| | | |___| | | | (_| | | | | |
                        \___/| .__/| .__/ \__, |  \____|_| |_|\__,_|_|_| |_|
                             |_|   |_|    |___/                             

Please choose a node type:
1) Full Node (download chain data and run locally)
2) Client Node (setup a daemon and query a public RPC)
        """ + bcolors.ENDC)
        if args.m == True and args.t == False:
            node = '1'
        elif args.t == True and args.m == False:
            args.m = True
            node = '1'
        else:
            node = input(bcolors.OKGREEN + 'Enter Choice: ' + bcolors.ENDC)

        if node == '1':
            subprocess.run(["clear"], shell=True)
            networkSelect()
        elif node == '2':
            subprocess.run(["clear"], shell=True)
            networkSelect()
        else:
            subprocess.run(["clear"], shell=True)
            restart()

    restart()


start()
