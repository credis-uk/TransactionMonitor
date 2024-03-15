using Service.Configuration;
using Service.Enums;
using Service.Packets;
using Service.TransactionMonitor;

namespace UnitTests
{
    public class TestTransactionMonitor
    {
        private const string CONFIG_FILE = "config.json";

        [SetUp]
        public void SetUp()
        {
            if (File.Exists(CONFIG_FILE))
            {
                File.Delete(CONFIG_FILE);
            }
        }

        [Test]
        [TestCase("dummy transaction data")]
        public void TestTransactionMonitorValidation(string data)
        {
            var mockAuthService = new MockTransactionAuthService(Config.Load<TransactionMonitorConfig>(CONFIG_FILE), TransactionAuthStatus.Approved);
            var service = new TransactionMonitorService(Config.Load<TransactionMonitorConfig>(CONFIG_FILE));
            service.Publish(TransactionPacket.Topic, new TransactionPacket() { Transaction = data });
            Thread.Sleep(1000);
            Assert.IsTrue(mockAuthService.IsTransactionAuthReceived);
        }
    }
}
