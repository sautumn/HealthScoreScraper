var page;
var data;


//TO DO
//an actual search bar for user input
//ability to sort by date
//search within a radius
//maybe display points on a map
//fix the inconsistent case on database entries
//turn radio buttons into a drop down menu
//fix ux
//allow scraper to scrape once a day

$(() => {
	$.getJSON('/json', (content) => {
		data = content;
		$('#types').on("change",handler);
		$('input[type=radio][name=sort]').on("change", handler);
		$('#placeTypes').on("change",handler);

		page = next(sortData.descending(data,"Food Service Establishment", "name"));
		showNextPage();
		$('#nextPage').on("click",showNextPage);
		$('#backPage').on("click",showBackPage);
	});
});



//Sort function
function getData(result){
	var collection = [];
	for (var i = 0; i < result.length; i++) {
		collection.push(result[i].name);
	}
	return collection;
}

var sortData = {
	ascending (data, field, prop){
		data = data.sort(function(a,b){
			if (a[prop] < b[prop]) return -1;
			if (b[prop] < a[prop]) return 1;
			return 0;
		});
		return data.filter((a) => a.type === field);
	},
	descending (data,field, prop){
		data = data.sort(function(a,b){
			if (a[prop] > b[prop]) return -1;
			if (b[prop] > a[prop]) return 1;
			return 0;
		});
		return data.filter((a) => a.type === field);
	}
}

//Pagination Function
function next(array){
	var index= 0;
	return function(n){
		var slice;
		//negative case
		if (n < 0){
			index += n ;
			slice = array.slice(index + n, index);
		}
		else {
			slice = array.slice(index, index + n);
			index += n ;
		}
		return slice;
	};	
}

//Display data function
function showNextPage(){
	$("#restaurants").html(page(10)
			.map(function(value) {
		    		return ['<tr><td>', 
		    					value.name,
		    				' </td><td>',
		    					value.address,
		    				' </td><td>',  
		    					value.score, 
		    				'</td><td>',
		    				"<a href = '",value.currScoreLink,
		    				"'>",
		    					"Inspection Report",
		    				'</a></td><td>',
		    					value.scoreDate,
		    					'</td><td>',
		    				"<a href = '",value.pastScoreLink,
		    				"'>",
		    					"Past Reports",
		    				'</a></td><td>',
		    					value.type,
		    				' </td></tr>'].join('');
					}).join(''));	
}
function showBackPage(){
	$("#restaurants").html(page(-10)
			.map(function(value) {
		    		return ['<tr><td>', 
		    					value.name,
		    				' </td><td>', 
		    					value.score, 
		    				'</td><td>',
		    					value.type,
		    				' </td></tr>'].join('');
					}).join(''));	
}
function handler(){
	var type = $('#types option:selected')[0].value;
	var placeType = $('#placeTypes option:selected')[0].value;
	var direction = $('input[type=radio][name=sort]:checked')[0].value;
	page = next(sortData[direction](data,placeType, type));
	showNextPage();
}
