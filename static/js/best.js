$companyList = $("#company-list");

async function getBestCompanies() {
	const resp = await axios.get("/api/companies/ranked/best/e");
	const companies = resp.data.companies;
	return companies;
}

async function populateList() {
	const companies = await getBestCompanies();
	for (const company of companies) {
		$listItem = makeListItem(company);
		$companyList.append($listItem);
	}
}

function makeListItem(company) {
	website = company.profile.website;
	const $listItem = $(`<a href="${website}">`);
	$listItem.addClass("list-group-item");
	$listItem.addClass("list-group-item-action");

	$profile = makeProfileOverview(company.profile);

	$listItem.append($profile);
	return $listItem;
}

function makeProfileOverview(profile) {
	$profile = $("<div class='row'>");
	$leftDiv = $("<div>");
	$rightDiv = $("<div>");
	$logo = makeLogo(profile.website);
	$symbol = $("<div>");
	$name = $("<div>");

	$profile.addClass("");
	$leftDiv.addClass("px-2 d-flex flex-column justify-content-center");
	$rightDiv.addClass("px-2 d-flex flex-column justify-content-center");
	$symbol.addClass("h4");

	$symbol.text(profile.symbol);
	$name.text(profile.name);

	$leftDiv.append($logo);
	$rightDiv.append($symbol);
	$rightDiv.append($name);

	$profile.append($leftDiv);
	$profile.append($rightDiv);

	return $profile;
}

function makeLogo(url) {
	// Get domain
	domain = new URL(url);
	domain = domain.hostname.replace("www.", "");

	// Create the div
	$div = $(`<div>`);
	$div.addClass("logo");

	// Create the img
	$img = $("<img>");
	$img.attr("src", `https://logo.clearbit.com/${domain}`);

	$div.append($img);

	return $div;
}

populateList();
