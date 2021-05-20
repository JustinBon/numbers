document.addEventListener('DOMContentLoaded', function() {
    var raw_data = JSON.parse(window.localStorage.getItem('data'));
    var data = Object.values(raw_data);
    
    var rolling_average = [];

    for(i=0;i<data.length;i++){
        rolling_average.push(data.slice(0,i+1) / (i + 1));
        // gaat fout
    };
    console.log(rolling_average)

});