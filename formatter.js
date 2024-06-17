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

// Standard image generation
async function standardImageGeneration(file) {
    let full = site.assets.images + file;
    let directory = path.dirname(full) + "/";

    console.log("Generating different versions of " + full + " …");
    
    let metadata = await Image("./src" + full, {
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

    return metadata;
}

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

    image: async (file, description, caption, orientation) => {
        let original = site.assets.images + file;

        let metadata = await standardImageGeneration(file);

        var sizes = "(max-width: 750px) 98vw, 60vw"
        if (orientation === "vertical") {
            sizes = "(max-width: 750px) 98vw, 30vw"
        }

        let attributes = {
            alt: description,
            sizes: sizes,
            loading: "lazy",
            decoding: "async",
        };
        return `<figure class="image">\n    <a href="${original}">${Image.generateHTML(metadata, attributes)}</a>\n    <figcaption class="image-caption">${caption}</figcaption>\n</figure>\n`;
    },

    thumbnail: async (file) => {
        let metadata = await standardImageGeneration(file);

        return metadata.webp[0].url;
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
