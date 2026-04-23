using CorePlan.Data;
using CorePlan.Models;
using MySqlConnector;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Input;

namespace CorePlan.ViewModels
{
    public class CalendarViewModel : INotifyPropertyChanged
    {
        private readonly DatabaseService db;
        private readonly int _employeeId;

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

        public string DepartmentDisplay => !string.IsNullOrEmpty(Department) ? $"{Department} Department" : "";

        public ICommand DayTappedCommand { get; }
        public ICommand AddOrUpdateAppointmentCommand { get; }

        public CalendarViewModel(int employeeId)
        {
            _employeeId = employeeId;
            db = new DatabaseService();

            DayTappedCommand = new Command<CalendarDay>(OnDayTapped);
            AddOrUpdateAppointmentCommand = new Command(async () => await AddOrUpdateAppointmentAsync());
        }


        public ObservableCollection<Client> AssignedClients { get; set; } = new();

        private Client _selectedClient;
        public Client SelectedClient
        {
            get => _selectedClient;
            set
            {
                if (_selectedClient != value)
                {
                    _selectedClient = value;
                    OnPropertyChanged();
                    IsClientPlaceholderVisible = _selectedClient == null;
                }
            }
        }

        private bool _isClientPlaceholderVisible = true;
        public bool IsClientPlaceholderVisible
        {
            get => _isClientPlaceholderVisible;
            set
            {
                if (_isClientPlaceholderVisible != value)
                {
                    _isClientPlaceholderVisible = value;
                    OnPropertyChanged();
                }
            }
        }


        public async Task LoadDataAsync()
        {
            var db = new DatabaseService();
            Department = await db.GetDepartmentNameByEmployeeIdAsync(_employeeId);

            var clients = await db.GetClientsByEmployeeIdAsync(_employeeId);
            AssignedClients.Clear();
            foreach (var client in clients)
            {
                AssignedClients.Add(client);
            }


            var days = await GenerateCalendarDaysAsync();
            CalendarDays = days;
            OnPropertyChanged(nameof(CalendarDays));

            var today = DateTime.Today;
            var todayDay = CalendarDays.FirstOrDefault(d =>
                d.IsCurrentMonth && d.Date.Date == today);

            if (todayDay != null)
            {
                OnDayTapped(todayDay); 
            }
        }

        private DateTime _currentMonth = DateTime.Today;
        public string CurrentMonthYear => _currentMonth.ToString("MMMM yyyy", CultureInfo.InvariantCulture);


        public async Task GoToPreviousMonth()
        {
            _currentMonth = _currentMonth.AddMonths(-1);
            await LoadCalendarForCurrentMonth();
            OnPropertyChanged(nameof(CurrentMonthYear));
        }

        public async Task GoToNextMonth()
        {
            _currentMonth = _currentMonth.AddMonths(1);
            await LoadCalendarForCurrentMonth();
            OnPropertyChanged(nameof(CurrentMonthYear));
        }

        public async Task LoadCalendarForCurrentMonth()
        {
            var days = await GenerateCalendarDaysAsync(_currentMonth);
            CalendarDays = days;
            OnPropertyChanged(nameof(CalendarDays));
        }

        public ObservableCollection<CalendarDay> CalendarDays { get; set; }

