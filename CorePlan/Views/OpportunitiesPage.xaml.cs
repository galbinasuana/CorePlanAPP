using CorePlan.Models;
using CorePlan.ViewModels;


namespace CorePlan.Views;

public partial class OpportunitiesPage : ContentPage
{
    private OpportunitiesViewModel viewModel;
    private readonly int _employeeId;

    public OpportunitiesPage(int employeeId)
	{
        InitializeComponent();
        _employeeId = employeeId;
        NavigationPage.SetHasNavigationBar(this, false);
        viewModel = new OpportunitiesViewModel(employeeId);
        BindingContext = viewModel;
    }

    private void OnPrevPageClicked(object sender, EventArgs e)
    {
        viewModel.PrevPage();
    }

    private void OnNextPageClicked(object sender, EventArgs e)
    {
        viewModel.NextPage();
    }

    private async void OnDashboardTapped(object sender, EventArgs e)
    {
        await Navigation.PushAsync(new DashboardPage(_employeeId));
    }

    private async void OnCalendarTapped(object sender, EventArgs e)
    {
        await Navigation.PushAsync(new CalendarPage(_employeeId));
    }
    private void OnResetFiltersClicked(object sender, EventArgs e)
    {
        viewModel.ResetFilters();
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