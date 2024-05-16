module.exports = function () {
	return {
		eleventy: process.env.ELEVENTY_ENVIRONMENT || "development",
	};
};
