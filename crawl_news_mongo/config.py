def categoryProcess(category):
    if (category == "តារា&កម្សាន្ដ") or (category == "តារា") or (category == "កម្សាន្ត") or (
            category == "សិល្បៈកម្សាន្ត"):
        return "Star & Entertainment"
    elif category == "សង្គម":
        return "Social"
    elif category == "ប្លែកៗ":
        return "Odd"
    elif (category == "សម្រស់&សុខភាព") or (category == "សុខភាព") or (category == "សម្រស់") or (
            category == "សម្រស់ និងសុខភាព"):
        return "Beautiful & Health"
    elif category == "យល់ដឹង":
        return "Knowledge"
    elif category == "បច្ចេកវិទ្យា":
        return "Technology"
    elif category == "ប្រលោមលោក&អប់រំ":
        return "Novel & Education"
    elif category == "ព័ត៌មានជាតិ":
        return "National News"
    elif (category == "អន្តរជាតិ") or (category == "ព័ត៌មានអន្តរជាតិ"):
        return "International"
    elif category == "នយោបាយ":
        return "Politics"
    elif (category == "សេដ្ឋកិច្ច & អចលនទ្រព្យ") or (category == "សេដ្ឋកិច្ច") or (category == "អចលនទ្រព្យ"):
        return "Economics & Real Estate"
    elif category == "ជីវប្រវត្តិឥស្សរជន":
        return "Elite biographies"
    elif category == "សន្តិសុខ និង សង្គម":
        return "Security and society"
    elif category == "បរិយាយ":
        return "Describe"
    elif category == "តារាខ្មែរ":
        return "Khmer Artist"
    elif (category == "កីឡាអន្ដរជាតិ") or (category == "កីឡាជាតិ") or (category == "កីទ្បា") or (category == "កីឡា"):
        return "Sport"
    elif category == "ជីវិត & ការងារ":
        return "Life & Work"
    elif category == "ស្នេហាស្នេហ៍ហឺត":
        return "Love"
    elif category == "ទេសចរណ៍":
        return "Tours"
    elif category == "ចរាចរណ៍ថ្ងៃនេះ":
        return "Traffic Today"
    elif category == "បាក់ឌុប២០១៩":
        return "Creative Arts and Design 2019"
    elif category == "ឃ្លាំងគំនិត":
        return "Mindset repository"
    elif category == "បែបផែនជីវិត":
        return "Lifestyle"
    elif category == "ព័ត៍មានទូទៅ":
        return "General Information"
    elif category == "POP FEED":
        return category


def convert_month_to_int(month):
    if (month == "Jan") or (month == "January"):
        int_month = 1
    elif (month == "Feb") or (month == "February"):
        int_month = 2
    elif (month == "Mar") or (month == "March"):
        int_month = 3
    elif (month == "Apr") or (month == "April"):
        int_month = 4
    elif month == "May":
        int_month = 5
    elif (month == "Jun") or (month == "June"):
        int_month = 6
    elif (month == "Jul") or (month == "July"):
        int_month = 7
    elif (month == "Aug") or (month == "August"):
        int_month = 8
    elif (month == "Sep") or (month == "September"):
        int_month = 9
    elif (month == "Oct") or (month == "October"):
        int_month = 10
    elif (month == "Nov") or (month == "November"):
        int_month = 11
    elif (month == "Dec") or (month == "December"):
        int_month = 12
    return int_month


# chuyen thanh False neu ra database chinh thuc
def DebugMode():
    return False