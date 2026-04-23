namespace CorePlan.Views;

public partial class ManagerDashboardPage : ContentPage
{
    private int managerId;

    public ManagerDashboardPage(int managerId)
	{
		InitializeComponent();
        this.managerId = managerId;
        NavigationPage.SetHasNavigationBar(this, false);
    }

    private async void OnAiButtonClicked(object sender, EventArgs e)
    {
        await Navigation.PushAsync(new AIPanel());
    }


    private void OnCloseAiOverlayClicked(object sender, EventArgs e)
    {
        AiOverlay.IsVisible = false;
    }

    private void OnLogoutClicked(object sender, EventArgs e)
    {
        Application.Current.MainPage = new NavigationPage(new MainPage());
    }
}