        public async Task<ObservableCollection<CalendarDay>> GenerateCalendarDaysAsync(DateTime? selectedDate = null)
        {
            var calendarDays = new ObservableCollection<CalendarDay>();

            DateTime today = selectedDate ?? DateTime.Now;
            DateTime firstDayOfMonth = new DateTime(today.Year, today.Month, 1);
            int daysInMonth = DateTime.DaysInMonth(today.Year, today.Month);

            int startOffset = ((int)firstDayOfMonth.DayOfWeek + 6) % 7;

            // 🔹 Zile din luna anterioară
            DateTime prevMonth = today.AddMonths(-1);
            int daysInPrevMonth = DateTime.DaysInMonth(prevMonth.Year, prevMonth.Month);

            for (int i = startOffset - 1; i >= 0; i--)
            {
                int day = daysInPrevMonth - i;
                calendarDays.Add(new CalendarDay
                {
                    Date = new DateTime(prevMonth.Year, prevMonth.Month, day),
                    DayNumber = day.ToString(),
                    IsCurrentMonth = false,
                    CalendarActivities = new List<CalendarActivity>()
                });
            }

            // 🔹 Obține programările din DB pentru luna curentă și employee_id
            var db = new DatabaseService();
            var appointments = await db.GetAppointmentsForMonth(today.Year, today.Month, _employeeId);

            // Grupăm programările pe zi
            var groupedAppointments = appointments
                .GroupBy(a => a.Date.Day)
                .ToDictionary(g => g.Key, g => g.ToList());

            // 🔹 Zilele lunii curente
            for (int day = 1; day <= daysInMonth; day++)
            {
                var date = new DateTime(today.Year, today.Month, day);

                var calendarDay = new CalendarDay
                {
                    Date = date,
                    DayNumber = day.ToString(),
                    IsCurrentMonth = true,
                    CalendarActivities = new List<CalendarActivity>()
                };

                if (groupedAppointments.TryGetValue(day, out var dailyAppointments))
                {
                    foreach (var appointment in dailyAppointments)
                    {

                        // 🔹 Pentru afișarea vizuală în celulă (scurt)
                        calendarDay.CalendarActivities.Add(new CalendarActivity
                        {
                            Title = appointment.Title,
                            Color = GetColorFromTag(appointment.ColorTag)
                        });

                        // 🔹 Pentru afișarea completă în lista de activități când dai click pe zi
                        calendarDay.Activities.Add(new Appointment
                        {
                            AppointmentId = appointment.AppointmentId,
                            Title = appointment.Title,
                            StartTime = appointment.StartTime,
                            EndTime = appointment.EndTime,
                            ClientName = appointment.ClientName,
                            Location = appointment.Location,
                            ColorTag = appointment.ColorTag,
                            Date = appointment.Date
                        });
                    }
                }


                calendarDays.Add(calendarDay);
            }

            // 🔹 Zile din luna următoare (până completăm 35 zile în total)
            int nextDay = 1;
            while (calendarDays.Count < 35)
            {
                DateTime nextMonth = today.AddMonths(1);
                calendarDays.Add(new CalendarDay
                {
                    Date = new DateTime(nextMonth.Year, nextMonth.Month, nextDay),
                    DayNumber = nextDay.ToString(),
                    IsCurrentMonth = false,
                    CalendarActivities = new List<CalendarActivity>()
                });

                nextDay++;
            }

            return calendarDays;
        }


        private ObservableCollection<Appointment> _selectedDayActivities = new();
        public ObservableCollection<Appointment> SelectedDayActivities
        {
            get => _selectedDayActivities;
            set
            {
                _selectedDayActivities = value;
                OnPropertyChanged();
            }
        }

        private CalendarDay _selectedCalendarDay;

        public event PropertyChangedEventHandler? PropertyChanged;

        public CalendarDay SelectedCalendarDay
        {
            get => _selectedCalendarDay;
            set
            {
                _selectedCalendarDay = value;
                OnPropertyChanged();
            }
        }


        public ObservableCollection<CalendarDay> Days { get; set; } = new();
        public ObservableCollection<Appointment> AllAppointments { get; set; } = new();
        public ObservableCollection<Appointment> SelectedDayAppointments { get; set; } = new();

        public string SelectedDayTitle => $"Activities for {SelectedDate.ToString("dd MMMM", CultureInfo.InvariantCulture)}";

