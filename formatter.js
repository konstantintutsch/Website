// NodeJS
var path = require('path');

// Plugins
const Image = require("@11ty/eleventy-img");


// Data
const site = require("./src/_data/site.json");
const social = require("./src/_data/social.json");

// Functions
const dateConversion = require("./date.js");
const generalTools = require("./tools.js");

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

    image: async (file, description, caption, thumbnail) => {
        let original = site.assets.images + file;

        var display = original;
        let directory = path.dirname(original) + "/";

        console.log("Generating different versions of " + original + " …");
        let metadata = await Image("./src" + original, {
            widths: ["auto", 300, 600, 1000, 1500],
            formats: ["webp"],
            outputDir: "./build" + directory,
            filenameFormat: function (id, src, width, format, options) {
                const extension = path.extname(src);
                const base = path.basename(src, extension);

                return `${base}-${width}.${format}`;
            },
            urlPath: directory,
            useCache: true,
        });

        let attributes = {
            alt: description,
            sizes: "(max-width: 750px) 98vw, 60vw",
            loading: "lazy",
            decoding: "async",
        };

        return `<figure class="image">\n    <a href="${original}">${Image.generateHTML(metadata, attributes)}</a>\n    <figcaption class="image-caption">${caption}</figcaption>\n</figure>\n`;
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
