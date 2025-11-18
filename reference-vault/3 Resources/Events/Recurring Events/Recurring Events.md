
```dataviewjs
// Get today's date
const today = DateTime.now();

// Function to convert 24h time to 12h time with AM/PM
function formatTime12h(time24h) {
    if (!time24h || time24h === "N/A") return "N/A";
    
    // Parse the hour and minute
    const [hours, minutes] = time24h.split(':').map(num => parseInt(num, 10));
    
    if (isNaN(hours) || isNaN(minutes)) return time24h;
    
    // Convert to 12-hour format
    const period = hours >= 12 ? "PM" : "AM";
    const hours12 = hours % 12 || 12; // Convert 0 to 12 for 12 AM
    
    // Format as "1:30 PM" etc.
    return `${hours12}:${minutes.toString().padStart(2, '0')} ${period}`;
}

// Helper function for ordinal suffixes
function getOrdinalSuffix(day) {
    if (typeof day === 'string') day = parseInt(day);
    if (isNaN(day)) return '';
    
    if (day % 10 === 1 && day % 100 !== 11) return 'st';
    if (day % 10 === 2 && day % 100 !== 12) return 'nd';
    if (day % 10 === 3 && day % 100 !== 13) return 'rd';
    return 'th';
}

// ========== WEEKLY EVENTS ==========
dv.header(2, "Weekly Recurring Events");

// Get all files in the Weekly folder
const weeklyEvents = dv.pages()
    .where(p => p.weeklyRecurDay);

// Map of day numbers to names for sorting and display
const dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const dayMap = {};
dayNames.forEach((name, index) => {
    dayMap[name.toLowerCase()] = index;
});

// Sort events by day of week and start time
const sortedWeekly = weeklyEvents.sort(p => [
    // Sort by day number
    p.weeklyRecurDay ? (typeof p.weeklyRecurDay === 'number' ? p.weeklyRecurDay : dayMap[p.weeklyRecurDay.toLowerCase()]) : 7,
    // Then by start time
    p.startTime || "23:59"
]);

// Render the table
dv.table(["Event", "Day", "Start Time", "End Time"],
    sortedWeekly.map(p => [
        p.file.link,
        p.weeklyRecurDay,
        formatTime12h(p.startTime),
        formatTime12h(p.endTime)
    ])
);

// ========== MONTHLY EVENTS ==========
dv.header(2, "Monthly Recurring Events");

// Get all files in the Monthly folder
const monthlyEvents = dv.pages()
    .where(p => p.monthlyRecurDay);

// Sort events by day of month and start time
const sortedMonthly = monthlyEvents.sort(p => [
    // Sort by day of month
    parseInt(p.monthlyRecurDay) || 32,
    // Then by start time
    p.startTime || "23:59"
]);

// Render the table
dv.table(["Event", "Day of Month", "Start Time", "End Time"],
    sortedMonthly.map(p => [
        p.file.link,
        p.monthlyRecurDay ? (p.monthlyRecurDay + getOrdinalSuffix(p.monthlyRecurDay)) : "N/A",
        formatTime12h(p.startTime),
        formatTime12h(p.endTime)
    ])
);

// ========== YEARLY EVENTS ==========
dv.header(2, "Yearly Recurring Events");

// Get all files in the Yearly folder
const yearlyEvents = dv.pages('"3 Resources/Events/Recurring Events/Yearly"')
    .where(p => p.recurMonth && p.recurDay);

// Month names for sorting and display
const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const monthMap = {};
monthNames.forEach((name, index) => {
    monthMap[name.toLowerCase()] = index;
});

// Sort events by month, day and start time
const sortedYearly = yearlyEvents.sort(p => [
    // Sort by month number
    p.recurMonth ? (typeof p.recurMonth === 'number' ? p.recurMonth - 1 : monthMap[p.recurMonth.toLowerCase()]) : 12,
    // Then by day
    parseInt(p.recurDay) || 32,
    // Then by start time
    p.startTime || "23:59"
]);

// Render the table
dv.table(["Event", "Date", "Start Time", "End Time"],
    sortedYearly.map(p => {
        // Format the date as "Month Day"
        let monthDisplay = p.recurMonth;
        if (typeof p.recurMonth === 'number') {
            monthDisplay = monthNames[p.recurMonth - 1];
        }
        
        let dateDisplay = monthDisplay + " " + p.recurDay;
        if (p.recurDay) {
            dateDisplay += getOrdinalSuffix(p.recurDay);
        }
        
        return [
            p.file.link,
            dateDisplay,
            formatTime12h(p.startTime),
            formatTime12h(p.endTime)
        ];
    })
);
```

---

