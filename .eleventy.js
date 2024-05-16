const site = require("./src/_data/site.json");
const social = require("./src/_data/social.json");

function prettyDate(value) {
    const date = new Date(value);
    const formatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' });
    const formattedDate = formatter.format(date);
    return formattedDate;
}

module.exports = function (eleventyConfig) {
    eleventyConfig.addPassthroughCopy("src/assets");

    eleventyConfig.addFilter("stringDate", function(value) {
        return prettyDate(value);
    });
    eleventyConfig.addFilter("xmlDate", function(value) {
        console.log(`New XML time: “${value}”`);
        const date = new Date(value);
        return date.toISOString();
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
