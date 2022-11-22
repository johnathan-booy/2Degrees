async function highlightScores(name) {
	const $environmentalDivs = document.getElementsByClassName("environmental");
	const $socialDivs = document.getElementsByClassName("social");
	const $governanceDivs = document.getElementsByClassName("governance");
	const $totalDivs = document.getElementsByClassName("total");

	const distributions = await getESGDistributions(name);

	addHighlights($environmentalDivs, distributions.environmental);
	addHighlights($socialDivs, distributions.social);
	addHighlights($governanceDivs, distributions.governance);
	addHighlights($totalDivs, distributions.total);
}

async function getESGDistributions(name) {
	const resp = await axios.get(`/api/esg/distributions/${name}`);
	if (resp.status !== 200) {
		return;
	}
	return resp.data.distributions;
}

function addHighlights($divs, distribution) {
	for (const $div of $divs) {
		const score = $div.dataset.score;
		if (score >= distribution.best) {
			$div.classList.add("best");
		} else if (score <= distribution.worst) {
			$div.classList.add("worst");
		}
	}
}
