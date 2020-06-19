const Data = {
    line_plotData: {
        label: ['2008', '2009', '2010', '2011', '2012', '2013', '2014'],
        data: [[0, 50, 75, 50, 25, 40, 50, 60],
                [50, 75, 30, 50, 75, 50, 100]],
        Color: ['rgb(38, 206, 232)','rgb(116, 73, 189)'],
        datalabel: ['Tablets', 'Desktops']
    },
    bar_plotData: {
        label: ['2005','', '2007', '', '2009', '', '2011','', '2013', '',  '2015'],
        data: [[35, 50, 75, 50, 75, 50, 35, 50, 35, 50, 75],
                [220, 120, 200, 150, 200, 150, 100, 75, 150, 75, 200, 220, 150],
                [330, 220, 250, 220, 320, 250, 180, 140, 150, 140, 240, 310, 200]],
        Color: ['rgb(126, 87, 194)', 'rgb(179, 157, 219)', 'rgb(238, 232, 246)'],
        datalabel: ['Desktops', 'Tablets', 'Mobiles']
    }
}


function plot_graph(type, id='myChart') {
    const ctx = document.getElementById(id).getContext('2d');
    let Datasets = [];
    let Label;
    
    if(type === 'line'){
        for (let index = 0; index < 2; index++) {
            const element = {
                label: Data.line_plotData.datalabel[index],
                borderColor: Data.line_plotData.Color[index],
                borderWidth: 5,
                backgroundColor: 'rgb(0,0,0,0)',
                data: Data.line_plotData.data[index]
            };
            Datasets.push(element);
        }
        Label = Data.line_plotData.label;
    }
    else{
        for (let index = 0; index < 3; index++) {
            const element = {
                label: Data.bar_plotData.datalabel[index],
                borderColor: Data.bar_plotData.Color[index],
                borderWidth: 5,
                backgroundColor: Data.bar_plotData.Color[index],
                data: Data.bar_plotData.data[index]
            };
            Datasets.push(element);
        }
        Label = Data.bar_plotData.label;
    }

    let myChart = new Chart(ctx, {
        type: type,

        data: {
            labels: Label,

            datasets: Datasets,
        },
        
        //configuration option go here
        options: {
            scales: {
                xAxes: [{
                    stacked: true
                }]
            }
        }
    });
}