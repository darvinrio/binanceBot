let domain = 'http://127.0.0.1:5000'

var exampleSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_5m");


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

fetch(domain + '/history')
	.then((r) => r.json())
	.then((response) => {
		console.log(response)
		candleSeries.setData(response)
	})

// exampleSocket.onmessage = function (event) {
	
// 	var msgObj = JSON.parse(event.data)

// 	var candle = msgObj.k

// 	candleSeries.update({
// 		time : candle.t, 
// 		open : candle.o, 
// 		high : candle.h, 
// 		low : candle.l, 
// 		close : candle.c 
// 	})
// }