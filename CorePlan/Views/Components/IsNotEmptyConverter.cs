using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CorePlan.Views.Components
{
    public class IsNotEmptyConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            bool isNotEmpty = false;

            if (value is int count)
                isNotEmpty = count > 0;
            else if (value is string str)
                isNotEmpty = !string.IsNullOrWhiteSpace(str);

            bool invert = (parameter?.ToString() == "invert");
            return invert ? !isNotEmpty : isNotEmpty;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => throw new NotImplementedException();
    }

}
