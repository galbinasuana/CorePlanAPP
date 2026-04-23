using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CorePlan.Models
{
    public class CalendarDay
    {
        public DateTime Date { get; set; }               
        public string DayNumber { get; set; }
        public bool IsCurrentMonth { get; set; }
        public bool IsSelected { get; set; }
        public bool HasAppointment { get; set; }


        public List<Appointment> Activities { get; set; } = new();
        public List<CalendarActivity> CalendarActivities { get; set; } = new();
    }
}
