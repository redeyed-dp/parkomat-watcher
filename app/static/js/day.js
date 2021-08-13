$(document).ready(function() {
    $('#month').change(function() {
        setDays();
    });
    $('#year').change(function() {
        setDays();
    });
});

function setDays() {
    var year = $('#year').val();
    var month = $('#month').val();
    var days = new Date(year, month, 0).getDate();
    console.log(days);
    $('#day').empty();
    for(let i = 1; i <= days; i++) {
        var option = document.createElement("option");
        option.text = i;
        option.value = i;
        $('#day').append(option)
    }
}