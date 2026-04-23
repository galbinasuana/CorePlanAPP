using System;
using CorePlan.Views;
using Microsoft.Maui.Controls;

namespace CorePlan
{
    public partial class MainPage : ContentPage
    {
        private string selectedRole = "Employee";

        public MainPage()
        {
            InitializeComponent();
            HighlightSelectedRole();
            NavigationPage.SetHasNavigationBar(this, false);
        }

        private void OnEmployeeClicked(object sender, EventArgs e)
        {
            selectedRole = "Employee";
            HighlightSelectedRole();
        }

        private void OnManagerClicked(object sender, EventArgs e)
        {
            selectedRole = "Manager";
            HighlightSelectedRole();
        }

        private void HighlightSelectedRole()
        {
            if (selectedRole == "Employee")
            {
                EmployeeButton.BackgroundColor = Color.FromArgb("#1A2A47");
                EmployeeButton.TextColor = Colors.White;

                ManagerButton.BackgroundColor = Colors.Transparent;
                ManagerButton.TextColor = Color.FromArgb("#1A2A47");
            }
            else
            {
                ManagerButton.BackgroundColor = Color.FromArgb("#1A2A47");
                ManagerButton.TextColor = Colors.White;

                EmployeeButton.BackgroundColor = Colors.Transparent;
                EmployeeButton.TextColor = Color.FromArgb("#1A2A47");
            }
        }

        private bool isPasswordVisible = false;

        private void OnTogglePasswordVisibilityClicked(object sender, EventArgs e)
        {
            isPasswordVisible = !isPasswordVisible;
            PasswordEntry.IsPassword = !isPasswordVisible;

            TogglePasswordVisibilityButton.Source = isPasswordVisible ? "show.png" : "hide.png";
        }


        private async void OnSignInClicked(object sender, EventArgs e)
        {
            string username = UsernameEntry.Text?.Trim();
            string password = PasswordEntry.Text;

            if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(password))
            {
                await DisplayAlert("Error", "Please enter both username and password.", "OK");
                return;
            }

            var db = new CorePlan.Data.DatabaseService();

            if (selectedRole == "Employee")
            {
                int? employeeId = db.GetEmployeeIdByCredentials(username, password);
                if (employeeId.HasValue)
                {
                    Application.Current.MainPage = new NavigationPage(new DashboardPage(employeeId.Value));
                }
                else
                {
                    await DisplayAlert("Login Failed", "Invalid employee credentials.", "OK");
                }
            }
            else if (selectedRole == "Manager")
            {
                int? managerId = db.GetManagerIdByCredentials(username, password);
                if (managerId.HasValue)
                {
                    Application.Current.MainPage = new NavigationPage(new ManagerDashboardPage(managerId.Value));
                }
                else
                {
                    await DisplayAlert("Login Failed", "Invalid manager credentials.", "OK");
                }
            }
        }


    }
}
