using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

namespace CorePlan.Models
{
    public class Appointment
    {
        public DateTime Date { get; set; }
        public string Title { get; set; }
        public string StartTime { get; set; }
        public string EndTime { get; set; }
        public string ClientName { get; set; }
        public string Location { get; set; }
        public string ColorTag { get; set; }
        public int AppointmentId { get; set; }

        public int ClientId { get; set; }
        public int EmployeeId { get; set; }

        public string TimeRange => $"{StartTime} - {EndTime}";

        public ICommand EditCommand { get; set; }
        public ICommand DeleteCommand { get; set; }
    }
}
