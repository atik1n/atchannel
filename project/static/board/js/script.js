function buttonFlip(btn) {
	var loc = btn.id.substr(btn.id.indexOf('-')+1)
	var form = document.getElementById("form-" + loc);

	if (form.style.display === "none") {
		form.style.display = "block";
		btn.classList.add('btn-pressed')
		btn.classList.remove('btn-normal')
	} else {
		form.style.display = "none";
		btn.classList.add('btn-normal')
		btn.classList.remove('btn-pressed')
	}
}

function textChange(caller) {
	var field = caller.id.substr(0, caller.id.indexOf('-'))
	var top = document.getElementById(field + "-top");
	var bottom = document.getElementById(field + "-bottom");

	if (caller == top) {
		bottom.value = caller.value
	} else {
		top.value = caller.value
	}
}

function addLink(number) {
	var top = document.getElementById("text-top");
	var bottom = document.getElementById("text-bottom");

	top.value = top.value + " >>" + number
	bottom.value = top.value
}

function setCHStyle(styleName) {
  var expires = "";
  var date = new Date();
  date.setTime(date.getTime() + (365*24*60*60*1000));
  expires = "; expires=" + date.toUTCString();
  document.cookie = "highlight_style" + "=" + (styleName || "")  + expires + "; path=/";
  window.location.reload(true);
}

function setStyle(styleName) {
  var expires = "";
  var date = new Date();
  date.setTime(date.getTime() + (365*24*60*60*1000));
  expires = "; expires=" + date.toUTCString();
  document.cookie = "style" + "=" + (styleName || "")  + expires + "; path=/";
  window.location.reload(true);
}