using IronPython.Hosting;
using Microsoft.Scripting.Hosting;
using Newtonsoft.Json;
using Service.Enums;
using Service.Globals;
using Service.Packets;

namespace Service.TransactionMonitor
{
    public class TransactionMonitorService : MqttService
    {
        public override string Name => Services.TransactionMonitor;

        private ScriptEngine Engine;
        private ScriptScope Scope;

        private string AiScriptFilename => ((TransactionMonitorConfig)Config).AiScriptFilename;

        public TransactionMonitorService(TransactionMonitorConfig config) : base(config)
        {
            Engine = Python.CreateEngine();
            Scope = Engine.CreateScope();
            Subscribe(LogPacket.Topic, HandleTransactionMessage);
        }

        private void HandleTransactionMessage(string message)
        {
            try
            {
                var packet = JsonConvert.DeserializeObject<TransactionPacket>(message);

                Engine.ExecuteFile(AiScriptFilename, Scope);
                float result = (float)Scope.GetVariable("my_function")(packet.Transaction);
                var status = result < 0.5 ? TransactionAuthStatus.Approved : TransactionAuthStatus.Denied;

                Publish(TransactionAuthPacket.Topic, new TransactionAuthPacket() { Status = status, ConfidenceScore = result });
            }
            catch (Exception e)
            {
                Log(LogLevel.Error, e.Message, e.StackTrace);
            }
        }
    }
}
