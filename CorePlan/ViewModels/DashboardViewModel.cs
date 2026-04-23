using CorePlan.Data;
using CorePlan.Models;
using LiveChartsCore;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Globalization;
using System.Runtime.CompilerServices;

namespace CorePlan.ViewModels
{
    public class DashboardViewModel : INotifyPropertyChanged
    {
        private readonly int _employeeId;

        private string _fullName;
        public string FullName
        {
            get => _fullName;
            set
            {
                if (_fullName != value)
                {
                    _fullName = value;
                    OnPropertyChanged();
                    OnPropertyChanged(nameof(WelcomeMessage));
                }
            }
        }

        private string _department;
        public string Department
        {
            get => _department;
            set
            {
                if (_department != value)
                {
                    _department = value;
                    OnPropertyChanged();
                    OnPropertyChanged(nameof(DepartmentDisplay));
                }
            }
        }

        public string WelcomeMessage => $"Welcome, {FullName}";
        public string DepartmentDisplay => !string.IsNullOrEmpty(Department) ? $"{Department} Department" : "";

        public ObservableCollection<DashboardCard> DashboardCards { get; set; } = new();

        public DashboardViewModel(int employeeId)
        {
            _employeeId = employeeId;
        }

        public ObservableCollection<SalesDataModel> SalesData { get; set; } = new();

        public async Task InitializeAsync()
        {
            var dbService = new DatabaseService();

            FullName = await dbService.GetEmployeeNameByIdAsync(_employeeId);
            Department = await dbService.GetDepartmentNameByEmployeeIdAsync(_employeeId);

            await LoadDashboardCardsAsync();
            OnPropertyChanged(nameof(DashboardCards));

            SalesData = new ObservableCollection<SalesDataModel>
            {
                new SalesDataModel { Month = "Feb", Value = 12000 },
                new SalesDataModel { Month = "Mar", Value = 18000 },
                new SalesDataModel { Month = "Apr", Value = 24000 },
                new SalesDataModel { Month = "May", Value = 20000 },
                new SalesDataModel { Month = "Jun", Value = 27000 },
                new SalesDataModel { Month = "Jul", Value = 22000 },
            };

            OnPropertyChanged(nameof(SalesData));
        }

        


        private async Task LoadDashboardCardsAsync()
        {
            var dbService = new DatabaseService();
            var today = DateTime.Today.ToString("yyyy-MM-dd");

            int appointments = await dbService.CountAppointmentsAsync(_employeeId, today);
            int followUps = await dbService.CountFollowUpsAsync(_employeeId, today);
            int tasks = await dbService.CountTasksDueTodayAsync(_employeeId, today);
            int deadlines = await dbService.CountDeadlinesDueTodayAsync(_employeeId, today);

            string contentToday = $"Meetings: {appointments}\nFollow-ups: {followUps}\nTasks: {tasks}\nDeadline(s): {deadlines}";

            var card1 = new DashboardCard
            {
                Title = "📌 Today’s Tasks",
                Content = contentToday
            };

            var upcomingDeals = await dbService.GetUpcomingSalesDeadlinesThisWeekAsync(_employeeId);
            var contentDeals = upcomingDeals.Any()
                ? string.Join("\n", upcomingDeals.Select(d => $"{d.Title} – {d.DueDate:ddd, dd MMM}"))
                : "No deals due this week.";

            var card2 = new DashboardCard
            {
                Title = "📅 Deals to Close This Week",
                Content = contentDeals
            };

            var (target, actual) = await dbService.GetMonthlyTargetProgressAsync(_employeeId);
            string content3;

            if (target > 0)
            {
                double percent = (double)(actual / target) * 100;
                string status = percent >= 60
                    ? "📈 On track to reach your goal."
                    : "⚠️ Behind schedule — needs attention.";

                content3 = $"Progress: {percent:F1}%\nTarget: ${target:N0}\nAchieved: ${actual:N0}\n{status}";
            }
            else
            {
                content3 = "No target data available.";
            }

            var card3 = new DashboardCard
            {
                Title = "🎯 Monthly Target Progress",
                Content = content3
            };

            var alerts = await dbService.GenerateSmartAlertsAsync(_employeeId);

            string alertsContent = alerts.Any()
            ? string.Join("\n", alerts.Select(a => a.message))
            : "✅ No active alerts.";



            var card4 = new DashboardCard
            {
                Title = "📢 Alerts & Warnings",
                Content = alertsContent
            };


            DashboardCards.Clear();
            DashboardCards.Add(card1);
            DashboardCards.Add(card2);
            DashboardCards.Add(card3);
            DashboardCards.Add(card4);
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged([CallerMemberName] string propertyName = null) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));

