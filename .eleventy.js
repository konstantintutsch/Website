// Functions
const dateConversion = require("./date.js");
const stringFormatter = require("./formatter.js");
const generalTools = require("./tools.js");

module.exports = function (eleventyConfig) {
    eleventyConfig.addPassthroughCopy("src/assets");

    eleventyConfig.addFilter("stringDate", function(value) { return dateConversion.string(value); });
    eleventyConfig.addFilter("rfcDate", function(value) { return dateConversion.rfc822(value); });
    eleventyConfig.addFilter("isoDate", function(value) { return dateConversion.iso8601(value); });
    eleventyConfig.addFilter("age", function(value) { return dateConversion.age(value); });
    eleventyConfig.addFilter("thumbnail", async function(value) { return await stringFormatter.thumbnail(value); })

    eleventyConfig.addShortcode("transformFavicon", async function(input, output) { return await generalTools.transformFavicon(input, output); });
    eleventyConfig.addShortcode("social", function(id, name = "", classes = "", extra = "", tracking = "") { return stringFormatter.social(id, name, classes, extra, tracking); });
    eleventyConfig.addShortcode("image", async function(file, description, caption, orientation = "horizontal") { return await stringFormatter.image(file, description, caption, orientation); });
    eleventyConfig.addShortcode("post", function(post) { return stringFormatter.post(post); });
    eleventyConfig.addShortcode("reference", function(id, pageURL) { return stringFormatter.reference(id, pageURL); });

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
