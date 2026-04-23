using CorePlan.Models;
using CorePlan.ViewModels;
using System.ComponentModel;


namespace CorePlan.Views;

public partial class CalendarPage : ContentPage
{
    private readonly CalendarViewModel viewModel;
    private readonly int _employeeId;

    public CalendarPage(int employeeId)
	{
        InitializeComponent();
        _employeeId = employeeId;
        viewModel = new CalendarViewModel(employeeId);
        BindingContext = viewModel;
        HiddenStartTimePicker.PropertyChanged += HiddenStartTimePicker_PropertyChanged;
        HiddenEndTimePicker.PropertyChanged += HiddenEndTimePicker_PropertyChanged;
        LoadData();
        NavigationPage.SetHasNavigationBar(this, false);
    }

    private async void LoadData()
    {
        await viewModel.LoadDataAsync();
    }

    private void HiddenStartTimePicker_PropertyChanged(object sender, PropertyChangedEventArgs e)
    {
        if (e.PropertyName == nameof(HiddenStartTimePicker.Time))
        {
            StartTimeEntry.Text = DateTime.Today.Add(HiddenStartTimePicker.Time).ToString("HH:mm");
        }
    }

    private void HiddenEndTimePicker_PropertyChanged(object sender, PropertyChangedEventArgs e)
    {
        if (e.PropertyName == nameof(HiddenEndTimePicker.Time))
        {
            EndTimeEntry.Text = DateTime.Today.Add(HiddenEndTimePicker.Time).ToString("HH:mm");
        }
    }

    private void StartTimeEntry_Focused(object sender, FocusEventArgs e)
    {
        HiddenStartTimePicker.Focus();
    }

    private void EndTimeEntry_Focused(object sender, FocusEventArgs e)
    {
        HiddenEndTimePicker.Focus();
    }

    private void DateEntry_Focused(object sender, FocusEventArgs e)
    {
        HiddenDatePicker.Focus(); 
    }

    private void OnDateSelected(object sender, DateChangedEventArgs e)
    {
        DateEntry.Text = e.NewDate.ToString("dd/MM/yyyy");
    }


    private async void OnDashboardTapped(object sender, EventArgs e)
    {
        await Navigation.PushAsync(new DashboardPage(_employeeId));
    }

    private async void OnOpportunitiesTapped(object sender, EventArgs e)
    {
        await Navigation.PushAsync(new OpportunitiesPage(_employeeId));
    }


    private void ClientPicker_SelectedIndexChanged(object sender, EventArgs e)
    {
        ClientPlaceholder.IsVisible = ClientPicker.SelectedIndex == -1;
    }

    private void ColorTagPicker_SelectedIndexChanged(object sender, EventArgs e)
    {
        ColorTagPlaceholder.IsVisible = ColorTagPicker.SelectedIndex == -1;
    }

    private async void OnAddActivityClicked(object sender, EventArgs e)
    {
        if (BindingContext is CalendarViewModel vm)
        {
            await vm.AddOrUpdateAppointmentAsync();
        }
    }

    private async void OnPreviousMonthClicked(object sender, EventArgs e)
    {
        if (BindingContext is CalendarViewModel vm)
            await vm.GoToPreviousMonth();
    }

    private async void OnNextMonthClicked(object sender, EventArgs e)
    {
        if (BindingContext is CalendarViewModel vm)
            await vm.GoToNextMonth();
    }

    protected override void OnDisappearing()
    {
        base.OnDisappearing();
    }

    private void OnLogoutClicked(object sender, EventArgs e)
    {
#if WINDOWS
    ChatbotService.Stop();
#endif
        Application.Current.MainPage = new NavigationPage(new MainPage());
    }

}