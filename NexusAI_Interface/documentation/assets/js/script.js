$(window).on('load', function () {
	var scrollLink = $(".scroll");

	// Smooth scrolling
	scrollLink.on("click", function () {
		e.preventDefault();
		$("body,html").animate({
			scrollTop: $(this.hash).offset().top,
		},
			2000
		);
	});

	// Active link switching
	$(window).scroll(function () {
		var scrollbarLocation = $(this).scrollTop();

		scrollLink.each(function () {
			var sectionOffset = $(this.hash).offset().top - 100;

			if (sectionOffset <= scrollbarLocation) {
				$(this).parent().addClass("active");
				$(this).parent().parent().siblings().children("h3").removeClass("active");
			}
		});
	});

	$("#html").jstree();
});