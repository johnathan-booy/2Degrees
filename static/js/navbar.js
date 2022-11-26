let navToggle = document.getElementById("nav-toggle");
let navIcon = document.querySelector("#nav-toggle > i");
let navList = document.getElementById("nav-list");
let nav = document.querySelector("nav");
let height = nav.clientHeight + "px";

navToggle.addEventListener("click", (event) => {
	navList.classList.toggle("active");
	if (navList.classList.contains("active")) {
		toggleIcon();
		navExpand();
	} else {
		toggleIcon();
		navCollapse();
	}
});

function toggleIcon() {
	navIcon.classList.toggle("fa-xmark");
	navIcon.classList.toggle("fa-bars");
}

function navExpand() {
	navList.style.display = "block";
	navList.style.height = "0px";
	setTimeout(function () {
		navList.style.height = height;
	}, 0);
}

function navCollapse() {
	navList.style.height = "0px";
	navList.addEventListener(
		"transitionend",
		function () {
			navList.classList.remove("active");
			navList.removeAttribute("style");
		},
		{
			once: true,
		}
	);
}
