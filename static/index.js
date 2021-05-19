document.addEventListener('DOMContentLoaded', function() {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    var data = JSON.parse(window.localStorage.getItem("data"));
    console.log(data)
    localStorage.removeItem('data');
    make_graph(data)

    function make_graph(data) {
        console.log('test')
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
    };

    socket.on('connect', () => {
        document.querySelector('#get_data').onclick = () => {
            socket.emit('request data');
        };
    });

    socket.on("send data", (data) => {  
        make_graph(data);
    });


});