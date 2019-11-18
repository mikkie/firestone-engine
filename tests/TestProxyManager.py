import unittest
from firestone_engine.ProxyManager import ProxyManager

class TestProxyManager(unittest.TestCase):
    
    
    def setUp(self):
        self.proxyManager = ProxyManager()
        self.assertEqual(len(self.proxyManager.proxy_pool), 10)


    def test_get_proxy(self):
        for i in range(0, 12):
            print(self.proxyManager.get_proxy())


if __name__ == "__main__":
    unittest.main()

# to debug in vscode uncomment this block
import ptvsd
# 5678 is the default attach port in the VS Code debug configurations
print("start debug on port 5678")
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()