// Data
const site = require("./src/_data/site.json");
const social = require("./src/_data/social.json");

// Functions
const dateConversion = require("./date.js");

module.exports = {
    social: (id, name, classes, extra, tracking) => {
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
    },

    image: (file, description, caption, thumbnail) => {
        var display = file
        if (thumbnail == true) {
            display+="-thumbnail.jpg";
        }

        return `<figure class="image">\n    <a href="${site.assets.images}${file}"><img class="image-display" src="${site.assets.images}${display}" alt="${description}" loading="lazy"></a>\n    <figcaption class="image-caption">${caption}</figcaption>\n</figure>\n`;
    },

    post: (post) => {
        if (post.data.date === undefined) {
            date = "1970-01-01T00:00:00Z"
        } else {
            date = post.data.date
        }

        return `<div class="preview">\n    <a class="preview-title" href="${post.url}">${post.data.title}</a>\n    <p class="preview-date">${dateConversion.string(date)}</p>\n</div>\n`;
    },

    reference: (id, pageURL) => {
        return `<sup><a href="${site.url}${pageURL}#${id}">${id}</a></sup>\n`;
    },
}
