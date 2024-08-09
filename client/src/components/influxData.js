



function getData(board, time, device) {
	let rawData;
	fetch("./data?board=" + board + "&time=" + time + "&device=" + device)
		.then(res => res.json())
		.then(out => rawData = out)
		.catch(err => console.log(err));

	return rawData;
	
	}