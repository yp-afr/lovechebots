var can = $('#clicked_buttons').get(0).getContext('2d');

var bar = new Chart(can, {
	type: 'bar',
	data: {
		labels: [],
		datasets: [{
			data: [],
			borderWidth: 2,
			borderColor:'#F85C50',
			backgroundColor: '#FBCEB5'
		}]
	},
	options: {
		plugins: {
			legend: {
				display: false
			}
		},
		scales: {
			y: {
				beginAtZero: true,
				ticks:{stepSize: 1}
			},
		}
	}
});

var int = setInterval(function () {
	$.ajax({
		url: "/get_stats/",
		context: document.body
	}).done(function(data) {
	    var cats = data.jsonarray.map(function(e){
			return e.cat
		});
		var labels = data.jsonarray.map(function(e){
			return e.sub
		});
		var dat = data.jsonarray.map(function(e){
			return e.c
		});
		bar.data.labels = labels.slice(0,10)
		bar.data.datasets.forEach((dataset) => {
			dataset.data = dat.slice(0,10);
		});
		bar.update()
		var text = ""
        for(let i = 0; i < labels.length; i++)
        {
            text += "Кол-во кликов по " + cats[i] + " - " + labels[i] + ": " + dat[i] + '<br />';
        }
        var logElem = document.querySelector("#clicks_p");
        logElem.innerHTML = text
	})
}
,2000)

$('#pills-home-tab').click(function(){
    document.querySelector("#subs_stats").innerHTML = "Loading..."
})

$('#pills-profile-tab').click(function(){
    document.querySelector("#unsubs_stats").innerHTML = "Loading..."
})

    var dint = setInterval(function () {
        if($('#pills-home-tab').hasClass('active'))
        {
            setTimeout(this, 1000);
            $.ajax({
                url: "/get_subscriptions_stats/",
                context: document.body
            }).done(function(data) {
                var text = ""
                for(let i = 0; i < data["wth_cats"].length; i++)
                {
                    text += "Подписано на " + data["wth_cats"][i][0] + ": " + data["wth_cats"][i][1] + '<br />';
                }
                var logElem = document.querySelector("#subs_stats");
                logElem.innerHTML = text
                for(let i = 0; i < data["wth_subcats"].length; i++)
                {
                    text += "Подписано на " + data["wth_subcats"][i][0] + " - " + data["wth_subcats"][i][1] + ": " + data["wth_subcats"][i][2] + '<br />';
                }
                var logElem = document.querySelector("#subs_stats");
                logElem.innerHTML = text



            })
        }
}
,2000)




    var cint = setInterval(function () {
        if($('#pills-profile-tab').hasClass('active'))
        {
            setTimeout(this, 1000);
            $.ajax({
                url: "/get_unsubscribe_stats/",
                context: document.body
            }).done(function(data) {
                var text = ""
                for(let i = 0; i < data["wth_cats"].length; i++)
                {
                    text += data["wth_cats"][i][0] + ": " + data["wth_cats"][i][1] + '<br />';
                }
                var logElem = document.querySelector("#subs_stats");
                logElem.innerHTML = text
                for(let i = 0; i < data["wth_subcats"].length; i++)
                {
                    text += data["wth_subcats"][i][0] + " - " + data["wth_subcats"][i][1] + ": " + data["wth_subcats"][i][2] + '<br />';
                }
                var elem = document.querySelector("#unsubs_stats");
                elem.innerHTML = text

	})
        }
 }
,2000)








var new_users = document.getElementById('new_users7');
var new_users = new Chart(new_users7, {
	type: 'line',
	data: chartData1,
	options: {
		plugins: {
			legend: {
				display: false
			}
		},
		scales: {
			y: {
				beginAtZero: true,
				ticks:{stepSize: 1}
			},
		}
	}
});
document.getElementById("users_last_day").classList.add("active")
document.getElementById("users_last_day").onclick = function() {
	new_users.data = chartData1;
	new_users.update();
	document.getElementById("users_last_day").classList.add("active")
	if (document.getElementById("users_seven_days").classList.contains("active")) {
		document.getElementById("users_seven_days").classList.remove("active");
	}
	if (document.getElementById("users_thirty_days").classList.contains("active")) {
		document.getElementById("users_thirty_days").classList.remove("active");
	}

};
document.getElementById("users_seven_days").onclick = function() {
	new_users.data = chartData7;
	new_users.update();
	document.getElementById("users_seven_days").classList.add("active")
	if (document.getElementById("users_last_day").classList.contains("active")) {
		document.getElementById("users_last_day").classList.remove("active");
	}
	if (document.getElementById("users_thirty_days").classList.contains("active")) {
		document.getElementById("users_thirty_days").classList.remove("active");
	}
};
document.getElementById("users_thirty_days").onclick = function() {
	new_users.data = chartData30;
	new_users.update();
	document.getElementById("users_thirty_days").classList.add("active")
	if (document.getElementById("users_seven_days").classList.contains("active")) {
		document.getElementById("users_seven_days").classList.remove("active");
	}
	if (document.getElementById("users_last_day").classList.contains("active")) {
		document.getElementById("users_last_day").classList.remove("active");
	}
};


