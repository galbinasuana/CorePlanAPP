using CorePlan.Data;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;
using LiveChartsCore;
using LiveChartsCore.SkiaSharpView;

namespace CorePlan.ViewModels
{
    public class OpportunitiesViewModel : INotifyPropertyChanged
    {
        public event PropertyChangedEventHandler PropertyChanged;
        private readonly DatabaseService db;
        private readonly int _employeeId;
        private const int PageSize = 8; 
        private List<ClientDealDisplay> allFilteredDeals = new();
        private List<ClientDealDisplay> originalAllDeals = new();

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

        private int currentPage = 1;
        private int totalPages = 1;

        public int CurrentPage
        {
            get => currentPage;
            set
            {
                if (currentPage != value)
                {
                    currentPage = value;
                    OnPropertyChanged();
                    OnPropertyChanged(nameof(PageInfoText));
                    LoadOpportunitiesForCurrentPage(); 
                }
            }
        }

        public int TotalPages
        {
            get => totalPages;
            set
            {
                if (totalPages != value)
                {
                    totalPages = value;
                    OnPropertyChanged();
                    OnPropertyChanged(nameof(PageInfoText));
                }
            }
        }

        public string PageInfoText => $"Page {CurrentPage} of {TotalPages}";

        public List<string> ClientNameList { get; set; } = new();
        public Dictionary<int, string> ClientIdNameMap { get; set; } = new();

        private string selectedClient;
        public string SelectedClient
        {
            get => selectedClient;
            set
            {
                if (selectedClient != value)
                {
                    selectedClient = value;
                    OnPropertyChanged();
                    IsClientPlaceholderVisible = string.IsNullOrEmpty(selectedClient);
                }
            }
        }

        public Command ApplyFiltersCommand { get; }
        public Command ResetFiltersCommand { get; }

        private double minValue = 0;
        private double maxValue = 30000; // sau altă valoare maximă reală

        private double selectedMinValue = 0;
        private double selectedMaxValue = 30000;

        public double MinValue
        {
            get => minValue;
            set { minValue = value; OnPropertyChanged(); }
        }

        public double MaxValue
        {
            get => maxValue;
            set { maxValue = value; OnPropertyChanged(); }
        }

        public double SelectedMinValue
        {
            get => selectedMinValue;
            set { selectedMinValue = value; OnPropertyChanged(); }
        }

        public double SelectedMaxValue
        {
            get => selectedMaxValue;
            set { selectedMaxValue = value; OnPropertyChanged(); }
        }

        private List<string> _dealStages;
        public List<string> DealStages
        {
            get => _dealStages;
            set
            {
                _dealStages = value;
                OnPropertyChanged();
            }
        }

        private string _selectedDealStage;
        public string SelectedDealStage
        {
            get => _selectedDealStage;
            set
            {
                _selectedDealStage = value;
                OnPropertyChanged();
            }
        }


        private void ApplyFilters()
        {
            IEnumerable<ClientDealDisplay> filtered = originalAllDeals;

            if (!string.IsNullOrEmpty(SelectedClient))
                filtered = filtered.Where(d => d.ClientName == SelectedClient);

            if (!string.IsNullOrEmpty(SelectedDealStage))
                filtered = filtered.Where(d => d.DealStage == SelectedDealStage);

            filtered = filtered.Where(d =>
                d.ExpectedValue >= (decimal)SelectedMinValue &&
                d.ExpectedValue <= (decimal)SelectedMaxValue);

            allFilteredDeals = filtered.ToList();

            TotalPages = (int)Math.Ceiling(allFilteredDeals.Count / (double)PageSize);
            CurrentPage = 1;
            LoadOpportunitiesForCurrentPage();
        }

        public void ResetFilters()
        {
            SelectedClient = null;
            SelectedDealStage = null;  
            SelectedMinValue = MinValue;
            SelectedMaxValue = MaxValue;

            allFilteredDeals = originalAllDeals.ToList();

            TotalPages = (int)Math.Ceiling(allFilteredDeals.Count / (double)PageSize);
            CurrentPage = 1;
            LoadOpportunitiesForCurrentPage();

            IsClientPlaceholderVisible = true;
        }




        private bool isClientPlaceholderVisible = true;
        public bool IsClientPlaceholderVisible
        {
            get => isClientPlaceholderVisible;
            set
            {
                if (isClientPlaceholderVisible != value)
                {
                    isClientPlaceholderVisible = value;
                    OnPropertyChanged();
                }
            }
        }

        private async Task LoadClientsForFilterAsync()
        {
            var dict = await db.GetClientsForEmployeeAsync(_employeeId);
            ClientIdNameMap = dict;
            ClientNameList = dict.Values.ToList();

            OnPropertyChanged(nameof(ClientNameList));
        }



        public ObservableCollection<ClientDealDisplay> Deals { get; set; } = new();


        public OpportunitiesViewModel(int employeeId)
        {
            _employeeId = employeeId;
            db = new DatabaseService();
            ApplyFiltersCommand = new Command(ApplyFilters);
            ResetFiltersCommand = new Command(ResetFilters);


            Task.Run(async () =>
            {
                await LoadClientsForFilterAsync();  
                await LoadDealsAsync();             
            });

        }

        private async Task LoadDealsAsync()
        {
            var clients = await db.GetClientsByEmployeeIdAsync(_employeeId);
            var clientIds = clients.Select(c => c.ClientId).ToList();
            var allDeals = await db.GetClientDealsAsync();

            var filtered = allDeals
                .Where(d => clientIds.Contains(d.ClientId))
                .Select(d => new ClientDealDisplay
                {
                    ClientName = clients.FirstOrDefault(c => c.ClientId == d.ClientId)?.ClientName ?? "Unknown",
                    DealName = d.DealName,
                    DealStage = d.DealStage,
                    ExpectedValue = d.ExpectedValue,
                    CloseDateFormatted = d.CloseDate.ToString("MMMM dd")
                });

            originalAllDeals = filtered.ToList();
            allFilteredDeals = originalAllDeals.ToList();

            DealStages = originalAllDeals
            .Select(d => d.DealStage)
            .Where(stage => !string.IsNullOrWhiteSpace(stage))
            .Distinct()
            .OrderBy(stage => stage)
            .ToList();

            Debug.WriteLine($"Found {clients.Count} clients and {allFilteredDeals.Count} deals for employee {_employeeId}");

            TotalPages = (int)Math.Ceiling(allFilteredDeals.Count / (double)PageSize);
            CurrentPage = 1;

            LoadOpportunitiesForCurrentPage();
        }

        private void LoadOpportunitiesForCurrentPage()
        {
            Deals.Clear();

            var pageDeals = allFilteredDeals
                .Skip((CurrentPage - 1) * PageSize)
                .Take(PageSize);

            foreach (var deal in pageDeals)
                Deals.Add(deal);
        }


        public void NextPage()
        {
            if (CurrentPage < TotalPages)
                CurrentPage++;
        }

        public void PrevPage()
        {
            if (CurrentPage > 1)
                CurrentPage--;
        }

        protected void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    public class ClientDealDisplay
    {
        public string ClientName { get; set; }
        public string DealName { get; set; }
        public string DealStage { get; set; }
        public decimal ExpectedValue { get; set; }
        public string CloseDateFormatted { get; set; }
    }

}
