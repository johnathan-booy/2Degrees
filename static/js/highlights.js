async function getESGDistributions() {
	const resp = await axios.get("/api/esg/distributions");
	if (resp.status !== 200) {
		return;
	}
	return resp.data.distributions;
}

async function highlightScores() {
	const $environmentalDivs = document.getElementsByClassName("environmental");
	const $socialDivs = document.getElementsByClassName("social");
	const $governanceDivs = document.getElementsByClassName("governance");
	const $totalDivs = document.getElementsByClassName("total");

	const distributions = await getESGDistributions();

	addHighlights($environmentalDivs, distributions.environmental);
	addHighlights($socialDivs, distributions.social);
	addHighlights($governanceDivs, distributions.governance);
	addHighlights($totalDivs, distributions.total);
}

function addHighlights($divs, distribution) {
	for (const $div of $divs) {
		const score = $div.dataset.score;
		if (score >= distribution.top) {
			$div.classList.add("high-score");
		} else if (score <= distribution.bottom) {
			$div.classList.add("low-score");
		}
	}
}

highlightScores();
