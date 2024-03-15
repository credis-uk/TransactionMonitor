using Service.TransactionMonitor;
using Service;
using Service.Configuration;

ServiceFactory.ServiceRunner<TransactionMonitorService>(Config.Load<TransactionMonitorConfig>("config.json"));