        public async Task LoadCalendarAsync()
        {
            CalendarDays = await GenerateCalendarDaysAsync();
            OnPropertyChanged(nameof(CalendarDays));

            var today = DateTime.Today;
            var todayDay = CalendarDays.FirstOrDefault(d => d.Date.Date == today && d.IsCurrentMonth);

            if (todayDay != null)
            {
                SelectedCalendarDay = todayDay;
                SelectedDate = todayDay.Date;
                SelectedDayAppointments = new ObservableCollection<Appointment>(todayDay.Activities);
                OnPropertyChanged(nameof(SelectedCalendarDay));
                OnPropertyChanged(nameof(SelectedDate));
                OnPropertyChanged(nameof(SelectedDayAppointments));
            }
        }

        private bool _hasActivities;
        public bool HasActivities
        {
            get => _hasActivities;
            set
            {
                if (_hasActivities != value)
                {
                    _hasActivities = value;
                    OnPropertyChanged(nameof(HasActivities));
                    OnPropertyChanged(nameof(HasNoActivities)); 
                }
            }
        }

        public bool HasNoActivities => !HasActivities;




        private async void OnDayTapped(CalendarDay tappedDay)
        {
            if (tappedDay == null || !tappedDay.IsCurrentMonth)
                return;

            foreach (var day in CalendarDays)
                day.IsSelected = false;

            tappedDay.IsSelected = true;
            SelectedDate = tappedDay.Date;
            OnPropertyChanged(nameof(SelectedDayTitle));
            SelectedCalendarDay = tappedDay;

            SelectedDayAppointments.Clear();

            var appointments = await db.GetAppointmentsByDateAsync(SelectedDate, _employeeId);

            foreach (var appt in appointments)
            {
                appt.ClientName = await db.GetClientNameByIdAsync(appt.ClientId);
                appt.EditCommand = new Command(() => EditAppointment(appt));
                appt.DeleteCommand = new Command(async () => await DeleteAppointment(appt));
                SelectedDayAppointments.Add(appt);
            }

            HasActivities = SelectedDayAppointments.Any();
        }

        public bool IsEditing { get; set; } = false;
        public int EditingAppointmentId { get; set; }

        private Appointment _appointmentBeingEdited;
        public Appointment AppointmentBeingEdited
        {
            get => _appointmentBeingEdited;
            set
            {
                _appointmentBeingEdited = value;
                OnPropertyChanged(nameof(AppointmentBeingEdited));
            }
        }

        public ICommand EditCommand { get; set; }

        private async void EditAppointment(Appointment appointment)
        {
            // 1. Obține clienții
            var clientDict = await db.GetClientsForEmployeeAsync(_employeeId);

            // 2. Setează AssignedClients
            AssignedClients = new ObservableCollection<Client>(
                clientDict.Select(kvp => new Client
                {
                    ClientId = kvp.Key,
                    ClientName = kvp.Value
                })
            );

            // 3. Notifică UI-ul că AssignedClients s-a schimbat
            OnPropertyChanged(nameof(AssignedClients));

            // 4. Așteaptă binding-ul (important dacă Picker apare "gol")
            await Task.Delay(100);

            // 5. Setează clientul selectat
            SelectedClient = AssignedClients.FirstOrDefault(c => c.ClientId == appointment.ClientId);
            OnPropertyChanged(nameof(SelectedClient));

            // 6. Populează restul câmpurilor
            NewTitle = appointment.Title;
            SelectedDate = appointment.Date;
            StartTimeString = appointment.StartTime;
            EndTimeString = appointment.EndTime;
            Location = appointment.Location;
            SelectedColorTag = appointment.ColorTag;

            // ✅ Linia esențială pentru a face update corect
            AppointmentBeingEdited = appointment;

            // 7. Setează mod editare și UI
            IsEditMode = true;
            EditingAppointmentId = appointment.AppointmentId;

            FormTitle = "Edit Activity";
            SubmitButtonText = "Update";

            // 8. Notifică UI-ul pentru toate câmpurile
            OnPropertyChanged(nameof(NewTitle));
            OnPropertyChanged(nameof(SelectedDate));
            OnPropertyChanged(nameof(StartTimeString));
            OnPropertyChanged(nameof(EndTimeString));
            OnPropertyChanged(nameof(Location));
            OnPropertyChanged(nameof(SelectedColorTag));
            OnPropertyChanged(nameof(FormTitle));
            OnPropertyChanged(nameof(SubmitButtonText));
        }


