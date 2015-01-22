xyzzy = {}; // decent variable name/10
xyzzy.room = $('meta[name=x-room]').attr('content');
xyzzy.handle = $('meta[name=x-handle]').attr('content');
xyzzy.socket = null;
xyzzy.members = [];

xyzzy.connect = function () {
	var socket = xyzzy.socket = io.connect(('https:' == document.location.protocol ? 'https://' : 'http://') + document.domain + ':' + location.port);
	socket.on("connect", function () {
		console.log("xyzzy: Connected to server!");
	});
	return socket;
};

xyzzy.join = function (room, force) {
	// If force == false, this just lets you change rooms.
	if (room === xyzzy.room && !force) {
		// Rejoining? Uh.. Nope?
		return;
	}

	// Reset member list.
	xyzzy.members = [];

	// Bail from current room.
	console.log("xyzzy: Leaving room '%s'", xyzzy.room);
	xyzzy.socket.emit("leave", {room: xyzzy.room});

	// Update and join the new one.
	xyzzy.room = room;
	console.log("xyzzy: Joining room '%s'", xyzzy.room);
	xyzzy.socket.emit("join", {handle: xyzzy.handle, room: xyzzy.room});
};

xyzzy.changeHandle = function (new_, local) {
	if (new_ === xyzzy.handle) {
		return;
	}
	console.log("xyzzy: Changing handle from '%s' to '%s'", xyzzy.handle, new_);
	xyzzy.handle = new_;

	$(".x-handle").text(xyzzy.handle);
	$(".x-handle-value").val(xyzzy.handle);
	if (!local && xyzzy.socket !== null) {
		xyzzy.socket.emit("player.rehandle", {handle: xyzzy.handle});
	}
};

xyzzy.geocities = function geocities(on) {
	// Hardcoding locations, whoo!
	var x = "/static/css/geo.bootstrap.min.css",
		y = "/static/css/bootstrap.css";
	var $z = $("#page-styles");
	if (on) {
		console.log("xyzzy: geocities enabled");
		$z.attr("href", x);
		$("html").addClass("geocities");
	} else { //$z.attr("href") == x) {
		console.log("xyzzy: geocities disabled");
		$z.attr("href", y);
		$("html").removeClass("geocities")
	}
}
