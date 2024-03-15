using Newtonsoft.Json;
using Service;
using Service.Configuration;
using Service.Enums;
using Service.Packets;

namespace UnitTests
{
    public class MockTransactionAuthService : MqttService
    {
        private TransactionAuthStatus ExpectedStatus;

        public bool IsTransactionAuthReceived { get; private set; }

        public MockTransactionAuthService(Config config, TransactionAuthStatus status) : base(config)
        {
            ExpectedStatus = status;
            Subscribe(TransactionAuthPacket.Topic, HandleTransactionAuthMessage);
        }

        private void HandleTransactionAuthMessage(string message)
        {
            var packet = JsonConvert.DeserializeObject<TransactionAuthPacket>(message);
            Assert.NotNull(packet);
            Assert.AreEqual(ExpectedStatus, packet.Status);
            IsTransactionAuthReceived = true;
        }
    }
}
