# Prepare and import smart contract into blockchain:

import os
import sys
import time
import datetime
from neo.Settings import settings
from neocore.Fixed8 import Fixed8
from neo.Wallets.utils import to_aes_key
from twisted.internet import reactor, task
from neo.Core.Blockchain import Blockchain
from neo.Network.NodeLeader import NodeLeader
from neo.Prompt.Commands.BuildNRun import BuildAndRun
from neo.Prompt.Commands.Invoke import test_invoke, InvokeContract
from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Implementations.Notifications.LevelDB.NotificationDB import NotificationDB
from neo.Prompt.Commands.LoadSmartContract import LoadContract, generate_deploy_script
from neo.Implementations.Blockchains.LevelDB.LevelDBBlockchain import LevelDBBlockchain


class ImportSC:
    chain = None
    twist = None
    wallet = None
    deferred = None
    start_dt = None
    start_height = None

    # args:
    args = []
    scPath = None

    def __init__(self, args=None, chain=None, twist=None):
        self.chain = chain
        self.twist = twist
        self.start_height = self.chain.Height
        self.start_dt = datetime.datetime.utcnow()

        self.args = args
        self.scPath = args[0]

        password = to_aes_key("coz")
        self.wallet = UserWallet.Open("/neo-python/neo-privnet.wallet", password)

        dbloop = task.LoopingCall(self.chain.PersistBlocks)
        dbloop_deferred = dbloop.start(.1)
        dbloop_deferred.addErrback(self.on_loopError)

        walletdb_loop = task.LoopingCall(self.wallet.ProcessBlocks)
        self.wallet_loop_deferred = walletdb_loop.start(1)
        self.wallet_loop_deferred.addErrback(self.on_loopError)

        self.wallet.Rebuild()

    def on_loopError(self, err):
        print("On DB loop error! %s (%s) " % (err, self.wallet.WalletHeight))
        self.twist.stop()

    def show_state(self):
        height = self.chain.Height
        headers = self.chain.HeaderHeight

        print("--------------------------------------")
        print("Progress: %s / %s" % (height, headers))
        print("Wallet Height: %s" % self.wallet.WalletHeight)
        print("--------------------------------------")
        print(self.wallet.GetSyncedBalances())
        print("--------------------------------------")

    @property
    def isSynced(self):
        height = self.chain.Height
        headers = self.chain.HeaderHeight
        return height == headers and self.wallet.IsSynced

    def worker(self):
        self.chain.Pause()
        BuildAndRun(self.args, wallet=self.wallet, verbose=True)
        self.chain.Resume()

        avm_path = self.scPath.replace('.py', '.avm')
        self.args[0] = avm_path

        from_addr = None

        code = LoadContract(args=self.args)

        # /scripts/sc.avm 0710 02 True False False
        if code:
            script = generate_deploy_script(code.Script,
                                            "myTestSmartContract",  # name
                                            "test",  # version
                                            "",  # author
                                            "",  # email
                                            "",  # description
                                            code.ContractProperties,
                                            code.ReturnTypeBigInteger,
                                            code.ParameterList)
            if script is not None:
                tx, fee, results, num_ops = test_invoke(script, self.wallet, [], from_addr=from_addr)
                if tx is not None and results is not None:
                    print("Test deploy invoke successful")
                    print("Deploy Invoke TX GAS cost: %s " % (tx.Gas.value / Fixed8.D))
                    print("Deploy Invoke TX Fee: %s " % (fee.value / Fixed8.D))
                    print("-------------------------")
                    while not self.isSynced:
                        self.show_state()
                        time.sleep(1)
                    result = InvokeContract(self.wallet, tx, Fixed8.Zero(), from_addr=from_addr)
                    print("Result: ", result.ToJson(), self.isSynced)
                    print("Result: ", tx.ToJson())

            print("Script:", script)


def main():
    args = sys.argv[1:]
    args += os.getenv('CONTRACT_FILE', '').split(' ')
    args += os.getenv('CONTRACT_ARGS', '').split(' ')
    args = list(filter(None, args))

    if len(args) < 2:  # must provide file name and arguments
        print("WARN! No smart contracts args... skip")
        return

    settings.setup_privnet(True)
    settings.set_log_smart_contract_events(True)

    # Instantiate the blockchain and subscribe to notifications
    blockchain = LevelDBBlockchain(settings.chain_leveldb_path)
    Blockchain.RegisterBlockchain(blockchain)

    app = ImportSC(args, blockchain, reactor)

    # Try to set up a notification db
    if NotificationDB.instance():
        NotificationDB.instance().start()

    reactor.callInThread(app.worker)

    NodeLeader.Instance().Start()

    reactor.run()

    NotificationDB.close()
    Blockchain.Default().Dispose()
    NodeLeader.Instance().Shutdown()


if __name__ == "__main__":
    main()
