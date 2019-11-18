import unittest
from firestone_engine.ProxyManager import ProxyManager

class TestProxyManager(unittest.TestCase):
    
    
    def setUp(self):
        self.proxyManager = ProxyManager()

    def test_get_proxy(self):
        proxy_list = []
        self.proxyManager.get_proxy()
        self.assertGreater(self.proxyManager.get_pool_size(), 0)
        i = 0
        while i <= self.proxyManager.get_pool_size():
            proxy = self.proxyManager.get_proxy()
            proxy_list.append(proxy)
            print(proxy)
            i += 1
        self.assertEqual(proxy_list[0], proxy_list[len(proxy_list) - 1]) 


if __name__ == "__main__":
    unittest.main()

# to debug in vscode uncomment this block
import ptvsd
# 5678 is the default attach port in the VS Code debug configurations
print("start debug on port 5678")
ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
ptvsd.wait_for_attach()