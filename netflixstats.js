function getShowList() {
	console.log("hey");
	$.ajax({
	  url: "http://10.12.40.67:4321/?email="+$("#email").val()+"&password="+$("#pass").val(),
	  success: function(resp) {
			gotShowList(resp);
		},
	  dataType: "json",
	});
}

function gotShowList(list) {
	if(list.fail == "true") {
		$("#err").show();
		$("#loader").hide();
		$("#login").show();
		return;
	}
	console.log(list);
	$("#loader").hide();
	$("#stats").show();
	$("#date").html(list.lastDate);
	$("#date2").html(list.lastDate);
	for(var i = 0; i < Object.keys(list).length; i++) {
		var currCount = list[i];
		var currTitle = Object.keys(list)[i];
		if(currTitle != "lastDate") {
			var currRow = $("#listBody").append("<tr></tr>").children().last();
			$(currRow).append("<td>" + currTitle + "</td>");
			$(currRow).append("<td>" + list[currTitle] + "</td>");
			console.log(currTitle);
			$.ajax({
			  url: "http://netflixroulette.net/api/api.php?title=" + currTitle,
				targRow: $(currRow),
				count: list[currTitle],
			  success: function(resp) {
					var runtime = resp.runtime;
					var match = runtime.match(/\d+\.?\d*/);
					if(match && !isNaN(match[0])) {
						this.targRow.append("<td>" + ((match[0]*this.count)/60.0).toFixed(2) + " hours" + "</td>");
					} else {
						this.targRow.append("<td>N/A</td>");
					}
				},
				error: function(resp) {
					this.targRow.append("<td>N/A</td>");
					console.log($(currRow))
				},
			  dataType: "json",
			});
		}
	}
}
