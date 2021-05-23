document.addEventListener('DOMContentLoaded', function() {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // get data on page load
    var raw_data = JSON.parse(window.localStorage.getItem('data'));
    var data = Object.values(raw_data);

    // sum function
    function sum(total, num) {
        return total + num;
    };

    // request new data from backend
    function get_updated_data() {
        socket.emit('request data');
    };

    // set data to the potentially new updated data
    socket.on("send data", (new_data) => {  
        data = new_data
    });
    
    // calculate rolling average of data
    function get_rolling_average(data){
        var rolling_average = [];

        for(i=0;i<data.length;i++){
            array_slice = data.slice(0,i+1).reduce(sum);
            average = array_slice / (i + 1);

            // round average to 2 decimal points
            rolling_average.push(Math.round((average + Number.EPSILON) * 100) / 100);

        };
        return rolling_average
    };

    function not_picked(data_func){
        let result = {};
        data_func = data_func.reverse();

        for (let i=1; i<10; i++){
            let number = i;
            let max = 0;
            let counter = 0;
            for (let j=0; j<data_func.length; j++) {
                let picked = data_func[j];
                if (picked == number){
                    if (counter > max) {
                        max = counter;
                    };
                    counter = 0;

                } else {
                    counter++;
                };
            };
            result[number] = max;
        };
        return result;
    };

    function get_pie_values(numbers) {
        let counter = {};
        for (let i=0; i<numbers.length; i++){
            let pick = numbers[i];
            if (pick in counter){
                counter[pick]++;
            } else{
                counter[pick] = 1;
            };
        };

        let result = [];
        for (let x in Object.keys(counter)){
            let temp_dict = {value: counter[x], name: x};
            result.push(temp_dict);
        };
        console.log(result);
        return result;
    };

    function update_graph(data) {
        var rolling_average = get_rolling_average(data);

        var x_values = [];
        for(i=1;i<rolling_average.length + 1;i++) {
            x_values.push(i)
        };

        // set up graph
        let myChart = echarts.init(document.getElementById('rolling-average'));
        option = {
            title: {
                text: 'Average over time'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Average over time', 'Picked number']
            },
            xAxis: {
                type: 'category',
                data: x_values
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: rolling_average,
                type: 'line',
                name: 'Average over time'
            },
            {
                data: data,
                type: 'bar',
                name: 'Picked number'
            }]
        };

        myChart.setOption(option);
    };

    function update_not_picked_graph(data) {
        var values = not_picked(data);
        console.log(values);
        // set up graph
        let myChart = echarts.init(document.getElementById('not-picked'));
        option = {
            title: {
                text: 'Longest time not picked'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['Number of days not picked',]
            },
            yAxis: {
                type: 'category',
                data: Object.keys(values),
                inverse: true
            },

            xAxis: {
                max: 'dataMax',
            },

            series: [{
                data: Object.values(values),
                type: 'bar',
                name: 'Days not picked'
            }]
        };

        myChart.setOption(option);

    };


    function pie(data){
        let values = get_pie_values(Object.values(data));
        let myChart = echarts.init(document.getElementById('part-of-whole'));

        option = {
            tooltip: {
                trigger: 'item'
            },
            legend: {
                top: '5%',
                left: 'center'
            },
            series: [
                {
                    name: 'Part of total',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    avoidLabelOverlap: false,
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: '40',
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: values
                }
            ]
        };
        myChart.setOption(option);
    };


    update_graph(data);
    update_not_picked_graph(data);
    pie(data)
});