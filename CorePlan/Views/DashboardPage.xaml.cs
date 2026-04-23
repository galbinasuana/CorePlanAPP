using CorePlan.Models;
using CorePlan.ViewModels;

namespace CorePlan.Views;

public partial class DashboardPage : ContentPage
{
    private readonly DashboardViewModel viewModel;
    private readonly int employeeId;

    public DashboardPage(int employeeId)
    {
        InitializeComponent();
        this.employeeId = employeeId;
        viewModel = new DashboardViewModel(employeeId);
        BindingContext = viewModel;
        Loaded += async (s, e) => await viewModel.InitializeAsync();
        NavigationPage.SetHasNavigationBar(this, false);
    }

    private async void OnCalendarTapped(object sender, EventArgs e)
    {
        await Navigation.PushAsync(new CalendarPage(employeeId));
    }

    private async void OnOpportunitiesTapped(object sender, EventArgs e)
    {
        await Navigation.PushAsync(new OpportunitiesPage(employeeId));
    }

    private void OnChatbotTapped(object sender, EventArgs e)
    {
#if WINDOWS
    ChatbotService.Start();
#endif
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