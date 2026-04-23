using CorePlan.Models;
using MySqlConnector;
using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CorePlan.Data
{
    public class Employee
    {
        public int EmployeeId { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public int UserId { get; set; }
        public int DepartmentId { get; set; }
    }

    public class DatabaseService
    {
        private readonly string _connectionString = "server=localhost;port=3306;user=root;password=*Parola*1234*;database=coreplan_db";

        public async Task<List<Employee>> GetAllEmployeesAsync()
        {
            var employees = new List<Employee>();

            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            using var command = new MySqlCommand("SELECT * FROM employees", connection);
            using var reader = await command.ExecuteReaderAsync();

            while (await reader.ReadAsync())
            {
                employees.Add(new Employee
                {
                    EmployeeId = Convert.ToInt32(reader["employee_id"]),
                    FirstName = reader["first_name"].ToString(),
                    LastName = reader["last_name"].ToString(),
                    UserId = Convert.ToInt32(reader["user_id"]),
                    DepartmentId = Convert.ToInt32(reader["department_id"])
                });
            }

            return employees;
        }

        public async Task<string?> ValidateUserAsync(string username, string password)
        {
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            var query = @"
                SELECT e.first_name, e.last_name
                FROM users u
                JOIN employees e ON u.user_id = e.user_id
                WHERE u.username = @username AND u.password = @password";

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@username", username);
            command.Parameters.AddWithValue("@password", password);

            using var reader = await command.ExecuteReaderAsync();

            if (await reader.ReadAsync())
            {
                string firstName = reader["first_name"].ToString();
                string lastName = reader["last_name"].ToString();
                return $"{firstName} {lastName}";
            }

            return null;
        }

        public int? GetEmployeeIdByCredentials(string username, string password)
        {
            using var connection = new MySqlConnection(_connectionString);
            connection.Open();

            string query = @"
                SELECT e.employee_id
                FROM users u
                INNER JOIN employees e ON u.user_id = e.user_id
                WHERE u.username = @username AND u.password = @password";

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@username", username);
            command.Parameters.AddWithValue("@password", password);

            var result = command.ExecuteScalar();
            return result != null ? Convert.ToInt32(result) : (int?)null;
        }

        public int? GetManagerIdByCredentials(string username, string password)
        {
            using var connection = new MySqlConnection(_connectionString);
            connection.Open();

            string query = @"
                SELECT m.manager_id
                FROM managers m
                JOIN users u ON m.user_id = u.user_id
                WHERE u.username = @username AND u.password = @password";

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@username", username);
            command.Parameters.AddWithValue("@password", password);

            var result = command.ExecuteScalar();
            return result != null ? Convert.ToInt32(result) : (int?)null;
        }


        public async Task<string> GetEmployeeNameByIdAsync(int employeeId)
        {
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            var query = @"SELECT first_name, last_name 
                  FROM employees 
                  WHERE employee_id = @employeeId";

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@employeeId", employeeId);

            using var reader = await command.ExecuteReaderAsync();

            if (await reader.ReadAsync())
            {
                string firstName = reader.GetString("first_name");
                string lastName = reader.GetString("last_name");
                return $"{firstName} {lastName}";
            }

            return null;
        }

        public async Task<string> GetDepartmentNameByEmployeeIdAsync(int employeeId)
        {
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            var query = @"SELECT d.department_name
                  FROM employees e
                  JOIN departments d ON e.department_id = d.department_id
                  WHERE e.employee_id = @employeeId";

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@employeeId", employeeId);

            using var reader = await command.ExecuteReaderAsync();

            if (await reader.ReadAsync())
            {
                return reader.GetString("department_name");
            }

            return null;
        }

        public async Task<int> CountAppointmentsAsync(int employeeId, string date)
        {
            using var conn = new MySqlConnection(_connectionString);
            await conn.OpenAsync();

            string query = @"SELECT COUNT(*) FROM appointments 
                     WHERE employee_id = @employeeId AND appointment_date = @date";

            using var cmd = new MySqlCommand(query, conn);
            cmd.Parameters.AddWithValue("@employeeId", employeeId);
            cmd.Parameters.AddWithValue("@date", date);

            return Convert.ToInt32(await cmd.ExecuteScalarAsync());
        }

        public async Task<int> CountFollowUpsAsync(int employeeId, string date)
        {
            using var conn = new MySqlConnection(_connectionString);
            await conn.OpenAsync();

            string query = @"SELECT COUNT(*) FROM followups 
                     WHERE employee_id = @employeeId AND followup_date = @date";

            using var cmd = new MySqlCommand(query, conn);
            cmd.Parameters.AddWithValue("@employeeId", employeeId);
            cmd.Parameters.AddWithValue("@date", date);

            return Convert.ToInt32(await cmd.ExecuteScalarAsync());
        }

        public async Task<int> CountTasksDueTodayAsync(int employeeId, string date)
        {
            using var conn = new MySqlConnection(_connectionString);
            await conn.OpenAsync();

            string query = @"SELECT COUNT(*) FROM tasks 
                     WHERE employee_id = @employeeId AND due_date = @date";

            using var cmd = new MySqlCommand(query, conn);
            cmd.Parameters.AddWithValue("@employeeId", employeeId);
            cmd.Parameters.AddWithValue("@date", date);

            return Convert.ToInt32(await cmd.ExecuteScalarAsync());
        }

        public async Task<int> CountDeadlinesDueTodayAsync(int employeeId, string date)
        {
            using var conn = new MySqlConnection(_connectionString);
            await conn.OpenAsync();

            string query = @"SELECT COUNT(*) FROM deadlines 
                     WHERE employee_id = @employeeId AND due_date = @date";

            using var cmd = new MySqlCommand(query, conn);
            cmd.Parameters.AddWithValue("@employeeId", employeeId);
            cmd.Parameters.AddWithValue("@date", date);

            return Convert.ToInt32(await cmd.ExecuteScalarAsync());
        }

        public async Task<List<SalesDeal>> GetUpcomingSalesDeadlinesThisWeekAsync(int employeeId)
        {
            var deals = new List<SalesDeal>();

            try
            {
                using var conn = new MySqlConnection(_connectionString);
                await conn.OpenAsync();

                var startOfWeek = DateTime.Today.AddDays(-(int)DateTime.Today.DayOfWeek + (int)DayOfWeek.Monday);
                var endOfWeek = startOfWeek.AddDays(6);

                string query = @"
                        SELECT deal_id, title, deadline 
                        FROM sales_deals
                        WHERE employee_id = @employeeId
                          AND deadline BETWEEN @startOfWeek AND @endOfWeek
                        ORDER BY deadline ASC;
                    ";

                using var cmd = new MySqlCommand(query, conn);
                cmd.Parameters.AddWithValue("@employeeId", employeeId);
                cmd.Parameters.AddWithValue("@startOfWeek", startOfWeek.ToString("yyyy-MM-dd"));
                cmd.Parameters.AddWithValue("@endOfWeek", endOfWeek.ToString("yyyy-MM-dd"));

                using var reader = await cmd.ExecuteReaderAsync();
                while (await reader.ReadAsync())
                {
                    var deal = new SalesDeal
                    {
                        DealId = reader.GetInt32("deal_id"),
                        Title = reader.GetString("title"),
                        DueDate = reader.GetDateTime("deadline")
                    };

                    deals.Add(deal);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"[ERROR] Failed to fetch upcoming sales deadlines: {ex.Message}");
            }

            return deals;
        }

        public async Task<(decimal Target, decimal Actual)> GetMonthlyTargetProgressAsync(int employeeId)
        {
            try
            {
                using var conn = new MySqlConnection(_connectionString);
                await conn.OpenAsync();

                string monthYear = DateTime.Now.ToString("yyyy-MM");
                string query = @"
                    SELECT sales_target, actual_sales
                    FROM monthly_targets
                    WHERE employee_id = @employeeId AND month_year = @monthYear
                    ORDER BY updated_at DESC
                    LIMIT 1;";

                using var cmd = new MySqlCommand(query, conn);
                cmd.Parameters.AddWithValue("@employeeId", employeeId);
                cmd.Parameters.AddWithValue("@monthYear", monthYear);

                using var reader = await cmd.ExecuteReaderAsync();
                if (await reader.ReadAsync())
                {
                    decimal target = reader.GetDecimal("sales_target");
                    decimal actual = reader.GetDecimal("actual_sales");
                    return (target, actual);
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"[ERROR] MonthlyTargetProgress: {ex.Message}");
            }

            return (0, 0);
        }

        public async Task<Dictionary<int, int>> GenerateSmartAlertsRawAsync(int employeeId)
        {
            var results = new Dictionary<int, int>();
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            // 1. Overdue Deadlines
            var cmd1 = new MySqlCommand(@"
              SELECT COUNT(*) 
              FROM deadlines 
              WHERE employee_id = @employeeId 
              AND due_date < CURDATE() 
              AND status != 'Completed'", connection);
            cmd1.Parameters.AddWithValue("@employeeId", employeeId);
            int overdue = Convert.ToInt32(await cmd1.ExecuteScalarAsync());
            if (overdue > 0) results[101] = overdue;
            //var overdueCount = Convert.ToInt32(await cmd1.ExecuteScalarAsync());
            //if (overdueCount > 0)
            //    results.Add((101, $"📌 You have {overdueCount} overdue deadline{(overdueCount > 1 ? "s" : "")}!"));

            // 2. Upcoming Follow-ups Without Reminders
            var cmd2 = new MySqlCommand(@"
              SELECT COUNT(*) 
              FROM followups 
              WHERE employee_id = @employeeId 
              AND DATEDIFF(followup_date, CURDATE()) = 1 
              AND reminder_days_before = 0", connection);
            cmd2.Parameters.AddWithValue("@employeeId", employeeId);
            int followups = Convert.ToInt32(await cmd2.ExecuteScalarAsync());
            if (followups > 0) results[102] = followups;
            //var missingReminders = Convert.ToInt32(await cmd2.ExecuteScalarAsync());
            //if (missingReminders > 0)
            //    results.Add((102, $"🔔 You have {missingReminders} follow-up{(missingReminders > 1 ? "s" : "")} tomorrow with no reminder set."));

            // 4. Deals past close date and still open
            var cmd4 = new MySqlCommand(@"
              SELECT COUNT(*) 
              FROM client_deals cd
              JOIN followups f ON cd.client_id = f.client_id
              WHERE f.employee_id = @employeeId
              AND cd.close_date < CURDATE()
              AND cd.deal_stage IN ('Prospecting', 'Negotiation')", connection);
            cmd4.Parameters.AddWithValue("@employeeId", employeeId);
            int deals = Convert.ToInt32(await cmd4.ExecuteScalarAsync());
            if (deals > 0) results[104] = deals;
            //var expiredDeals = Convert.ToInt32(await cmd4.ExecuteScalarAsync());
            //if (expiredDeals > 0)
            //    results.Add((104, $"💼 You have {expiredDeals} deal{(expiredDeals > 1 ? "s" : "")} past expected close date still open."));

            // 5. Monthly Target Progress using `sales_targets`
            var cmdTarget = new MySqlCommand(@"
              SELECT target_amount
              FROM sales_targets
              WHERE employee_id = @employeeId
              AND MONTH(target_month) = MONTH(CURDATE())
              AND YEAR(target_month) = YEAR(CURDATE())", connection);
            cmdTarget.Parameters.AddWithValue("@employeeId", employeeId);
            var targetObj = await cmdTarget.ExecuteScalarAsync();

            if (targetObj != null && decimal.TryParse(targetObj.ToString(), out decimal target) && target > 0)
            {
                var cmdSales = new MySqlCommand(@"
                  SELECT COALESCE(SUM(expected_value), 0)
                  FROM client_deals cd
                  JOIN followups f ON cd.client_id = f.client_id
                  WHERE f.employee_id = @employeeId
                  AND cd.deal_stage = 'Closed Won'
                  AND MONTH(cd.close_date) = MONTH(CURDATE())
                  AND YEAR(cd.close_date) = YEAR(CURDATE())", connection);
                cmdSales.Parameters.AddWithValue("@employeeId", employeeId);
                var sales = Convert.ToDecimal(await cmdSales.ExecuteScalarAsync());

                var percent = (sales / target) * 100;
                if (percent < 60)
                    results[105] = (int)Math.Round(percent);
            }

            return results;

            //if (targetObj != null && decimal.TryParse(targetObj.ToString(), out decimal monthlyTarget) && monthlyTarget > 0)
            //{
            //    var cmdSales = new MySqlCommand(@"
            //      SELECT COALESCE(SUM(expected_value), 0)
            //      FROM client_deals cd
            //      JOIN followups f ON cd.client_id = f.client_id
            //      WHERE f.employee_id = @employeeId
            //      AND cd.deal_stage = 'Closed Won'
            //      AND MONTH(cd.close_date) = MONTH(CURDATE())
            //      AND YEAR(cd.close_date) = YEAR(CURDATE())", connection);
            //    cmdSales.Parameters.AddWithValue("@employeeId", employeeId);
            //    var closedSales = Convert.ToDecimal(await cmdSales.ExecuteScalarAsync());

            //    var percentage = (closedSales / monthlyTarget) * 100;
            //    if (percentage < 60)
            //    {
            //        results.Add((105, $"⚠️ Behind schedule — only {Math.Round(percentage)}% of monthly target reached."));
            //    }
            //}

            //return results;
        }


        public async Task<List<(int id, string message)>> GenerateSmartAlertsAsync(int employeeId)
        {
            var rawAlerts = await GenerateSmartAlertsRawAsync(employeeId);
            var formattedAlerts = new List<(int, string)>();

            foreach (var kvp in rawAlerts.OrderBy(k => k.Key))
            {
                int id = kvp.Key;
                int value = kvp.Value;

                switch (id)
                {
                    case 101:
                        formattedAlerts.Add((id, $"📌 You have {value} overdue deadline{(value > 1 ? "s" : "")}!"));
                        break;
                    case 102:
                        formattedAlerts.Add((id, $"🔔 You have {value} follow-up{(value > 1 ? "s" : "")} tomorrow with no reminder set."));
                        break;
                    case 104:
                        formattedAlerts.Add((id, $"💼 You have {value} deal{(value > 1 ? "s" : "")} past expected close date still open."));
                        break;
                    case 105:
                        formattedAlerts.Add((id, $"⚠️ Behind schedule — only {value}% of monthly target reached."));
                        break;
                }
            }

            return formattedAlerts;
        }

        public async Task<List<Client>> GetClientsByEmployeeIdAsync(int employeeId)
        {
            var clients = new List<Client>();
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            string query = "SELECT client_id, name FROM clients WHERE assigned_to = @employeeId";

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@employeeId", employeeId);

            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                clients.Add(new Client
                {
                    ClientId = reader.GetInt32("client_id"),
                    ClientName = reader.GetString("name")
                });
            }

            return clients;
        }

        public async Task<List<Appointment>> GetAppointmentsForMonth(int year, int month, int employeeId)
        {
            var appointments = new List<Appointment>();

            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            string query = @"
                SELECT a.title, a.color_tag, a.appointment_date,
                       a.start_time, a.end_time, a.location,
                       c.name
                FROM appointments a
                LEFT JOIN clients c ON a.client_id = c.client_id
                WHERE a.employee_id = @employeeId
                AND YEAR(a.appointment_date) = @year
                AND MONTH(a.appointment_date) = @month
            ";

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@employeeId", employeeId);
            command.Parameters.AddWithValue("@year", year);
            command.Parameters.AddWithValue("@month", month);

            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                appointments.Add(new Appointment
                {
                    Title = reader["title"].ToString(),
                    ColorTag = reader["color_tag"].ToString(),
                    Date = Convert.ToDateTime(reader["appointment_date"]),
                    StartTime = reader["start_time"]?.ToString(),
                    EndTime = reader["end_time"]?.ToString(),
                    Location = reader["location"]?.ToString(),
                    ClientName = reader["name"]?.ToString()
                });
            }

            return appointments;
        }



        public async Task<bool> AppointmentConflictExistsAsync(Appointment appointment)
        {
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            string query = @"
                SELECT COUNT(*) FROM appointments
                WHERE employee_id = @employeeId
                AND appointment_date = @date
                AND (
                    (start_time < @endTime AND end_time > @startTime)
                )";

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@employeeId", appointment.EmployeeId);
            command.Parameters.AddWithValue("@date", appointment.Date.ToString("yyyy-MM-dd"));
            command.Parameters.AddWithValue("@startTime", appointment.StartTime);
            command.Parameters.AddWithValue("@endTime", appointment.EndTime);

            var result = await command.ExecuteScalarAsync();
            return Convert.ToInt32(result) > 0;
        }

        public async Task InsertAppointmentAsync(Appointment appointment)
        {
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            string query = @"
                INSERT INTO appointments (title, appointment_date, start_time, end_time, location, client_id, color_tag, employee_id)
                VALUES (@title, @date, @start, @end, @location, @clientId, @colorTag, @employeeId)";

            using var cmd = new MySqlCommand(query, connection);
            cmd.Parameters.AddWithValue("@title", appointment.Title);
            cmd.Parameters.AddWithValue("@date", appointment.Date.ToString("yyyy-MM-dd"));
            cmd.Parameters.AddWithValue("@start", appointment.StartTime);
            cmd.Parameters.AddWithValue("@end", appointment.EndTime);
            cmd.Parameters.AddWithValue("@location", appointment.Location);
            cmd.Parameters.AddWithValue("@clientId", appointment.ClientId);
            cmd.Parameters.AddWithValue("@colorTag", appointment.ColorTag);
            cmd.Parameters.AddWithValue("@employeeId", appointment.EmployeeId);

            await cmd.ExecuteNonQueryAsync();
        }

        public async Task<int> GetClientIdByNameAsync(string clientName)
        {
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            string query = "SELECT client_id FROM clients WHERE name = @name LIMIT 1";
            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@name", clientName);

            var result = await command.ExecuteScalarAsync();
            return result != null ? Convert.ToInt32(result) : 0;
        }

        public async Task<string> GetClientNameByIdAsync(int clientId)
        {
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            string query = "SELECT name FROM clients WHERE client_id = @clientId LIMIT 1";
            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@clientId", clientId);

            var result = await command.ExecuteScalarAsync();
            return result != null ? result.ToString() : "Unknown";
        }

        public async Task<Dictionary<int, string>> GetAllClientsAsDictionaryAsync()
        {
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            string query = "SELECT client_id, name FROM clients";
            using var command = new MySqlCommand(query, connection);
            using var reader = await command.ExecuteReaderAsync();

            var dict = new Dictionary<int, string>();
            while (await reader.ReadAsync())
            {
                dict.Add(reader.GetInt32(0), reader.GetString(1));
            }

            return dict;
        }

        public async Task<Dictionary<int, string>> GetClientsForEmployeeAsync(int employeeId)
        {
            var result = new Dictionary<int, string>();

            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            string query = "SELECT client_id, name FROM clients WHERE assigned_to = @employeeId";
            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@employeeId", employeeId);

            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                int id = reader.GetInt32(0);
                string name = reader.GetString(1);
                result[id] = name;
            }

            return result;
        }


        public async Task<List<Appointment>> GetAppointmentsByDateAsync(DateTime selectedDate, int employeeId)
        {
            var appointments = new List<Appointment>();
            string query = "SELECT * FROM appointments WHERE appointment_date = @date AND employee_id = @employeeId";

            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@date", selectedDate.ToString("yyyy-MM-dd"));
            command.Parameters.AddWithValue("@employeeId", employeeId);

            using var reader = await command.ExecuteReaderAsync();
            while (await reader.ReadAsync())
            {
                appointments.Add(new Appointment
                {
                    AppointmentId = reader.GetInt32("appointment_id"),
                    Title = reader.GetString("title"),
                    Date = reader.GetDateTime("appointment_date"),
                    StartTime = DateTime.Today.Add(reader.GetTimeSpan("start_time")).ToString("HH:mm"),
                    EndTime = DateTime.Today.Add(reader.GetTimeSpan("end_time")).ToString("HH:mm"),
                    Location = reader.GetString("location"),
                    ClientId = reader.GetInt32("client_id"),
                    ColorTag = reader.GetString("color_tag"),
                    EmployeeId = reader.GetInt32("employee_id")
                });
            }

            return appointments;
        }


        public async Task UpdateAppointmentAsync(Appointment appointment)
        {
            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            string query = @"
            UPDATE appointments
            SET title = @title,
                appointment_date = @date,
                start_time = @start,
                end_time = @end,
                location = @location,
                client_id = @clientId,
                color_tag = @colorTag,
                employee_id = @employeeId
            WHERE appointment_id = @id";

            using var cmd = new MySqlCommand(query, connection);
            cmd.Parameters.AddWithValue("@title", appointment.Title);
            cmd.Parameters.AddWithValue("@date", appointment.Date.ToString("yyyy-MM-dd"));
            cmd.Parameters.AddWithValue("@start", appointment.StartTime);
            cmd.Parameters.AddWithValue("@end", appointment.EndTime);
            cmd.Parameters.AddWithValue("@location", appointment.Location);
            cmd.Parameters.AddWithValue("@clientId", appointment.ClientId);
            cmd.Parameters.AddWithValue("@colorTag", appointment.ColorTag);
            cmd.Parameters.AddWithValue("@employeeId", appointment.EmployeeId);
            cmd.Parameters.AddWithValue("@id", appointment.AppointmentId);

            await cmd.ExecuteNonQueryAsync();
        }


        public async Task DeleteAppointmentAsync(Appointment appointment)
        {
            string query = "DELETE FROM appointments WHERE appointment_id = @id";

            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            using var command = new MySqlCommand(query, connection);
            command.Parameters.AddWithValue("@id", appointment.AppointmentId);

            await command.ExecuteNonQueryAsync();
        }

        public async Task<List<ClientDeal>> GetClientDealsAsync()
        {
            var deals = new List<ClientDeal>();

            using var connection = new MySqlConnection(_connectionString);
            await connection.OpenAsync();

            var query = "SELECT client_id, deal_name, deal_stage, expected_value, close_date FROM client_deals";

            using var command = new MySqlCommand(query, connection);
            using var reader = await command.ExecuteReaderAsync();

            while (await reader.ReadAsync())
            {
                deals.Add(new ClientDeal
                {
                    ClientId = reader.GetInt32("client_id"),
                    DealName = reader.GetString("deal_name"),
                    DealStage = reader.GetString("deal_stage"),
                    ExpectedValue = reader.GetDecimal("expected_value"),
                    CloseDate = reader.GetDateTime("close_date")
                });
            }

            return deals;
        }

        //public int? GetUserIdByUsername(string username)
        //{
        //    using var connection = new MySqlConnection(_connectionString);
        //    connection.Open();

        //    using var command = new MySqlCommand("SELECT user_id FROM users WHERE username = @username", connection);
        //    command.Parameters.AddWithValue("@username", username);

        //    var result = command.ExecuteScalar();
        //    return result != null ? Convert.ToInt32(result) : (int?)null;
        //}

        //public int? GetEmployeeIdByUserId(int userId)
        //{
        //    using var connection = new MySqlConnection(_connectionString); 
        //    connection.Open();

        //    using var command = connection.CreateCommand();
        //    command.CommandText = @"
        //        SELECT employee_id
        //        FROM employees
        //        WHERE user_id = @user_id
        //        LIMIT 1;
        //    ";
        //    command.Parameters.AddWithValue("@user_id", userId); 

        //    var result = command.ExecuteScalar();
        //    return result != null ? Convert.ToInt32(result) : (int?)null;
        //}

        //public string? GetDepartmentNameByUserId(int userId)
        //{
        //    using var connection = new MySqlConnection(_connectionString);
        //    connection.Open();

        //    using var command = connection.CreateCommand();
        //    command.CommandText = @"
        //        SELECT d.department_name
        //        FROM departments d
        //        JOIN employees e ON e.department_id = d.department_id
        //        WHERE e.user_id = @userId
        //        LIMIT 1;
        //    ";
        //    command.Parameters.AddWithValue("@userId", userId);

        //    var result = command.ExecuteScalar();
        //    return result != null ? result.ToString() : null;
        //}

    }
}