```dataviewjs

// Configuration - Set the number of days to look ahead
const daysAhead = 200; 

// Get today's date and cutoff date
const today = dv.date("today");
const cutoffDate = dv.date(today.plus({"day": daysAhead}));

// Header for the report
dv.header(2, `Upcoming Birthdays (Next ${daysAhead} Days)`);

// Debug information
dv.paragraph(`Looking for birthdays between ${today.toFormat("yyyy-MM-dd")} and ${cutoffDate.toFormat("yyyy-MM-dd")}`);

// Add DEBUG mode to show extra information
const DEBUG = false;

// Find all documents using the Person template
let people = dv.pages()
    .where(p => p.template && String(p.template).includes("Template - Person"));

if (DEBUG) {
    dv.paragraph(`Found ${people.length} documents with Template - Person`);
}

// Further filter to those with birthdays
let peopleWithBirthdays = people.where(p => p.birthday);
if (DEBUG) {
    dv.paragraph(`Of those, ${peopleWithBirthdays.length} have a birthday property`);
}

// Function to parse different date formats
function parseDate(dateStr) {
    if (!dateStr) return null;
    
    // If it's already a date object or Luxon DateTime
    if (dateStr instanceof Date || (dateStr.year && dateStr.month && dateStr.day)) {
        return dateStr;
    }
    
    // Try different formats
    try {
        // Convert to string if it's not already
        const str = String(dateStr);
        
        // Check for MM/DD/YYYY format
        if (str.match(/^\d{1,2}\/\d{1,2}\/\d{4}$/)) {
            const parts = str.split('/');
            const month = parseInt(parts[0], 10);
            const day = parseInt(parts[1], 10);
            const year = parseInt(parts[2], 10);
            return dv.date(`${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`);
        }
        
        // Check for YYYY-MM-DD format
        if (str.match(/^\d{4}-\d{1,2}-\d{1,2}$/)) {
            return dv.date(str);
        }
        
        // Try using dv.date directly (works for many formats)
        return dv.date(str);
    } catch (error) {
        console.log(`Error parsing date: ${dateStr}`, error);
        return null;
    }
}

// Function to get this year's birthday date
function getBirthdayThisYear(birthdayDate) {
    try {
        // Parse the birthday to get a date object
        const birthDate = parseDate(birthdayDate);
        if (!birthDate) return null;
        
        // Create a date for this year's birthday
        let thisYearBirthday = dv.date(`${today.year}-${birthDate.month.toString().padStart(2, '0')}-${birthDate.day.toString().padStart(2, '0')}`);
        
        // If the birthday has already passed this year, use next year
        if (thisYearBirthday < today) {
            thisYearBirthday = dv.date(`${today.year + 1}-${birthDate.month.toString().padStart(2, '0')}-${birthDate.day.toString().padStart(2, '0')}`);
        }
        
        return thisYearBirthday;
    } catch (error) {
        console.log(`Error processing birthday: ${birthdayDate}`, error);
        return null;
    }
}

// Function to calculate age on the upcoming birthday
function getUpcomingAge(birthdayDate) {
    try {
        const birthDate = parseDate(birthdayDate);
        if (!birthDate) return "Unknown";
        
        const thisYearBirthday = getBirthdayThisYear(birthDate);
        if (!thisYearBirthday) return "Unknown";
        
        // Calculate the age they will be on their upcoming birthday
        return thisYearBirthday.year - birthDate.year;
    } catch (error) {
        return "Unknown";
    }
}

// Function to format date as "Month Day (DayOfWeek)"
function formatBirthdayDate(date) {
    try {
        if (!date) return "Invalid date";
        return date.toFormat("MMMM d") + getOrdinalSuffix(date.day) + date.toFormat(" (cccc)");
    } catch (error) {
        return "Date format error";
    }
}

// Function to get ordinal suffix for a day number
function getOrdinalSuffix(day) {
    if (day % 10 === 1 && day % 100 !== 11) return 'st';
    if (day % 10 === 2 && day % 100 !== 12) return 'nd';
    if (day % 10 === 3 && day % 100 !== 13) return 'rd';
    return 'th';
}

// Debug: Show all people with birthdays to diagnose the issue
if (DEBUG) {
    dv.paragraph("All people with birthdays (for debugging):");
    dv.table(
        ["Person", "Birthday Raw Value", "Parsed Month/Day", "This Year's Date", "Days Until"],
        peopleWithBirthdays.map(p => {
            try {
                const parsed = parseDate(p.birthday);
                const thisYear = getBirthdayThisYear(p.birthday);
                const daysUntil = thisYear ? Math.round(thisYear.diff(today, "days").days) : "Error";
                
                return [
                    p.file.link, 
                    String(p.birthday),
                    parsed ? `${parsed.month}/${parsed.day}` : "Parse Error",
                    thisYear ? thisYear.toFormat("yyyy-MM-dd") : "Date Error",
                    daysUntil
                ];
            } catch (error) {
                return [p.file.link, String(p.birthday), "Error", "Error", "Error"];
            }
        })
    );
}

// Filter for birthdays in the specified timeframe and sort by date
let upcomingBirthdays = [];
try {
    upcomingBirthdays = peopleWithBirthdays
        .filter(p => {
            try {
                const thisYearBirthday = getBirthdayThisYear(p.birthday);
                return thisYearBirthday && thisYearBirthday >= today && thisYearBirthday <= cutoffDate;
            } catch (error) {
                console.log(`Error filtering birthday for ${p.file.name}:`, error);
                return false;
            }
        })
        .sort(p => {
            try {
                return getBirthdayThisYear(p.birthday);
            } catch (error) {
                return null;
            }
        });
} catch (error) {
    dv.paragraph(`Error processing birthdays: ${error}`);
}

// Calculate days until birthday
function daysUntilBirthday(birthdayDate) {
    try {
        const thisYearBirthday = getBirthdayThisYear(birthdayDate);
        if (!thisYearBirthday) return "Unknown";
        
        const diff = thisYearBirthday.diff(today, "days");
        return Math.round(diff.days);
    } catch (error) {
        return "Unknown";
    }
}

// Display results in a table
if (upcomingBirthdays.length > 0) {
    dv.table(
        ["Person", "Upcoming Birthday", "Age Will Be", "Days Until"],
        upcomingBirthdays.map(p => {
            try {
                return [
                    p.file.link,
                    formatBirthdayDate(getBirthdayThisYear(p.birthday)),
                    getUpcomingAge(p.birthday),
                    daysUntilBirthday(p.birthday)
                ];
            } catch (error) {
                return [p.file.link, "Error processing", "Error", "Error"];
            }
        })
    );
} else {
    dv.paragraph(`No birthdays found in the next ${daysAhead} days.`);
}
    
```
