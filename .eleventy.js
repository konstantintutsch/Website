const site = require("./src/_data/site.json");
const social = require("./src/_data/social.json");

function prettyDate(value) {
    const date = new Date(value);
    const formatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' });
    const formattedDate = formatter.format(date);
    return formattedDate;
}

function leadingZero(num) {
  num = num.toString();
  while (num.length < 2) num = "0" + num;
  while (num < 0 && num.length < 3) num = "-0" + (num * -1);
  return num;
}

module.exports = function (eleventyConfig) {
    eleventyConfig.addPassthroughCopy("src/assets");

    eleventyConfig.addFilter("stringDate", function(value) {
        return prettyDate(value);
    });
    eleventyConfig.addFilter("xmlDate", function(value) {
        // RFC-822
        const dayStrings = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        const monthStrings = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        const timeStamp = Date.parse(value);
        const date = new Date(timeStamp);

        const day = dayStrings[date.getDay()];
        const dayNumber = leadingZero(date.getDate());
        const month = monthStrings[date.getMonth()];
        const year = date.getFullYear();
        const time = `${leadingZero(date.getHours())}:${leadingZero(date.getMinutes())}:00`;
        const timezone = leadingZero(date.getTimezoneOffset() * -1 / 60);
        var timezoneString = ""
        if (timezone > 0) {
            timezoneString += "+";
        }
        timezoneString += timezone;
        if (timezone.length === 2) {
            timezoneString += "00";
        } else {
            timezoneString += "0";
        }

        return `${day}, ${dayNumber} ${month} ${year} ${time} ${timezoneString}`;
    });

    eleventyConfig.addShortcode("social", function(id, name = "", classes = "", extra = "", tracking = "") {
        let data = social[id];

        if (name === "") {
            name = data.value;
        }
        if (classes !== "") {
            classes = " " + classes;
        }
        if (tracking === "") {
            tracking = `social-${id}`;
        }

        return `<a class="social${classes}" rel="me" data-umami-event="${tracking}" href="${data.url}${extra}">${name}</a>\n`;
    });
    eleventyConfig.addShortcode("image", function(file, description, caption, thumbnail = false) {
        var display = file
        if (thumbnail == true) {
            display+="-thumbnail.jpg";
        }

        return `<figure class="image">\n    <a href="${site.assets.images}${file}"><img class="image-display" src="${site.assets.images}${display}" alt="${description}" loading="lazy"></a>\n    <figcaption class="image-caption">${caption}</figcaption>\n</figure>\n`;
    });
    eleventyConfig.addShortcode("navPost", function(post) {
        if (post.data.date === undefined) {
            date = "1970-01-01T00:00:00+00:00"
        } else {
            date = post.data.date
        }
        return `<div class="preview">\n    <a class="preview-title" href="${post.url}">${post.data.title}</a>\n    <p class="preview-date">${prettyDate(date)}</p>\n</div>\n`;
    });
    eleventyConfig.addShortcode("reference", function(id, pageURL) {
        return `<sup><a href="${site.url}${pageURL}#${id}">${id}</a></sup>\n`;
    })

    eleventyConfig.setNunjucksEnvironmentOptions({
        throwOnUndefined: false,
        trimBlocks: true,
        lstripBlocks: true
	});

    return {
        markdownTemplateEngine: "njk",
        dir: {
            input: "src",
            output: "build",
        },
    };
};
