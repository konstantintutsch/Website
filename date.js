const tools = require("./tools.js");

module.exports = {
    string: (value) => {
        const date = new Date(value);
        const formatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' });
        const formattedDate = formatter.format(date);
        return formattedDate;
    },

    rfc822: (value) => {
        const dayStrings = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        const monthStrings = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        const timeStamp = Date.parse(value);
        const date = new Date(timeStamp);

        // get single values
        const day = dayStrings[date.getDay()];
        const dayNumber = tools.leadingZero(date.getDate());
        const month = monthStrings[date.getMonth()];
        const year = date.getFullYear();

        // calculate time
        const time = `${tools.leadingZero(date.getHours())}:${tools.leadingZero(date.getMinutes())}:00`;

        // calculate time zone
        const timeZone = tools.leadingZero(date.getTimezoneOffset() * -1 / 60);
        var timeZoneString = ""
        // add + if offset is positive
        if (timeZone > 0) {
            timeZoneString += "+";
        }
        timeZoneString += timeZone;
        // decide whether zeros need to be added to complete timezone
        if (timeZone.length === 2) {
            timeZoneString += "00";
        } else {
            // convert a .5 (h) offset to 30 (min) offset
            timeZoneString = timeZoneString.replace(",5", "30");
        }

        return `${day}, ${dayNumber} ${month} ${year} ${time} ${timeZoneString}`;
    },
}
