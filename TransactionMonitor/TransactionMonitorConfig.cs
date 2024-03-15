using Service.Configuration;

namespace Service.TransactionMonitor
{
    public class TransactionMonitorConfig : Config
    {
        public string AiScriptFilename { get; set; } = "AITransactionMonitor.py";
    }
}
