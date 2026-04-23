using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CorePlan.Models
{
    public class ClientDeal
    {
        public int ClientId { get; set; }
        public string DealName { get; set; }
        public string DealStage { get; set; }
        public decimal ExpectedValue { get; set; }
        public DateTime CloseDate { get; set; }
    }
}