        private async Task DeleteAppointment(Appointment appointment)
        {
            bool confirm = await Application.Current.MainPage.DisplayAlert(
                "Confirm Delete",
                $"Are you sure you want to delete this appointment?\n\n" +
                $"🕘 {appointment.StartTime} - {appointment.EndTime}\n" +
                $"👤 {appointment.ClientName}\n📍 {appointment.Location}\n" +
                $"📝 {appointment.Title}",
                "Yes", "Cancel");

            if (!confirm)
                return;

            try
            {
                await db.DeleteAppointmentAsync(appointment);

                AllAppointments.Remove(appointment);
                SelectedDayAppointments.Remove(appointment);

                if (SelectedCalendarDay != null)
                    SelectedCalendarDay.HasAppointment = SelectedDayAppointments.Count > 0;

                var updatedDays = await GenerateCalendarDaysAsync();
                CalendarDays = updatedDays;
                OnPropertyChanged(nameof(CalendarDays));

                if (SelectedCalendarDay != null)
                    OnDayTapped(SelectedCalendarDay);
            }
            catch (Exception ex)
            {
                await Application.Current.MainPage.DisplayAlert("Error", $"Could not delete: {ex.Message}", "OK");
            }
        }

        private async Task RefreshCalendarAndActivities()
        {
            var days = await GenerateCalendarDaysAsync();
            CalendarDays = days;
            OnPropertyChanged(nameof(CalendarDays));

            Console.WriteLine("Calendar refreshed. Days count: " + days.Count());

            if (SelectedCalendarDay != null)
                OnDayTapped(SelectedCalendarDay);
        }

        private string GetColorFromTag(string colorTag)
        {
            return colorTag switch
            {
                string s when s.Contains("Green") => "#3AB96E",
                string s when s.Contains("Blue") => "#2a72de",
                string s when s.Contains("Orange") => "#FFA500",
                string s when s.Contains("Red") => "#ff3b30",
                _ => "#808080"
            };
        }

        public async Task<string> ValidateAppointmentAsync(Appointment appt)
        {
            if (appt.Date < DateTime.Today)
                return "Date is in the past.";

            if (appt.Date.DayOfWeek == DayOfWeek.Saturday || appt.Date.DayOfWeek == DayOfWeek.Sunday)
                return "Appointments cannot be scheduled on weekends.";

            if (appt.Date == DateTime.Today)
            {
                var now = DateTime.Now.TimeOfDay;
                var start = DateTime.Parse(appt.StartTime).TimeOfDay;
                if (start < now)
                    return "Start time is in the past.";
            }

            var startHour = DateTime.Parse(appt.StartTime).Hour;
            var endHour = DateTime.Parse(appt.EndTime).Hour;

            if (startHour < 8 || endHour > 20)
                return "Appointment must be between 8:00 AM and 8:00 PM.";

            var startTimeParsed = DateTime.Parse(appt.StartTime);
            var endTimeParsed = DateTime.Parse(appt.EndTime);
            if (startTimeParsed >= endTimeParsed)
                return "Start time must be earlier than end time.";

            var db = new DatabaseService();
            if (await db.AppointmentConflictExistsAsync(appt))
                return "There is a conflict with another appointment.";

            return null; 
        }

        public string NewTitle { get; set; }
        public DateTime SelectedDate { get; set; } = DateTime.Today;
        public string StartTimeString { get; set; }
        public string EndTimeString { get; set; }
        public string Location { get; set; }
        public string SelectedClientName { get; set; }
        public string SelectedColorTag { get; set; }
        public int LoggedInEmployeeId { get; set; }


