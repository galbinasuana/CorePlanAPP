using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;


namespace CorePlan.Models
{
    public static class ChatbotService
    {
        private static Process chatbotProcess;
        public static bool IsActive { get; private set; } = false;

        public static void Start()
        {
            if (chatbotProcess != null && chatbotProcess.HasExited)
            {
                chatbotProcess.Dispose();
                chatbotProcess = null;
                IsActive = false;
            }

            if (IsActive)
                return;

            try
            {
                chatbotProcess = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = @"D:\Ase\Disertatie\Aplicatie\CorePlanApp\ChatbotWebView\bin\Debug\net8.0-windows\ChatbotWebView.exe",
                        UseShellExecute = true
                    },
                    EnableRaisingEvents = true
                };

                chatbotProcess.Exited += (s, e) =>
                {
                    IsActive = false;
                    chatbotProcess.Dispose();
                    chatbotProcess = null;
                };

                chatbotProcess.Start();
                IsActive = true;
            }
            catch (Exception ex)
            {
                Debug.WriteLine("❌ Failed to start chatbot: " + ex.Message);
                IsActive = false;
            }
        }


        public static void Stop()
        {
            try
            {
                if (chatbotProcess != null && !chatbotProcess.HasExited)
                {
                    chatbotProcess.Kill(true); 
                    chatbotProcess.Dispose();
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine("⚠️ Failed to stop chatbot: " + ex.Message);
            }
            finally
            {
                chatbotProcess = null;
                IsActive = false;
            }
        }

    }
}
