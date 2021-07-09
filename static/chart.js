let domain = 'http://127.0.0.1:5000'

var exampleSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_1m");


var chart = LightweightCharts.createChart(document.getElementById('chart'), {
	width: 1280,
  	height: 720,
	layout: {
		backgroundColor: '#000000',
		textColor: 'rgba(255, 255, 255, 0.9)',
	},
	grid: {
		vertLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
		horzLines: {
			color: 'rgba(197, 203, 206, 0.5)',
		},
	},
	crosshair: {
		mode: LightweightCharts.CrosshairMode.Normal,
	},
	rightPriceScale: {
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
	timeScale: {
		timeVisible: true,
		borderColor: 'rgba(197, 203, 206, 0.8)',
	},
});

var candleSeries = chart.addCandlestickSeries({
  upColor: '#008000',
  downColor: '#FF0000',
  borderDownColor: '#FF0000',
  borderUpColor: '#008000',
  wickDownColor: '#FF0000',
  wickUpColor: '#008000',
});


// -----------------------------------------------
var sct = chart.addLineSeries({
	color: '#FFFC33',
	lineWidth: 2,
});
var scb = chart.addLineSeries({
	color: '#FFFC33',
	lineWidth: 2,
});
var mct = chart.addLineSeries({
	color: 'rgba(4, 111, 232, 1)',
	lineWidth: 2,
});
var mcb = chart.addLineSeries({
	color: 'rgba(4, 111, 232, 1)',
	lineWidth: 2,
});
// -----------------------------------------------


fetch(domain + '/history')
	.then((r) => r.json())
	.then((response) => {
		// console.log(response)
		candleSeries.setData(response)
	})

fetch(domain + '/hccp')
	.then((r) => r.json())
	.then((response) => {
		// console.log(response)
		// console.log(response[0]['mcb'])
		sct.setData(response[0]['sct'])
		scb.setData(response[0]['scb'])
		mct.setData(response[0]['mct'])
		mcb.setData(response[0]['mcb'])
	})

// exampleSocket.onmessage = function (event) {
	
// 	var msgObj = JSON.parse(event.data)

// 	var candle = msgObj.k

// 	candleSeries.update({
// 		time : candle.t / 1000, 
// 		open : candle.o, 
// 		high : candle.h, 
// 		low : candle.l, 
// 		close : candle.c 
// 	})
// }