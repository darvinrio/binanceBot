let domain = 'http://127.0.0.1:5000'

var exampleSocket = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@kline_1m");


var chart = LightweightCharts.createChart(document.getElementById('chart'), {
	width: 1280,
  	height: 720,
	layout: {
		backgroundColor: '#1C2833',
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

const downColr = '#E74C3C'
const upColr = '#48C9B0' 
var candleSeries = chart.addCandlestickSeries({
  upColor: upColr,
  downColor: downColr,
  borderDownColor: downColr,
  borderUpColor: upColr,
  wickDownColor:downColr,
  wickUpColor: upColr,
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

	var candleSeries2 = chart.addCandlestickSeries({
		upColor: '#FFFC33',
		downColor: 'rgba(4, 111, 232, 1)',
		borderDownColor: 'rgba(4, 111, 232, 1)',
		borderUpColor: '#FFFC33',
		wickDownColor:'rgba(4, 111, 232, 1)',
		wickUpColor: '#FFFC33',
		})

	  var k = True

exampleSocket.onmessage = function (event) {
	
	var msgObj = JSON.parse(event.data)
	var candle = msgObj.k


	candleSeries2.update({
		time : candle.t / 1000, 
		open : candle.o, 
		high : candle.h, 
		low : candle.l, 
		close : candle.c 
	})
}