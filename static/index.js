document.addEventListener('DOMContentLoaded', function() {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        document.querySelector('#get_data').onclick = () => {
            socket.emit('request data');
        };
    });

    socket.on("send data", (data) => {
        console.log(data)
        var myChart = echarts.init(document.getElementById('main'));
    
        // specify chart configuration item and data
        var option = {
            title: {
                text: 'Today\'s number'
            },
            tooltip: {},
            legend: {
                data:Object.keys(data)
            },
            xAxis: {
                data: [1,2,3,4,5,6,7,8,9,10]
            },
            yAxis: {},
            series: [{
                name: 'Numbers',
                type: 'bar',
                data: Object.values(data)
            }]
        };

        myChart.setOption(option);
    });

});