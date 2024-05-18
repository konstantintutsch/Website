module.exports = {
    leadingZero: (number) => {
        number = number.toString();
        while (number.length < 2) number = "0" + number;
        while (number < 0 && number.length < 3) number = "-0" + (number * -1);
        return number;
    },
}