        //public async Task InitializeAsync()
        //{
        //    var dbService = new DatabaseService();

        //    FullName = await dbService.GetEmployeeNameByIdAsync(_employeeId);
        //    Department = await dbService.GetDepartmentNameByEmployeeIdAsync(_employeeId);

        //    await LoadDashboardCardsAsync();

        //    OnPropertyChanged(nameof(DashboardCards));
        //}

        //public event PropertyChangedEventHandler PropertyChanged;
        //protected void OnPropertyChanged([CallerMemberName] string propertyName = null) =>
        //    PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));

        //public ObservableCollection<DashboardCard> DashboardCards { get; set; } = new ObservableCollection<DashboardCard>
        //{
        //    new DashboardCard
        //    {
        //        Title = "📌 Today's Tasks",
        //        Content = "Meetings: 3\nFollow-ups: 2\nPitch: GlobalTech\nDeadline: 5 PM"
        //    },
        //    new DashboardCard
        //    {
        //        Title = "📈 Recent Opportunities",
        //        Content = "NovaTower Expansion (€54,000)\nEastPoint Logistics (€40,000)"
        //    },
        //    new DashboardCard
        //    {
        //        Title = "🤝 Client Engagement",
        //        Content = "Top Engaged: GlobalTech\nClient Notes: Positive feedback and upsell potential"
        //    },
        //    new DashboardCard
        //    {
        //        Title = "📊 Weekly Summary",
        //        Content = "Leads: 45\nDeals: 6\nRevenue: €126,000"
        //    }
        //};

        //public ObservableCollection<DashboardCard> DashboardCards { get; set; } = new ObservableCollection<DashboardCard>();

        //private async Task LoadDashboardCardsAsync()
        //{
        //    var dbService = new DatabaseService();
        //    var today = DateTime.Today.ToString("yyyy-MM-dd");

        //    int appointments = await dbService.CountAppointmentsAsync(_employeeId, today);
        //    int followUps = await dbService.CountFollowUpsAsync(_employeeId, today);
        //    int tasks = await dbService.CountTasksDueTodayAsync(_employeeId, today);
        //    int deadlines = await dbService.CountDeadlinesDueTodayAsync(_employeeId, today);

        //    DashboardCards.Clear();

        //    var todayCard = new DashboardCard
        //    {
        //        Title = "📌 Today’s Focus",
        //        AppointmentsCount = appointments,
        //        FollowUpsCount = followUps,
        //        TasksDueCount = tasks,
        //        DeadlinesCount = deadlines
        //    };

        //    await AppendDealsToMainCardAsync(todayCard);

        //    DashboardCards.Add(todayCard);
        //}


        //private async Task AppendDealsToMainCardAsync(DashboardCard card)
        //{
        //    var dbService = new DatabaseService();
        //    var deals = await dbService.GetUpcomingSalesDeadlinesThisWeekAsync(_employeeId);

        //    if (deals != null && deals.Any())
        //    {
        //        foreach (var deal in deals)
        //        {
        //            var day = deal.DueDate.ToString("ddd", CultureInfo.InvariantCulture);
        //            card.DealsThisWeek.Add($"{deal.Title} – {day}");
        //        }
        //    }
        //    else
        //    {
        //        card.DealsThisWeek.Add("No deals due this week.");
        //    }
        //}


        


    }
}