        public async Task AddOrUpdateAppointmentAsync()
        {
            if (SelectedClient == null)
            {
                await Application.Current.MainPage.DisplayAlert("Validation Error", "Please select a client.", "OK");
                return;
            }

            int clientId = SelectedClient.ClientId;

            if (AppointmentBeingEdited != null)
            {
                // 🔄 Update
                AppointmentBeingEdited.Title = NewTitle;
                AppointmentBeingEdited.Date = SelectedDate;
                AppointmentBeingEdited.StartTime = StartTimeString;
                AppointmentBeingEdited.EndTime = EndTimeString;
                AppointmentBeingEdited.Location = Location;
                AppointmentBeingEdited.ClientId = clientId;
                AppointmentBeingEdited.ColorTag = SelectedColorTag;

                var error = await ValidateAppointmentAsync(AppointmentBeingEdited);
                if (error != null)
                {
                    await Application.Current.MainPage.DisplayAlert("Validation Error", error, "OK");
                    return;
                }

                await db.UpdateAppointmentAsync(AppointmentBeingEdited);
                await Application.Current.MainPage.DisplayAlert("Updated", "Activity updated successfully!", "OK");
            }
            else
            {
                // ➕ Insert
                var appointment = new Appointment
                {
                    Title = NewTitle,
                    Date = SelectedDate,
                    StartTime = StartTimeString,
                    EndTime = EndTimeString,
                    Location = Location,
                    ClientId = clientId,
                    ColorTag = SelectedColorTag,
                    EmployeeId = _employeeId
                };

                var error = await ValidateAppointmentAsync(appointment);
                if (error != null)
                {
                    await Application.Current.MainPage.DisplayAlert("Validation Error", error, "OK");
                    return;
                }

                await db.InsertAppointmentAsync(appointment);
                await Application.Current.MainPage.DisplayAlert("Success", "Activity added!", "OK");
            }

            // 🔁 Refresh calendar
            var updatedDays = await GenerateCalendarDaysAsync(SelectedDate);
            CalendarDays = updatedDays;
            OnPropertyChanged(nameof(CalendarDays));
            if (SelectedCalendarDay != null)
                OnDayTapped(SelectedCalendarDay);

            ClearForm();
            AppointmentBeingEdited = null;
            SubmitButtonText = "Add";
            FormTitle = "Add New Activity";
        }


        private string _formTitle = "Add New Activity";
        public string FormTitle
        {
            get => _formTitle;
            set
            {
                _formTitle = value;
                OnPropertyChanged();
            }
        }

        private string _submitButtonText = "Add Activity";
        public string SubmitButtonText
        {
            get => _submitButtonText;
            set
            {
                _submitButtonText = value;
                OnPropertyChanged();
            }
        }

        private bool _isEditMode = false;
        public bool IsEditMode
        {
            get => _isEditMode;
            set
            {
                _isEditMode = value;
                OnPropertyChanged();
            }
        }


        public void ClearForm()
        {
            IsEditMode = false;
            FormTitle = "Add New Activity";
            SubmitButtonText = "Add Activity";

            NewTitle = string.Empty;
            SelectedDate = DateTime.Today;
            StartTimeString = string.Empty;
            EndTimeString = string.Empty;
            Location = string.Empty;
            SelectedClient = null; 
            SelectedColorTag = null;

            OnPropertyChanged(nameof(NewTitle));
            OnPropertyChanged(nameof(SelectedDate));
            OnPropertyChanged(nameof(StartTimeString));
            OnPropertyChanged(nameof(EndTimeString));
            OnPropertyChanged(nameof(Location));
            OnPropertyChanged(nameof(SelectedClient));
            OnPropertyChanged(nameof(SelectedColorTag));
        }

        protected void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }


    }
}
