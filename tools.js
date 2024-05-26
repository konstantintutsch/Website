const pluginImage = require("@11ty/eleventy-img");

// Site data
const site = require("./src/_data/site.json");

module.exports = {
    leadingZero: (number) => {
        number = number.toString();
        while (number.length < 2) number = "0" + number;
        while (number < 0 && number.length < 3) number = "-0" + (number * -1);
        return number;
    },

    transformImage: async (input, output, sizes, formats) => {
        let metadata = await new pluginImage.Image(input, {
            heights: sizes,
            formats: formats,
            urlPath: output,
        });

        return `<!-- ${metadata.src} transformed to ${metadata.options.formats} with height ${metadata.options.heights} -->\n`;
    },
}
