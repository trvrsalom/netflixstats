var link = "";
function fixlink() {
	link = $("#linkIn").val();
	link = link.replace(/(http:\/\/www)\1/, '$1'));
	console.log(link);
}

function getData() {
	document.getElementById('txt').style.display = "inline-block";
	document.getElementById('stuffs').style.display = "none";
	document.getElementById('loader').style.display = "inline-block";
	$.get( "http://api.smmry.com/?SM_API_KEY=C6780529F2&SM_URL=" + link, function( data ) {
		document.getElementById('stuffs').style.display = "inline-block";
		document.getElementById('loader').style.display = "none";
	});
}