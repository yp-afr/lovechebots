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


var new_posts30 = document.getElementById('new_posts30');
var new_posts = new Chart(new_posts30, {
	type: 'line',
	data: chartData30_posts,
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