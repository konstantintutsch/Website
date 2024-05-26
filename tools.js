// NodeJS
var path = require('path');

// Plugins
const Image = require("@11ty/eleventy-img");

module.exports = {
    leadingZero: (number) => {
        number = number.toString();
        while (number.length < 2) number = "0" + number;
        while (number < 0 && number.length < 3) number = "-0" + (number * -1);
        return number;
    },

    transformFavicon: async (input, output) => {
        let metadata = await new Image("./src" + input, {
            widths: ["48", "96", "144", "180", "192"],
            formats: ["png"],
            outputDir: "./build" + output,
            filenameFormat: function (id, src, width, format, options) {
                const extension = path.extname(src);
                const base = path.basename(src, extension);

                return `${base}-${width}.${format}`;
            },
            urlPath: output,
            useCache: true,
            svgAllowUpscale: true,
        });

        return `<!-- Favicon raster images generated from ${input} -->\n`;
    },
}
