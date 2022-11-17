$companiesTable = $("#companies-table tbody");

async function getBestCompanies() {
	const resp = await axios.get("/api/companies/ranked/best/e");
	const companies = resp.data.companies;
	return companies;
}

async function getESGRanges() {
	const resp = await axios.get("/api/esg/ranges");
	const ranges = resp.data.ranges;
	return ranges;
}

async function populateCompaniesTable() {
	const companies = await getBestCompanies();
	const esgRanges = await getESGRanges();
	for (let i = 0; i < companies.length; i++) {
		const company = companies[i];
		const $tr = makeCompanyTr(i, company, esgRanges);
		$companiesTable.append($tr);
	}
}

function makeCompanyTr(idx, company, esgRanges) {
	const $tr = $(`<tr>`);

	const $rank = makeRankTd(idx + 1);
	const $profile = makeProfileTd(company.profile);
	const $e = makeESGTd("environmental", company, esgRanges);
	const $s = makeESGTd("social", company, esgRanges);
	const $g = makeESGTd("governance", company, esgRanges);
	const $t = makeESGTd("total", company, esgRanges);

	$tr.append($rank);
	$tr.append($profile);
	$tr.append($e);
	$tr.append($s);
	$tr.append($g);
	$tr.append($t);

	return $tr;
}

function makeRankTd(rank) {
	const $td = $("<td>");
	const $innerDiv = $("<div>");
	const $span = $("<span>");

	$innerDiv.addClass(
		"table-inner d-flex justify-content-center align-items-center"
	);

	$span.text(rank);

	$innerDiv.append($span);
	$td.append($innerDiv);

	return $td;
}

function makeProfileTd(profile) {
	const $td = $("<td>");
	const $innerDiv = $("<div>");
	const $leftDiv = $("<div>");
	const $rightDiv = $("<div>");
	const $logo = makeLogo(profile);
	const $symbol = $("<div>");
	const $name = $("<div>");

	$innerDiv.addClass("table-inner d-flex justify-content-start");
	$leftDiv.addClass("px-2 d-flex flex-column justify-content-center");
	$rightDiv.addClass("px-2 d-flex flex-column justify-content-center");
	$symbol.addClass("h4");

	$symbol.text(profile.symbol);
	$name.text(profile.name);

	$leftDiv.append($logo);
	$rightDiv.append($symbol);
	$rightDiv.append($name);

	$innerDiv.append($leftDiv);
	$innerDiv.append($rightDiv);

	$td.append($innerDiv);

	return $td;
}

function makeLogo(profile) {
	// Create the div
	const $div = $(`<div>`);
	$div.addClass("logo");

	// Insert image if available
	try {
		let domain = new URL(profile.website);
		domain = domain.hostname.replace("www.", "");

		const $img = $("<img>");
		$img.attr("src", `https://logo.clearbit.com/${domain}`);
		$div.append($img);
	} catch (error) {
		console.log(error);
		const $inner = $("<div class='text-muted'>");
		$inner.text(profile.symbol[0]);
		$div.append($inner);
	}

	return $div;
}

function makeESGTd(type, company, esgRanges) {
	const $td = $("<td>");

	type = type.toLowerCase();

	const range = esgRanges[type];
	if (!range) {
		return $td;
	}
	const { min, max } = range;

	const score = company.esg_ratings.scores[type + "_score"];
	const size = `${parseInt(((score - min) / (max - min)) * 50) + 20}px`;
	console.log(size);

	// Make elements

	const $innerDiv = $("<div>")
		.addClass("table-inner d-flex justify-content-center align-items-center")
		.appendTo($td);
	const $esgBubble = $("<div>")
		.addClass("esg-bubble d-flex align-items-center justify-content-center")
		.css("height", size)
		.css("width", size)
		.appendTo($innerDiv);
	const $esgText = $("<span>")
		.addClass("text-white")
		.text(score)
		.appendTo($esgBubble);

	switch (type) {
		case "environmental":
			$esgBubble.addClass("bg-success");
			break;
		case "social":
			$esgBubble.addClass("bg-warning");
			break;
		case "governance":
			$esgBubble.addClass("bg-danger");
			break;
		case "total":
			$esgBubble.addClass("bg-primary");
			break;
	}

	return $td;
}

populateCompaniesTable();
